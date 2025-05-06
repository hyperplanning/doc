[Hyperplan](https://www.hyperplan.fr) is dedicated to enhancing the growth and sustainability of the entire agri-food chain by providing reliable, real-time information on crop production. Amidst the increasing volatility in agricultural production due to climate change, market demand shifts, and geopolitical disturbances, we believes in the critical importance of having real-time, reliable visibility into agricultural production. Our mission is to offer unparalleled insight that drives the growth and sustainability of the whole agri-food chain, leveraging advanced remote sensing data and AI technology to transform parcel-level data into actionable decisions for daily operations.

Hyperplan provides an API access to his clients and partnership companies.

## [API](./docs/api_reference.md) Reference
The [Hyperplan API](./docs/api_reference.md) is designed for efficient parcel data management, featuring endpoints for accessing parcel and label metadata, and incorporating advanced search capabilities for thorough data retrieval and analysis. It aims to simplify parcel data access, providing in-depth insights for streamlined operations.

### Zones and Zone Management

A key feature of the Hyperplan API is its ability to manage and query zones. Zones represent geographical areas such as departments, municipalities, postal codes, and other administrative regions. Each zone belongs to a specific zone group, and zones can be queried to retrieve detailed metadata including boundaries, centroids, and unique identifiers for Mapbox integration. For more details on zone groups and zone management, refer to the [Zones Documentation](./docs/zones.md), where the full list of zone groups and zone-related operations is described.

### Facilities Management

The Hyperplan API also enables the management and retrieval of facilities. Facilities represent physical locations such as warehouses, depots, or other types of organizational units. Each facility is associated with specific geographical coordinates, and optionally, a CRM code for further integration with CRM systems. The API provides detailed metadata for each facility, including its name, location, and unique identifier. For more details on facilities and their management, refer to the [Facilities Documentation](./docs/facilities.md), where the complete list of available facilities and related operations is documented.


### Label Metadata

Label metadata includes detailed information about parcel labels such as unique identifiers, names, descriptions, categories (e.g., "TEXT"), and properties indicating the frequency of application (yearly, weekly). It also includes visual differentiation features like color and icon, and validation criteria depending on the label type (TEXT, NUMERICAL, DATE, OBJECT).

The API provides detailed label metadata in a predefined format, including validation types and choices, enhancing data annotation and retrieval in complex systems. Additionally, it outlines available labels within the Hyperplan Organization, covering various parcel characteristics from area and crop details to environmental conditions and parcel properties, excluding private labels.

### Parcel-Specific Information

For parcel-specific information, the API supports retrieving detailed data by parcel ID, with optional filters for labels, years, and weeks, offering a comprehensive view of parcel characteristics and changes over time.

### Farms

The [Farm API](./docs/farms.md) allows users to associate and disassociate farms with organizations, which is reflected visually in map interfaces (e.g., from black to green when linked). In addition to managing this linkage, the API supports attaching data layers—such as market share or coverage metrics—to farms. These layers can be filtered by criteria like crop type and are aggregated at the organization level. This setup enables practical data analysis and visualization, helping teams monitor trends and make decisions based on reliable, structured information.

### Aggregation and Analysis

The API also provides reduce operations, enabling users to perform aggregate calculations (sum, average, etc.) on selected parcel attributes based on specific filters and bins. This feature is particularly useful for generating summaries and insights across multiple parcels, allowing for deeper analysis and better decision-making on a large scale. By applying binning and filtering techniques, users can tailor their data exploration to specific areas of interest, gaining valuable insights into agricultural trends and performance metrics.


## HyperClient
[HyperClient](./docs/quickstart.md) is a powerful and simple-to-use API client python library designed to make HTTP requests to the HyperAPI. It simplifies the process of interacting with the API by providing a straightforward method of making GET, POST, and DELETE requests, handling authentication, and processing responses.

- Easy to use API for making HTTP requests (GET, POST, DELETE)
- Automatic handling of authentication
- Supports session persistence across requests
- Simplifies the process of working with JSON data

## Hyperplan API Quickstart with Python: Accessing Parcel Data

This [quickstart](./docs/quickstart.md) guide will show you how to retrieve parcel information using Hyperplan's API and the HyperClient Python library. This example focuses on retrieving parcel-specific data, showcasing a core functionality of the API.

**Before you Begin**:

*   You need an active Hyperplan account with API access.
*   You should have the HyperClient Python library installed. While the sources don't provide installation instructions, you can likely find them in the full documentation for the 'hyperplanning/doc' repository on GitHub.
*   You'll need a valid authentication token for the API. 

**Note**: This guide assumes you have a basic understanding of Python and making API requests.


