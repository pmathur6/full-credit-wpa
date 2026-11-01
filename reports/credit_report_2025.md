# Credit report: 2025

## 1. Accounting identities (must hold exactly)

- Events: 189,735. Offense credits equal the event's change on 100.000%; defense credits equal minus the change on 100.000% (max gaps 3.33e-16 / 3.33e-16)
- Events with no credit rows: 0; events with no change in win probability (decided games): 7,061
- Teams whose total credit equals wins minus summed starting win probability: 30 of 30 (max gap 5.91e-15)
- Credit rows with no player (coaching buckets): 36,487; non-coaching rows with no player: 0

| Team | W | G | Credited | Wins - starting WP |
|---|---|---|---|---|
| MIL | 97 | 162 | +16.00 | +16.00 |
| PHI | 96 | 162 | +15.00 | +15.00 |
| TOR | 94 | 162 | +13.00 | +13.00 |
| NYY | 94 | 162 | +13.00 | +13.00 |
| LAD | 93 | 162 | +12.00 | +12.00 |
| CHC | 92 | 162 | +11.00 | +11.00 |
| SD | 90 | 162 | +9.00 | +9.00 |
| SEA | 90 | 162 | +9.00 | +9.00 |
| BOS | 89 | 162 | +8.00 | +8.00 |
| CLE | 88 | 162 | +7.00 | +7.00 |
| HOU | 87 | 162 | +6.00 | +6.00 |
| DET | 87 | 162 | +6.00 | +6.00 |
| NYM | 83 | 162 | +2.00 | +2.00 |
| CIN | 83 | 162 | +2.00 | +2.00 |
| KC | 82 | 162 | +1.00 | +1.00 |
| TEX | 81 | 162 | -0.00 | +0.00 |
| SF | 81 | 162 | -0.00 | +0.00 |
| AZ | 80 | 162 | -1.00 | -1.00 |
| MIA | 79 | 162 | -2.00 | -2.00 |
| STL | 78 | 162 | -3.00 | -3.00 |
| TB | 77 | 162 | -4.00 | -4.00 |
| ATH | 76 | 162 | -5.00 | -5.00 |
| ATL | 76 | 162 | -5.00 | -5.00 |
| BAL | 75 | 162 | -6.00 | -6.00 |
| LAA | 72 | 162 | -9.00 | -9.00 |
| PIT | 71 | 162 | -10.00 | -10.00 |
| MIN | 70 | 162 | -11.00 | -11.00 |
| WSH | 66 | 162 | -15.00 | -15.00 |
| CWS | 60 | 162 | -21.00 | -21.00 |
| COL | 43 | 162 | -38.00 | -38.00 |

## 2. Outfield vs Savant OAA

- Outfield catch chances credited to the same fielder Savant names: 99.99%
- Outfielders (primary position LF/CF/RF) compared: 251; correlation of our outs-above-expected with Savant OAA: **0.972**; mean absolute difference 1.01 outs

Largest differences (Savant OAA includes direction/arm adjustments and other positions):

| Player | Savant OAA | Ours (outs - catch prob) |
|---|---|---|
| Pete Crow-Armstrong | +24 | +18.6 |
| Brooks Baldwin | -11 | -6.1 |
| Tyler Freeman | -13 | -8.4 |
| Nathan Lukes | +3 | -1.3 |
| Julio Rodríguez | +11 | +7.5 |
| Randy Arozarena | -5 | -8.2 |
| Sal Frelick | +7 | +3.8 |
| Brenton Doyle | +6 | +2.8 |

## 3. Leaderboards (eye test)

Wins added. Hitters 300+ PA, pitchers 300+ batters faced. `trad` = traditional WPA (batter / pitcher gets the whole play).

### Hitters: top 10 total

| Player | Pos | Team | total | batting | baserunning | fielding | trad_bat |
|---|---|---|---|---|---|---|---|
| Shohei Ohtani | P/DH | LAD | +6.15 | +4.63 | +0.68 | +0.13 | +4.92 |
| Aaron Judge | RF/DH | NYY | +5.58 | +5.18 | -0.02 | +0.41 | +5.11 |
| Bobby Witt Jr. | SS | KC | +5.54 | +2.28 | +1.55 | +1.71 | +2.52 |
| Geraldo Perdomo | SS | AZ | +5.27 | +3.15 | +0.90 | +1.22 | +2.90 |
| Fernando Tatis Jr. | RF | SD | +5.17 | +2.60 | +1.79 | +0.78 | +2.38 |
| Byron Buxton | CF | MIN | +3.97 | +2.52 | +1.14 | +0.31 | +2.48 |
| Corbin Carroll | RF | AZ | +3.78 | +2.62 | +0.75 | +0.41 | +1.98 |
| Bo Bichette | SS | TOR | +3.41 | +2.81 | -0.03 | +0.64 | +3.11 |
| Freddie Freeman | 1B | LAD | +3.31 | +3.93 | +0.20 | -0.82 | +4.64 |
| Jeremy Peña | SS | HOU | +3.19 | +1.04 | +0.85 | +1.30 | +1.14 |

### Hitters: bottom 10 total

| Player | Pos | Team | total | batting | baserunning | fielding | trad_bat |
|---|---|---|---|---|---|---|---|
| Carlos Correa | SS/3B | MIN/HOU | -4.35 | -1.99 | +0.15 | -2.51 | -1.80 |
| Austin Riley | 3B | ATL | -4.15 | -2.22 | -0.24 | -1.68 | -2.30 |
| Eric Wagaman | 1B/LF/DH | MIA | -4.05 | -2.49 | -0.38 | -1.17 | -2.81 |
| Willi Castro | 2B/RF/LF/3B | MIN/CHC | -3.94 | -2.20 | +0.22 | -1.97 | -2.19 |
| Matt McLain | 2B | CIN | -3.70 | -4.13 | +0.77 | -0.34 | -4.24 |
| Josh Jung | 3B | TEX | -3.69 | -2.29 | -0.32 | -1.08 | -2.10 |
| Alek Thomas | CF | AZ | -3.68 | -1.85 | -0.18 | -1.65 | -1.99 |
| Nick Castellanos | RF | PHI | -3.51 | -2.57 | -0.33 | -0.62 | -2.71 |
| Lenyn Sosa | 2B/1B/DH | CWS | -3.50 | -2.90 | +0.34 | -0.94 | -2.70 |
| Logan O'Hoppe | C/DH | LAA | -3.41 | -2.98 | -0.11 | -0.32 | -3.12 |

### Fielding: top 10

| Player | Pos | Team | fielding |
|---|---|---|---|
| Brayan Rocchio | SS/2B | CLE | +1.80 |
| Xander Bogaerts | SS/DH | SD | +1.72 |
| Bobby Witt Jr. | SS | KC | +1.71 |
| Ceddanne Rafaela | CF/2B | BOS | +1.69 |
| Pete Crow-Armstrong | CF | CHC | +1.59 |
| Xavier Edwards | 2B/SS | MIA | +1.59 |
| Mookie Betts | SS | LAD | +1.50 |
| Steven Kwan | LF | CLE | +1.48 |
| Corey Seager | SS | TEX | +1.39 |
| Anthony Volpe | SS | NYY | +1.32 |

### Fielding: bottom 10

| Player | Pos | Team | fielding |
|---|---|---|---|
| Eugenio Suárez | 3B | AZ/SEA | -4.01 |
| Brendan Donovan | 2B/LF | STL | -2.57 |
| Thomas Saggese | 2B/SS/3B | STL | -2.51 |
| Carlos Correa | SS/3B | MIN/HOU | -2.51 |
| Pete Alonso | 1B | NYM | -2.36 |
| Manny Machado | 3B/DH | SD | -2.22 |
| Brooks Lee | SS/3B/2B | MIN | -2.10 |
| Yoán Moncada | 3B | LAA | -2.08 |
| Willi Castro | 2B/RF/LF/3B | MIN/CHC | -1.97 |
| Casey Schmitt | 2B/3B/1B | SF | -1.96 |

### Baserunning: top 10

| Player | Pos | Team | baserunning |
|---|---|---|---|
| Fernando Tatis Jr. | RF | SD | +1.79 |
| Bobby Witt Jr. | SS | KC | +1.55 |
| José Ramírez | 3B/DH | CLE | +1.19 |
| Elly De La Cruz | SS | CIN | +1.17 |
| Byron Buxton | CF | MIN | +1.14 |
| Trevor Story | SS | BOS | +1.09 |
| CJ Abrams | SS | WSH | +1.09 |
| Ceddanne Rafaela | CF/2B | BOS | +1.09 |
| Francisco Lindor | SS | NYM | +1.05 |
| Zach McKinstry | 3B/SS/RF/LF | DET | +1.04 |

### Baserunning: bottom 10

| Player | Pos | Team | baserunning |
|---|---|---|---|
| Cal Raleigh | C/DH | SEA | -0.79 |
| Jonathan Aranda | 1B/DH | TB | -0.73 |
| Alexander Canario | LF/CF/RF | PIT | -0.70 |
| Romy Gonzalez | 1B/2B | BOS | -0.61 |
| Ty France | 1B/DH | MIN/TOR | -0.60 |
| Rafael Devers | 1B/DH | SF/BOS | -0.60 |
| Drew Waters | LF/CF/RF | KC | -0.58 |
| Tommy Pham | LF | PIT | -0.50 |
| Vinnie Pasquantino | 1B/DH | KC | -0.50 |
| Tyler Freeman | RF/2B/DH | COL | -0.49 |

### Pitchers: top 10

| Player | Pos | Team | pitching | fielding | trad_pit |
|---|---|---|---|---|---|
| Garrett Crochet | P | BOS | +5.64 | +0.15 | +5.00 |
| Cristopher Sánchez | P | PHI | +5.05 | +0.26 | +4.65 |
| Paul Skenes | P | PIT | +4.91 | +0.16 | +5.15 |
| Tarik Skubal | P | DET | +4.07 | -0.10 | +4.24 |
| Yoshinobu Yamamoto | P | LAD | +3.95 | +0.16 | +4.09 |
| Cade Smith | P | CLE | +3.81 | -0.27 | +2.34 |
| Max Fried | P | NYY | +3.43 | +0.21 | +2.40 |
| Freddy Peralta | P | MIL | +3.36 | +0.09 | +3.74 |
| Andrew Abbott | P | CIN | +3.34 | +0.08 | +2.74 |
| Chris Sale | P | ATL | +3.17 | +0.10 | +2.79 |

### Pitchers: bottom 10

| Player | Pos | Team | pitching | fielding | trad_pit |
|---|---|---|---|---|---|
| Jack Kochanowicz | P | LAA | -2.06 | +0.02 | -2.79 |
| Germán Márquez | P | COL | -1.90 | +0.14 | -3.55 |
| Charlie Morton | P | BAL/DET/ATL | -1.87 | +0.02 | -2.35 |
| Tyler Alexander | P | CWS/MIL | -1.71 | +0.23 | -2.70 |
| Antonio Senzatela | P | COL | -1.50 | +0.28 | -2.95 |
| Jake Irvin | P | WSH | -1.49 | +0.09 | -2.81 |
| Tanner Gordon | P | COL | -1.48 | +0.06 | -1.54 |
| Mitchell Parker | P | WSH | -1.44 | +0.07 | -1.78 |
| Erick Fedde | P | STL/ATL/MIL | -1.35 | +0.13 | -1.47 |
| Bryce Miller | P | SEA | -1.33 | +0.01 | -1.27 |

### Pitchers hurt most by their defense (our pitching credit above traditional WPA: fielders took some blame)

| Player | Pos | Team | gap | pitching | trad_pit |
|---|---|---|---|---|---|
| Andre Pallante | P | STL | +1.79 | -0.82 | -2.61 |
| Dylan Cease | P | SD | +1.68 | +0.80 | -0.87 |
| Germán Márquez | P | COL | +1.65 | -1.90 | -3.55 |
| Cade Smith | P | CLE | +1.48 | +3.81 | +2.34 |
| Eduardo Rodriguez | P | AZ | +1.46 | +0.06 | -1.39 |
| Antonio Senzatela | P | COL | +1.45 | -1.50 | -2.95 |
| Tylor Megill | P | NYM | +1.41 | +0.85 | -0.56 |
| Yusei Kikuchi | P | LAA | +1.39 | +1.50 | +0.11 |
| Logan Allen | P | CLE | +1.33 | +1.14 | -0.19 |
| Kyle Freeland | P | COL | +1.33 | -0.23 | -1.56 |

### Pitchers helped most by their defense (our pitching credit below traditional WPA: fielders took some credit)

| Player | Pos | Team | gap | pitching | trad_pit |
|---|---|---|---|---|---|
| Nathan Eovaldi | P | TEX | -1.56 | +2.56 | +4.13 |
| Drew Rasmussen | P | TB | -1.45 | +1.40 | +2.85 |
| Tyler Phillips | P | MIA | -1.38 | +0.98 | +2.36 |
| Noah Cameron | P | KC | -1.33 | +1.01 | +2.34 |
| Emerson Hancock | P | SEA | -1.13 | -0.90 | +0.23 |
| Nick Martinez | P | CIN | -1.02 | -0.78 | +0.24 |
| Seth Lugo | P | KC | -0.93 | -0.87 | +0.06 |
| Grant Holmes | P | ATL | -0.85 | -0.46 | +0.39 |
| Hunter Brown | P | HOU | -0.74 | +2.95 | +3.69 |
| Jacob deGrom | P | TEX | -0.69 | +2.34 | +3.03 |

### Coaching (team)

| Team | bunt call | defensive indifference | intentional walk | positioning | total |
|---|---|---|---|---|---|
| SEA | +0.34 | +0.05 | -0.35 | +2.30 | +2.33 |
| CIN | +0.02 | -0.00 | -0.08 | +1.48 | +1.41 |
| CHC | +0.09 | -0.01 | -0.08 | +1.00 | +1.00 |
| TB | +0.19 | -0.02 | -0.09 | +0.77 | +0.85 |
| STL | -0.03 | -0.01 | -0.16 | +0.77 | +0.57 |
| CWS | +0.10 | -0.04 | -0.38 | +0.88 | +0.56 |
| PIT | +0.19 | -0.00 | -0.27 | +0.59 | +0.51 |
| HOU | +0.01 | -0.00 | -0.06 | +0.43 | +0.38 |
| LAA | +0.08 | -0.02 | -0.58 | +0.90 | +0.38 |
| CLE | -0.00 | -0.01 | -0.15 | +0.51 | +0.35 |
| ATL | -0.02 | -0.01 | -0.35 | +0.54 | +0.16 |
| MIN | +0.02 | -0.04 | -0.30 | +0.40 | +0.08 |
| NYM | -0.05 | -0.00 | -0.11 | +0.18 | +0.02 |
| SD | -0.05 | -0.01 | -0.34 | +0.10 | -0.30 |
| DET | -0.00 | -0.03 | -0.14 | -0.29 | -0.46 |
| BOS | +0.11 | +0.00 | -0.16 | -0.51 | -0.56 |
| MIA | -0.08 | -0.00 | -0.24 | -0.35 | -0.67 |
| TEX | +0.12 | -0.01 | -0.34 | -0.46 | -0.69 |
| SF | +0.35 | -0.04 | -0.23 | -0.81 | -0.73 |
| WSH | +0.03 | -0.02 | -0.02 | -0.77 | -0.78 |
| TOR | +0.06 | +0.00 | -0.55 | -0.34 | -0.83 |
| BAL | +0.07 | -0.01 | -0.17 | -0.74 | -0.84 |
| NYY | -0.03 | +0.03 | -0.07 | -0.98 | -1.04 |
| KC | +0.05 | -0.01 | -0.14 | -0.99 | -1.10 |
| LAD | +0.03 | -0.04 | -0.38 | -0.84 | -1.23 |
| MIL | +0.05 | -0.02 | -0.36 | -0.99 | -1.31 |
| ATH | +0.07 | +0.00 | -0.27 | -1.12 | -1.31 |
| AZ | +0.13 | -0.01 | -0.29 | -1.28 | -1.46 |
| PHI | -0.00 | +0.00 | -0.16 | -1.87 | -2.03 |
| COL | -0.03 | +0.00 | -0.17 | -2.52 | -2.72 |

### Bucket totals (league)

- def / coaching: -11.3
- def / fielding: -100.1
- def / pitching: +276.4
- off / baserunning: +61.0
- off / batting: -227.9
- off / coaching: +1.8
