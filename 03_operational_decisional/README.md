# TP 3 — Du système opérationnel au système décisionnel

Ce TP reprend les deux jeux de données utilisés dans les chapitres précédents et les fait entrer dans une architecture décisionnelle simple en couches **Bronze / Silver / Gold**.

L'objectif n'est plus seulement de corriger des problèmes de qualité, mais de comprendre :

- où conserver les données reçues ;
- où appliquer les transformations ;
- comment intégrer plusieurs sources ;
- comment publier une couche commune destinée à l'analyse.

## Structure du dossier

```text
03_operational_decisional/
├── README.md
├── data/
│   ├── spaceship_titanic_missing.csv
│   └── passenger_biometrics.csv
└── notebook/
    └── 03_architecture_decisionnelle_etudiant.py
```

## Prérequis

Avant de commencer, vous devez disposer :

- d'un compte **Databricks Free Edition** ;
- des notions vues dans les chapitres 1 et 2 ;
- des deux fichiers CSV présents dans le dossier `data/`.

> **Important :** utilisez bien **Databricks Free Edition** et non l'offre **Free Trial** ou une autre version nécessitant la configuration d'un environnement cloud ou d'un moyen de paiement.

## Mise en place dans Databricks

### 1. Importer le notebook

Dans Databricks :

1. ouvrez votre **Workspace** ;
2. créez éventuellement un dossier dédié au TP ;
3. importez le fichier :

```text
notebook/03_architecture_decisionnelle_etudiant.py
```

Le fichier `.py` est reconnu par Databricks comme un notebook.

### 2. Préparer l'environnement

Exécutez les premières cellules du notebook.

Elles permettent notamment de créer :

- un schéma `bronze` ;
- un schéma `silver` ;
- un schéma `gold` ;
- un volume `tp03_sources`.

### 3. Charger les données

Dans **Catalog Explorer**, ouvrez le volume `tp03_sources` puis chargez les deux fichiers :

```text
spaceship_titanic_missing.csv
passenger_biometrics.csv
```

Revenez ensuite dans le notebook.

## Déroulement du TP

Le TP suit les étapes suivantes :

```text
Sources CSV
    ↓
Bronze
    ↓
Silver
    ↓
Intégration
    ↓
Gold
    ↓
Analyse SQL
```

Vous allez notamment :

1. charger et contrôler les fichiers sources ;
2. créer les tables Bronze ;
3. vérifier que Bronze conserve bien les données reçues ;
4. rejouer certaines règles de Data Quality vues précédemment ;
5. construire les tables Silver ;
6. intégrer les deux sources grâce à `PassengerId` ;
7. produire une table Gold orientée analyse ;
8. répondre à plusieurs questions avec SQL.

## Architecture construite

```text
CSV sources
   │
   ▼
BRONZE
├── passengers
└── biometrics
   │
   ▼
SILVER
├── passengers
├── biometrics
└── passengers_enriched
   │
   ▼
GOLD
└── passenger_kpis_by_homeplanet
```

## Rappel sur les couches

### Bronze

La couche Bronze conserve les données au plus proche de ce qui a été reçu.

Les problèmes de qualité ne doivent pas être corrigés directement dans cette couche.

### Silver

La couche Silver contient des données :

- typées ;
- nettoyées ;
- corrigées ;
- enrichies ;
- intégrées entre plusieurs sources.

Les règles de Data Quality des chapitres précédents seront réutilisées à ce niveau.

### Gold

La couche Gold contient des données préparées pour un usage analytique ou métier.

Dans ce TP, elle servira à produire quelques indicateurs synthétiques.

## Conseils

- Exécutez le notebook dans l'ordre.
- Ne supprimez pas les données de Bronze pour corriger une erreur.
- Vérifiez régulièrement le nombre de lignes et l'unicité de `PassengerId`.
- Lisez les questions de réflexion avant d'écrire le code.
- Utilisez les résultats des TP précédents pour retrouver les traitements à appliquer.

## Objectif final

À la fin du TP, vous devez être capables d'expliquer le rôle de chaque couche :

```text
Bronze → conserver
Silver → nettoyer et intégrer
Gold   → préparer pour l'analyse
```

et de comprendre pourquoi une architecture en couches facilite :

- le reprocessing ;
- la reproductibilité ;
- l'intégration de plusieurs sources ;
- le partage d'une référence commune pour l'analyse.
