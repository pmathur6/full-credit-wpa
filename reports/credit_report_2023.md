# Credit report: 2023

## 1. Accounting identities (must hold exactly)

- Events: 190,790. Offense credits equal the event's change on 100.000%; defense credits equal minus the change on 100.000% (max gaps 3.33e-16 / 3.33e-16)
- Events with no credit rows: 0; events with no change in win probability (decided games): 6,598
- Teams whose total credit equals wins minus summed starting win probability: 30 of 30 (max gap 5.33e-15)
- Credit rows with no player (coaching buckets): 149,468; non-coaching rows with no player: 0

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
- Infield positioning credit by team (wins): KC -2.99, SF -2.58, COL -1.94, OAK -1.77, AZ -1.58, SEA -1.58, PHI -1.47, TEX -1.44, STL -1.30, LAA -0.82, DET -0.34, HOU -0.12, NYM -0.08, CWS -0.06, SD -0.04, CIN +0.05, CLE +0.25, PIT +0.64, BOS +0.76, MIN +0.91, WSH +0.95, NYY +1.09, TB +1.16, TOR +1.40, CHC +1.45, ATL +1.45, MIA +1.90, MIL +2.18, LAD +3.31, BAL +3.33

League fielding credit by position (wins): 1B -9.7, 2B -5.5, 3B +15.8, C -16.0, CF -15.1, LF -14.9, P +1.6, RF -26.7, SS +5.5

## 2b. Stolen-base defense vs Savant

- catcher stealing runs: 98 players; correlation of our steal-attempt credit (wins, leverage-weighted) with Savant's (runs): **0.795**
- pitcher running-game runs: 655 players; correlation of our steal-attempt credit (wins, leverage-weighted) with Savant's (runs): **0.573**

## 3. Leaderboards (eye test)

Wins added. Hitters 300+ PA, pitchers 300+ batters faced. `trad` = traditional WPA (batter / pitcher gets the whole play).

### Hitters: top 10 total

| Player | Pos | Team | total | batting | baserunning | fielding | trad_bat |
|---|---|---|---|---|---|---|---|
| Shohei Ohtani | P/DH | LAA | +6.17 | +4.17 | +0.60 | -0.08 | +4.13 |
| Corbin Carroll | LF/RF/CF | AZ | +6.04 | +4.23 | +1.94 | -0.13 | +3.84 |
| Ronald Acuña Jr. | RF | ATL | +5.79 | +5.32 | +1.53 | -1.07 | +5.69 |
| Mookie Betts | RF/2B/SS | LAD | +5.31 | +5.02 | +0.33 | -0.04 | +5.07 |
| Bryce Harper | 1B/DH | PHI | +5.25 | +5.24 | +0.09 | -0.08 | +5.79 |
| TJ Friedl | CF/LF | CIN | +4.78 | +3.46 | +1.40 | -0.07 | +3.37 |
| Kyle Tucker | RF | HOU | +4.50 | +4.37 | +0.95 | -0.82 | +4.23 |
| José Ramírez | 3B/DH | CLE | +4.34 | +2.33 | +1.18 | +0.84 | +2.60 |
| Yordan Alvarez | LF/DH | HOU | +4.06 | +4.10 | -0.07 | +0.04 | +4.30 |
| Matt Olson | 1B | ATL | +3.82 | +4.26 | +0.65 | -1.09 | +4.58 |

### Hitters: bottom 10 total

| Player | Pos | Team | total | batting | baserunning | fielding | trad_bat |
|---|---|---|---|---|---|---|---|
| Myles Straw | CF | CLE | -5.02 | -4.40 | +0.72 | -1.34 | -4.27 |
| Tim Anderson | SS | CWS | -3.85 | -3.96 | +0.35 | -0.23 | -4.24 |
| Yasmani Grandal | C/DH | CWS | -3.57 | -2.32 | -0.39 | -0.86 | -2.24 |
| Martín Maldonado | C | HOU | -3.45 | -2.96 | -0.06 | -0.42 | -2.97 |
| Ty France | 1B | SEA | -3.10 | -2.27 | -0.07 | -0.77 | -2.20 |
| Teoscar Hernández | RF/DH | SEA | -3.06 | -1.68 | +0.16 | -1.54 | -1.96 |
| Alejandro Kirk | C/DH | TOR | -3.02 | -2.56 | -0.37 | -0.08 | -2.39 |
| Jurickson Profar | LF/DH | COL/SD | -2.96 | -0.63 | -0.17 | -2.16 | -0.56 |
| Christian Vázquez | C | MIN | -2.68 | -2.28 | -0.29 | -0.10 | -2.57 |
| Alec Burleson | LF/1B/RF/DH | STL | -2.66 | -2.22 | +0.26 | -0.70 | -1.51 |

### Fielding: top 10

| Player | Pos | Team | fielding |
|---|---|---|---|
| Eugenio Suárez | 3B | SEA | +1.93 |
| Francisco Lindor | SS | NYM | +1.74 |
| Ke'Bryan Hayes | 3B | PIT | +1.71 |
| Maikel Garcia | 3B/SS | KC | +1.58 |
| J.D. Davis | 3B/1B/DH | SF | +1.34 |
| Dansby Swanson | SS | CHC | +1.22 |
| Nicky Lopez | 2B/3B/SS | KC/ATL | +1.19 |
| Nolan Arenado | 3B/DH | STL | +1.11 |
| Zach McKinstry | 3B/2B/RF/SS/LF | DET | +1.11 |
| Brenton Doyle | CF | COL | +1.11 |

### Fielding: bottom 10

| Player | Pos | Team | fielding |
|---|---|---|---|
| Jurickson Profar | LF/DH | COL/SD | -2.16 |
| Enrique Hernández | SS/2B/CF/3B/LF/1B | BOS/LAD | -2.01 |
| Kyle Schwarber | LF/DH | PHI | -1.98 |
| Luis Arraez | 2B/1B | MIA | -1.71 |
| Seiya Suzuki | RF | CHC | -1.65 |
| Keibert Ruiz | C/DH | WSH | -1.58 |
| Lane Thomas | RF/CF | WSH | -1.57 |
| Bryan De La Cruz | LF/RF | MIA | -1.57 |
| Teoscar Hernández | RF/DH | SEA | -1.54 |
| Jordan Walker | RF/LF | STL | -1.52 |

### Baserunning: top 10

| Player | Pos | Team | baserunning |
|---|---|---|---|
| Corbin Carroll | LF/RF/CF | AZ | +1.94 |
| Ronald Acuña Jr. | RF | ATL | +1.53 |
| TJ Friedl | CF/LF | CIN | +1.40 |
| Jorge Mateo | SS | BAL | +1.23 |
| José Ramírez | 3B/DH | CLE | +1.18 |
| Willi Castro | LF/CF/3B/2B | MIN | +1.15 |
| Christian Yelich | LF/DH | MIL | +1.01 |
| Francisco Lindor | SS | NYM | +0.98 |
| Kyle Tucker | RF | HOU | +0.95 |
| Ozzie Albies | 2B | ATL | +0.95 |

### Baserunning: bottom 10

| Player | Pos | Team | baserunning |
|---|---|---|---|
| Vladimir Guerrero Jr. | 1B/DH | TOR | -0.64 |
| Keibert Ruiz | C/DH | WSH | -0.59 |
| Andrew Vaughn | 1B | CWS | -0.55 |
| Nathaniel Lowe | 1B | TEX | -0.53 |
| Juan Soto | LF | SD | -0.52 |
| Brandon Drury | 2B/1B | LAA | -0.50 |
| Rob Refsnyder | LF/CF/DH | BOS | -0.46 |
| Alec Bohm | 3B/1B | PHI | -0.46 |
| Daniel Vogelbach | DH | NYM | -0.43 |
| Yasmani Grandal | C/DH | CWS | -0.39 |

### Pitchers: top 10

| Player | Pos | Team | pitching | fielding | trad_pit |
|---|---|---|---|---|---|
| Tanner Scott | P | MIA | +4.28 | +0.07 | +4.70 |
| Gerrit Cole | P | NYY | +4.11 | +0.05 | +4.53 |
| Blake Snell | P | SD | +3.37 | -0.05 | +4.21 |
| Sonny Gray | P | MIN | +2.89 | +0.09 | +3.06 |
| Kevin Gausman | P | TOR | +2.85 | +0.08 | +2.22 |
| Zac Gallen | P | AZ | +2.58 | -0.13 | +2.77 |
| Kodai Senga | P | NYM | +2.55 | +0.03 | +2.70 |
| George Kirby | P | SEA | +2.46 | +0.16 | +2.82 |
| Justin Verlander | P | NYM/HOU | +2.43 | +0.04 | +1.86 |
| Zach Eflin | P | TB | +2.31 | -0.03 | +1.93 |

### Pitchers: bottom 10

| Player | Pos | Team | pitching | fielding | trad_pit |
|---|---|---|---|---|---|
| Adam Wainwright | P | STL | -2.92 | +0.01 | -2.80 |
| Jordan Lyles | P | KC | -2.53 | -0.09 | -3.49 |
| Luke Weaver | P | CIN/SEA/NYY | -2.47 | -0.08 | -3.15 |
| Noah Syndergaard | P | LAD/CLE | -2.43 | +0.09 | -2.35 |
| Chris Flexen | P | COL/SEA | -2.35 | +0.03 | -2.41 |
| Joey Wentz | P | DET | -2.16 | -0.01 | -2.52 |
| Trevor Williams | P | WSH | -2.00 | +0.09 | -2.65 |
| Austin Gomber | P | COL | -1.97 | +0.09 | -1.28 |
| Zach Davies | P | AZ | -1.85 | +0.10 | -1.90 |
| Carlos Hernández | P | KC | -1.81 | +0.05 | -2.55 |

### Pitchers hurt most by their defense (our pitching credit above traditional WPA: fielders took some blame)

| Player | Pos | Team | gap | pitching | trad_pit |
|---|---|---|---|---|---|
| Emmanuel Clase | P | CLE | +3.20 | +1.43 | -1.77 |
| Ian Gibaut | P | CIN | +1.73 | +1.67 | -0.06 |
| Aaron Nola | P | PHI | +1.72 | +2.04 | +0.32 |
| Patrick Sandoval | P | LAA | +1.48 | +0.26 | -1.22 |
| Jake Bird | P | COL | +1.31 | -0.56 | -1.88 |
| Drew Smyly | P | CHC | +1.25 | -0.77 | -2.02 |
| Josh Winckowski | P | BOS | +1.23 | +0.89 | -0.34 |
| Jack Flaherty | P | STL/BAL | +1.10 | +0.19 | -0.91 |
| Rich Hill | P | PIT/SD | +1.09 | -1.48 | -2.57 |
| Tyler Anderson | P | LAA | +1.05 | -0.78 | -1.82 |

### Pitchers helped most by their defense (our pitching credit below traditional WPA: fielders took some credit)

| Player | Pos | Team | gap | pitching | trad_pit |
|---|---|---|---|---|---|
| Framber Valdez | P | HOU | -1.61 | +0.54 | +2.15 |
| Kyle Bradish | P | BAL | -1.21 | +1.43 | +2.63 |
| José Berríos | P | TOR | -1.12 | +0.12 | +1.25 |
| Merrill Kelly | P | AZ | -1.11 | +0.80 | +1.91 |
| Colin Rea | P | MIL | -1.08 | -1.30 | -0.22 |
| Chris Bassitt | P | TOR | -1.00 | +0.47 | +1.47 |
| Dean Kremer | P | BAL | -0.96 | -0.06 | +0.90 |
| Ty Blach | P | COL | -0.90 | -1.80 | -0.90 |
| Braxton Garrett | P | MIA | -0.86 | +1.17 | +2.04 |
| Freddy Peralta | P | MIL | -0.85 | +0.69 | +1.53 |

### Coaching (team)

| Team | bunt call | defensive indifference | intentional walk | positioning | total |
|---|---|---|---|---|---|
| BAL | +0.01 | +0.00 | -0.23 | +5.76 | +5.55 |
| CHC | +0.15 | -0.01 | -0.06 | +2.98 | +3.07 |
| LAD | -0.01 | -0.02 | -0.20 | +2.99 | +2.76 |
| TB | +0.04 | -0.01 | -0.06 | +2.53 | +2.50 |
| MIL | -0.07 | +0.00 | -0.15 | +2.61 | +2.39 |
| PIT | -0.19 | -0.00 | -0.19 | +1.64 | +1.26 |
| BOS | -0.03 | -0.01 | -0.15 | +1.37 | +1.18 |
| WSH | -0.02 | -0.00 | -0.37 | +1.44 | +1.05 |
| NYY | -0.01 | -0.02 | -0.14 | +1.09 | +0.92 |
| TOR | +0.01 | +0.01 | -0.45 | +1.18 | +0.75 |
| MIN | +0.14 | -0.00 | -0.21 | +0.78 | +0.70 |
| ATL | -0.01 | -0.02 | -0.18 | +0.90 | +0.69 |
| DET | +0.06 | -0.01 | -0.06 | +0.54 | +0.54 |
| MIA | -0.18 | -0.01 | -0.20 | +0.75 | +0.35 |
| CWS | +0.04 | +0.00 | -0.18 | +0.30 | +0.17 |
| CLE | -0.05 | -0.01 | -0.05 | -0.30 | -0.41 |
| SD | +0.05 | -0.02 | -0.14 | -0.44 | -0.55 |
| HOU | +0.03 | +0.06 | -0.04 | -0.66 | -0.62 |
| CIN | -0.11 | -0.03 | -0.12 | -0.46 | -0.72 |
| SEA | +0.08 | +0.01 | -0.46 | -0.49 | -0.86 |
| NYM | -0.13 | -0.00 | -0.19 | -0.98 | -1.30 |
| PHI | -0.03 | -0.01 | -0.06 | -1.42 | -1.51 |
| AZ | -0.05 | -0.02 | -0.19 | -1.34 | -1.60 |
| COL | -0.10 | -0.01 | -0.21 | -1.93 | -2.25 |
| OAK | -0.22 | +0.00 | -0.43 | -2.37 | -3.02 |
| LAA | -0.09 | -0.02 | -0.65 | -2.40 | -3.16 |
| STL | +0.03 | +0.01 | -0.06 | -3.47 | -3.49 |
| SF | +0.06 | -0.02 | -0.29 | -3.37 | -3.62 |
| TEX | +0.05 | +0.00 | -0.30 | -3.44 | -3.68 |
| KC | +0.08 | -0.00 | -0.04 | -4.53 | -4.48 |

### Bucket totals (league)

- def / coaching: -6.9
- def / fielding: -65.1
- def / pitching: +104.2
- off / baserunning: +79.3
- off / batting: -111.1
- off / coaching: -0.5
