# Introduction

Bienvenue dans la documentation de connexion à l’API Hyperplanning.
Ce document vous guidera pas à pas pour accéder à l’API, en suivant les étapes décrites dans la section **Quickstart**
de la [documentation officielle](https://hyperplanning.github.io/doc/docs/quickstart.html).

## Prérequis

1. **Identifiants**
    - Vous devez disposer des identifiants qui vous ont été envoyés (nom d’utilisateur et mot de passe ou jeton).
2. **URL de connexion**
    - Vous devez également connaître l’URL de base de l’API :
      `https://backend-cdn-endpoint-prod-afccapcwframgnag.z02.azurefd.net`.

## Objectif

- Se connecter à l’API Hyperplanning et tester rapidement un premier appel pour vérifier que tout fonctionne.

Dans les sections suivantes, nous détaillerons les différentes étapes pour configurer votre environnement, vous
authentifier auprès de l’API, et récupérer les informations d’**assolement**, de **rendement** et de **volume**.

> *Remarque : N’hésitez pas à vérifier régulièrement
la [documentation officielle Quickstart](https://hyperplanning.github.io/doc/docs/quickstart.html) pour bénéficier des
dernières mises à jour et recommandations.*

## Récupération des données

La route principale permettant de récupérer les données est :  `elastic/search/reduce`.

Cette route constitue le point d’accès central pour effectuer la **récupération des données d’assolement, de rendement
et de volume** par différentes cultures et au niveau des différentes zones.

### Exemple - Récupérer les assolements

##### Exemple d’appel en Python

Pour illustrer la récupération de l’assolement pour les années 2023, 2024 et 2025 dans une zone précise, voici un
exemple de code Python.
Ici, nous utilisons l'objet `client` (dont l’instanciation est expliquée dans la partie Quickstart de la documentation)
pour envoyer une requête `POST` à la route `elastic/search/reduce` avec le **payload** suivant :

```python
payload = {
    "agg": [
        {
            "operation": "sum",
            "metaId": 3
        }
    ],
    "filters": [
        [
            {
                "metaId": "zone",
                "operation": "in",
                "value": [
                    "cjikt35x83t1z2rnx"
                ]
            },
            {
                "metaId": 1,
                "operation": "in",
                "value": [
                    5,
                    20,
                    10,
                    1
                ],
                "dateIn": [
                    [
                        None,
                        2023
                    ],
                    [
                        None,
                        2024
                    ],
                    [
                        None,
                        2025
                    ]
                ]
            }
        ]
    ],
    "bins": [
        {
            "metaId": 1,
            "operation": "in",
            "value": [
                5,
                20,
                10,
                1
            ]
        },
        {
            "metaId": "year",
            "operation": "in",
            "value": [
                2023,
                2024,
                2025
            ]
        }
    ]
}

data_response = client.post("elastic/search/reduce", data=payload).json()
```

### Détail du `payload`

Le `payload` utilisé ici comporte trois sections principales : **agg**, **filters** et **bins**.

1. **`agg`**
    - Contient un tableau d’objets décrivant l’opération d’agrégation et le label concerné.
    - Dans cet exemple, une seule agrégation est définie :
        - **`operation = "sum"`** : indique que nous voulons calculer la somme.
        - **`metaId = 3`** : correspond au label représentant la **surface**.
    - Ainsi, nous allons calculer la somme de la surface pour tous les éléments qui répondent aux critères du filtre.
    - Si dateRange est spécifié cela correspond à la valeur cumulé sur la plage donnée

2. **`filters`**
    - Définit la liste des conditions qui vont **restreindre** le périmètre des données à récupérer.
    - Dans l’exemple, on retrouve trois filtres dans un tableau imbriqué :
        1. **`metaId = "zone_group"`**, `operation = "equal"`, `value = 47`
            - Sélectionne un **groupe de zones** spécifique (ID 47) qui correspond aux sections de l'organisation.
        2. **`metaId = "zone"`**, `operation = "in"`, `value = ["cjikt35x83t1z2rnxpdmjs7y7"]`
            - Sélectionne la **zone** ayant l’identifiant cjikt35x83t1z2rnxpdmjs7y7.
        3. **`metaId = 1`**, `operation = "in"`**, avec une liste de valeurs correspondant aux **cultures** (ex. 5, 20,
           10, etc.).
            - Le champ **`dateIn`** associe ces cultures aux années 2023, 2024 et 2025 (sous forme de paires
              `[None, année]`).
    - Si dateRange ou dateIn est précisé il filtre le metaId précisé

3. **`bins`**
    - Permet de **regrouper** les résultats selon un ou plusieurs critères.
    - Dans l’exemple, deux regroupements sont définis :
        1. **`metaId = 1`** : regrouper selon le **type de culture**.
        2. **`metaId = "year"`** : regrouper selon l’**année** (2023, 2024 et 2025).
    - Ainsi, les résultats de l’agrégation (la somme des surfaces) seront **segmentés** à la fois par culture et par
      année.
    - Si dateRange est précisé il filtre le metaId précisé

Formats :

- dateRange : [[min_week|None, min_year], [max_week|None, max_year]]
- dateIn : [List([week|None, year])]
- metaId : ['zone', 'zone_group', 'year', 'week', 'int']

> **En résumé :**
> - **`agg`** : détermine la **somme** à calculer sur le label `metaId = 3` (surface).
> - **`filters`** : applique un filtre sur un groupe de zones (`zone_group = 47`), une zone spécifique (`zone = 42314`),
    et un ensemble de cultures (`metaId = 1`, liste de valeurs) liées aux années 2023 à 2025.
> - **`bins`** : **bascule** les résultats par culture (`metaId = 1`) et par année (`year`), permettant d’obtenir la
    somme des surfaces pour chaque combinaison (culture, année).

### Exemple de retour de la requête

Une fois votre requête envoyée à la route `elastic/search/reduce` (avec l’agrégation `metaId = 3` et `operation = sum`),
la réponse se présente généralement sous la forme d’un tableau d’objets :

```json
[
  {
    "keys": [
      {
        "key": "1",
        "value": 19
      },
      {
        "key": "year",
        "value": 2024
      }
    ],
    "sum_3": 10112.84
  },
  {
    "keys": [
      {
        "key": "1",
        "value": 19
      },
      {
        "key": "year",
        "value": 2025
      }
    ],
    "sum_3": 10033.29
  }
]
```

- **`keys`** :
    - Il s’agit d’un tableau où chaque élément correspond à un critère ou un groupe (culture, année, etc.).
    - Par exemple, `key: "1"` fait référence au **label 1**, c’est-à-dire la **culture**, et la `value` associée (ex.
      `19`) est l’**identifiant** de cette culture.
    - `key: "year"` indique l’année considérée (ex. `2024`, `2025`, etc.).

- **`sum_3`** :
    - Ce champ correspond à l’opération d’agrégation (`sum`) appliquée au **label** dont l’identifiant `metaId` est **3
      ** (dans notre cas, la **surface**).
    - Sa valeur (ex. `10112.84` ou `10033.29`) représente la **somme des surfaces** pour la combinaison **(culture,
      année)** définie dans `keys`.

> **En résumé :**
> - La liste renvoie autant d’éléments que nécessaire, chacun décrivant les résultats agrégés pour une combinaison **(
    culture, année)**.
> - L’attribut `sum_3` représente la somme totale des surfaces correspondant à la paire **(culture, année)**.

#### Récupération du volume

Pour récupérer le **volume** au lieu de la surface, il suffit de remplacer la section `agg` par :

```json
{
  "operation": "sum",
  "metaId": 10
}
```

Ici, `metaId = 10` correspond au volume, et l’opération sum renverra la somme du **volume** pour les mêmes filtres et
groupes définis.

#### Récupération du rendement

Pour calculer le **rendement** sous forme de moyenne pondérée, vous pouvez utiliser la structure suivante dans la
section `agg` :

```json
[
  {
    "operation": "avg",
    "metaId": 9,
    "weightedMetaId": 3
  }
]
```

- **`metaId = 9`** : Correspond au label représentant le **rendement**.
- **`operation = "avg"`** : Indique que nous allons calculer une **moyenne** du rendement.
- **`weightedMetaId = 3`** : Permet de **pondérer** la moyenne du rendement par la **surface** (label `metaId = 3`), si
  vous souhaitez obtenir un rendement moyen tenant compte de la taille des parcelles concernées.

> **En pratique**, cela vous renverra la moyenne pondérée du rendement (label 9) en fonction de la surface (label 3),
> pour les filtres et années que vous aurez spécifiés dans votre requête.

### Pour aller plus loin

- Pour en savoir plus sur la façon de récupérer les **identifiants des zones** (comme les sections ou autres), veuillez
  consulter la [documentation dédiée aux zones](https://hyperplanning.github.io/doc/docs/zones.html).
- Pour obtenir davantage de détails concernant les **labels**, leurs **identifiants**, ainsi que les **identifiants des
  cultures**, reportez-vous à la [référence de l’API](https://hyperplanning.github.io/doc/docs/api_reference.html).

### Correspondance Zones et id de zones du reduce

Procédure de correspondance des zones (administratives / customs) avec les id de zone du reduce.

#### Etape 1 : Récupérer l’ID du zone group désiré.

`GET /v1/zone-groups`

Dans le name vous trouverez le nom du type de zone ainsi que le zone group correspondant.
Par exemple municipalité aura l’ID 2 et sections l’ID 47.

#### Etape 2 : Récupérer la liste des zones:

`GET /v1/zones/{zone_group_id}`

Paramètres de la route:

Besoin recherché

- zone_group_id > remplacer par la valeur précédemment sélectionné
- includeZoneCode > True

Amélioration des performances:

- simplifyGeometry > True
- preserveTopology > True
- tolerance > 1
- precision > 1
- mapboxIdOnly > False

Vous obtiendrez ici une liste de zones appartenant au zone group demandé avec pour infos:

- Id: sera le même Id présent dans le réduce pour la correspondance
- name: nom de la zone
- code: code de la zone (si municipalité = code postal par exemple)

Le reduce matchera donc avec l’ID précédement trouvé.
