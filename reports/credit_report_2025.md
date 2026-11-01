# Credit report: 2025

## 1. Accounting identities (must hold exactly)

- Events: 189,735. Offense credits equal the event's change on 100.000%; defense credits equal minus the change on 100.000% (max gaps 3.33e-16 / 3.33e-16)
- Events with no credit rows: 0; events with no change in win probability (decided games): 7,061
- Teams whose total credit equals wins minus summed starting win probability: 30 of 30 (max gap 6.30e-15)
- Credit rows with no player (coaching buckets): 150,904; non-coaching rows with no player: 0

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

- After moving positioning to coaching, infielders' outs above expected match Savant OAA: correlation 1.000, max gap 0.90 outs
- Infield positioning credit by team (wins): STL -2.21, PHI -1.92, NYM -1.16, CLE -1.02, DET -0.97, HOU -0.94, BAL -0.70, CIN -0.66, CWS -0.64, COL -0.58, KC -0.42, SD -0.38, AZ -0.23, WSH -0.22, BOS -0.18, MIN -0.14, TOR +0.04, TEX +0.25, SF +0.32, LAA +0.39, ATH +0.48, MIA +0.59, MIL +0.74, NYY +0.84, ATL +0.95, LAD +1.19, PIT +1.22, CHC +1.22, TB +2.39, SEA +2.81

League fielding credit by position (wins): 1B -19.6, 2B +5.8, 3B +11.8, C -12.4, CF +1.8, LF -10.8, P -10.6, RF -14.3, SS +35.4

## 2b. Stolen-base defense vs Savant

- catcher stealing runs: 100 players; correlation of our steal-attempt credit (wins, leverage-weighted) with Savant's (runs): **0.787**
- pitcher running-game runs: 647 players; correlation of our steal-attempt credit (wins, leverage-weighted) with Savant's (runs): **0.470**

## 3. Leaderboards (eye test)

Wins added. Hitters 300+ PA, pitchers 300+ batters faced. `trad` = traditional WPA (batter / pitcher gets the whole play).

### Hitters: top 10 total

| Player | Pos | Team | total | batting | baserunning | fielding | trad_bat |
|---|---|---|---|---|---|---|---|
| Bobby Witt Jr. | SS | KC | +7.34 | +2.28 | +1.55 | +3.51 | +2.52 |
| Shohei Ohtani | P/DH | LAD | +6.11 | +4.63 | +0.68 | +0.09 | +4.92 |
| Geraldo Perdomo | SS | AZ | +5.84 | +3.15 | +0.90 | +1.79 | +2.90 |
| Aaron Judge | RF/DH | NYY | +5.58 | +5.18 | -0.02 | +0.41 | +5.11 |
| José Ramírez | 3B/DH | CLE | +5.34 | +2.87 | +1.19 | +1.28 | +3.14 |
| Fernando Tatis Jr. | RF | SD | +5.20 | +2.60 | +1.79 | +0.81 | +2.38 |
| Bo Bichette | SS | TOR | +3.99 | +2.81 | -0.03 | +1.22 | +3.11 |
| Byron Buxton | CF | MIN | +3.97 | +2.52 | +1.14 | +0.31 | +2.48 |
| Freddie Freeman | 1B | LAD | +3.78 | +3.93 | +0.20 | -0.34 | +4.64 |
| Corbin Carroll | RF | AZ | +3.77 | +2.62 | +0.75 | +0.40 | +1.98 |

### Hitters: bottom 10 total

| Player | Pos | Team | total | batting | baserunning | fielding | trad_bat |
|---|---|---|---|---|---|---|---|
| Alek Thomas | CF | AZ | -3.68 | -1.85 | -0.18 | -1.65 | -1.99 |
| Eric Wagaman | 1B/LF/DH | MIA | -3.67 | -2.49 | -0.38 | -0.79 | -2.81 |
| Nick Castellanos | RF | PHI | -3.51 | -2.57 | -0.33 | -0.62 | -2.71 |
| Logan O'Hoppe | C/DH | LAA | -3.45 | -2.98 | -0.11 | -0.36 | -3.12 |
| JJ Bleday | CF/RF/LF/DH | ATH | -3.35 | -2.68 | -0.03 | -0.64 | -2.63 |
| Willi Castro | 2B/RF/LF/3B | MIN/CHC | -3.33 | -2.20 | +0.22 | -1.36 | -2.19 |
| Jordan Walker | RF | STL | -2.89 | -2.29 | +0.23 | -0.83 | -1.96 |
| Edgar Quero | C/DH | CWS | -2.84 | -2.05 | -0.23 | -0.56 | -1.95 |
| Tyler Freeman | RF/2B/DH | COL | -2.78 | -1.04 | -0.49 | -1.25 | -0.94 |
| Matt McLain | 2B | CIN | -2.73 | -4.13 | +0.77 | +0.62 | -4.24 |

### Fielding: top 10

| Player | Pos | Team | fielding |
|---|---|---|---|
| Bobby Witt Jr. | SS | KC | +3.51 |
| Masyn Winn | SS | STL | +2.64 |
| Xavier Edwards | 2B/SS | MIA | +2.00 |
| Xander Bogaerts | SS/DH | SD | +1.93 |
| Mauricio Dubón | LF/2B/SS/3B/CF | HOU | +1.84 |
| Geraldo Perdomo | SS | AZ | +1.79 |
| Willy Adames | SS | SF | +1.77 |
| Tommy Edman | 2B/CF/3B | LAD | +1.72 |
| Ceddanne Rafaela | CF/2B | BOS | +1.66 |
| Matt Chapman | 3B | SF | +1.61 |

### Fielding: bottom 10

| Player | Pos | Team | fielding |
|---|---|---|---|
| Alek Thomas | CF | AZ | -1.65 |
| Juan Soto | RF | NYM | -1.62 |
| Pete Alonso | 1B | NYM | -1.57 |
| Kristian Campbell | 2B | BOS | -1.45 |
| Heliot Ramos | LF | SF | -1.42 |
| Willi Castro | 2B/RF/LF/3B | MIN/CHC | -1.36 |
| Kyle Tucker | RF/DH | CHC | -1.30 |
| Gavin Lux | LF/2B/DH | CIN | -1.28 |
| Michael Toglia | 1B | COL | -1.26 |
| Jo Adell | CF/RF | LAA | -1.26 |

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
| SEA | +0.34 | +0.05 | -0.35 | +5.01 | +5.04 |
| TB | +0.19 | -0.02 | -0.09 | +3.39 | +3.47 |
| CHC | +0.09 | -0.01 | -0.08 | +2.35 | +2.34 |
| PIT | +0.19 | -0.00 | -0.27 | +1.84 | +1.76 |
| ATL | -0.02 | -0.01 | -0.35 | +1.42 | +1.04 |
| LAA | +0.08 | -0.02 | -0.58 | +1.28 | +0.76 |
| CIN | +0.02 | -0.00 | -0.08 | +0.80 | +0.73 |
| LAD | +0.03 | -0.04 | -0.38 | +0.54 | +0.15 |
| CWS | +0.10 | -0.04 | -0.38 | +0.24 | -0.08 |
| MIA | -0.08 | -0.00 | -0.24 | +0.22 | -0.10 |
| NYY | -0.03 | +0.03 | -0.07 | -0.05 | -0.12 |
| MIN | +0.02 | -0.04 | -0.30 | +0.19 | -0.13 |
| SF | +0.35 | -0.04 | -0.23 | -0.42 | -0.34 |
| TEX | +0.12 | -0.01 | -0.34 | -0.14 | -0.36 |
| HOU | +0.01 | -0.00 | -0.06 | -0.34 | -0.39 |
| MIL | +0.05 | -0.02 | -0.36 | -0.25 | -0.57 |
| SD | -0.05 | -0.01 | -0.34 | -0.22 | -0.62 |
| TOR | +0.06 | +0.00 | -0.55 | -0.27 | -0.76 |
| CLE | -0.00 | -0.01 | -0.15 | -0.60 | -0.76 |
| ATH | +0.07 | +0.00 | -0.27 | -0.58 | -0.77 |
| BOS | +0.11 | +0.00 | -0.16 | -0.84 | -0.89 |
| WSH | +0.03 | -0.02 | -0.02 | -0.98 | -0.99 |
| NYM | -0.05 | -0.00 | -0.11 | -0.84 | -1.00 |
| KC | +0.05 | -0.01 | -0.14 | -1.25 | -1.36 |
| DET | -0.00 | -0.03 | -0.14 | -1.26 | -1.43 |
| STL | -0.03 | -0.01 | -0.16 | -1.25 | -1.45 |
| AZ | +0.13 | -0.01 | -0.29 | -1.39 | -1.57 |
| BAL | +0.07 | -0.01 | -0.17 | -1.48 | -1.58 |
| COL | -0.03 | +0.00 | -0.17 | -3.02 | -3.23 |
| PHI | -0.00 | +0.00 | -0.16 | -3.54 | -3.70 |

### Bucket totals (league)

- def / coaching: -8.7
- def / fielding: -13.0
- def / pitching: +186.9
- off / baserunning: +61.0
- off / batting: -227.9
- off / coaching: +1.8
