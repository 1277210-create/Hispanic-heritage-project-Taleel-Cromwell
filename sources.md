# 📚 Data Sources, Metadata Mappings & Mathematical Methodology

## 1. Official Data Source & API Specifications

All historical observations in the **Hispanic Heritage Historical Data Explorer** are retrieved dynamically from the official **World Bank Open Data API (v2)**.

* **API Base URL:** `http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}`
* **Query Parameters:** `?date={start_year}:{end_year}&format=json&per_page=100`
* **Historical Interval Requested:** $t_0 = \text{Current Year} - 70$ through $t_1 = \text{Current Year} - 1$ (1956–2025 inclusive).
* **Data Retrieval Protocol:** Live REST API requests are executed via HTTP GET with a strict 12-second timeout and cached locally for 24 hours using Streamlit session state (`@st.cache_data`).

---

## 2. Complete Indicator Mappings, Definitions & Usage Constraints

| Indicator Name | Official Series Code | Measurement Units | Definition & Data Integrity Usage Rules | Physical Constraint Domain |
| :--- | :--- | :--- | :--- | :--- |
| **Life Expectancy at Birth** | `SP.DYN.LE00.IN` | Years | Total years a newborn infant would live if prevailing mortality patterns at birth remain constant throughout its life. | $[0, 110]$ |
| **Unemployment (National Estimate)** | `SL.UEM.TOTL.NE.ZS` | % of Total Labor Force | Share of the labor force without work but available for and seeking employment (National Estimate). | $[0, 100]$ |
| **GDP per Capita** | `NY.GDP.PCAP.CD` | Current US$ | Gross domestic product divided by midyear population. **Note:** Represents aggregate economic productivity per person, **NOT** average personal income or household wealth. | $[0, 250000]$ |
| **Crude Birth Rate** | `SP.DYN.CBRT.IN` | Births per 1,000 People | Annual number of live births occurring per 1,000 midyear population. **Note:** Standardized rate, **NOT** total annual birth count. | $[0, 100]$ |
| **Net Migration** | `SM.POP.NETM` | Headcount Balance | Total net number of migrants (immigrants minus emigrants) over a five-year period or annual estimate. **Note:** Represents net balance, **NOT** total emigration count. | $[-10^7, 10^7]$ |
| **Intentional Homicide Rate** | `VC.IHR.PSRC.P5` | Per 100,000 People | Unlawful deaths purposefully inflicted on a person by another person, expressed per 100,000 population. | $[0, 300]$ |
| **Consumer Price Inflation** | `FP.CPI.TOTL.ZG` | Annual % Change | Annual percentage change in the cost to the average consumer of acquiring a basket of goods and services. | $[-100, 100000]$ |
| **Central Government Debt** | `GC.DOD.TOTL.GD.ZS` | % of GDP | Gross liabilities of central government including debt securities and loans, expressed as a share of annual GDP. | $[0, 1000]$ |
| **Total Reserves (Includes Gold)** | `FI.RES.TOTL.CD` | Current US$ | Monetary gold, special drawing rights (SDRs), IMF reserve positions, and foreign exchange held by monetary authorities. | $[0, 10^{14}]$ |
| **External Balance on Goods/Services** | `NE.RSB.GNFS.ZS` | % of GDP | Exports of goods and services minus imports of goods and services, expressed as a percentage of annual GDP. | $[-100, 100]$ |

---

## 3. Country ISO-2 Mappings & Regional Context

| Country Name | ISO-2 Code | Regional Role & Comparative Purpose |
| :--- | :--- | :--- |
| **Nicaragua** | `NI` | **Primary Focus Country** |
| **Brazil** | `BR` | **Primary Regional Benchmark** (Largest economy & population in Latin America) |
| **Mexico** | `MX` | Major North American / Mesoamerican Benchmark |
| **Argentina** | `AR` | Southern Cone Macroeconomic Benchmark |
| **Colombia** | `CO` | Andean Regional Benchmark |
| **Chile** | `CL` | High-Income Regional Benchmark |
| **Peru** | `PE` | Central Andean Economic Benchmark |
| **Venezuela** | `VE` | Northern South American Benchmark |
| **Ecuador** | `EC` | Dollarized Andean Economy Benchmark |
| **Uruguay** | `UY` | High Social-Development Southern Cone Benchmark |

---

## 4. Mathematical Foundations & Calculus Methodology

### Centered Time Transformation
To prevent severe numerical ill-conditioning in the Vandermonde matrix during polynomial fitting ($d \in [3, 8]$), the time variable $Y$ (calendar year) is centered around its mean $\bar{Y}$:

$$t = Y - \bar{Y}, \quad \text{where } \bar{Y} = \frac{1}{n} \sum_{i=1}^n Y_i$$

The centered polynomial function $\hat{Y}(t)$ is formulated as:

$$\hat{Y}(t) = a_d t^d + a_{d-1} t^{d-1} + \dots + a_1 t + a_0$$

### Analytical Calculus Suite

1. **Instantaneous Rate of Change ($P'(t)$):**
   $$P'(t) = \frac{d}{dt} \hat{Y}(t) = \sum_{k=1}^d k \cdot a_k t^{k-1}$$
   *Represents the instantaneous velocity or rate of growth/decline of the indicator per year.*

2. **Acceleration & Concavity ($P''(t)$):**
   $$P''(t) = \frac{d^2}{dt^2} \hat{Y}(t) = \sum_{k=2}^d k(k-1) \cdot a_k t^{k-2}$$
   * $P''(t) > 0$: Curve is **concave up** (growth is accelerating or decline is slowing).
   * $P''(t) < 0$: Curve is **concave down** (growth is slowing or decline is accelerating).

3. **Critical Point Classification ($P'(t) = 0$):**
   Evaluated via the **Second Derivative Test**:
   * If $P''(t_c) < 0 \implies \hat{Y}(t_c)$ is a **Local Maximum**.
   * If $P''(t_c) > 0 \implies \hat{Y}(t_c)$ is a **Local Minimum**.
   * If $P''(t_c) = 0 \implies$ Inconclusive (potential inflection point or saddle point).

4. **Inflection Points ($P''(t) = 0$):**
   Points $t_i$ where $P''(t_i) = 0$ with an explicit sign change across $t_i \pm \epsilon$.

---

## 5. Academic Citation & Data Provenance Guidelines

### Primary Data Source Citation
> World Bank. (2026). *World Development Indicators API v2*. Washington, D.C.: The World Bank Group. Retrieved October 2026 from `http://api.worldbank.org/v2/`.

### Methodological References
1. **United Nations Population Division:** *World Population Prospects 2024*. New York: United Nations Department of Economic and Social Affairs.
2. **International Monetary Fund:** *Government Finance Statistics Manual 2014*. Washington, D.C.: IMF.
3. **Burden, R. L., & Faires, J. D. (2015):** *Numerical Analysis (10th ed.)*. Cengage Learning. *(Section on Least Squares Polynomial Approximation & Ill-Conditioned Matrices).*