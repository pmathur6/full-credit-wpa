# Infield model: 2024

- Ground balls: 52,735; converted to an out: 0.729; sprint speed coverage: 99.8%

| Predictor | AUC | Brier | Mean predicted |
|---|---|---|---|
| 1 - xBA (old stand-in) | 0.739 | 0.1701 | 0.753 |
| Model, no alignment | 0.808 | 0.1451 | 0.729 |
| Model, with alignment | 0.810 | 0.1443 | 0.729 |

Calibration (with alignment):

| Predicted | n | Mean predicted | Actual |
|---|---|---|---|
| (0.0, 0.2] | 1,970.0 | 0.137 | 0.121 |
| (0.2, 0.4] | 4,589.0 | 0.303 | 0.304 |
| (0.4, 0.6] | 6,408.0 | 0.506 | 0.511 |
| (0.6, 0.8] | 11,412.0 | 0.713 | 0.711 |
| (0.8, 0.9] | 13,830.0 | 0.857 | 0.857 |
| (0.9, 0.95] | 11,274.0 | 0.925 | 0.927 |
| (0.95, 1.0] | 3,252.0 | 0.961 | 0.964 |

By alignment (positioning effect = with - without):

| Alignment | n | Actual | Without alignment | With alignment |
|---|---|---|---|---|
| Infield shade | 11,634.0 | 0.739 | 0.736 | 0.737 |
| Standard | 35,765.0 | 0.729 | 0.728 | 0.729 |
| Strategic | 5,109.0 | 0.709 | 0.721 | 0.710 |
