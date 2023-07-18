# A11yScore

The A11yScore is a sophisticated tool that evaluates the accessibility of a set of URLs under a specific domain. By considering various severity levels of violations and the unique identifiers for each type of pass, the algorithm offers a composite score that reflects the accessibility status of the analyzed URLs. While excelling in identifying and weighting accessibility issues based on their severity, frequency, and associated standards, the score's accuracy and utility may depend on the quality and characteristics of the input data. It's important to note that this score may not entirely capture the user experience of individuals with disabilities.

## Variables

These are options which are used to select which URLs are used to generate the results.

-   domain : The domain within which the URLs are located.
-   axe tag : Specific axe-core rule tags (e.g., wcag2a, wcag2aa) to filter the rules applied. (not in this version)
-   transformation : The type of transformation to apply to the data. Options include "logarithmic", "exponential", and "none". (not in this version)

## Endpoint

```
https://reports.gova11y.io/metrics/a11yscore?format=html&domain=www.va.gov
```

## Severity Levels

These static weights are applied to each of the severity levels. By assigning weights to different violation types, the algorithm recognizes that not all accessibility issues impact users equally.

-   Sc = severity of critical violations
-   Ss = severity of serious violations
-   Smo = severity of moderate violations
-   Smi = severity of minor violations

## Input Values

These are generated from the list of urls.

### Violations

-   Vc = count of critical violations
-   Vs = count of serious violations
-   Vmo = count of moderate violations
-   Vmi = count of minor violations

### Passes

-   Pt = count of total passes

### Meta

-   Ut = count of URLs analyzed

### Resolved Values

-   Vt = count of total violations
-   Pt = count of total passes

## Normalization

Handled in app/api/metrics/a11yscore/normalize.py

Normalization is used to adjust the counts of violations and passes, making them comparable across different scales. This step is crucial as it ensures that large counts of violations or passes don't disproportionately influence the final score.

The normalization process involves dividing each count by the total count of violations or passes. This process produces a proportional value, which can be interpreted as the relative contribution of each violation or pass to the total count. Normalized values are then used in subsequent computations.

### Output Values

-   `NVt` : Normalized Total Violations
-   `NVc` : Normalized Critical Violations
-   `NVs` : Normalized Severe Violations
-   `NVmo` : Normalized Moderate Violations
-   `NVmi` : Normalized Minor Violations

## Weighting

### Weight by Violation Severity

Handled by `weight_normalized_violations` function in [weight.py](app/api/metrics/a11yscore/weight.py)

**Outputs**

-   `WVt` : Weighted Total Violations
-   `WVc` : Weighted Critical Violations
-   `WVs` : Weighted Severe Violations
-   `WVmo` : Weighted Moderate Violations
-   `WVmi` : Weighted Minor Violations

## Calculation

This takes the normalized and weighted values.

At the end of **Calculation**, we have a single number for the domain that can be compared to all domain sizes. CMS.gov with over 100k urls can be compared to plainlanguage.gov with its 91 urls.

```
a11yscore = (total_weighted_violations) / Ut
```
