# Credit report: 2025

## 1. Accounting identities (must hold exactly)

- Events: 189,735. Offense credits equal the event's change on 100.000%; defense credits equal minus the change on 100.000% (max gaps 3.33e-16 / 3.33e-16)
- Events with no credit rows: 0; events with no change in win probability (decided games): 7,061
- Teams whose total credit equals wins minus summed starting win probability: 30 of 30 (max gap 6.30e-15)
- Credit rows with no player (coaching buckets): 88,685; non-coaching rows with no player: 0

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

## 2a. Infield vs Savant OAA

- Infielders (primary 1B/2B/3B/SS) compared: 316; correlation of our ground-ball outs-above-expected with Savant infield OAA: **0.619** (185 with 100+ chances: 0.617)
- Savant judges each fielder from where he actually stood; our model only knows the alignment type, so team positioning is still inside our fielders' numbers. Gap by team (ours - Savant, outs) shows it:

| Position | Players (100+) | Correlation |
|---|---|---|
| 1B | 31 | 0.770 |
| 2B | 59 | 0.622 |
| 3B | 51 | 0.786 |
| SS | 44 | 0.406 |

Gap by team (outs): STL -33, PHI -28, NYM -18, CLE -14, DET -14, HOU -12, CWS -11, COL -10, MIN -10, BAL -10, CIN -9, KC -8, AZ -7, SD -5, WSH -5, BOS -4, TOR +0, LAA +2, TEX +3, SF +5, NYY +8, ATH +8, MIA +9, MIL +10, ATL +17, LAD +19, CHC +19, PIT +21, TB +32, SEA +35

League fielding credit by position (wins): 1B -18.1, 2B +6.7, 3B +12.0, C -12.4, CF +1.8, LF -10.8, P -10.6, RF -14.3, SS +33.8

## 2b. Stolen-base defense vs Savant

- catcher stealing runs: 100 players; correlation of our steal-attempt credit (wins, leverage-weighted) with Savant's (runs): **0.787**
- pitcher running-game runs: 647 players; correlation of our steal-attempt credit (wins, leverage-weighted) with Savant's (runs): **0.470**

## 3. Leaderboards (eye test)

Wins added. Hitters 300+ PA, pitchers 300+ batters faced. `trad` = traditional WPA (batter / pitcher gets the whole play).

### Hitters: top 10 total

| Player | Pos | Team | total | batting | baserunning | fielding | trad_bat |
|---|---|---|---|---|---|---|---|
| Shohei Ohtani | P/DH | LAD | +6.11 | +4.63 | +0.68 | +0.09 | +4.92 |
| Geraldo Perdomo | SS | AZ | +5.93 | +3.15 | +0.90 | +1.88 | +2.90 |
| Bobby Witt Jr. | SS | KC | +5.69 | +2.28 | +1.55 | +1.86 | +2.52 |
| Aaron Judge | RF/DH | NYY | +5.58 | +5.18 | -0.02 | +0.41 | +5.11 |
| Fernando Tatis Jr. | RF | SD | +5.20 | +2.60 | +1.79 | +0.81 | +2.38 |
| José Ramírez | 3B/DH | CLE | +4.66 | +2.87 | +1.19 | +0.60 | +3.14 |
| Bo Bichette | SS | TOR | +4.08 | +2.81 | -0.03 | +1.30 | +3.11 |
| Byron Buxton | CF | MIN | +3.97 | +2.52 | +1.14 | +0.31 | +2.48 |
| Corbin Carroll | RF | AZ | +3.77 | +2.62 | +0.75 | +0.40 | +1.98 |
| Freddie Freeman | 1B | LAD | +3.66 | +3.93 | +0.20 | -0.47 | +4.64 |

### Hitters: bottom 10 total

| Player | Pos | Team | total | batting | baserunning | fielding | trad_bat |
|---|---|---|---|---|---|---|---|
| Eric Wagaman | 1B/LF/DH | MIA | -3.73 | -2.49 | -0.38 | -0.85 | -2.81 |
| Alek Thomas | CF | AZ | -3.68 | -1.85 | -0.18 | -1.65 | -1.99 |
| Nick Castellanos | RF | PHI | -3.51 | -2.57 | -0.33 | -0.62 | -2.71 |
| Logan O'Hoppe | C/DH | LAA | -3.45 | -2.98 | -0.11 | -0.36 | -3.12 |
| Willi Castro | 2B/RF/LF/3B | MIN/CHC | -3.39 | -2.20 | +0.22 | -1.42 | -2.19 |
| JJ Bleday | CF/RF/LF/DH | ATH | -3.35 | -2.68 | -0.03 | -0.64 | -2.63 |
| Matt McLain | 2B | CIN | -3.23 | -4.13 | +0.77 | +0.12 | -4.24 |
| Jordan Walker | RF | STL | -2.89 | -2.29 | +0.23 | -0.83 | -1.96 |
| Edgar Quero | C/DH | CWS | -2.84 | -2.05 | -0.23 | -0.56 | -1.95 |
| Lenyn Sosa | 2B/1B/DH | CWS | -2.81 | -2.90 | +0.34 | -0.25 | -2.70 |

### Fielding: top 10

| Player | Pos | Team | fielding |
|---|---|---|---|
| Xavier Edwards | 2B/SS | MIA | +2.49 |
| Ryan McMahon | 3B | COL/NYY | +1.90 |
| Geraldo Perdomo | SS | AZ | +1.88 |
| Taylor Walls | SS | TB | +1.87 |
| Bobby Witt Jr. | SS | KC | +1.86 |
| Dansby Swanson | SS | CHC | +1.78 |
| Anthony Volpe | SS | NYY | +1.78 |
| Brayan Rocchio | SS/2B | CLE | +1.73 |
| Xander Bogaerts | SS/DH | SD | +1.73 |
| Nico Hoerner | 2B | CHC | +1.73 |

### Fielding: bottom 10

| Player | Pos | Team | fielding |
|---|---|---|---|
| Pete Alonso | 1B | NYM | -1.90 |
| Brendan Donovan | 2B/LF | STL | -1.70 |
| Alek Thomas | CF | AZ | -1.65 |
| Eugenio Suárez | 3B | AZ/SEA | -1.63 |
| Juan Soto | RF | NYM | -1.62 |
| Thomas Saggese | 2B/SS/3B | STL | -1.47 |
| Willi Castro | 2B/RF/LF/3B | MIN/CHC | -1.42 |
| Heliot Ramos | LF | SF | -1.42 |
| Kristian Campbell | 2B | BOS | -1.37 |
| Kyle Tucker | RF/DH | CHC | -1.30 |

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
| Garrett Crochet | P | BOS | +5.36 | -0.04 | +5.00 |
| Paul Skenes | P | PIT | +4.81 | +0.03 | +5.15 |
| Cristopher Sánchez | P | PHI | +4.24 | +0.02 | +4.65 |
| Tarik Skubal | P | DET | +3.76 | -0.19 | +4.24 |
| Cade Smith | P | CLE | +3.75 | -0.35 | +2.34 |
| Yoshinobu Yamamoto | P | LAD | +3.58 | +0.05 | +4.09 |
| Max Fried | P | NYY | +3.05 | +0.12 | +2.40 |
| Andrew Abbott | P | CIN | +2.97 | -0.06 | +2.74 |
| Zack Wheeler | P | PHI | +2.95 | +0.03 | +3.29 |
| Freddy Peralta | P | MIL | +2.87 | +0.01 | +3.74 |

### Pitchers: bottom 10

| Player | Pos | Team | pitching | fielding | trad_pit |
|---|---|---|---|---|---|
| Jack Kochanowicz | P | LAA | -2.48 | -0.10 | -2.79 |
| Germán Márquez | P | COL | -2.37 | +0.04 | -3.55 |
| Tyler Alexander | P | CWS/MIL | -2.31 | +0.15 | -2.70 |
| Antonio Senzatela | P | COL | -2.22 | +0.25 | -2.95 |
| Charlie Morton | P | BAL/DET/ATL | -1.98 | -0.19 | -2.35 |
| Jake Irvin | P | WSH | -1.87 | -0.02 | -2.81 |
| Tanner Gordon | P | COL | -1.63 | -0.04 | -1.54 |
| Mitchell Parker | P | WSH | -1.63 | -0.07 | -1.78 |
| Jordan Hicks | P | SF/BOS | -1.61 | -0.05 | -2.21 |
| Bryce Miller | P | SEA | -1.56 | -0.00 | -1.27 |

### Pitchers hurt most by their defense (our pitching credit above traditional WPA: fielders took some blame)

| Player | Pos | Team | gap | pitching | trad_pit |
|---|---|---|---|---|---|
| Dylan Cease | P | SD | +1.66 | +0.79 | -0.87 |
| Cade Smith | P | CLE | +1.41 | +3.75 | +2.34 |
| Andre Pallante | P | STL | +1.41 | -1.21 | -2.61 |
| Tylor Megill | P | NYM | +1.25 | +0.69 | -0.56 |
| Germán Márquez | P | COL | +1.18 | -2.37 | -3.55 |
| Casey Mize | P | DET | +1.07 | +1.33 | +0.25 |
| Jesús Luzardo | P | PHI | +1.07 | +2.76 | +1.69 |
| Eduardo Rodriguez | P | AZ | +1.02 | -0.37 | -1.39 |
| Trevor Williams | P | WSH | +1.00 | -0.66 | -1.66 |
| Kyle Hendricks | P | LAA | +0.94 | +0.49 | -0.45 |

### Pitchers helped most by their defense (our pitching credit below traditional WPA: fielders took some credit)

| Player | Pos | Team | gap | pitching | trad_pit |
|---|---|---|---|---|---|
| Nathan Eovaldi | P | TEX | -1.65 | +2.47 | +4.13 |
| Drew Rasmussen | P | TB | -1.61 | +1.25 | +2.85 |
| Noah Cameron | P | KC | -1.60 | +0.74 | +2.34 |
| Tyler Phillips | P | MIA | -1.54 | +0.82 | +2.36 |
| Grant Holmes | P | ATL | -1.32 | -0.93 | +0.39 |
| Nick Martinez | P | CIN | -1.21 | -0.97 | +0.24 |
| Seth Lugo | P | KC | -1.17 | -1.11 | +0.06 |
| Emerson Hancock | P | SEA | -1.10 | -0.87 | +0.23 |
| Hunter Brown | P | HOU | -1.04 | +2.65 | +3.69 |
| Adrian Houser | P | CWS/TB | -1.01 | +0.82 | +1.82 |

### Coaching (team)

| Team | bunt call | defensive indifference | intentional walk | positioning | total |
|---|---|---|---|---|---|
| SEA | +0.34 | +0.05 | -0.35 | +2.21 | +2.23 |
| CIN | +0.02 | -0.00 | -0.08 | +1.46 | +1.39 |
| CHC | +0.09 | -0.01 | -0.08 | +1.12 | +1.12 |
| TB | +0.19 | -0.02 | -0.09 | +1.00 | +1.08 |
| STL | -0.03 | -0.01 | -0.16 | +0.97 | +0.77 |
| CWS | +0.10 | -0.04 | -0.38 | +0.89 | +0.56 |
| HOU | +0.01 | -0.00 | -0.06 | +0.59 | +0.55 |
| PIT | +0.19 | -0.00 | -0.27 | +0.62 | +0.54 |
| LAA | +0.08 | -0.02 | -0.58 | +0.89 | +0.37 |
| CLE | -0.00 | -0.01 | -0.15 | +0.42 | +0.26 |
| NYM | -0.05 | -0.00 | -0.11 | +0.32 | +0.17 |
| ATL | -0.02 | -0.01 | -0.35 | +0.47 | +0.09 |
| MIN | +0.02 | -0.04 | -0.30 | +0.33 | +0.01 |
| SD | -0.05 | -0.01 | -0.34 | +0.17 | -0.23 |
| DET | -0.00 | -0.03 | -0.14 | -0.29 | -0.46 |
| TEX | +0.12 | -0.01 | -0.34 | -0.38 | -0.61 |
| SF | +0.35 | -0.04 | -0.23 | -0.74 | -0.66 |
| MIA | -0.08 | -0.00 | -0.24 | -0.37 | -0.69 |
| BOS | +0.11 | +0.00 | -0.16 | -0.66 | -0.71 |
| WSH | +0.03 | -0.02 | -0.02 | -0.76 | -0.77 |
| TOR | +0.06 | +0.00 | -0.55 | -0.31 | -0.79 |
| BAL | +0.07 | -0.01 | -0.17 | -0.78 | -0.88 |
| KC | +0.05 | -0.01 | -0.14 | -0.82 | -0.93 |
| NYY | -0.03 | +0.03 | -0.07 | -0.89 | -0.95 |
| LAD | +0.03 | -0.04 | -0.38 | -0.65 | -1.04 |
| ATH | +0.07 | +0.00 | -0.27 | -1.06 | -1.25 |
| MIL | +0.05 | -0.02 | -0.36 | -0.99 | -1.32 |
| AZ | +0.13 | -0.01 | -0.29 | -1.17 | -1.34 |
| PHI | -0.00 | +0.00 | -0.16 | -1.62 | -1.78 |
| COL | -0.03 | +0.00 | -0.17 | -2.44 | -2.65 |

### Bucket totals (league)

- def / coaching: -9.8
- def / fielding: -12.0
- def / pitching: +186.9
- off / baserunning: +61.0
- off / batting: -227.9
- off / coaching: +1.8
