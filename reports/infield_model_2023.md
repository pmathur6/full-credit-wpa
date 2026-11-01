# Infield model: 2023

- Ground balls: 53,174; converted to an out: 0.732; sprint speed coverage: 99.9%

| Predictor | AUC | Brier | Mean predicted |
|---|---|---|---|
| 1 - xBA (old stand-in) | 0.742 | 0.1678 | 0.755 |
| Model, no alignment | 0.811 | 0.1428 | 0.732 |
| Model, with alignment | 0.813 | 0.1424 | 0.732 |

Calibration (with alignment):

| Predicted | n | Mean predicted | Actual |
|---|---|---|---|
| (0.0, 0.2] | 2,015.0 | 0.134 | 0.110 |
| (0.2, 0.4] | 4,414.0 | 0.307 | 0.310 |
| (0.4, 0.6] | 6,527.0 | 0.507 | 0.505 |
| (0.6, 0.8] | 11,300.0 | 0.713 | 0.709 |
| (0.8, 0.9] | 13,943.0 | 0.858 | 0.863 |
| (0.9, 0.95] | 11,767.0 | 0.925 | 0.926 |
| (0.95, 1.0] | 3,208.0 | 0.962 | 0.965 |

By alignment (positioning effect = with - without):

| Alignment | n | Actual | Without alignment | With alignment |
|---|---|---|---|---|
| Infield shade | 10,468.0 | 0.743 | 0.741 | 0.741 |
| Standard | 38,244.0 | 0.733 | 0.731 | 0.734 |
| Strategic | 4,292.0 | 0.693 | 0.716 | 0.696 |
