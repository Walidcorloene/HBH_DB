# Test technique
## Introduction
Lors de ce test vous allez créer une table *person* au format OMOP-CDM à partir des tables T_MCOAAC et T_MCOAAB du **SNDS**. Les colonnes de la table *person* et leurs équivalents dans le SNDS sont reportées ci-dessous. Le nom des variables utiles pour le test vous est communiqué dans l'énoncé et dans les questions ; une connaissance des tables du SNDS n'est donc pas requise pour la réalisation du test.

Les questions sont à réaliser dans l'ordre et sont par ordre de difficulté croissante. La plupart des questions sont volontairement vagues ; dans ce cas, choisissez une interprétation raisonnable. L'objectif du test est d'avoir un support de conversation pour le second entretien et de discuter autour du raisonnement.

Le test est à réaliser en **maximum deux heures**. Il est très probable que vous ne finissiez pas toutes les questions dans le temps imparti ; ce n'est absolument pas un problème.

Le test comporte une partie traitement des données, une partie construction de la nouvelle table (en SQL) ainsi qu'une partie base de données.


## Présentation du SNDS
Le SNDS historique est une base de données médico-administrative comportant principalement les remboursements de soins de ville et les hospitalisations pour la quasi-totalité de la population française. De par son système de sécurité sociale, la France fait partie des rares pays qui disposent de systèmes d’informations médico-administratives couvrant l’ensemble du territoire et de la population.

Le SNDS est alimenté par trois bases de données :
• le SNIIRAM (Système National d’Information Inter-Régimes de l’Assurance Maladie) : Les Caisses Primaires d’Assurance Maladie remontent l’ensemble des informations issues des remboursements à la CNAM (Caisse Nationale de l’Assurence Malaide)
• le PMSI (Programme de Médicalisation des Systèmes d’Information) : Chaque établissement de santé enregistre chacun des séjours hospitaliers sous forme derésumés de sortie standardisé (RSS) qui sont ensuite transmis à l’Agence Technique de l’Information Hospitalière (ATIH). Ce dernier remonte ensuite les données consolidées à la CNAM pour intégration dans le SNDS
• le CépiDc : Le CépiDc de l’Inserm gère la Base de Causes Médicales de Décès (BCMD). Il ne traite que la partie médicale du certificat de décès. Par conséquent, la base ne contient aucun nom. Les données sont transmises à la CNAM pour intégration dans le SNDS

# Présentation du format OMOP-CDM

Le modèle commun de données OMOP-CDM (Observational Medical Outcomes Partnership - Common Data Model) est un modèle relationnel de bases de données de santé, qui a pour objectif l'interopérabilité entre les différentes bases d'analyse en santé, qu'elles soient cliniques ou médico-administratives.

Le modèle commun OMOP-CDM est maintenu et développé au sein de la communauté open-source OHDSI (Observational Health Data Sciences and Informatics - prononcer "odyssée").


## Format de données

Deux tables de données de synthèse vous sont fournies : T_MCOAAC et T_MCOAAB. Ces tables correspondent aux personnes ayant eu des soins à l'hôpital et la description de leur séjour à l'hôpital. Vous pouvez utiliser les ressources en lignes du HDH pour en savoir plus sur ces tables. Les données sont des données fictives qui respectent le format et type des données réelles du SNDS. Il n'y a donc aucune cohérence médicale dans ces données.
* [Documentation](https://documentation-snds.health-data-hub.fr)
* [Dictionnaire](https://drees.shinyapps.io/dico-snds/)

L'identifiant anonymisé des personnes dans la table T_MCOAAC correspond à la variable `NIR_ANO_17`. Les clés de jointure entre les tables T_MCOAAC et T_MCOAAB sont les variables `ETA_NUM` (numéro finess juridique de l'établissement de santé) et `RSA_NUM`.



| format OMOP-CDM | équivalent dans le SNDS |
| -------- | -------- |
| person_id   | à calculer |
| person_source_value    | variable `NIR_ANO_17` de la table T_MCOAAC  |
| gender_concept_id  (chercher les valeurs correspondantes dans la [documentation](https://www.ohdsi.org/web/wiki/doku.php))  | variable `COD_SEX` de la table T_MCOAAB = [1 si un homme, 2 = si c'est une femme, 0/9 si mal renseigné ou indéterminé]     |
| year_of_birth     | à calculer  |

## Questions

Les questions 1 à 6 sont à traiter en Python, dans un script ou dans un notebook, en utilisant un moteur SQL de votre choix, par exemple sqlite. Vous pourrez vous servir de l'ORM sqlalchemy. Vous serez attentif à coder le plus possible en orienté objet.

Vous utiliserez un répertoire git local avec des commits réguliers. Vous enverrez ce repo compressé par courriel comme rendu final aux personnes qui vous feront passer l’entretien, en prenant soin d'y inclure le répertoire .git/.

1. Créer la table *person* dans la base de données choisie.
2. Ouvrir les tables T_MCOAAC et T_MCOAAB, et enlever les doublons et les valeurs manquantes. Calculer le nombre de lignes pour chaque table, la distribution homme/femme de la table T_MCOAAB.
3. Remplir la colonne **person_source_value** de la table *person*.
4. Remplir la colonne **gender_concept_id** de la table *person* avec les équivalents au format OMOP-CDM, et enlever les patients pour qui le sexe n'est pas défini dans le SNDS classique.
5. Créer un identifiant unique **person_id** tel qu'un **person_source_value** corresponde à un **person_id**. On demande ici de créer un *nouvel* identifiant, qui ne permette pas facilement de retrouver **person_source_value**. Par exemple, il faut imaginer que les valeurs de **person_source_value** sont des numéros de sécurité sociale: ce sont des données sensibles qu'on ne peut pas utiliser telles quelles. 
6. Calculer l'**année de naissance** à partir des tables T_MCOAAC (utiliser la variable `EXE_SOI_DTD`) et T_MCOAAB (utiliser la variable `AGE_ANN`).
7. Produire un graphique représentant, pour chaque sexe, la distribution des dates de naissance. Si vous produisez un script et pas un notebook, veillez à sauvegarder la figure résultante.
8. Ecrire un script en bash permettant de récupérer `person.csv` (en utilisant "|" comme délimiteur). Récupérer **person_id**, **gender_concept_id** et **year_of_birth**. Pour chaque **gender_concept_id**, afficher le plus grand **year_of_birth** avec le **person_id** correspondant.


**En cas de problème, n'hésitez pas à nous contacter.**
