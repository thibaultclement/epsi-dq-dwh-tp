# Databricks notebook source
# MAGIC %md
# MAGIC # TP 3 - Du système opérationnel au système décisionnel
# MAGIC ## Version étudiant - Databricks Free Edition
# MAGIC
# MAGIC Dans les deux premiers TP, nous avons appris à **diagnostiquer** et **corriger** certains problèmes de qualité.
# MAGIC
# MAGIC Ici, la question change :
# MAGIC
# MAGIC > Où conserver la donnée reçue ? Où appliquer les corrections ? Comment intégrer plusieurs sources ? Comment publier une donnée commune pour l'analyse ?
# MAGIC
# MAGIC Nous allons construire une architecture simple :
# MAGIC
# MAGIC ```text
# MAGIC Sources CSV → Bronze → Silver → Gold → SQL
# MAGIC ```
# MAGIC
# MAGIC Le but n'est pas de refaire entièrement les TP 1 et 2, mais de **rejouer leurs règles de qualité dans une architecture décisionnelle**.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Préparer le workspace
# MAGIC
# MAGIC Le notebook utilise le **catalogue courant** et crée trois schémas :
# MAGIC
# MAGIC - `bronze` : données proches de la source ;
# MAGIC - `silver` : données nettoyées et intégrées ;
# MAGIC - `gold` : données préparées pour un usage analytique.
# MAGIC
# MAGIC Un volume `tp03_sources` est également créé pour recevoir les deux CSV.
# MAGIC
# MAGIC Cette partie est fournie : exécutez la cellule puis chargez les deux CSV demandés dans le volume indiqué.

# COMMAND ----------
from uuid import uuid4

from pyspark.sql import functions as F
from pyspark.sql import types as T

CURRENT_CATALOG = spark.sql("SELECT current_catalog() AS catalog").first()["catalog"]
print("Catalogue courant :", CURRENT_CATALOG)

for schema in ["bronze", "silver", "gold"]:
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS `{CURRENT_CATALOG}`.`{schema}`")

spark.sql(f"CREATE SCHEMA IF NOT EXISTS `{CURRENT_CATALOG}`.`tp03`")
spark.sql(
    f"CREATE VOLUME IF NOT EXISTS `{CURRENT_CATALOG}`.`tp03`.`tp03_sources`"
)

VOLUME_PATH = f"/Volumes/{CURRENT_CATALOG}/tp03/tp03_sources"
PASSENGERS_PATH = f"{VOLUME_PATH}/spaceship_titanic_missing.csv"
BIOMETRICS_PATH = f"{VOLUME_PATH}/passenger_biometrics.csv"

print("Volume :", VOLUME_PATH)
print("\nChargez maintenant dans ce volume :")
print("- spaceship_titanic_missing.csv")
print("- passenger_biometrics.csv")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Charger les fichiers sources
# MAGIC
# MAGIC **Important :** nous ne corrigeons rien à ce stade.
# MAGIC
# MAGIC Les fichiers doivent être lus avec leurs colonnes sous forme de chaînes de caractères. Le typage métier sera réalisé en Silver.
# MAGIC
# MAGIC ### Travail
# MAGIC 1. Chargez les deux CSV avec Spark.
# MAGIC 2. Conservez `header=True` et désactivez l'inférence automatique du schéma.
# MAGIC 3. Affichez quelques lignes de chaque source.

# COMMAND ----------
# TODO - Charger les deux fichiers avec spark.read.csv(...)
#
# passengers_source = (...)
# biometrics_source = (...)
#
# print("Passengers :", passengers_source.count(), "lignes")
# print("Biometrics :", biometrics_source.count(), "lignes")
# display(passengers_source.limit(10))
# display(biometrics_source.limit(10))

raise NotImplementedError("TODO - charger les deux fichiers sources")

# COMMAND ----------
# MAGIC %md
# MAGIC ### Contrôle des sources
# MAGIC
# MAGIC Les deux fichiers doivent contenir 4 000 passagers et partager la clé `PassengerId`.
# MAGIC
# MAGIC ### Questions
# MAGIC - Combien de lignes contient chaque source ?
# MAGIC - `PassengerId` est-il unique dans chaque fichier ?
# MAGIC - Les 4 000 identifiants sont-ils communs aux deux sources ?

# COMMAND ----------
# TODO - Vérifier le nombre de lignes, l'unicité de PassengerId et le nombre d'identifiants communs.
#
# Indices :
# - count()
# - select(...).distinct().count()
# - join(..., "PassengerId", "inner")

raise NotImplementedError("TODO - contrôler les deux sources")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. Construire Bronze
# MAGIC
# MAGIC Bronze conserve les données **telles qu'elles ont été reçues**.
# MAGIC
# MAGIC Nous ajoutons uniquement des métadonnées d'ingestion :
# MAGIC
# MAGIC - `_source_file` ;
# MAGIC - `_ingested_at` ;
# MAGIC - `_load_id`.
# MAGIC
# MAGIC Aucune imputation ni correction d'outlier ne doit être réalisée ici.
# MAGIC
# MAGIC ### Question
# MAGIC Pourquoi est-il important de conserver les anomalies et les valeurs manquantes dans Bronze ?

# COMMAND ----------
# TODO - Compléter la fonction pour ajouter les trois métadonnées d'ingestion.
def add_ingestion_metadata(df, source_file: str, load_id: str):
    # À compléter
    raise NotImplementedError("TODO - ajouter les métadonnées d'ingestion")

# COMMAND ----------
# TODO - Créer un load_id pour chaque source, construire bronze_passengers et bronze_biometrics,
# puis enregistrer les deux DataFrames dans :
# - <catalog>.bronze.passengers
# - <catalog>.bronze.biometrics
#
# Indices : uuid4(), write.mode("overwrite").saveAsTable(...)

raise NotImplementedError("TODO - créer les deux tables Bronze")

# COMMAND ----------
# MAGIC %md
# MAGIC ### Vérifier que Bronze contient toujours les problèmes de qualité
# MAGIC
# MAGIC C'est **normal et souhaité** : Bronze sert à conserver la donnée reçue afin de pouvoir rejouer les traitements plus tard.
# MAGIC
# MAGIC ### Travail
# MAGIC Comptez les valeurs manquantes de `HomePlanet`, `CryoSleep` et `RoomService` dans `bronze.passengers`.

# COMMAND ----------
# TODO - Écrire une requête SQL qui compte les valeurs manquantes des trois colonnes.
#
# bronze_missing = spark.sql(f"""
# SELECT ...
# FROM `{CURRENT_CATALOG}`.`bronze`.`passengers`
# """)
# display(bronze_missing)

raise NotImplementedError("TODO - contrôler les valeurs manquantes dans Bronze")

# COMMAND ----------
# MAGIC %md
# MAGIC ### Biométrie : repérer quelques anomalies manifestes
# MAGIC
# MAGIC Recherchez dans `bronze.biometrics` des valeurs clairement suspectes :
# MAGIC
# MAGIC - taille inférieure à 3 ;
# MAGIC - taille supérieure à 1000 ;
# MAGIC - poids négatif ;
# MAGIC - poids supérieur à 500.

# COMMAND ----------
# TODO - Écrire une requête SQL pour afficher les lignes concernées.

raise NotImplementedError("TODO - inspecter les anomalies biométriques dans Bronze")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 4. Construire Silver - reprendre les décisions DQ des TP précédents
# MAGIC
# MAGIC Nous **ne refaisons pas l'étude complète** des mécanismes de manque et des méthodes d'anomalies.
# MAGIC
# MAGIC Nous rejouons les décisions retenues précédemment :
# MAGIC
# MAGIC ### Valeurs manquantes
# MAGIC - `HomePlanet` → mode ;
# MAGIC - `CryoSleep` → régression logistique avec `Age`, `FoodCourt`, `Spa` ;
# MAGIC - `RoomService` → indicateur de manque + médiane.
# MAGIC
# MAGIC ### Biométrie
# MAGIC - corriger les erreurs identifiables ;
# MAGIC - conserver les valeurs rares mais plausibles ;
# MAGIC - signaler les cas restant à investiguer.

# COMMAND ----------
# MAGIC %md
# MAGIC ### 4.1 Silver - passengers : typage
# MAGIC
# MAGIC Avant d'appliquer les règles DQ, construisez une version typée de `bronze.passengers` :
# MAGIC
# MAGIC - `CryoSleep` et `VIP` en booléens ;
# MAGIC - `Age`, `RoomService`, `FoodCourt`, `Spa` en `double` ;
# MAGIC - conservez les métadonnées d'ingestion.

# COMMAND ----------
# TODO - Construire passengers_typed à partir de bronze.passengers.
#
# Indices :
# - spark.table(...)
# - F.col(...).cast("double")
# - F.when(...).when(...).otherwise(...)

raise NotImplementedError("TODO - typer la table passengers")

# COMMAND ----------
# MAGIC %md
# MAGIC ### 4.2 `HomePlanet` - imputation par le mode
# MAGIC
# MAGIC Reprenez la règle retenue au TP 1 :
# MAGIC
# MAGIC 1. calculez le mode de `HomePlanet` sur les valeurs observées ;
# MAGIC 2. remplacez uniquement les valeurs manquantes ;
# MAGIC 3. stockez le résultat dans `passengers_silver`.

# COMMAND ----------
# TODO - Calculer le mode puis imputer HomePlanet.

raise NotImplementedError("TODO - imputer HomePlanet par le mode")

# COMMAND ----------
# MAGIC %md
# MAGIC ### 4.3 `CryoSleep` - régression logistique
# MAGIC
# MAGIC Reprenez les trois variables utilisées au TP 1 :
# MAGIC
# MAGIC - `Age` ;
# MAGIC - `FoodCourt` ;
# MAGIC - `Spa`.
# MAGIC
# MAGIC Le dataset est petit : vous pouvez convertir temporairement les colonnes utiles en pandas, entraîner une `LogisticRegression`, puis réinjecter les prédictions dans Spark.

# COMMAND ----------
import pandas as pd
from sklearn.linear_model import LogisticRegression

# TODO -
# 1. sélectionner PassengerId, CryoSleep, Age, FoodCourt, Spa ;
# 2. convertir en pandas ;
# 3. séparer lignes observées / manquantes ;
# 4. entraîner LogisticRegression(max_iter=1000) ;
# 5. prédire CryoSleep pour les lignes manquantes ;
# 6. convertir les prédictions en DataFrame Spark ;
# 7. joindre les prédictions à passengers_silver ;
# 8. remplacer uniquement les CryoSleep manquants.

raise NotImplementedError("TODO - imputer CryoSleep avec une régression logistique")

# COMMAND ----------
# MAGIC %md
# MAGIC ### 4.4 `RoomService` - indicateur de manque + médiane
# MAGIC
# MAGIC L'information qu'une valeur était initialement absente doit être conservée.
# MAGIC
# MAGIC ### Travail
# MAGIC 1. Créez `RoomService_missing` **avant** l'imputation.
# MAGIC 2. Calculez la médiane observée de `RoomService`.
# MAGIC 3. Remplacez les valeurs manquantes par cette médiane.
# MAGIC 4. Enregistrez ensuite `silver.passengers`.

# COMMAND ----------
# TODO - Créer le flag de manque, calculer la médiane et imputer RoomService.
# Indice pour la médiane : approxQuantile("RoomService", [0.5], 0.0)

raise NotImplementedError("TODO - traiter RoomService")

# COMMAND ----------
# MAGIC %md
# MAGIC ### Contrôle de la table Silver passengers
# MAGIC
# MAGIC Vérifiez :
# MAGIC
# MAGIC - qu'il reste 4 000 lignes ;
# MAGIC - que `HomePlanet`, `CryoSleep` et `RoomService` ne contiennent plus de valeurs manquantes ;
# MAGIC - que le nombre de `RoomService_missing = 1` est bien conservé.

# COMMAND ----------
# TODO - Écrire les contrôles nécessaires.

raise NotImplementedError("TODO - contrôler silver.passengers")

# COMMAND ----------
# MAGIC %md
# MAGIC ### 4.5 Silver - biometrics : typage puis corrections
# MAGIC
# MAGIC Commencez par convertir `height_cm` et `weight_kg` en `double`.
# MAGIC
# MAGIC Rejouez ensuite les corrections déterministes du TP 2 **dans cet ordre** :
# MAGIC
# MAGIC 1. inversion probable taille / poids : `height_cm` entre 70 et 100 ET `weight_kg` entre 150 et 220 ;
# MAGIC 2. taille saisie en mètres : taille entre 1.0 et 2.5 → multiplier par 100 ;
# MAGIC 3. décalage de décimale sur la taille : taille > 1000 → diviser par 10 ;
# MAGIC 4. décalage de décimale sur le poids : poids > 500 → diviser par 10 ;
# MAGIC 5. poids négatif → valeur absolue.
# MAGIC
# MAGIC Conservez un indicateur booléen pour chaque correction appliquée.

# COMMAND ----------
# TODO - Construire biometrics_typed puis biometrics_clean en appliquant les cinq règles.
#
# Noms d'indicateurs conseillés :
# - _swap_detected
# - _height_unit_corrected
# - _height_decimal_corrected
# - _weight_decimal_corrected
# - _negative_weight_corrected

raise NotImplementedError("TODO - corriger les erreurs biométriques déterministes")

# COMMAND ----------
# MAGIC %md
# MAGIC ### Vérifier les corrections déterministes
# MAGIC
# MAGIC Comptez combien de lignes ont été concernées par chacune des cinq corrections.

# COMMAND ----------
# TODO - Agréger les indicateurs de correction avec sum(cast("int")).

raise NotImplementedError("TODO - compter les corrections biométriques")

# COMMAND ----------
# MAGIC %md
# MAGIC ### 4.6 Conserver les valeurs rares et signaler les cas à investiguer
# MAGIC
# MAGIC Après correction des erreurs identifiables, utilisez un **Isolation Forest** avec :
# MAGIC
# MAGIC - `n_estimators=200` ;
# MAGIC - `contamination=0.01` ;
# MAGIC - `random_state=42`.
# MAGIC
# MAGIC Les observations inhabituelles ne doivent **pas** être supprimées. Ajoutez un booléen `needs_review`.

# COMMAND ----------
from sklearn.ensemble import IsolationForest

# TODO -
# 1. convertir PassengerId, height_cm, weight_kg en pandas ;
# 2. entraîner IsolationForest ;
# 3. produire isolation_forest et needs_review ;
# 4. reconvertir les flags en Spark ;
# 5. joindre à biometrics_clean ;
# 6. enregistrer silver.biometrics.

raise NotImplementedError("TODO - ajouter le flag needs_review avec Isolation Forest")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 5. Intégrer les deux sources
# MAGIC
# MAGIC Les deux sources partagent `PassengerId`.
# MAGIC
# MAGIC Utilisez `silver.passengers` comme table de référence et réalisez un **LEFT JOIN** avec `silver.biometrics`.
# MAGIC
# MAGIC ### Questions avant de coder
# MAGIC - Pourquoi un `LEFT JOIN` plutôt qu'un `INNER JOIN` ?
# MAGIC - Quel risque existe si `PassengerId` n'est pas unique dans `silver.biometrics` ?
# MAGIC - Combien de lignes attendez-vous après la jointure ?

# COMMAND ----------
# TODO -
# 1. charger les deux tables Silver ;
# 2. contrôler l'unicité de PassengerId ;
# 3. joindre les deux sources ;
# 4. vérifier que le nombre de lignes reste égal à 4 000 ;
# 5. enregistrer silver.passengers_enriched.

raise NotImplementedError("TODO - intégrer passengers et biometrics")

# COMMAND ----------
# MAGIC %md
# MAGIC ### Contrôle de l'intégration
# MAGIC
# MAGIC Écrivez une requête SQL retournant :
# MAGIC
# MAGIC - le nombre total de lignes ;
# MAGIC - le nombre de `PassengerId` distincts ;
# MAGIC - le nombre de passagers sans biométrie.

# COMMAND ----------
# TODO - Écrire la requête SQL de contrôle.

raise NotImplementedError("TODO - contrôler la jointure")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 6. Créer une couche Gold orientée analyse
# MAGIC
# MAGIC Silver contient maintenant une vue intégrée au niveau **passager**.
# MAGIC
# MAGIC Construisez une table Gold par `HomePlanet` contenant :
# MAGIC
# MAGIC - `passenger_count` : nombre de passagers ;
# MAGIC - `cryosleep_rate` : part des passagers en cryosommeil ;
# MAGIC - `avg_room_service` : dépense moyenne RoomService ;
# MAGIC - `avg_height_cm` : taille moyenne ;
# MAGIC - `avg_weight_kg` : poids moyen ;
# MAGIC - `biometrics_to_review` : nombre de profils biométriques à investiguer ;
# MAGIC - `room_service_initially_missing` : nombre de valeurs RoomService initialement manquantes.
# MAGIC
# MAGIC Enregistrez cette table sous :
# MAGIC
# MAGIC `gold.passenger_kpis_by_homeplanet`
# MAGIC
# MAGIC Nous ne construisons pas encore de schéma en étoile : ce sera l'objet du chapitre de modélisation dimensionnelle.

# COMMAND ----------
# TODO - Construire gold_homeplanet avec groupBy(...).agg(...) puis l'enregistrer.

raise NotImplementedError("TODO - construire la table Gold")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 7. Interroger Gold avec SQL
# MAGIC
# MAGIC Les consommateurs n'ont plus besoin de connaître :
# MAGIC
# MAGIC - les deux CSV d'origine ;
# MAGIC - les règles d'imputation ;
# MAGIC - les erreurs de saisie biométriques ;
# MAGIC - la jointure entre les sources.
# MAGIC
# MAGIC Ils interrogent une couche publiée et commune.

# COMMAND ----------
# MAGIC %md
# MAGIC ### Question 1 - Combien de passagers proviennent de chaque planète ?

# COMMAND ----------
# TODO - Requête SQL.

raise NotImplementedError("TODO - question SQL 1")

# COMMAND ----------
# MAGIC %md
# MAGIC ### Question 2 - Quelle planète présente la plus forte proportion de passagers en cryosommeil ?

# COMMAND ----------
# TODO - Requête SQL.

raise NotImplementedError("TODO - question SQL 2")

# COMMAND ----------
# MAGIC %md
# MAGIC ### Question 3 - Où trouve-t-on le plus de profils biométriques encore à investiguer ?
# MAGIC
# MAGIC Affichez également le taux de profils à revoir en pourcentage du nombre de passagers de chaque planète.

# COMMAND ----------
# TODO - Requête SQL.

raise NotImplementedError("TODO - question SQL 3")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Bilan
# MAGIC
# MAGIC Complétez le schéma avec vos propres mots :
# MAGIC
# MAGIC ```text
# MAGIC CSV
# MAGIC  ↓
# MAGIC Bronze   : ...
# MAGIC  ↓
# MAGIC Silver   : ...
# MAGIC  ↓
# MAGIC Gold     : ...
# MAGIC  ↓
# MAGIC SQL      : ...
# MAGIC ```
# MAGIC
# MAGIC ### Questions finales
# MAGIC 1. Pourquoi ne corrige-t-on pas directement les données dans Bronze ?
# MAGIC 2. Quelle différence faites-vous entre Silver et Gold dans ce TP ?
# MAGIC 3. Si la règle d'imputation de `HomePlanet` est améliorée demain, quelles couches doivent être reconstruites ?
