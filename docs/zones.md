# Zone Groups

## Fetching Available Zone Groups
GET `/v1/zone-groups`

This endpoint retrieves a list of zone groups, including administrative zone groups (such as municipalities, postal codes, departments, regions, and countries) as well as specific zone groups associated with your organization, for which you have viewing permissions.

### Parameters
This endpoint does not require any parameters.

### Response

The response is an array of zone group objects, where each object provides information about a specific zone group. Below is a breakdown of the fields in the response:

#### Response Fields:
- `editors` (array of integers): The users who last edited or having edition access to the zone group.
- `isPublic` (boolean): A flag indicating whether the zone group is public (`true`) or restricted to specific users (`false`).
- `id` (integer): The unique identifier for the zone group.
- `floor` (nullable, string): This field indicates the atomic unit or base level of the zone within the zone group. It specifies the smallest unit that constitutes the zone group, and its value can vary depending on the specific zone structure.
- `isExclusive` (boolean): A flag that indicates whether the zone group's areas are exclusive (`true`, meaning they do not overlap geographically) or non-exclusive (`false`, meaning they can overlap geographically).
- `name` (string): The name of the zone group (e.g., "Municipalities", "Postal codes", "Departments", etc.).
- `mapboxId` (string): The unique identifier for the zone group used in the Mapbox system for visualization (e.g., `adm3`, `pos4`, `adm2`).
- `isValid` (boolean): A flag indicating whether the zone group is valid (have at least one section).

### Example Response

```json
[
  {
    "editors": [123],
    "isPublic": true,
    "id": 2,
    "floor": null,
    "isExclusive": true,
    "name": "Municipalities",
    "mapboxId": "adm3"
  },
  {
    "editors": [],
    "isPublic": true,
    "id": 3,
    "floor": null,
    "isExclusive": true,
    "name": "Postal codes",
    "mapboxId": "pos4"
  },
  {
    "editors": [],
    "isPublic": true,
    "id": 4,
    "floor": null,
    "isExclusive": true,
    "name": "Departments",
    "mapboxId": "adm2"
  },
  {
    "editors": [],
    "isPublic": true,
    "id": 5,
    "floor": null,
    "isExclusive": true,
    "name": "Regions",
    "mapboxId": "adm1"
  },
  {
    "editors": [],
    "isPublic": true,
    "id": 6,
    "floor": null,
    "isExclusive": true,
    "name": "Country",
    "mapboxId": "adm0"
  }
]
```
### Explanation of Example:

- **"Municipalities" (id: 2)**: This is a public zone group representing municipal-level administrative boundaries. The `isExclusive: true` flag indicates that the zones in this group do not overlap geographically. It has a `mapboxId` of `"adm3"`, meaning it corresponds to the municipal level in the Mapbox hierarchy.

- **"Postal codes" (id: 3)**: This zone group represents postal code regions and is public. The `isExclusive: true` flag means that the zones in this group are geographically exclusive (no overlap). It has a `mapboxId` of `"pos4"`.

- **"Departments" (id: 4)**: A public zone group representing department-level boundaries. The `isExclusive: true` flag indicates that the departments are geographically exclusive (no overlap). It has a `mapboxId` of `"adm2"`.

- **"Regions" (id: 5)**: This zone group represents regional boundaries and is public. The `isExclusive: true` flag means the regions do not overlap. It has a `mapboxId` of `"adm1"`.

- **"Country" (id: 6)**: This group represents country-level boundaries and is public. The `isExclusive: true` flag means the country boundaries do not overlap with others in this group. It has a `mapboxId` of `"adm0"`.

### Notes:

- **Visibility**: The `isPublic` field indicates whether the zone group can be viewed by everyone (`true`) or is restricted (`false`).

- **Geographical Exclusivity**: The `isExclusive` field indicates whether the zones in the group are geographically exclusive (`true`) or can overlap with one another (`false`). This is an important distinction when dealing with boundaries that might overlap versus those that are strictly delineated (such as administrative regions).

- **Mapbox Integration**: The `mapboxId` is essential for rendering the specific zone group on Mapbox-based maps and relates to the level of administrative boundaries (e.g., municipalities, postal codes, regions).

### Additional Information:
Organizations may have custom zone groups that are not public but are available for use within the organization, depending on viewing permissions and geographical exclusivity settings.


# Zones

## Fetching Zones by Zone Group
GET `/v1/zones/{zone_group_id}`

This endpoint retrieves a list of zones within a specified zone group, with optional parameters to control the level of detail in the response (e.g., geometry, precision, and zone code).

### Parameters

- `zone_group_id` (integer, required, path): The unique identifier of the zone group to retrieve zones from.
- `simplifyGeometry` (boolean, optional, query): If set to `true`, the geometry of the zones will be simplified.
  - Default: `true`
- `preserveTopology` (boolean, optional, query): If set to `true`, the geometry simplification will preserve the topology of the zones.
  - Default: `true`
- `tolerance` (number, optional, query): Defines the tolerance level for geometry simplification. A lower value results in a more detailed geometry.
  - Default: `0.001`
- `precision` (number, optional, query): Defines the precision of the geometry. A lower value results in higher precision.
  - Default: `0.001`
- `mapboxIdOnly` (boolean, optional, query): If set to `true`, the response will only include the `mapboxId`. If `false`, it will include both the geometry and the centroid.
  - Default: `true`
- `includeZoneCode` (boolean, optional, query): If set to `true`, the response will include the zone code along with other data.
  - Default: `false`

### Response

The response is an array of zone objects with the following fields:

#### Response Fields:
- `id` (integer): The unique identifier for the zone.
- `name` (string): The name of the zone, typically including both the name and code (e.g., "Ain (01)").
- `mapboxId` (string): The unique identifier of the zone used in Mapbox for visualization.

### Example Request

**Request:**

```bash
GET /v1/zones/1?simplifyGeometry=true&preserveTopology=true&tolerance=0.001&precision=0.001&mapboxIdOnly=true&includeZoneCode=false
```

**Response:**

```json
[
  {
    "id": 40921,
    "name": "Ain (01)",
    "mapboxId": "dXJuOm1ieGJuZDpBUlJMOnY0"
  },
  {
    "id": 40922,
    "name": "Aisne (02)",
    "mapboxId": "dXJuOm1ieGJuZDpBaFJMOnY0"
  },
  {
    "id": 40923,
    "name": "Allier (03)",
    "mapboxId": "dXJuOm1ieGJuZDpCUlJMOnY0"
  }
]
```
### Explanation of Example

- **"Ain (01)" (id: 40921)**: This represents the zone for the Ain department, with a unique `mapboxId` used for rendering in Mapbox.
- **"Aisne (02)" (id: 40922)**: Similarly, this is the zone for the Aisne department, also with its own unique `mapboxId`.
- **"Allier (03)" (id: 40923)**: This zone represents the Allier department with its `mapboxId`.

### Notes

- **Geometry Simplification**: The `simplifyGeometry` parameter is useful when you want to reduce the complexity of the geometry data, especially for visualization or performance reasons. The `tolerance` and `precision` parameters allow you to fine-tune this simplification.
- **Mapbox Integration**: The `mapboxIdOnly` parameter controls whether the response should include only the `mapboxId` for integration with Mapbox, or more detailed data such as the geometry and centroid of each zone.
- **Zone Codes**: If the `includeZoneCode` parameter is set to `true`, the response will include additional information such as the zone code, which can be useful for administrative or organizational purposes.

## Fetching a Specific Zone
GET `/v1/zone/{zone_id}`

This endpoint retrieves detailed information about a specific zone, including its name, geometry, and centroid.

### Parameters

- `zone_id` (integer, required, path): The unique identifier of the zone to retrieve.

### Response

The response is a JSON object containing detailed information about the zone. Below is a breakdown of the fields in the response:

#### Response Fields:
- `id` (integer): The unique identifier for the zone.
- `name` (string): The name of the zone, typically including both the name and code (e.g., "Aube (10)").
- `mapboxId` (string): The unique identifier for the zone used in Mapbox for visualization.
- `geometry` (string): The geometry of the zone, represented as a `MULTIPOLYGON`. This provides the geographical boundaries of the zone.
- `centroid` (string): The centroid of the zone, represented as a `POINT` with longitude and latitude coordinates.
- `zoneGroupId` (integer): The identifier of the zone group to which this zone belongs.

### Example Request

**Request:**

```bash
GET /v1/zone/40930
```
**Response:**

```json
{
  "id": 40930,
  "name": "Aube (10)",
  "mapboxId": "dXJuOm1ieGJuZDpEQlJMOnY0",
  "geometry": "MULTIPOLYGON (((3.414789 48.390269, ...)))",
  "centroid": "POINT (4.190270441237304 48.320556499999995)",
  "zoneGroupId": 4
}
```
### Explanation of Example

- **"Aube (10)" (id: 40930)**: This represents the zone for the Aube department. The zone has a `mapboxId` for rendering in Mapbox. Its geographical boundaries are defined by the `geometry` field, and its `centroid` represents the central point of the zone.

### Notes

- **Geometry**: The `geometry` field provides the boundaries of the zone in the `MULTIPOLYGON` format. This field can contain a lot of data and may be simplified for visualization or performance purposes.
- **Centroid**: The `centroid` field provides the central point of the zone, which can be useful for identifying the approximate center of the geographical area.
- **Zone Group**: The `zoneGroupId` helps in identifying which zone group the zone belongs to, such as departments, municipalities, or postal codes.

