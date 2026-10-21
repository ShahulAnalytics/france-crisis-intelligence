# France current-scenario evidence snapshot

**Prepared:** 20 October 2026  
**Purpose:** Ground the dashboard in the latest official releases available on the preparation date. Reference periods differ by indicator; do not label every observation “October 2026”.

## Latest official observations

| Indicator | Latest value | Reference period | Interpretation |
|---|---:|---|---|
| National CPI inflation | +3.1% year on year | September 2026 | Headline inflation accelerated from 2.4% in August, mainly due to energy. |
| Food-price inflation | +1.4% year on year | September 2026 | Food inflation is positive but materially below headline inflation. This is not evidence of shortages by itself. |
| Energy prices | +21.3% year on year | September 2026 | A key source of renewed household cost pressure. |
| Services prices | +2.4% year on year | September 2026 | Services inflation accelerated. |
| GDP | 0.0% quarter on quarter | Q2 2026 | Output was flat after a 0.2% contraction in Q1. |
| Household purchasing power per consumption unit | -0.6% quarter on quarter | Q2 2026 | Indicates household income pressure in real terms. |
| Household savings rate | 17.2% | Q2 2026 | Down from 17.9% in Q1. |
| Unemployment rate | 8.3% | Q2 2026 | Increased 0.2 percentage points quarter on quarter. |

## Sources

- INSEE, [September 2026 CPI final results](https://www.insee.fr/en/statistiques/9080263), published 15 October 2026.
- INSEE, [Economic dashboard](https://www.insee.fr/en/statistiques/2405582), updated 6 October 2026.
- INSEE, [Q2 2026 national accounts](https://www.insee.fr/en/statistiques/9040046?sommaire=9010792), detailed figures published 28 August 2026.

## Evidence-led interpretation

The latest releases support a finding of **renewed price pressure and household economic strain alongside weak output**, not a blanket claim that France is in a food-supply crisis. Food inflation is +1.4% year on year, while energy inflation is +21.3%; evidence of shortages would require separate supply-chain, availability, stock, import, and food-insecurity data.

## Rules for the live dashboard

1. Display the source, release date, reference period, unit, and last successful refresh for every indicator.
2. Keep CPI and HICP distinct; they are related but not interchangeable.
3. Treat a failed API request as missing data, never as zero or a valid observation.
4. Do not present a forecast as a fact. Backtest models on chronological holdouts and show prediction intervals.
5. News feeds are discovery tools. Verify claims against primary sources before using them as factual evidence.
