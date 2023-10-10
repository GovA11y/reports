<div>
  <p>
    <img src="https://raw.githubusercontent.com/GovA11y/.github/main/assets/logos/transparent/full.svg" alt="GovA11y Logo" width="20%" align="left">
    <h1 style="display:inline">GovA11y Reporting</h1></p>
    This service generates reports and data exports of GovA11y. Eventually, it will also include control mechanisms.
    <br>
  </p><br>
  <br clear="all">
</div>

[![🏗️📤 Build and publish 🐳 images](https://github.com/GovA11y/reports/actions/workflows/containerize.yml/badge.svg)](https://github.com/GovA11y/reports/actions/workflows/containerize.yml)



## Queries

Below are the queries used by the service.

### URL Parameters

## Output Formatting

The API supports output in several formats:

- CSV
- XLSX
- HTML
- XML
- YAML
- JSON (default)

To specify the output format, include the `format` URL parameter in your request. For example, to request CSV output, your URL might look like `http://example.com/endpoint?format=csv`. When requesting CSV or XLSX output, the response will include a `Content-Disposition` header that prompts the client to download the response as a file.

## Endpoints

This section describes the available API endpoints.

### Domains

These endpoints provide metrics and insights about domains.

#### `/domain/summary`
Returns a summary of information for a specific domain.
##### Method: `GET`

##### URL Parameters:

- `domain` (Optional): Specifies the domain for which to return a summary. If not provided, defaults to 'nasa.gov'.
- `format` (Optional): Specifies the output format of the results. The supported formats are CSV, XLSX, HTML, XML, YAML, and JSON. If not provided, defaults to JSON.

##### Output Format:
You can specify the output format by including the `format` URL parameter in your request. The supported formats are `CSV`, `XLSX`, `HTML`, `XML`, `YAML`, and `JSON` (default).

##### Response Fields:

- `domain_id`: The identifier of the domain, from the `targets.domains` table in the Postgres database.
- `domain`: The domain name, also from the `targets.domains` table.
- `url_count`: The number of active URLs for the domain, from the `targets.urls` table.

### Axe Assessments

These endpoints provide data from Axe accessibility tests.

#### `/axe/summary`
Returns a summary of Axe accessibility test results for a specific domain.
##### Method: `GET`


##### URL Parameters:

- `domain` (Optional): Specifies the domain for which to return a summary. If not provided, defaults to 'gsa.gov'.
- `format` (Optional): Specifies the output format of the results. The supported formats are CSV, XLSX, HTML, XML, YAML, and JSON. If not provided, defaults to JSON.

##### Output Format:
You can specify the output format by including the `format` URL parameter in your request. The supported formats are `CSV`, `XLSX`, `HTML`, `XML`, `YAML`, and `JSON` (default).

##### Response Fields:
The response fields can vary depending on the specifics of the test results. A typical response would include fields such as:

- `domain_name`: The name of the domain for which the tests were run.
- `urls_tested`: The number of URLs from the domain that were tested.
- `count_passes`: The number of accessibility tests that passed.
- `count_violations`: The number of accessibility tests that resulted in violations.
- `count_incompatibles`: The number of tests that resulted in incompatible instances.
- `count_recent_tests`: The total number of tests that have been conducted recently.


#### `/axe/results_raw`
Returns raw results from Axe accessibility tests for a specific domain.
##### Method: `GET`

##### URL Parameters:

- **`domain`** (Optional): Specifies the domain for which to return test results. If not provided, defaults to 'nasa.gov'.
- **`limit`** (Optional): Specifies the number of results to return. If not provided, defaults to '5000'.
- **`rule_type`** (Optional): Specifies the type of rules to include in the results.
  If not provided, defaults to all types. To select multiple types, enter them as a comma separated list.

  Example: `&rule_type=violations` or `&rule_type=violations,inapplicable`
  Possible values: `inapplicable`, `passes`, `violations`, `incomplete`

- **`format`** (Optional): Specifies the output format of the results. The supported formats are CSV, XLSX, HTML, XML, YAML, and JSON. If not provided, defaults to JSON.

  The following **MUST** include both `tested_from` & `tested_to` for a result. Format dates like this: `YYYY-MM-DD`

- **`tested_from`** (Optional): Specifies the oldest test included in results.
- **`tested_to`** (Optional): Specifies the most recent test included in results.

##### Output Format:
You can specify the output format by including the `format` URL parameter in your request. The supported formats are `CSV`, `XLSX`, `HTML`, `XML`, `YAML`, and `JSON` (default).

##### Response Fields:
The response fields can vary depending on the specifics of the test results. A typical response would include fields such as:

- `domain_id`: The unique identifier of the domain for which the tests were run.
- `domain`: The name of the domain for which the tests were run.
- `url_id`: The unique identifier of the URL that was tested.
- `url`: The actual URL that was tested.
- `scan_id`: The unique identifier of the scan.
- `rule_id`: The unique identifier of the rule applied in the test.
- `test_id`: The unique identifier of the test.
- `tested_at`: The timestamp when the test was performed.
- `rule_type`: The type of rule applied in the test.
- `axe_id`: The unique identifier of the Axe accessibility test.
- `impact`: The impact level of the rule violation (if applicable).
- `target`: The element that violated the rule (if applicable).
- `html`: The HTML of the element that violated the rule (if applicable).
- `failure_summary`: A summary of the test failure (if applicable).
- `created_at`: The timestamp when the test result was created.
- `active`: Indicates if the test result is active.
- `section508`: Indicates if the test result is Section 508 compliant.
- `super_waggy`: An attribute related to Wagtail CMS accessibility evaluation (if applicable).
- `max_tested_at`: The latest timestamp when the test was performed (if applicable).


#### `/axe/domain_error_summary`
Provides a summary of Axe accessibility test results specifically for domains. This means that you can obtain an overview of the accessibility issues identified during the tests for a particular domain or set of domains.
##### Method: `GET`


##### URL Parameters:

- `domain` (Required): Specifies the domain & sub-domains for which to return a summary. If not provided, defaults to 'nasa.gov'.
- `format` (Optional): Specifies the output format of the results. The supported formats are CSV, XLSX, HTML, XML, YAML, and JSON. If not provided, defaults to JSON.

##### Output Format:
You can specify the output format by including the `format` URL parameter in your request. The supported formats are `CSV`, `XLSX`, `HTML`, `XML`, `YAML`, and `JSON` (default).

##### Response Fields:
The response fields can vary depending on the specifics of the test results. A typical response would include fields such as:

- `domain_name`: The name of the domain for which the tests were run.
- `urls_tested`: The number of URLs from the domain that were tested.
- `count_critical`: The number of critical accessibility violations.
- `count_serious`: The number of serious accessibility violations.
- `count_moderate`: The number of moderate accessibility violations.
- `count_minor`: The total number minor accessibility violations.



### Activity

These endpoints provide data from GovA11y Activity

#### `imports/axe_tests`
Returns a summary of Axe accessibility tests imported into ClickHouse
##### Method: `GET`


##### URL Parameters:

- `domain` (Optional): Specifies the domain for which to return a summary. If not provided, defaults to 'gsa.gov'.
 **`format`** (Optional): Specifies the output format of the results. The supported formats are CSV, XLSX, HTML, XML, YAML, and JSON. If not provided, defaults to JSON.

- **`imported_from`** (Optional): Specifies the oldest test included in results. Format dates like this: `YYYY-MM-DD` Defaults to beginning of time.
- **`imported_to`** (Optional): Specifies the most recent test included in results. Format dates like this: `YYYY-MM-DD` Defaults to end of time.


##### Output Format:
You can specify the output format by including the `format` URL parameter in your request. The supported formats are `CSV`, `XLSX`, `HTML`, `XML`, `YAML`, and `JSON` (default).

##### Response Fields:
The response fields can vary depending on the specifics of the test results. A typical response would include fields such as:

- `domain`: The name of the domain for which the tests were run.
- `imported_total`: The total number of axe tests imported for the `domain`.
- `imported_range`: The number of axe tests imported for the `domain` within the specified time range.
- `imported_minute_15`: The number of axe tests imported for the `domain` within the past 15 minutes.
- `imported_hour_1`: The number of axe tests imported for the `domain` within the past 1 hour.
- `imported_hour_12`: The number of axe tests imported for the `domain` within the past 12 hours.
- `imported_week`: The number of axe tests imported for the `domain` within the past week.
- `imported_month`: The number of axe tests imported for the `domain` within the past month.
