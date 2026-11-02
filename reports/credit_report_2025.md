# Credit report: 2025

## 1. Accounting identities (must hold exactly)

- Events: 189,735. Offense credits equal the event's change on 100.000%; defense credits equal minus the change on 100.000% (max gaps 4.44e-16 / 5.55e-16)
- Events with no credit rows: 0; events with no change in win probability (decided games): 7,061
- Teams whose total credit equals wins minus summed starting win probability: 30 of 30 (max gap 5.52e-15)
- Credit rows with no player (coaching buckets): 150,584; non-coaching rows with no player: 0

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
| TEX | 81 | 162 | +0.00 | +0.00 |
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
- Infield positioning credit by team (wins): STL -2.23, PHI -1.95, NYM -1.15, CLE -1.05, DET -0.98, HOU -0.95, BAL -0.71, CIN -0.67, CWS -0.66, COL -0.58, KC -0.40, SD -0.39, AZ -0.23, WSH -0.22, BOS -0.19, MIN -0.16, TOR +0.04, TEX +0.25, SF +0.32, LAA +0.39, ATH +0.48, MIA +0.59, MIL +0.75, NYY +0.83, ATL +0.95, LAD +1.20, CHC +1.23, PIT +1.25, TB +2.41, SEA +2.82

League fielding credit by position (wins): 1B -3.9, 2B -4.9, 3B +14.7, C -11.1, CF -7.2, LF -9.7, P -0.8, RF -29.2, SS +9.8

## 2b. Stolen-base defense vs Savant

- catcher stealing runs: 100 players; correlation of our steal-attempt credit (wins, leverage-weighted) with Savant's (runs): **0.788**
- pitcher running-game runs: 647 players; correlation of our steal-attempt credit (wins, leverage-weighted) with Savant's (runs): **0.471**

## 3. Leaderboards (eye test)

Wins added. Hitters 300+ PA, pitchers 300+ batters faced. `trad` = traditional WPA (batter / pitcher gets the whole play).

### Hitters: top 10 total

| Player | Pos | Team | total | batting | baserunning | fielding | trad_bat |
|---|---|---|---|---|---|---|---|
| Bobby Witt Jr. | SS | KC | +6.43 | +2.30 | +1.51 | +2.63 | +2.52 |
| Shohei Ohtani | P/DH | LAD | +6.16 | +4.63 | +0.67 | +0.06 | +4.92 |
| Aaron Judge | RF/DH | NYY | +5.59 | +5.17 | -0.02 | +0.43 | +5.11 |
| José Ramírez | 3B/DH | CLE | +5.46 | +2.86 | +1.17 | +1.44 | +3.14 |
| Fernando Tatis Jr. | RF | SD | +4.90 | +2.60 | +1.78 | +0.52 | +2.38 |
| Geraldo Perdomo | SS | AZ | +4.50 | +3.17 | +0.72 | +0.61 | +2.90 |
| Freddie Freeman | 1B | LAD | +4.29 | +3.88 | +0.25 | +0.16 | +4.64 |
| Vladimir Guerrero Jr. | 1B/DH | TOR | +3.55 | +3.27 | +0.24 | +0.04 | +3.38 |
| Byron Buxton | CF | MIN | +3.35 | +2.51 | +1.13 | -0.29 | +2.48 |
| Jorge Polanco | 2B/DH | SEA | +3.19 | +3.39 | -0.21 | +0.01 | +3.15 |

### Hitters: bottom 10 total

| Player | Pos | Team | total | batting | baserunning | fielding | trad_bat |
|---|---|---|---|---|---|---|---|
| Alek Thomas | CF | AZ | -3.95 | -1.77 | -0.21 | -1.97 | -1.99 |
| Nick Castellanos | RF | PHI | -3.93 | -2.57 | -0.31 | -1.05 | -2.71 |
| Jordan Walker | RF | STL | -3.68 | -2.28 | +0.22 | -1.63 | -1.96 |
| Logan O'Hoppe | C/DH | LAA | -3.57 | -2.99 | -0.19 | -0.39 | -3.12 |
| JJ Bleday | CF/RF/LF/DH | ATH | -3.50 | -2.80 | +0.08 | -0.78 | -2.63 |
| Willi Castro | 2B/RF/LF/3B | MIN/CHC | -3.43 | -2.20 | +0.22 | -1.46 | -2.19 |
| Eric Wagaman | 1B/LF/DH | MIA | -3.31 | -2.58 | -0.30 | -0.43 | -2.81 |
| Matt McLain | 2B | CIN | -3.21 | -4.13 | +0.61 | +0.31 | -4.24 |
| Lenyn Sosa | 2B/1B/DH | CWS | -3.05 | -2.90 | +0.34 | -0.49 | -2.70 |
| Angel Martínez | CF/2B | CLE | -2.97 | -1.50 | +0.13 | -1.59 | -1.72 |

### Fielding: top 10

| Player | Pos | Team | fielding |
|---|---|---|---|
| Bobby Witt Jr. | SS | KC | +2.63 |
| Masyn Winn | SS | STL | +1.95 |
| Steven Kwan | LF | CLE | +1.82 |
| Matt Chapman | 3B | SF | +1.78 |
| Ke'Bryan Hayes | 3B | PIT/CIN | +1.68 |
| Pete Crow-Armstrong | CF | CHC | +1.56 |
| Tommy Edman | 2B/CF/3B | LAD | +1.49 |
| Ceddanne Rafaela | CF/2B | BOS | +1.48 |
| José Ramírez | 3B/DH | CLE | +1.44 |
| Josh Jung | 3B | TEX | +1.40 |

### Fielding: bottom 10

| Player | Pos | Team | fielding |
|---|---|---|---|
| Alek Thomas | CF | AZ | -1.97 |
| Jo Adell | CF/RF | LAA | -1.89 |
| Ronald Acuña Jr. | RF | ATL | -1.70 |
| Heliot Ramos | LF | SF | -1.66 |
| Jordan Walker | RF | STL | -1.63 |
| Gavin Lux | LF/2B/DH | CIN | -1.61 |
| Angel Martínez | CF/2B | CLE | -1.59 |
| Teoscar Hernández | RF | LAD | -1.48 |
| Willi Castro | 2B/RF/LF/3B | MIN/CHC | -1.46 |
| Kyle Tucker | RF/DH | CHC | -1.33 |

### Baserunning: top 10

| Player | Pos | Team | baserunning |
|---|---|---|---|
| Fernando Tatis Jr. | RF | SD | +1.78 |
| Bobby Witt Jr. | SS | KC | +1.51 |
| José Ramírez | 3B/DH | CLE | +1.17 |
| Elly De La Cruz | SS | CIN | +1.15 |
| Byron Buxton | CF | MIN | +1.13 |
| Ceddanne Rafaela | CF/2B | BOS | +1.09 |
| Francisco Lindor | SS | NYM | +1.03 |
| CJ Abrams | SS | WSH | +1.02 |
| Chandler Simpson | CF/LF | TB | +0.99 |
| George Springer | RF/LF/CF/DH | TOR | +0.96 |

### Baserunning: bottom 10

| Player | Pos | Team | baserunning |
|---|---|---|---|
| Cal Raleigh | C/DH | SEA | -0.78 |
| Jonathan Aranda | 1B/DH | TB | -0.75 |
| Alexander Canario | LF/CF/RF | PIT | -0.71 |
| Ty France | 1B/DH | MIN/TOR | -0.61 |
| Vinnie Pasquantino | 1B/DH | KC | -0.60 |
| Rafael Devers | 1B/DH | SF/BOS | -0.60 |
| Drew Waters | LF/CF/RF | KC | -0.58 |
| Tyler Freeman | RF/2B/DH | COL | -0.55 |
| Romy Gonzalez | 1B/2B | BOS | -0.54 |
| James Wood | LF/DH | WSH | -0.51 |

### Pitchers: top 10

| Player | Pos | Team | pitching | fielding | trad_pit |
|---|---|---|---|---|---|
| Garrett Crochet | P | BOS | +5.20 | +0.05 | +5.00 |
| Paul Skenes | P | PIT | +5.01 | -0.02 | +5.15 |
| Cristopher Sánchez | P | PHI | +4.68 | +0.14 | +4.65 |
| Tarik Skubal | P | DET | +3.64 | -0.15 | +4.24 |
| Andrew Abbott | P | CIN | +3.50 | +0.02 | +2.74 |
| Cade Smith | P | CLE | +3.48 | -0.32 | +2.34 |
| Yoshinobu Yamamoto | P | LAD | +3.45 | +0.10 | +4.09 |
| Zack Wheeler | P | PHI | +3.12 | +0.01 | +3.29 |
| Hunter Brown | P | HOU | +3.12 | +0.05 | +3.69 |
| Jesús Luzardo | P | PHI | +2.99 | -0.09 | +1.69 |

### Pitchers: bottom 10

| Player | Pos | Team | pitching | fielding | trad_pit |
|---|---|---|---|---|---|
| Germán Márquez | P | COL | -2.40 | +0.08 | -3.55 |
| Tyler Alexander | P | CWS/MIL | -2.14 | +0.22 | -2.70 |
| Antonio Senzatela | P | COL | -2.06 | +0.39 | -2.95 |
| Charlie Morton | P | BAL/DET/ATL | -2.03 | -0.04 | -2.35 |
| Jack Kochanowicz | P | LAA | -1.92 | -0.04 | -2.79 |
| Jake Irvin | P | WSH | -1.83 | -0.01 | -2.81 |
| Chase Dollander | P | COL | -1.62 | -0.29 | -2.35 |
| Bryce Miller | P | SEA | -1.58 | +0.01 | -1.27 |
| Jordan Hicks | P | SF/BOS | -1.56 | -0.02 | -2.21 |
| Mitchell Parker | P | WSH | -1.48 | +0.02 | -1.78 |

### Pitchers hurt most by their defense (our pitching credit above traditional WPA: fielders took some blame)

| Player | Pos | Team | gap | pitching | trad_pit |
|---|---|---|---|---|---|
| Dylan Cease | P | SD | +1.66 | +0.78 | -0.87 |
| Kyle Hendricks | P | LAA | +1.46 | +1.01 | -0.45 |
| Andre Pallante | P | STL | +1.41 | -1.20 | -2.61 |
| Kyle Freeland | P | COL | +1.40 | -0.16 | -1.56 |
| Eduardo Rodriguez | P | AZ | +1.37 | -0.02 | -1.39 |
| Jesús Luzardo | P | PHI | +1.30 | +2.99 | +1.69 |
| Tylor Megill | P | NYM | +1.16 | +0.60 | -0.56 |
| Germán Márquez | P | COL | +1.15 | -2.40 | -3.55 |
| Cade Smith | P | CLE | +1.14 | +3.48 | +2.34 |
| Yusei Kikuchi | P | LAA | +1.06 | +1.17 | +0.11 |

### Pitchers helped most by their defense (our pitching credit below traditional WPA: fielders took some credit)

| Player | Pos | Team | gap | pitching | trad_pit |
|---|---|---|---|---|---|
| Nathan Eovaldi | P | TEX | -1.48 | +2.65 | +4.13 |
| Noah Cameron | P | KC | -1.36 | +0.98 | +2.34 |
| Drew Rasmussen | P | TB | -1.25 | +1.61 | +2.85 |
| Edwin Uceta | P | TB | -1.22 | -0.20 | +1.02 |
| Emerson Hancock | P | SEA | -1.16 | -0.93 | +0.23 |
| Grant Holmes | P | ATL | -1.11 | -0.72 | +0.39 |
| Nick Martinez | P | CIN | -1.09 | -0.85 | +0.24 |
| Seth Lugo | P | KC | -1.06 | -1.00 | +0.06 |
| Lucas Giolito | P | BOS | -0.94 | +0.46 | +1.40 |
| Brad Lord | P | WSH | -0.91 | -0.60 | +0.31 |

### Coaching (team)

| Team | bunt call | defensive indifference | intentional walk | positioning | total |
|---|---|---|---|---|---|
| SEA | +0.39 | +0.05 | -0.35 | +5.09 | +5.17 |
| TB | +0.20 | -0.02 | -0.09 | +3.52 | +3.60 |
| CHC | +0.08 | -0.01 | -0.08 | +2.38 | +2.38 |
| PIT | +0.23 | -0.00 | -0.27 | +1.83 | +1.80 |
| ATL | -0.01 | -0.01 | -0.35 | +1.49 | +1.12 |
| CIN | +0.04 | -0.00 | -0.08 | +0.84 | +0.80 |
| LAA | +0.08 | -0.02 | -0.58 | +1.32 | +0.80 |
| LAD | +0.08 | -0.04 | -0.38 | +0.56 | +0.21 |
| CWS | +0.12 | -0.04 | -0.38 | +0.32 | +0.02 |
| MIA | -0.05 | -0.00 | -0.24 | +0.23 | -0.06 |
| MIN | +0.02 | -0.04 | -0.30 | +0.24 | -0.07 |
| NYY | -0.03 | +0.03 | -0.07 | -0.22 | -0.28 |
| SF | +0.40 | -0.04 | -0.23 | -0.42 | -0.29 |
| TEX | +0.13 | -0.01 | -0.34 | -0.14 | -0.37 |
| HOU | +0.01 | -0.00 | -0.06 | -0.34 | -0.39 |
| MIL | +0.06 | -0.02 | -0.36 | -0.22 | -0.54 |
| SD | -0.05 | -0.01 | -0.34 | -0.22 | -0.62 |
| TOR | +0.11 | +0.00 | -0.55 | -0.23 | -0.67 |
| ATH | +0.07 | +0.00 | -0.27 | -0.52 | -0.72 |
| CLE | +0.02 | -0.01 | -0.15 | -0.64 | -0.78 |
| BOS | +0.11 | +0.00 | -0.16 | -0.77 | -0.82 |
| NYM | -0.05 | -0.00 | -0.11 | -0.81 | -0.97 |
| WSH | +0.03 | -0.02 | -0.02 | -0.98 | -0.99 |
| KC | +0.05 | -0.01 | -0.14 | -1.32 | -1.42 |
| STL | -0.04 | -0.01 | -0.16 | -1.22 | -1.43 |
| AZ | +0.13 | -0.01 | -0.29 | -1.32 | -1.49 |
| BAL | +0.08 | -0.01 | -0.17 | -1.44 | -1.53 |
| DET | -0.00 | -0.03 | -0.14 | -1.37 | -1.55 |
| COL | -0.03 | +0.00 | -0.17 | -3.00 | -3.21 |
| PHI | +0.01 | +0.00 | -0.16 | -3.54 | -3.69 |

### Bucket totals (league)

- def / coaching: -8.2
- def / fielding: -42.3
- def / pitching: +215.6
- off / baserunning: +55.6
- off / batting: -222.9
- off / coaching: +2.2
