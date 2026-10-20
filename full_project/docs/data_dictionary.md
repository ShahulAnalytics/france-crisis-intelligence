# Data dictionary

## Standard observation fields

- `dataset_id`: stable dataset identifier.
- `period`: observation period/date supplied or normalized by the source.
- `value`: numeric observation; units depend on the series definition.
- `source_url`: original public endpoint or source page.
- `retrieved_at_utc`: retrieval timestamp in UTC.
- `series_definition`: measure and unit description.
- `currency_code` / `quotation`: currency and exchange-rate direction when relevant.

## Research ledgers

- `claim_ledger.csv`: claim, evidence links, status and caveats.
- `event_ledger.csv`: dated events and source evidence.
- `food_supply_events.csv`: geographically and temporally bounded supply reports.
- `government_measures.csv`: policy announcements and implementation status.
- `loss_estimates.csv`: estimate, source, method, scope, period and overlap caveats.

Missing values must not be silently replaced with zero. Monetary amounts from different periods, geographies or overlapping categories must not be aggregated without normalization and a documented method.