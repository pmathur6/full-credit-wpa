# Infield model: 2025

- Ground balls: 52,496; converted to an out: 0.731; sprint speed coverage: 99.8%

| Predictor | AUC | Brier | Mean predicted |
|---|---|---|---|
| 1 - xBA (old stand-in) | 0.742 | 0.1688 | 0.752 |
| Model, no alignment | 0.810 | 0.1436 | 0.731 |
| Model, with alignment | 0.810 | 0.1433 | 0.731 |

Calibration (with alignment):

| Predicted | n | Mean predicted | Actual |
|---|---|---|---|
| (0.0, 0.2] | 1,840.0 | 0.141 | 0.105 |
| (0.2, 0.4] | 4,390.0 | 0.307 | 0.291 |
| (0.4, 0.6] | 6,430.0 | 0.508 | 0.509 |
| (0.6, 0.8] | 11,548.0 | 0.714 | 0.711 |
| (0.8, 0.9] | 14,481.0 | 0.857 | 0.862 |
| (0.9, 0.95] | 11,313.0 | 0.924 | 0.929 |
| (0.95, 1.0] | 2,494.0 | 0.961 | 0.969 |

By alignment (positioning effect = with - without):

| Alignment | n | Actual | Without alignment | With alignment |
|---|---|---|---|---|
| Infield shade | 12,601.0 | 0.744 | 0.742 | 0.742 |
| Standard | 34,575.0 | 0.728 | 0.728 | 0.729 |
| Strategic | 5,281.0 | 0.713 | 0.724 | 0.716 |
