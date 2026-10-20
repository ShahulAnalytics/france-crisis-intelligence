# Model card: baseline indicator forecasts

## Intended use
Exploratory short-horizon baselines for public economic indicator series to support monitoring and analyst review.

## Not intended for
Official forecasts, individual financial decisions, causal inference, declaring a national crisis, or estimating losses without validated inputs.

## Evaluation
Compare forecasts against naive and seasonal-naive baselines using time-ordered backtesting. Report MAE/RMSE and interval coverage where supported. Never randomly shuffle time-series observations.

## Limitations
Revisions, structural breaks, sparse history, measurement changes and policy shocks can invalidate extrapolation. Forecasts are conditional scenarios, not certainties. Do not label unvalidated projections as facts.