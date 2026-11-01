# Credit report: 2025

## 1. Accounting identities (must hold exactly)

- Events: 189,735. Offense credits equal the event's change on 100.000%; defense credits equal minus the change on 100.000% (max gaps 3.33e-16 / 5.55e-16)
- Events with no credit rows: 0; events with no change in win probability (decided games): 7,061
- Teams whose total credit equals wins minus summed starting win probability: 30 of 30 (max gap 6.19e-15)
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

League fielding credit by position (wins): 1B -4.3, 2B -5.6, 3B +13.0, C -11.3, CF -8.8, LF -13.5, P -1.5, RF -31.7, SS +8.3

## 2b. Stolen-base defense vs Savant

- catcher stealing runs: 100 players; correlation of our steal-attempt credit (wins, leverage-weighted) with Savant's (runs): **0.787**
- pitcher running-game runs: 647 players; correlation of our steal-attempt credit (wins, leverage-weighted) with Savant's (runs): **0.470**

## 3. Leaderboards (eye test)

Wins added. Hitters 300+ PA, pitchers 300+ batters faced. `trad` = traditional WPA (batter / pitcher gets the whole play).

### Hitters: top 10 total

| Player | Pos | Team | total | batting | baserunning | fielding | trad_bat |
|---|---|---|---|---|---|---|---|
| Bobby Witt Jr. | SS | KC | +6.46 | +2.28 | +1.55 | +2.63 | +2.52 |
| Shohei Ohtani | P/DH | LAD | +6.17 | +4.63 | +0.68 | +0.06 | +4.92 |
| Aaron Judge | RF/DH | NYY | +5.59 | +5.18 | -0.02 | +0.42 | +5.11 |
| José Ramírez | 3B/DH | CLE | +5.42 | +2.87 | +1.19 | +1.36 | +3.14 |
| Fernando Tatis Jr. | RF | SD | +4.95 | +2.60 | +1.79 | +0.56 | +2.38 |
| Geraldo Perdomo | SS | AZ | +4.62 | +3.15 | +0.90 | +0.57 | +2.90 |
| Freddie Freeman | 1B | LAD | +4.29 | +3.93 | +0.20 | +0.16 | +4.64 |
| Vladimir Guerrero Jr. | 1B/DH | TOR | +3.51 | +3.28 | +0.17 | +0.05 | +3.38 |
| Byron Buxton | CF | MIN | +3.34 | +2.52 | +1.14 | -0.32 | +2.48 |
| Jorge Polanco | 2B/DH | SEA | +2.90 | +3.11 | -0.18 | -0.03 | +3.15 |

### Hitters: bottom 10 total

| Player | Pos | Team | total | batting | baserunning | fielding | trad_bat |
|---|---|---|---|---|---|---|---|
| Nick Castellanos | RF | PHI | -4.20 | -2.57 | -0.33 | -1.30 | -2.71 |
| Alek Thomas | CF | AZ | -3.97 | -1.85 | -0.18 | -1.94 | -1.99 |
| Jordan Walker | RF | STL | -3.59 | -2.29 | +0.23 | -1.52 | -1.96 |
| Logan O'Hoppe | C/DH | LAA | -3.49 | -2.98 | -0.11 | -0.39 | -3.12 |
| Willi Castro | 2B/RF/LF/3B | MIN/CHC | -3.48 | -2.20 | +0.22 | -1.51 | -2.19 |
| JJ Bleday | CF/RF/LF/DH | ATH | -3.48 | -2.68 | -0.03 | -0.77 | -2.63 |
| Eric Wagaman | 1B/LF/DH | MIA | -3.32 | -2.49 | -0.38 | -0.44 | -2.81 |
| Angel Martínez | CF/2B | CLE | -3.15 | -1.51 | +0.13 | -1.76 | -1.72 |
| Lenyn Sosa | 2B/1B/DH | CWS | -3.09 | -2.90 | +0.34 | -0.54 | -2.70 |
| Matt McLain | 2B | CIN | -3.06 | -4.13 | +0.77 | +0.29 | -4.24 |

### Fielding: top 10

| Player | Pos | Team | fielding |
|---|---|---|---|
| Bobby Witt Jr. | SS | KC | +2.63 |
| Masyn Winn | SS | STL | +1.96 |
| Matt Chapman | 3B | SF | +1.79 |
| Pete Crow-Armstrong | CF | CHC | +1.54 |
| Ke'Bryan Hayes | 3B | PIT/CIN | +1.53 |
| Tommy Edman | 2B/CF/3B | LAD | +1.49 |
| Steven Kwan | LF | CLE | +1.43 |
| Ceddanne Rafaela | CF/2B | BOS | +1.39 |
| Josh Jung | 3B | TEX | +1.37 |
| José Ramírez | 3B/DH | CLE | +1.36 |

### Fielding: bottom 10

| Player | Pos | Team | fielding |
|---|---|---|---|
| Alek Thomas | CF | AZ | -1.94 |
| Jo Adell | CF/RF | LAA | -1.89 |
| Heliot Ramos | LF | SF | -1.80 |
| Angel Martínez | CF/2B | CLE | -1.76 |
| Ronald Acuña Jr. | RF | ATL | -1.72 |
| Gavin Lux | LF/2B/DH | CIN | -1.63 |
| Juan Soto | RF | NYM | -1.59 |
| Jordan Walker | RF | STL | -1.52 |
| Willi Castro | 2B/RF/LF/3B | MIN/CHC | -1.51 |
| Teoscar Hernández | RF | LAD | -1.49 |

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
| Garrett Crochet | P | BOS | +5.29 | +0.05 | +5.00 |
| Paul Skenes | P | PIT | +5.16 | -0.02 | +5.15 |
| Cristopher Sánchez | P | PHI | +4.92 | +0.14 | +4.65 |
| Tarik Skubal | P | DET | +3.66 | -0.15 | +4.24 |
| Cade Smith | P | CLE | +3.57 | -0.32 | +2.34 |
| Andrew Abbott | P | CIN | +3.55 | +0.02 | +2.74 |
| Yoshinobu Yamamoto | P | LAD | +3.49 | +0.10 | +4.09 |
| Jesús Luzardo | P | PHI | +3.37 | -0.09 | +1.69 |
| Zack Wheeler | P | PHI | +3.16 | +0.01 | +3.29 |
| Hunter Brown | P | HOU | +3.11 | +0.05 | +3.69 |

### Pitchers: bottom 10

| Player | Pos | Team | pitching | fielding | trad_pit |
|---|---|---|---|---|---|
| Germán Márquez | P | COL | -2.39 | +0.08 | -3.55 |
| Antonio Senzatela | P | COL | -2.16 | +0.38 | -2.95 |
| Tyler Alexander | P | CWS/MIL | -2.09 | +0.24 | -2.70 |
| Charlie Morton | P | BAL/DET/ATL | -2.00 | -0.04 | -2.35 |
| Jack Kochanowicz | P | LAA | -1.93 | -0.04 | -2.79 |
| Mitchell Parker | P | WSH | -1.65 | +0.02 | -1.78 |
| Bryce Miller | P | SEA | -1.56 | +0.01 | -1.27 |
| Jordan Hicks | P | SF/BOS | -1.56 | -0.02 | -2.21 |
| Tanner Gordon | P | COL | -1.48 | -0.01 | -1.54 |
| Jake Irvin | P | WSH | -1.48 | -0.02 | -2.81 |

### Pitchers hurt most by their defense (our pitching credit above traditional WPA: fielders took some blame)

| Player | Pos | Team | gap | pitching | trad_pit |
|---|---|---|---|---|---|
| Jesús Luzardo | P | PHI | +1.68 | +3.37 | +1.69 |
| Dylan Cease | P | SD | +1.68 | +0.80 | -0.87 |
| Eduardo Rodriguez | P | AZ | +1.56 | +0.17 | -1.39 |
| Kyle Hendricks | P | LAA | +1.43 | +0.98 | -0.45 |
| Kyle Freeland | P | COL | +1.41 | -0.15 | -1.56 |
| Andre Pallante | P | STL | +1.37 | -1.24 | -2.61 |
| Jake Irvin | P | WSH | +1.33 | -1.48 | -2.81 |
| Cade Smith | P | CLE | +1.23 | +3.57 | +2.34 |
| Tylor Megill | P | NYM | +1.16 | +0.60 | -0.56 |
| Germán Márquez | P | COL | +1.16 | -2.39 | -3.55 |

### Pitchers helped most by their defense (our pitching credit below traditional WPA: fielders took some credit)

| Player | Pos | Team | gap | pitching | trad_pit |
|---|---|---|---|---|---|
| Nathan Eovaldi | P | TEX | -1.52 | +2.61 | +4.13 |
| Noah Cameron | P | KC | -1.32 | +1.01 | +2.34 |
| Emerson Hancock | P | SEA | -1.20 | -0.96 | +0.23 |
| Edwin Uceta | P | TB | -1.20 | -0.17 | +1.02 |
| Seth Lugo | P | KC | -1.08 | -1.03 | +0.06 |
| Drew Rasmussen | P | TB | -1.08 | +1.77 | +2.85 |
| Grant Holmes | P | ATL | -1.01 | -0.62 | +0.39 |
| Nick Martinez | P | CIN | -0.95 | -0.71 | +0.24 |
| Brad Lord | P | WSH | -0.90 | -0.59 | +0.31 |
| Lucas Giolito | P | BOS | -0.88 | +0.52 | +1.40 |

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
- def / fielding: -55.2
- def / pitching: +229.0
- off / baserunning: +61.0
- off / batting: -227.9
- off / coaching: +1.8
