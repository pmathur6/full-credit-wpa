# Credit report: 2024

## 1. Accounting identities (must hold exactly)

- Events: 189,366. Offense credits equal the event's change on 100.000%; defense credits equal minus the change on 100.000% (max gaps 5.55e-16 / 5.55e-16)
- Events with no credit rows: 0; events with no change in win probability (decided games): 6,497
- Teams whose total credit equals wins minus summed starting win probability: 30 of 30 (max gap 4.32e-15)
- Credit rows with no player (coaching buckets): 150,287; non-coaching rows with no player: 0

| Team | W | G | Credited | Wins - starting WP |
|---|---|---|---|---|
| LAD | 98 | 162 | +17.00 | +17.00 |
| PHI | 95 | 162 | +14.00 | +14.00 |
| NYY | 94 | 162 | +13.00 | +13.00 |
| MIL | 93 | 162 | +12.00 | +12.00 |
| SD | 93 | 162 | +12.00 | +12.00 |
| CLE | 92 | 161 | +11.50 | +11.50 |
| BAL | 91 | 162 | +10.00 | +10.00 |
| ATL | 89 | 162 | +8.00 | +8.00 |
| AZ | 89 | 162 | +8.00 | +8.00 |
| NYM | 89 | 162 | +8.00 | +8.00 |
| HOU | 88 | 161 | +7.50 | +7.50 |
| KC | 86 | 162 | +5.00 | +5.00 |
| DET | 86 | 162 | +5.00 | +5.00 |
| SEA | 85 | 162 | +4.00 | +4.00 |
| STL | 83 | 162 | +2.00 | +2.00 |
| CHC | 83 | 162 | +2.00 | +2.00 |
| MIN | 82 | 162 | +1.00 | +1.00 |
| BOS | 81 | 162 | +0.00 | +0.00 |
| TB | 80 | 162 | -1.00 | -1.00 |
| SF | 80 | 162 | -1.00 | -1.00 |
| TEX | 78 | 162 | -3.00 | -3.00 |
| CIN | 77 | 162 | -4.00 | -4.00 |
| PIT | 76 | 162 | -5.00 | -5.00 |
| TOR | 74 | 162 | -7.00 | -7.00 |
| WSH | 71 | 162 | -10.00 | -10.00 |
| OAK | 69 | 162 | -12.00 | -12.00 |
| LAA | 63 | 162 | -18.00 | -18.00 |
| MIA | 62 | 162 | -19.00 | -19.00 |
| COL | 61 | 162 | -20.00 | -20.00 |
| CWS | 41 | 162 | -40.00 | -40.00 |

## 2. Outfield vs Savant OAA

- Outfield catch chances credited to the same fielder Savant names: 99.99%
- Outfielders (primary position LF/CF/RF) compared: 234; correlation of our outs-above-expected with Savant OAA: **0.976**; mean absolute difference 0.99 outs

Largest differences (Savant OAA includes direction/arm adjustments and other positions):

| Player | Savant OAA | Ours (outs - catch prob) |
|---|---|---|
| Jazz Chisholm Jr. | +9 | +0.1 |
| Mauricio Dubón | +10 | +4.2 |
| Alex Verdugo | +1 | -3.1 |
| Steven Kwan | +5 | +1.6 |
| Garrett Hampson | +8 | +5.2 |
| Daulton Varsho | +15 | +12.3 |
| Cody Bellinger | +0 | -2.7 |
| Teoscar Hernández | -9 | -11.7 |

## 2a. Infield vs Savant OAA

- Infielders (primary 1B/2B/3B/SS) compared: 317; correlation of our ground-ball outs-above-expected with Savant infield OAA: **0.555** (188 with 100+ chances: 0.549)
- Savant judges each fielder from where he actually stood; our model only knows the alignment type, so team positioning is still inside our fielders' numbers. Gap by team (ours - Savant, outs) shows it:

| Position | Players (100+) | Correlation |
|---|---|---|
| 1B | 31 | 0.745 |
| 2B | 53 | 0.621 |
| 3B | 54 | 0.669 |
| SS | 50 | 0.339 |

Gap by team (outs): KC -29, DET -21, SF -19, MIN -17, CIN -15, CWS -14, AZ -13, SD -13, NYY -10, PHI -10, STL -10, MIA -9, PIT -7, CLE -1, CHC -0, OAK -0, TEX +0, BAL +1, HOU +3, MIL +4, ATL +5, NYM +6, TOR +11, COL +13, LAD +14, WSH +14, BOS +21, TB +23, LAA +33, SEA +36

- After moving positioning to coaching, infielders' outs above expected match Savant OAA: correlation 1.000, max gap 0.80 outs
- Infield positioning credit by team (wins): KC -2.29, DET -1.37, MIN -1.28, SF -1.23, SD -1.22, CIN -0.92, STL -0.87, AZ -0.84, PHI -0.84, NYY -0.63, CWS -0.62, MIA -0.44, PIT -0.30, CLE -0.08, TEX -0.03, OAK +0.02, BAL +0.05, CHC +0.17, MIL +0.27, NYM +0.30, HOU +0.31, ATL +0.44, LAD +0.69, TOR +0.82, COL +1.01, WSH +1.07, BOS +1.32, TB +1.38, LAA +1.92, SEA +2.14

League fielding credit by position (wins): 1B -4.9, 2B +0.3, 3B +11.0, C -13.1, CF -8.0, LF -13.1, P -0.2, RF -26.3, SS +4.0

## 2b. Stolen-base defense vs Savant

- catcher stealing runs: 94 players; correlation of our steal-attempt credit (wins, leverage-weighted) with Savant's (runs): **0.793**
- pitcher running-game runs: 646 players; correlation of our steal-attempt credit (wins, leverage-weighted) with Savant's (runs): **0.539**

## 3. Leaderboards (eye test)

Wins added. Hitters 300+ PA, pitchers 300+ batters faced. `trad` = traditional WPA (batter / pitcher gets the whole play).

### Hitters: top 10 total

| Player | Pos | Team | total | batting | baserunning | fielding | trad_bat |
|---|---|---|---|---|---|---|---|
| Shohei Ohtani | DH | LAD | +6.89 | +6.17 | +0.72 | +0.00 | +6.19 |
| Bobby Witt Jr. | SS | KC | +6.63 | +4.71 | +0.46 | +1.46 | +4.94 |
| Aaron Judge | CF/DH | NYY | +5.62 | +6.00 | +0.10 | -0.48 | +5.55 |
| Juan Soto | RF | NYY | +5.41 | +5.84 | -0.36 | -0.07 | +5.69 |
| Francisco Lindor | SS | NYM | +5.30 | +2.97 | +1.09 | +1.23 | +3.27 |
| José Ramírez | 3B/DH | CLE | +4.65 | +2.39 | +0.98 | +1.28 | +2.75 |
| Jurickson Profar | LF | SD | +3.77 | +4.35 | -0.06 | -0.52 | +4.50 |
| Corey Seager | SS/DH | TEX | +3.47 | +3.36 | -0.34 | +0.45 | +3.66 |
| Ketel Marte | 2B/DH | AZ | +3.47 | +3.11 | +0.19 | +0.16 | +3.04 |
| Jarren Duran | CF/LF | BOS | +3.34 | +1.16 | +1.36 | +0.82 | +1.70 |

### Hitters: bottom 10 total

| Player | Pos | Team | total | batting | baserunning | fielding | trad_bat |
|---|---|---|---|---|---|---|---|
| Jorge Polanco | 2B | SEA | -3.89 | -2.21 | -0.07 | -1.61 | -2.17 |
| Christopher Morel | 3B/2B/LF/DH | CHC/TB | -3.73 | -3.22 | +0.51 | -1.02 | -3.30 |
| Lenyn Sosa | 3B/2B | CWS | -3.50 | -2.53 | -0.14 | -0.83 | -2.75 |
| Leody Taveras | CF | TEX | -3.17 | -2.34 | +0.14 | -0.98 | -2.63 |
| Korey Lee | C/DH | CWS | -3.10 | -3.15 | +0.22 | -0.17 | -3.33 |
| Adolis García | RF/DH | TEX | -3.09 | -2.02 | +0.08 | -1.14 | -2.02 |
| Brandon Drury | 2B/3B/1B/DH | LAA | -2.99 | -3.41 | +0.08 | +0.34 | -3.43 |
| Zack Gelof | 2B | OAK | -2.93 | -3.26 | +0.91 | -0.58 | -3.54 |
| Orlando Arcia | SS | ATL | -2.91 | -3.45 | -0.02 | +0.57 | -3.59 |
| Bo Naylor | C | CLE | -2.78 | -2.10 | -0.22 | -0.46 | -1.90 |

### Fielding: top 10

| Player | Pos | Team | fielding |
|---|---|---|---|
| Andrés Giménez | 2B | CLE | +2.19 |
| Marcus Semien | 2B | TEX | +2.15 |
| Ezequiel Tovar | SS | COL | +1.77 |
| Bobby Witt Jr. | SS | KC | +1.46 |
| Mauricio Dubón | LF/2B/CF/1B/RF/3B | HOU | +1.39 |
| Joey Ortiz | 3B/SS | MIL | +1.37 |
| Ke'Bryan Hayes | 3B | PIT | +1.28 |
| José Ramírez | 3B/DH | CLE | +1.28 |
| Francisco Lindor | SS | NYM | +1.23 |
| Michael Siani | CF | STL | +1.20 |

### Fielding: bottom 10

| Player | Pos | Team | fielding |
|---|---|---|---|
| Jorge Polanco | 2B | SEA | -1.61 |
| Gavin Sheets | RF/1B/DH | CWS | -1.47 |
| Austin Martin | CF/LF/2B | MIN | -1.38 |
| Lane Thomas | RF/CF | WSH/CLE | -1.31 |
| Teoscar Hernández | LF/RF | LAD | -1.31 |
| Hunter Renfroe | RF | KC | -1.28 |
| Gleyber Torres | 2B | NYY | -1.25 |
| Bryan Reynolds | LF/RF/DH | PIT | -1.21 |
| Alec Burleson | RF/LF/1B/DH | STL | -1.21 |
| Jose F Miranda | 3B/1B/DH | MIN | -1.18 |

### Baserunning: top 10

| Player | Pos | Team | baserunning |
|---|---|---|---|
| Nico Hoerner | 2B/SS | CHC | +1.58 |
| Masyn Winn | SS | STL | +1.42 |
| Jarren Duran | CF/LF | BOS | +1.36 |
| Tyler Fitzgerald | SS | SF | +1.27 |
| Francisco Lindor | SS | NYM | +1.09 |
| Corbin Carroll | CF/RF | AZ | +1.08 |
| David Hamilton | SS/2B | BOS | +1.04 |
| Christian Yelich | LF/DH | MIL | +1.02 |
| José Ramírez | 3B/DH | CLE | +0.98 |
| Jacob Young | CF | WSH | +0.95 |

### Baserunning: bottom 10

| Player | Pos | Team | baserunning |
|---|---|---|---|
| Nick Madrigal | 3B/2B | CHC | -0.57 |
| Paul DeJong | SS/3B | CWS/KC | -0.44 |
| Spencer Horwitz | 1B/2B/DH | TOR | -0.43 |
| Masataka Yoshida | DH | BOS | -0.42 |
| Trent Grisham | CF | NYY | -0.41 |
| Andy Pages | CF/RF | LAD | -0.39 |
| Bo Bichette | SS | TOR | -0.38 |
| Carson Kelly | C | DET/TEX | -0.37 |
| Triston Casas | 1B | BOS | -0.37 |
| Juan Soto | RF | NYY | -0.36 |

### Pitchers: top 10

| Player | Pos | Team | pitching | fielding | trad_pit |
|---|---|---|---|---|---|
| Chris Sale | P | ATL | +4.49 | +0.19 | +4.20 |
| Tarik Skubal | P | DET | +4.48 | +0.13 | +4.65 |
| Paul Skenes | P | PIT | +4.22 | +0.02 | +3.72 |
| Tyler Holton | P | DET | +3.96 | +0.16 | +3.98 |
| Zack Wheeler | P | PHI | +3.72 | +0.25 | +4.15 |
| George Kirby | P | SEA | +3.69 | -0.14 | +2.06 |
| Luke Weaver | P | NYY | +3.54 | -0.09 | +3.52 |
| Ryan Walker | P | SF | +3.42 | +0.01 | +3.96 |
| Bryce Miller | P | SEA | +3.38 | -0.04 | +3.63 |
| Cristopher Sánchez | P | PHI | +3.15 | -0.10 | +1.76 |

### Pitchers: bottom 10

| Player | Pos | Team | pitching | fielding | trad_pit |
|---|---|---|---|---|---|
| Roddery Muñoz | P | MIA | -2.59 | -0.04 | -2.48 |
| Taijuan Walker | P | PHI | -2.36 | -0.04 | -2.58 |
| Griffin Canning | P | LAA | -2.19 | +0.21 | -1.79 |
| Dakota Hudson | P | COL | -1.81 | +0.04 | -2.14 |
| Patrick Corbin | P | WSH | -1.69 | +0.24 | -1.85 |
| Logan Allen | P | CLE | -1.61 | +0.02 | -1.53 |
| Miles Mikolas | P | STL | -1.41 | -0.08 | -1.31 |
| Ty Blach | P | COL | -1.40 | -0.01 | -1.46 |
| Frankie Montas | P | CIN/MIL | -1.39 | -0.07 | -1.45 |
| Kenta Maeda | P | DET | -1.19 | -0.05 | -2.37 |

### Pitchers hurt most by their defense (our pitching credit above traditional WPA: fielders took some blame)

| Player | Pos | Team | gap | pitching | trad_pit |
|---|---|---|---|---|---|
| MacKenzie Gore | P | WSH | +1.71 | +1.50 | -0.21 |
| Brandon Pfaadt | P | AZ | +1.68 | +1.50 | -0.18 |
| George Kirby | P | SEA | +1.63 | +3.69 | +2.06 |
| Chris Flexen | P | CWS | +1.52 | +0.43 | -1.09 |
| Cristopher Sánchez | P | PHI | +1.39 | +3.15 | +1.76 |
| Jalen Beeks | P | COL/PIT | +1.37 | -0.15 | -1.53 |
| Mitchell Parker | P | WSH | +1.21 | +0.80 | -0.41 |
| Kenta Maeda | P | DET | +1.18 | -1.19 | -2.37 |
| Joe Ryan | P | MIN | +1.17 | +1.97 | +0.80 |
| Ryan Feltner | P | COL | +1.16 | -0.93 | -2.08 |

### Pitchers helped most by their defense (our pitching credit below traditional WPA: fielders took some credit)

| Player | Pos | Team | gap | pitching | trad_pit |
|---|---|---|---|---|---|
| Ronel Blanco | P | HOU | -1.50 | +0.80 | +2.30 |
| Javier Assad | P | CHC | -1.28 | -0.63 | +0.65 |
| José Ureña | P | TEX | -1.14 | -0.11 | +1.04 |
| Jack Flaherty | P | DET/LAD | -1.14 | +0.91 | +2.05 |
| Bryse Wilson | P | MIL | -1.13 | -0.18 | +0.95 |
| Reynaldo López | P | ATL | -1.06 | +2.33 | +3.39 |
| Framber Valdez | P | HOU | -1.02 | +2.27 | +3.29 |
| Michael Lorenzen | P | TEX/KC | -0.98 | +0.62 | +1.60 |
| Spencer Schwellenbach | P | ATL | -0.92 | +0.40 | +1.31 |
| José Berríos | P | TOR | -0.88 | +0.20 | +1.08 |

### Coaching (team)

| Team | bunt call | defensive indifference | intentional walk | positioning | total |
|---|---|---|---|---|---|
| LAA | +0.11 | -0.01 | -0.36 | +2.53 | +2.28 |
| TB | +0.06 | -0.03 | -0.15 | +2.19 | +2.07 |
| MIL | +0.03 | -0.01 | -0.20 | +1.74 | +1.55 |
| BOS | +0.03 | +0.02 | -0.20 | +1.64 | +1.48 |
| SEA | -0.08 | +0.00 | -0.21 | +1.63 | +1.34 |
| HOU | -0.21 | -0.00 | -0.05 | +1.56 | +1.30 |
| ATL | -0.05 | +0.02 | -0.23 | +1.20 | +0.93 |
| WSH | -0.25 | -0.01 | -0.09 | +1.21 | +0.86 |
| CHC | +0.10 | -0.01 | -0.05 | +0.73 | +0.77 |
| LAD | +0.06 | +0.03 | -0.13 | +0.52 | +0.48 |
| CWS | -0.05 | +0.00 | -0.20 | +0.60 | +0.35 |
| BAL | +0.01 | -0.02 | -0.09 | +0.36 | +0.26 |
| OAK | +0.08 | +0.00 | -0.25 | -0.10 | -0.26 |
| COL | -0.16 | -0.02 | -0.16 | -0.11 | -0.44 |
| TEX | +0.01 | -0.01 | -0.40 | -0.17 | -0.58 |
| STL | -0.01 | -0.01 | -0.24 | -0.43 | -0.69 |
| PHI | -0.03 | +0.01 | -0.07 | -0.69 | -0.78 |
| NYM | -0.12 | -0.01 | -0.15 | -0.50 | -0.78 |
| TOR | -0.05 | +0.00 | -0.44 | -0.30 | -0.79 |
| CLE | +0.06 | -0.02 | -0.15 | -0.68 | -0.79 |
| MIA | -0.05 | +0.00 | -0.28 | -0.59 | -0.93 |
| DET | +0.03 | -0.00 | -0.13 | -0.88 | -0.98 |
| SF | -0.04 | -0.00 | -0.19 | -1.28 | -1.51 |
| PIT | +0.11 | +0.00 | -0.11 | -1.81 | -1.81 |
| SD | +0.02 | -0.02 | -0.15 | -1.74 | -1.89 |
| MIN | +0.05 | -0.03 | -0.07 | -1.86 | -1.92 |
| CIN | +0.16 | -0.08 | -0.12 | -1.91 | -1.95 |
| NYY | -0.02 | -0.01 | -0.19 | -1.90 | -2.13 |
| AZ | -0.41 | -0.03 | -0.44 | -3.19 | -4.07 |
| KC | +0.06 | -0.02 | -0.16 | -4.53 | -4.65 |

### Bucket totals (league)

- def / coaching: -12.7
- def / fielding: -50.2
- def / pitching: +217.4
- off / baserunning: +62.4
- off / batting: -216.4
- off / coaching: -0.6
