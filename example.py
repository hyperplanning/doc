from hyperapi.client import HyperClient
from tqdm import tqdm
import os

# Login
client = HyperClient("https://backend-cdn-endpoint-prod-afccapcwframgnag.z02.azurefd.net/v1")
auth = client.login(os.getenv("API_USR"), os.getenv("API_PWD"))

# Listing Available Label Metas
labels = client.get("labels/info")
labels = {l["name"]: l for l in labels.json()['labelInfos']}

# Getting Zones Groups
zone_groups = client.get("zone-groups").json()
zone_groups = {z["name"]: z for z in zone_groups['zoneGroups']}

# List all Departements
zone_group_id = zone_groups["Departments"]["id"]
deps = client.get(f"zones/{zone_group_id}").json()
deps = {d["name"]: d for d in deps['zones']}
dep_id = deps["Loire (42)"]["id"]

# Getting Commune composition of Target Department 'Loire (42)'
com_zone_group_id = zone_groups["Municipalities"]["id"]
coms = client.get(f"zones/composition/{com_zone_group_id}/{dep_id}").json()
coms = [c["id"] for c in coms["zoneIds"]]

# Searching Parcels in a commune
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

# Getting Label data for every parcels
data = []
for pid in tqdm(parcels):
    d = client.get(
        f"parcels/{pid}",
        params={"labelIds": [labels["NDVI"]["id"], labels["Area"]["id"]]},
    ).json()
    data.append({"id": d["id"], "labels": d["labels"]})

