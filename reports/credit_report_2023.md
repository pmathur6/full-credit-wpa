# Credit report: 2023

## 1. Accounting identities (must hold exactly)

- Events: 190,790. Offense credits equal the event's change on 100.000%; defense credits equal minus the change on 100.000% (max gaps 3.33e-16 / 4.44e-16)
- Events with no credit rows: 0; events with no change in win probability (decided games): 6,598
- Teams whose total credit equals wins minus summed starting win probability: 30 of 30 (max gap 7.11e-15)
- Credit rows with no player (coaching buckets): 149,258; non-coaching rows with no player: 0

| Team | W | G | Credited | Wins - starting WP |
|---|---|---|---|---|
| ATL | 104 | 162 | +23.00 | +23.00 |
| BAL | 101 | 162 | +20.00 | +20.00 |
| LAD | 100 | 162 | +19.00 | +19.00 |
| TB | 99 | 162 | +18.00 | +18.00 |
| MIL | 92 | 162 | +11.00 | +11.00 |
| HOU | 90 | 162 | +9.00 | +9.00 |
| PHI | 90 | 162 | +9.00 | +9.00 |
| TEX | 90 | 162 | +9.00 | +9.00 |
| TOR | 89 | 162 | +8.00 | +8.00 |
| SEA | 88 | 162 | +7.00 | +7.00 |
| MIN | 87 | 162 | +6.00 | +6.00 |
| MIA | 84 | 162 | +3.00 | +3.00 |
| AZ | 84 | 162 | +3.00 | +3.00 |
| CHC | 83 | 162 | +2.00 | +2.00 |
| SD | 82 | 162 | +1.00 | +1.00 |
| NYY | 82 | 162 | +1.00 | +1.00 |
| CIN | 82 | 162 | +1.00 | +1.00 |
| SF | 79 | 162 | -2.00 | -2.00 |
| BOS | 78 | 162 | -3.00 | -3.00 |
| DET | 78 | 162 | -3.00 | -3.00 |
| CLE | 76 | 162 | -5.00 | -5.00 |
| PIT | 76 | 162 | -5.00 | -5.00 |
| NYM | 75 | 162 | -6.00 | -6.00 |
| LAA | 73 | 162 | -8.00 | -8.00 |
| WSH | 71 | 162 | -10.00 | -10.00 |
| STL | 71 | 162 | -10.00 | -10.00 |
| CWS | 61 | 162 | -20.00 | -20.00 |
| COL | 59 | 162 | -22.00 | -22.00 |
| KC | 56 | 162 | -25.00 | -25.00 |
| OAK | 50 | 162 | -31.00 | -31.00 |

## 2. Outfield vs Savant OAA

- Outfield catch chances credited to the same fielder Savant names: 99.99%
- Outfielders (primary position LF/CF/RF) compared: 240; correlation of our outs-above-expected with Savant OAA: **0.968**; mean absolute difference 1.01 outs

Largest differences (Savant OAA includes direction/arm adjustments and other positions):

| Player | Savant OAA | Ours (outs - catch prob) |
|---|---|---|
| Willi Castro | +3 | -2.2 |
| Isiah Kiner-Falefa | +2 | -2.5 |
| Johan Rojas | +8 | +4.2 |
| Adolis García | +3 | -0.4 |
| Pavin Smith | -6 | -2.6 |
| Alek Thomas | +6 | +2.8 |
| Steven Kwan | +7 | +4.0 |
| Brandon Marsh | +7 | +4.1 |

## 2a. Infield vs Savant OAA

- Infielders (primary 1B/2B/3B/SS) compared: 318; correlation of our ground-ball outs-above-expected with Savant infield OAA: **0.511** (191 with 100+ chances: 0.499)
- Savant judges each fielder from where he actually stood; our model only knows the alignment type, so team positioning is still inside our fielders' numbers. Gap by team (ours - Savant, outs) shows it:

| Position | Players (100+) | Correlation |
|---|---|---|
| 1B | 32 | 0.649 |
| 2B | 62 | 0.445 |
| 3B | 45 | 0.605 |
| SS | 52 | 0.410 |

Gap by team (outs): KC -45, SF -37, COL -31, OAK -29, SEA -23, TEX -21, STL -21, PHI -21, AZ -20, LAA -10, DET -7, HOU -3, SD -1, CIN -1, NYM -1, CWS +4, CLE +7, WSH +13, PIT +13, MIN +15, TOR +17, TB +18, NYY +19, BOS +20, ATL +21, MIA +21, CHC +23, MIL +27, LAD +39, BAL +44

- After moving positioning to coaching, infielders' outs above expected match Savant OAA: correlation 1.000, max gap 0.30 outs
- Infield positioning credit by team (wins): KC -3.00, SF -2.59, COL -1.94, OAK -1.78, SEA -1.58, AZ -1.58, PHI -1.48, TEX -1.45, STL -1.32, LAA -0.82, DET -0.34, HOU -0.12, NYM -0.09, CWS -0.06, SD -0.04, CIN +0.04, CLE +0.26, PIT +0.64, BOS +0.76, MIN +0.92, WSH +0.97, NYY +1.09, TB +1.17, TOR +1.40, ATL +1.44, CHC +1.47, MIA +1.90, MIL +2.18, LAD +3.34, BAL +3.36

League fielding credit by position (wins): 1B -9.8, 2B -5.3, 3B +16.7, C -16.0, CF -12.5, LF -12.0, P +1.9, RF -24.3, SS +6.1

## 2b. Stolen-base defense vs Savant

- catcher stealing runs: 98 players; correlation of our steal-attempt credit (wins, leverage-weighted) with Savant's (runs): **0.795**
- pitcher running-game runs: 655 players; correlation of our steal-attempt credit (wins, leverage-weighted) with Savant's (runs): **0.573**

## 3. Leaderboards (eye test)

Wins added. Hitters 300+ PA, pitchers 300+ batters faced. `trad` = traditional WPA (batter / pitcher gets the whole play).

### Hitters: top 10 total

| Player | Pos | Team | total | batting | baserunning | fielding | trad_bat |
|---|---|---|---|---|---|---|---|
| Shohei Ohtani | P/DH | LAA | +6.15 | +4.17 | +0.60 | -0.08 | +4.13 |
| Corbin Carroll | LF/RF/CF | AZ | +6.10 | +4.24 | +1.93 | -0.08 | +3.84 |
| Ronald Acuña Jr. | RF | ATL | +5.91 | +5.36 | +1.53 | -0.99 | +5.69 |
| Mookie Betts | RF/2B/SS | LAD | +5.28 | +5.09 | +0.21 | -0.03 | +5.07 |
| Bryce Harper | 1B/DH | PHI | +5.23 | +5.23 | +0.09 | -0.08 | +5.79 |
| TJ Friedl | CF/LF | CIN | +5.04 | +3.57 | +1.34 | +0.12 | +3.37 |
| Kyle Tucker | RF | HOU | +4.69 | +4.37 | +0.96 | -0.64 | +4.23 |
| José Ramírez | 3B/DH | CLE | +4.35 | +2.32 | +1.16 | +0.87 | +2.60 |
| Corey Seager | SS | TEX | +4.13 | +4.33 | -0.18 | -0.02 | +4.41 |
| Yordan Alvarez | LF/DH | HOU | +4.05 | +4.09 | -0.08 | +0.04 | +4.30 |

### Hitters: bottom 10 total

| Player | Pos | Team | total | batting | baserunning | fielding | trad_bat |
|---|---|---|---|---|---|---|---|
| Myles Straw | CF | CLE | -4.56 | -4.40 | +0.69 | -0.86 | -4.27 |
| Tim Anderson | SS | CWS | -3.76 | -3.87 | +0.34 | -0.23 | -4.24 |
| Martín Maldonado | C | HOU | -3.44 | -2.95 | -0.06 | -0.42 | -2.97 |
| Yasmani Grandal | C/DH | CWS | -3.37 | -2.08 | -0.42 | -0.86 | -2.24 |
| Ty France | 1B | SEA | -3.08 | -2.24 | -0.06 | -0.78 | -2.20 |
| Teoscar Hernández | RF/DH | SEA | -3.01 | -1.68 | +0.16 | -1.49 | -1.96 |
| Alejandro Kirk | C/DH | TOR | -2.96 | -2.52 | -0.36 | -0.09 | -2.39 |
| Enrique Hernández | SS/2B/CF/3B/LF/1B | BOS/LAD | -2.89 | -1.21 | +0.33 | -2.01 | -0.71 |
| Alec Burleson | LF/1B/RF/DH | STL | -2.78 | -2.21 | +0.26 | -0.83 | -1.51 |
| Jurickson Profar | LF/DH | COL/SD | -2.70 | -0.64 | -0.17 | -1.88 | -0.56 |

### Fielding: top 10

| Player | Pos | Team | fielding |
|---|---|---|---|
| Eugenio Suárez | 3B | SEA | +1.99 |
| Francisco Lindor | SS | NYM | +1.76 |
| Ke'Bryan Hayes | 3B | PIT | +1.69 |
| Maikel Garcia | 3B/SS | KC | +1.57 |
| J.D. Davis | 3B/1B/DH | SF | +1.34 |
| Dansby Swanson | SS | CHC | +1.21 |
| Nicky Lopez | 2B/3B/SS | KC/ATL | +1.18 |
| Nolan Arenado | 3B/DH | STL | +1.14 |
| Zach McKinstry | 3B/2B/RF/SS/LF | DET | +1.12 |
| Daulton Varsho | LF/CF | TOR | +1.11 |

### Fielding: bottom 10

| Player | Pos | Team | fielding |
|---|---|---|---|
| Enrique Hernández | SS/2B/CF/3B/LF/1B | BOS/LAD | -2.01 |
| Kyle Schwarber | LF/DH | PHI | -1.92 |
| Jurickson Profar | LF/DH | COL/SD | -1.88 |
| Luis Arraez | 2B/1B | MIA | -1.73 |
| Seiya Suzuki | RF | CHC | -1.64 |
| Lane Thomas | RF/CF | WSH | -1.61 |
| Keibert Ruiz | C/DH | WSH | -1.58 |
| Teoscar Hernández | RF/DH | SEA | -1.49 |
| MJ Melendez | RF/LF/C/DH | KC | -1.46 |
| Jordan Walker | RF/LF | STL | -1.42 |

### Baserunning: top 10

| Player | Pos | Team | baserunning |
|---|---|---|---|
| Corbin Carroll | LF/RF/CF | AZ | +1.93 |
| Ronald Acuña Jr. | RF | ATL | +1.53 |
| TJ Friedl | CF/LF | CIN | +1.34 |
| Jorge Mateo | SS | BAL | +1.23 |
| José Ramírez | 3B/DH | CLE | +1.16 |
| Willi Castro | LF/CF/3B/2B | MIN | +1.13 |
| Christian Yelich | LF/DH | MIL | +1.01 |
| Ozzie Albies | 2B | ATL | +0.96 |
| Kyle Tucker | RF | HOU | +0.96 |
| Andrés Giménez | 2B | CLE | +0.94 |

### Baserunning: bottom 10

| Player | Pos | Team | baserunning |
|---|---|---|---|
| Vladimir Guerrero Jr. | 1B/DH | TOR | -0.62 |
| Keibert Ruiz | C/DH | WSH | -0.60 |
| Andrew Vaughn | 1B | CWS | -0.54 |
| Brandon Drury | 2B/1B | LAA | -0.53 |
| Nathaniel Lowe | 1B | TEX | -0.51 |
| Juan Soto | LF | SD | -0.51 |
| Alec Bohm | 3B/1B | PHI | -0.44 |
| Daniel Vogelbach | DH | NYM | -0.43 |
| Yasmani Grandal | C/DH | CWS | -0.42 |
| Willson Contreras | C/DH | STL | -0.39 |

### Pitchers: top 10

| Player | Pos | Team | pitching | fielding | trad_pit |
|---|---|---|---|---|---|
| Tanner Scott | P | MIA | +4.23 | +0.07 | +4.70 |
| Gerrit Cole | P | NYY | +4.11 | +0.05 | +4.53 |
| Blake Snell | P | SD | +3.35 | -0.05 | +4.21 |
| Sonny Gray | P | MIN | +2.86 | +0.09 | +3.06 |
| Kevin Gausman | P | TOR | +2.73 | +0.08 | +2.22 |
| Kodai Senga | P | NYM | +2.58 | +0.03 | +2.70 |
| Zac Gallen | P | AZ | +2.49 | -0.13 | +2.77 |
| George Kirby | P | SEA | +2.44 | +0.16 | +2.82 |
| Justin Verlander | P | NYM/HOU | +2.28 | +0.04 | +1.86 |
| Tarik Skubal | P | DET | +2.27 | -0.03 | +1.40 |

### Pitchers: bottom 10

| Player | Pos | Team | pitching | fielding | trad_pit |
|---|---|---|---|---|---|
| Adam Wainwright | P | STL | -2.90 | +0.01 | -2.80 |
| Jordan Lyles | P | KC | -2.62 | -0.08 | -3.49 |
| Chris Flexen | P | COL/SEA | -2.48 | +0.03 | -2.41 |
| Luke Weaver | P | CIN/SEA/NYY | -2.45 | -0.08 | -3.15 |
| Noah Syndergaard | P | LAD/CLE | -2.43 | +0.09 | -2.35 |
| Joey Wentz | P | DET | -2.15 | -0.01 | -2.52 |
| Trevor Williams | P | WSH | -1.99 | +0.09 | -2.65 |
| Austin Gomber | P | COL | -1.91 | +0.09 | -1.28 |
| Kyle Muller | P | OAK | -1.90 | -0.14 | -2.33 |
| Carlos Carrasco | P | NYM | -1.84 | -0.10 | -2.22 |

### Pitchers hurt most by their defense (our pitching credit above traditional WPA: fielders took some blame)

| Player | Pos | Team | gap | pitching | trad_pit |
|---|---|---|---|---|---|
| Emmanuel Clase | P | CLE | +3.09 | +1.32 | -1.77 |
| Aaron Nola | P | PHI | +1.60 | +1.92 | +0.32 |
| Ian Gibaut | P | CIN | +1.42 | +1.36 | -0.06 |
| Patrick Sandoval | P | LAA | +1.40 | +0.18 | -1.22 |
| Jake Bird | P | COL | +1.30 | -0.57 | -1.88 |
| Drew Smyly | P | CHC | +1.24 | -0.79 | -2.02 |
| Josh Winckowski | P | BOS | +1.20 | +0.87 | -0.34 |
| Lucas Giolito | P | CWS/LAA/CLE | +1.06 | -0.77 | -1.83 |
| Jack Flaherty | P | STL/BAL | +1.02 | +0.11 | -0.91 |
| Clarke Schmidt | P | NYY | +1.01 | -0.45 | -1.46 |

### Pitchers helped most by their defense (our pitching credit below traditional WPA: fielders took some credit)

| Player | Pos | Team | gap | pitching | trad_pit |
|---|---|---|---|---|---|
| Framber Valdez | P | HOU | -1.74 | +0.41 | +2.15 |
| Kyle Bradish | P | BAL | -1.26 | +1.37 | +2.63 |
| José Berríos | P | TOR | -1.18 | +0.07 | +1.25 |
| Merrill Kelly | P | AZ | -1.13 | +0.78 | +1.91 |
| Colin Rea | P | MIL | -1.10 | -1.32 | -0.22 |
| Chris Bassitt | P | TOR | -1.03 | +0.44 | +1.47 |
| Braxton Garrett | P | MIA | -1.03 | +1.01 | +2.04 |
| Dean Kremer | P | BAL | -1.01 | -0.11 | +0.90 |
| Justin Steele | P | CHC | -0.94 | +1.56 | +2.50 |
| Bryce Miller | P | SEA | -0.89 | +0.18 | +1.07 |

### Coaching (team)

| Team | bunt call | defensive indifference | intentional walk | positioning | total |
|---|---|---|---|---|---|
| BAL | +0.01 | +0.00 | -0.23 | +5.73 | +5.51 |
| CHC | +0.15 | -0.01 | -0.06 | +3.05 | +3.14 |
| LAD | -0.01 | -0.02 | -0.20 | +3.03 | +2.80 |
| TB | +0.04 | -0.01 | -0.06 | +2.54 | +2.51 |
| MIL | -0.07 | +0.00 | -0.15 | +2.66 | +2.45 |
| PIT | -0.19 | -0.00 | -0.19 | +1.67 | +1.29 |
| BOS | -0.03 | -0.01 | -0.15 | +1.32 | +1.14 |
| WSH | -0.02 | -0.00 | -0.37 | +1.53 | +1.14 |
| TOR | +0.01 | +0.01 | -0.45 | +1.25 | +0.83 |
| ATL | -0.01 | -0.02 | -0.18 | +1.01 | +0.80 |
| NYY | -0.00 | -0.02 | -0.14 | +0.96 | +0.80 |
| MIN | +0.14 | -0.00 | -0.21 | +0.81 | +0.73 |
| DET | +0.06 | -0.01 | -0.06 | +0.52 | +0.51 |
| MIA | -0.18 | -0.01 | -0.20 | +0.85 | +0.45 |
| CWS | +0.04 | +0.00 | -0.18 | +0.29 | +0.16 |
| CLE | -0.05 | -0.01 | -0.05 | -0.26 | -0.38 |
| HOU | +0.03 | +0.06 | -0.04 | -0.53 | -0.49 |
| SD | +0.05 | -0.02 | -0.14 | -0.38 | -0.49 |
| CIN | -0.12 | -0.03 | -0.12 | -0.41 | -0.68 |
| SEA | +0.08 | +0.01 | -0.46 | -0.45 | -0.82 |
| NYM | -0.13 | -0.00 | -0.19 | -0.95 | -1.27 |
| PHI | -0.03 | -0.01 | -0.06 | -1.30 | -1.39 |
| AZ | -0.04 | -0.02 | -0.19 | -1.38 | -1.63 |
| COL | -0.10 | -0.01 | -0.21 | -2.09 | -2.42 |
| OAK | -0.23 | +0.00 | -0.43 | -2.32 | -2.97 |
| LAA | -0.09 | -0.02 | -0.65 | -2.32 | -3.08 |
| STL | +0.03 | +0.01 | -0.06 | -3.54 | -3.56 |
| TEX | +0.05 | +0.00 | -0.30 | -3.33 | -3.58 |
| SF | +0.05 | -0.02 | -0.29 | -3.36 | -3.61 |
| KC | +0.08 | -0.00 | -0.04 | -4.54 | -4.50 |

### Bucket totals (league)

- def / coaching: -6.1
- def / fielding: -55.2
- def / pitching: +93.5
- off / baserunning: +73.0
- off / batting: -104.8
- off / coaching: -0.5
