# Farm API

## GET `/v1/farms`

### Description

This endpoint returns the list of farms grouped by the technical consultant (TC) they are associated with. If a farm is not linked to any technical consultant, it will appear under a `null` user identifier.

### Request

- **Method:** `GET`
- **URL:** `/v1/farms`
- **Parameters:** None

### Response

The response is a JSON object containing a list of dictionaries. Each dictionary represents a technical consultant and the farms they manage.

#### Response format:

```json
{
  "farms": [
    {
      "userId": 101,
      "farmCodes": [
        "XXXXXXXXXXXXXX"
      ]
    },
    {
      "userId": 102,
      "farmCodes": [
        "YYYYYYYYYYYYYY",
        "ZZZZZZZZZZZZZZ"
      ]
    },
    {
      "userId": null,
      "farmCodes": [
        "AAAAAAAAAAAAAA"
      ]
    }
  ]
}
```

### Fields

- **userId**: Identifier of the technical consultant responsible for the listed farms. If `null`, the farms are not assigned to any technical consultant.

- **farmCodes**: A list of unique identifiers (e.g., SIRET numbers) representing farms.

### Example

This response shows:

- One TC managing 1 farm  
- Another managing 2 farms  
- One farm not assigned to any TC


## POST `/v1/organization-farms/bulk`

### Description

This endpoint allows bulk association of farms to an organization.  
It supports both **creation** and **update** of farms:

- If the farm does **not exist**, it will be **created** and associated with the given organization.
- If the farm **already exists**, the endpoint will **update** the existing record with the new values provided in the payload.

Once the farm is associated, its status changes from **unlinked (black)** to **linked (green)** in the map visualization.

### Request

- **Method:** `POST`
- **URL:** `/v1/organization-farms/bulk`
- **Content-Type:** `application/json`

### Body

The request body should be a JSON array of farm objects with the following structure:

```json
[
  {
    "farm_code": "string",
    "name": "string",
    "third_party_code": "string",
    "address": "string",
    "city": "string",
    "postcode": "string",
    "organization_id": 0,
    "user_id": 0,
    "is_active": true,
    "deposit_code": "string",
    "custom_fields": {},
    "facility_id": 0
  }
]
```

### Fields

- **farm_code** *(string)*: Unique identifier of the farm (e.g., SIRET).
- **name** *(string)*: Name of the farm.
- **third_party_code** *(string)*: External reference code.
- **address** *(string)*: Farm's address.
- **city** *(string)*: City where the farm is located.
- **postcode** *(string)*: Postal code of the farm.
- **organization_id** *(integer)*: ID of the organization to associate the farm with.
- **user_id** *(integer)*: ID of the technical consultant (optional).
- **is_active** *(boolean)*: Indicates if the farm is active.
- **deposit_code** *(string)*: Optional code related to financial deposit or grouping.
- **custom_fields** *(object)*: Custom key-value metadata.
- **facility_id** *(integer)*: Internal reference to a facility if applicable.

### Response

- **201 Created**: All farms were successfully associated with the organization.

### Behavior

Farms newly linked to an organization will be visually updated from **black** (unassigned) to **green** (assigned) on the map interface.

### Example

```json
[
  {
    "farm_code": "12345678900011",
    "name": "Green Acres",
    "third_party_code": "EXT001",
    "address": "123 Field Lane",
    "city": "Springville",
    "postcode": "12345",
    "organization_id": 12,
    "user_id": 34,
    "is_active": true,
    "deposit_code": "DEPX01",
    "custom_fields": {
      "soil_type": "loam",
      "irrigation": true
    },
    "facility_id": 7
  }
]
```

## DELETE `/v1/organization-farms/bulk`

### Description

This endpoint allows the **bulk disassociation** of farms from a specific organization.  
Once a farm is detached, it changes its status on the map from **linked (green)** to **unlinked (black)**.

### Request

- **Method:** `DELETE`
- **URL:** `/v1/organization-farms/bulk`
- **Query Parameters:**

| Name       | Type              | Required | Description                                      |
|------------|-------------------|----------|--------------------------------------------------|
| farmCodes  | array of strings  | Yes      | List of farm codes (e.g., SIRETs) to detach.     |
| orgaId     | integer           | Yes      | ID of the organization from which to detach the farms. |

### Response

- **204 No Content**: Farms were successfully detached from the organization. No body is returned.

### Behavior

- The farms specified in the `farmCodes` list will be **disassociated** from the organization identified by `orgaId`.
- On the map interface, these farms will change color from **green** (assigned) back to **black** (unassigned).

### Example

**Request**

```http
DELETE /v1/organization-farms/bulk?farmCodes=12345678900011&farmCodes=98765432100022&orgaId=12
```

**Response**
```
204 No Content
```

## GET `/v1/farm-data-meta`

### Description

This endpoint returns the list of available **data layers** that can be visualized for farms in the context of a given organization.  
These layers define different types of aggregated information such as **market share**, **coverage**, and are typically displayed in a map or dashboard view.

> ⚠️ The `year` parameter is currently required but will be deprecated soon. It corresponds to the **farming campaign year**.

### Request

- **Method:** `GET`
- **URL:** `/v1/farm-data-meta`
- **Query Parameters:**

| Name  | Type    | Required | Description                                       |
|-------|---------|----------|---------------------------------------------------|
| year  | integer | No       | Year of the campaign. If not provided, returns available years. |

### Response

- **200 OK**: Returns metadata describing the available farm data layers.

#### Response Format (when year is provided)

```json
{
  "farmDataMeta": [
    {
      "id": 1,
      "orgaId": 1,
      "name": "Collect market share",
      "description": "Collected volume divided by the zone potential.",
      "operation": "sum",
      "labelMetaId": 10,
      "type": "Market Area",
      "lastUpdatedAt": "2023-09-16T12:11:43.000000",
      "possibleValues": [
        {
          "key": 1,
          "values": [2, 16, 5, 1, 12, 18, 11, 3, 4, 21]
        }
      ]
    }
  ]
}
```

#### Response Format (when year is not provided)

```json
{
  "farmDataMeta": [
    {
      "id": 1,
      "orgaId": 1,
      "name": "Collect market share",
      "description": "Collected volume divided by the zone potential.",
      "operation": "sum",
      "labelMetaId": 10,
      "type": "Market Area",
      "lastUpdatedAt": "2023-09-16T12:11:43.000000",
      "possibleValues": [
        {
          "key": 1,
          "values": [2, 16, 5, 1, 12, 18, 11, 3, 4, 21]
        }
      ]
    }
  ],
  "years": [2020, 2021, 2022, 2023, 2024]
}
```

### Fields

- **id** *(integer)*: Internal ID of the data layer.
- **orgaId** *(integer)*: ID of the organization this layer belongs to.
- **name** *(string)*: Name of the layer (e.g., "Flash coverage").
- **description** *(string)*: Description of what the layer represents.
- **operation** *(string)*: Aggregation method used (e.g., `"sum"`).
- **labelMetaId** *(integer)*: Metadata type associated with the data:  
  - `3` → related to **crop rotation** (*assolement*)  
  - `10` → related to **volume**
- **type** *(string)*: Category of the data layer (e.g., `"Market Area"`).
- **lastUpdatedAt** *(datetime)*: Timestamp of the last update.
- **possibleValues** *(array)*: Describes the label and list of available values:  
  - `key: 1` → refers to **label 1**, typically **crop**  
  - `values` → list of possible choices for that label, which can be mapped from label 1's options (e.g., different crop types)
- **years** *(array)*: List of available years for the farm data meta (only present when year parameter is not provided)

### Examples

#### With year parameter
```http
GET /v1/farm-data-meta?year=2024
```

#### Without year parameter
```http
GET /v1/farm-data-meta
```

## POST `/v1/farm-data/bulk`

### Description

This endpoint allows bulk submission of **farm-level data values** for a given year and data layer (identified by `farm_data_meta_id`).  
It supports both **insertion** of new values and **automatic update** if a record already exists for the same farm, year, and data layer.

> ℹ️ Each entry must be **unique** per combination of `farm_code`, `farm_data_meta_id`, and `year`.  
> If a matching entry already exists in the database, it will be **updated** with the new value.

### Request

- **Method:** `POST`
- **URL:** `/v1/farm-data/bulk`
- **Content-Type:** `application/json`

### Body

The request body should be a JSON array of data entries with the following structure:

```json
[
  {
    "farm_code": "string",
    "year": 0,
    "filter": {},
    "farm_data_meta_id": 0,
    "value": 0
  }
]
```

### Fields

- **farm_code** *(string)*: Unique identifier of the farm (e.g., SIRET).
- **year** *(integer)*: Year of the data (e.g., campaign year).
- **filter** *(object)*: A dictionary with a `key` and a `value`.  
  - `key: 1` refers to the **crop** label.  
  - `value` corresponds to the crop choice (which can be mapped using the label's choice list).
- **farm_data_meta_id** *(integer)*: Identifier of the data layer (as defined in `/v1/farm-data-meta`).
- **value** *(number)*: The numeric value to assign (e.g., `99.99`).

### Response

- **201 Created**: All data entries were successfully created or updated.

### Behavior

- New data entries are **created** when the combination of `farm_code`, `farm_data_meta_id`, and `year` does not yet exist.
- Existing entries matching this combination are **automatically updated** with the new `value` and `filter`.

### Example Input

```json
[
  {
    "farm_code": "xxxxxxxxxxxxxx",
    "year": 2020,
    "filter": [{'key': 1, 'value': 12}],
    "farm_data_meta_id": 1,
    "value": 99.99
  }
]
```

## DELETE `/v1/farm-data/bulk-delete`

### Description

This endpoint allows **bulk deletion** of farm data associated with a specific data layer (`farm_data_meta_id`) for one or more specified farms (`farm_codes`).  
It is used to remove values previously recorded for a given farm and data layer.

### Request

- **Method:** `DELETE`
- **URL:** `/v1/farm-data/bulk-delete`
- **Query Parameters:**

| Name              | Type             | Required | Description                                                                 |
|-------------------|------------------|----------|-----------------------------------------------------------------------------|
| farm_codes        | array of strings | Yes      | List of farm codes (e.g., SIRETs) for which data should be deleted.        |
| farm_data_meta_id | integer          | Yes      | ID of the data layer to delete data from (as defined in `/v1/farm-data-meta`). |

### Response

- **204 No Content**: The farm data entries were successfully deleted. No content is returned.

### Behavior

- Deletes all data entries matching the specified `farm_data_meta_id` **for each farm** in the `farm_codes` list.

### Example Request

```http
DELETE /v1/farm-data/bulk-delete?farm_codes=12345678900011&farm_codes=98765432100022&farm_data_meta_id=10
```

### Response

```
204 No Content
```

