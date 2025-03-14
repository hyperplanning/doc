# HyperPlan API - Quickstart

This guide provides a step-by-step explanation of how to interact with the HyperPlan API to authenticate, retrieve zone information, and fetch parcel data with associated labels.

## 1. Imports

```python
from hyperapi.client import HyperClient
from tqdm import tqdm
import os
```

## 2. Authentication
Instantiate the `HyperClient` to point to the HyperPlan API endpoint. Login using credentials stored in environment variables `API_USR` and `API_PWD`.

```python
client = HyperClient("https://backend-cdn-endpoint-prod-afccapcwframgnag.z02.azurefd.net/v1")
client.login(os.getenv("API_USR"), os.getenv("API_PWD"))
```

## 3. Listing Available Label Metas

This section retrieves metadata for all available labels and stores them in a dictionary with label names as keys for easier access using the `labels/info` endpoint:
```python
labels = client.get("labels/info")
labels = {l["name"]: l for l in labels.json()['labelInfos']}
```

## 4. Getting Zone Groups
Here, zone groups (e.g., Departments, Municipalities) are fetched from the API and stored in a dictionary with the zone group names as keys.
```python
zone_groups = client.get("zone-groups").json()
zone_groups = {z["name"]: z for z in zone_groups['zoneGroups']}
```

Then, let's list all "Departements" available, and select one: "Loire".
```python
zone_group_id = zone_groups["Departments"]["id"]
deps = client.get(f"zones/{zone_group_id}").json()
deps = {d["name"]: d for d in deps['zones']}
dep_id = deps["Loire (42)"]["id"]
```

We can now get a Commune composition of the Loire Departement:
```python
com_zone_group_id = zone_groups["Municipalities"]["id"]
coms = client.get(f"zones/composition/{com_zone_group_id}/{dep_id}").json()
coms = [c["id"] for c in coms["zoneIds"]]
```

## 4. Parcel Search
Parcel Search Allows us to find parcel ids according to any list of filters. Here we are doing a research based on location.


```python
search = {
    "filters": [
        [
            {
                "metaId": "zone",
                "operation": "in",
                "value": [coms[0]],
            }
        ]
    ],
    "label": {"metaId": 1, "year": 2023},
}

parcels = client.post(f"elastic/search/parcels", data=search).json()
parcels = [p["id"] for p in parcels]
```

## 5. Label Data Retrieval
Now we can iterate on every parcel and retrieve any label data from theses parcels:
```python
data = []
for pid in parcels:
    d = client.get(
        f"parcels/{pid}",
        params={"labelIds": [labels["NDVI"]["id"], labels["Area"]["id"]]},
    ).json()
    data.append({"id": d["id"], "labels": d["labels"]})
```





















