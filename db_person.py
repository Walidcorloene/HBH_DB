from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
from sqlalchemy.pool import QueuePool
from sqlalchemy import text
import hashlib


Base = declarative_base()


class Person(Base):
    __tablename__ = 'person'
    person_id = Column(Integer, primary_key=True, autoincrement=True)
    person_source_value = Column(String)
    gender_concept_id = Column(Integer)
    year_of_birth = Column(Integer)


class PersonDatabase(Person):
    def __init__(self, db_name):
        self.db_name = db_name
        self.engine = create_engine('sqlite:///person.db', poolclass=QueuePool)
        self.Session = sessionmaker(bind=self.engine)

    def create_person_table(self):
        Base.metadata.create_all(self.engine)
        print("Table 'person' created successfully.")

    def load_csv_data(self):
        t_mcoaac = pd.read_csv('T_MCOAAC.csv', sep='|')
        t_mcoaab = pd.read_csv('T_MCOAAB.csv', sep=',')
        return t_mcoaac, t_mcoaab

    def transformation(self):
        t_mcoaac, t_mcoaab = self.load_csv_data()
        t_mcoaab.drop_duplicates(inplace=True)
        t_mcoaac.dropna(inplace=True)
        t_mcoaab.dropna(inplace=True)
        print(f"the the number of line for t_mcoaab {len(t_mcoaab)}")
        print(f"the the number of line for t_mcoaac {len(t_mcoaac)}")
        homme = len(t_mcoaab[t_mcoaab['COD_SEX'] == 1])
        femme = len(t_mcoaab[t_mcoaab['COD_SEX'] == 2])
        autre = len(t_mcoaab[~t_mcoaab['COD_SEX'].isin([1, 2])])
        print(f"Distribution homme {homme} et femme {femme} et autre {autre}")
        merged = pd.merge(t_mcoaab, t_mcoaac, on=[
                          "ETA_NUM", "RSA_NUM"], how="inner")
        return merged

    def insert_NIR_into_person_table(self, df, col):
        with self.Session() as session:
            for value in df[col]:
                if value is not None:
                    person = Person(person_source_value=value)
                    session.add(person)
            session.commit()

    def update_gender_in_person_table(self, df, col):
        with self.Session() as session:
            for value in df[col]:
                if value is not None:
                    person = Person(gender_concept_id=value)
                    session.add(person)
            session.commit()
        print("Gender information updated successfully.")

    def generate_person_id(self, person_source_value):
        hash_object = hashlib.sha256(person_source_value.encode())
        truncated_hash = int(hash_object.hexdigest()[:16], 16)
        return truncated_hash

    def insert_column_into_person_table(self, df, col):
        with self.Session() as session:
            for value in df[col]:
                if value is not None:
                    person_id = self.generate_person_id(value)
                    person = Person(person_source_value=value,
                                    person_id=person_id)
                    session.add(person)
            session.commit()

    def close_connection(self):
        self.engine.dispose()
        print("Database connection closed.")


if __name__ == "__main__":
    db = PersonDatabase("person")
    db.create_person_table()
    res = db.transformation()
    db.insert_NIR_into_person_table(res, "NIR_ANO_17")
    db.update_gender_in_person_table(res, "COD_SEX")
    db.insert_column_into_person_table(res, "NIR_ANO_17")
    db.close_connection()
