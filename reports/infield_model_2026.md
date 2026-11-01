# Infield model: 2026

- Ground balls: 52,310; converted to an out: 0.730; sprint speed coverage: 99.8%

| Predictor | AUC | Brier | Mean predicted |
|---|---|---|---|
| 1 - xBA (old stand-in) | 0.736 | 0.1704 | 0.751 |
| Model, no alignment | 0.811 | 0.1435 | 0.731 |
| Model, with alignment | 0.813 | 0.1427 | 0.731 |

Calibration (with alignment):

| Predicted | n | Mean predicted | Actual |
|---|---|---|---|
| (0.0, 0.2] | 2,060.0 | 0.133 | 0.101 |
| (0.2, 0.4] | 4,452.0 | 0.306 | 0.308 |
| (0.4, 0.6] | 6,024.0 | 0.506 | 0.506 |
| (0.6, 0.8] | 11,543.0 | 0.715 | 0.713 |
| (0.8, 0.9] | 13,777.0 | 0.856 | 0.857 |
| (0.9, 0.95] | 10,713.0 | 0.925 | 0.927 |
| (0.95, 1.0] | 3,741.0 | 0.962 | 0.966 |

By alignment (positioning effect = with - without):

| Alignment | n | Actual | Without alignment | With alignment |
|---|---|---|---|---|
| Infield shade | 12,991.0 | 0.748 | 0.741 | 0.747 |
| Standard | 33,346.0 | 0.728 | 0.729 | 0.729 |
| Strategic | 5,845.0 | 0.704 | 0.718 | 0.706 |
