# Credit report: 2026

## 1. Accounting identities (must hold exactly)

- Events: 190,547. Offense credits equal the event's change on 100.000%; defense credits equal minus the change on 100.000% (max gaps 3.33e-16 / 3.33e-16)
- Events with no credit rows: 0; events with no change in win probability (decided games): 6,756
- Teams whose total credit equals wins minus summed starting win probability: 30 of 30 (max gap 5.33e-15)
- Credit rows with no player (coaching buckets): 150,248; non-coaching rows with no player: 0

| Team | W | G | Credited | Wins - starting WP |
|---|---|---|---|---|
| MIL | 103 | 162 | +22.00 | +22.00 |
| LAD | 100 | 162 | +19.00 | +19.00 |
| TB | 98 | 162 | +17.00 | +17.00 |
| ATL | 94 | 162 | +13.00 | +13.00 |
| NYY | 93 | 161 | +12.50 | +12.50 |
| SD | 91 | 162 | +10.00 | +10.00 |
| CHC | 89 | 162 | +8.00 | +8.00 |
| PHI | 88 | 162 | +7.00 | +7.00 |
| BOS | 87 | 162 | +6.00 | +6.00 |
| AZ | 86 | 162 | +5.00 | +5.00 |
| CLE | 85 | 162 | +4.00 | +4.00 |
| CWS | 84 | 162 | +3.00 | +3.00 |
| PIT | 82 | 162 | +1.00 | +1.00 |
| HOU | 81 | 162 | -0.00 | +0.00 |
| TEX | 80 | 162 | -1.00 | -1.00 |
| MIA | 80 | 162 | -1.00 | -1.00 |
| BAL | 79 | 161 | -1.50 | -1.50 |
| TOR | 79 | 162 | -2.00 | -2.00 |
| WSH | 77 | 162 | -4.00 | -4.00 |
| MIN | 77 | 162 | -4.00 | -4.00 |
| STL | 77 | 162 | -4.00 | -4.00 |
| DET | 76 | 162 | -5.00 | -5.00 |
| SEA | 76 | 162 | -5.00 | -5.00 |
| CIN | 75 | 162 | -6.00 | -6.00 |
| NYM | 74 | 162 | -7.00 | -7.00 |
| KC | 69 | 162 | -12.00 | -12.00 |
| SF | 65 | 162 | -16.00 | -16.00 |
| ATH | 64 | 162 | -17.00 | -17.00 |
| LAA | 62 | 162 | -19.00 | -19.00 |
| COL | 58 | 162 | -23.00 | -23.00 |

## 2. Outfield vs Savant OAA

- Outfield catch chances credited to the same fielder Savant names: 99.99%
- Outfielders (primary position LF/CF/RF) compared: 255; correlation of our outs-above-expected with Savant OAA: **0.980**; mean absolute difference 0.86 outs

Largest differences (Savant OAA includes direction/arm adjustments and other positions):

| Player | Savant OAA | Ours (outs - catch prob) |
|---|---|---|
| Jonny DeLuca | +14 | +10.0 |
| Fernando Tatis Jr. | +4 | +0.2 |
| Sal Frelick | +3 | -0.6 |
| Pete Crow-Armstrong | +26 | +22.5 |
| Jackson Merrill | +7 | +3.8 |
| Andy Pages | +10 | +6.9 |
| Chandler Simpson | +9 | +6.1 |
| Seiya Suzuki | +5 | +2.2 |

## 2a. Infield vs Savant OAA

- Infielders (primary 1B/2B/3B/SS) compared: 308; correlation of our ground-ball outs-above-expected with Savant infield OAA: **0.451** (191 with 100+ chances: 0.451)
- Savant judges each fielder from where he actually stood; our model only knows the alignment type, so team positioning is still inside our fielders' numbers. Gap by team (ours - Savant, outs) shows it:

| Position | Players (100+) | Correlation |
|---|---|---|
| 1B | 36 | 0.612 |
| 2B | 54 | 0.359 |
| 3B | 51 | 0.570 |
| SS | 50 | 0.400 |

Gap by team (outs): AZ -42, PHI -37, CIN -27, SD -22, STL -20, CLE -19, ATH -16, TEX -15, NYY -12, BAL -6, HOU -6, MIN -6, KC -6, COL -5, MIA -4, CWS -4, LAA -3, TOR -2, CHC +1, BOS +2, LAD +5, SF +7, ATL +8, NYM +10, MIL +11, PIT +14, SEA +23, WSH +33, DET +35, TB +57

- After moving positioning to coaching, infielders' outs above expected match Savant OAA: correlation 1.000, max gap 0.90 outs
- Infield positioning credit by team (wins): PHI -2.89, AZ -2.58, CIN -1.84, SD -1.65, STL -1.54, CLE -1.24, TEX -1.13, ATH -1.04, NYY -0.88, KC -0.48, COL -0.47, HOU -0.43, MIN -0.40, BAL -0.30, CWS -0.21, TOR -0.18, LAA -0.14, MIA -0.14, CHC +0.15, LAD +0.21, BOS +0.24, MIL +0.56, SF +0.78, NYM +0.79, ATL +0.88, PIT +1.00, SEA +1.29, DET +2.27, WSH +2.28, TB +3.73

League fielding credit by position (wins): 1B -4.3, 2B +0.3, 3B +10.0, C -13.0, CF -12.1, LF -8.2, P +1.9, RF -27.1, SS +9.1

## 2b. Stolen-base defense vs Savant

- catcher stealing runs: 108 players; correlation of our steal-attempt credit (wins, leverage-weighted) with Savant's (runs): **0.722**
- pitcher running-game runs: 641 players; correlation of our steal-attempt credit (wins, leverage-weighted) with Savant's (runs): **0.490**

## 3. Leaderboards (eye test)

Wins added. Hitters 300+ PA, pitchers 300+ batters faced. `trad` = traditional WPA (batter / pitcher gets the whole play).

### Hitters: top 10 total

| Player | Pos | Team | total | batting | baserunning | fielding | trad_bat |
|---|---|---|---|---|---|---|---|
| Pete Crow-Armstrong | CF | CHC | +6.35 | +4.31 | +1.36 | +0.67 | +3.93 |
| Brice Turang | 2B | MIL | +5.89 | +3.45 | +0.60 | +1.84 | +3.89 |
| Yordan Alvarez | LF/DH | HOU | +5.29 | +6.24 | -0.70 | -0.25 | +6.36 |
| Bobby Witt Jr. | SS | KC | +5.15 | +1.83 | +1.30 | +2.02 | +1.78 |
| Elly De La Cruz | SS/DH | CIN | +4.05 | +2.29 | +1.04 | +0.73 | +2.39 |
| Shohei Ohtani | P/DH | LAD | +3.74 | +2.01 | -0.19 | +0.17 | +2.22 |
| Alex Bregman | 3B/DH | CHC | +3.65 | +1.47 | +0.12 | +2.06 | +1.48 |
| Nick Kurtz | 1B | ATH | +3.36 | +2.87 | +0.26 | +0.22 | +3.08 |
| JJ Wetherholt | 2B/SS | STL | +3.33 | +1.09 | +0.63 | +1.61 | +1.32 |
| Brandon Lowe | 2B/DH | PIT | +2.96 | +1.43 | +0.29 | +1.24 | +1.53 |

### Hitters: bottom 10 total

| Player | Pos | Team | total | batting | baserunning | fielding | trad_bat |
|---|---|---|---|---|---|---|---|
| Ezequiel Tovar | SS | COL | -3.84 | -4.15 | +0.30 | +0.01 | -4.36 |
| Andruw Monasterio | SS/2B/1B/DH | BOS | -3.10 | -1.62 | -0.24 | -1.23 | -1.67 |
| Victor Caratini | C/1B | MIN | -2.83 | -1.82 | -0.47 | -0.55 | -1.50 |
| Cal Raleigh | C/DH | SEA | -2.79 | -2.18 | +0.04 | -0.65 | -2.11 |
| Jared Triolo | SS/3B | PIT | -2.77 | -2.41 | +0.38 | -0.75 | -2.74 |
| Marcus Semien | 2B | NYM | -2.75 | -2.11 | +0.12 | -0.76 | -2.81 |
| Heliot Ramos | LF/RF | SF/NYY | -2.75 | -1.84 | -0.15 | -0.76 | -2.38 |
| Nasim Nuñez | 2B/SS | WSH | -2.69 | -3.31 | +0.82 | -0.21 | -2.86 |
| Bo Bichette | 3B/SS | NYM | -2.53 | -2.27 | -0.17 | -0.09 | -1.93 |
| Josh Naylor | 1B | SEA | -2.52 | -2.58 | +0.14 | -0.08 | -2.30 |

### Fielding: top 10

| Player | Pos | Team | fielding |
|---|---|---|---|
| Masyn Winn | SS | STL | +2.28 |
| Alex Bregman | 3B/DH | CHC | +2.06 |
| Bobby Witt Jr. | SS | KC | +2.02 |
| Mookie Betts | SS | LAD | +1.99 |
| Brice Turang | 2B | MIL | +1.84 |
| Brayan Rocchio | SS/2B | CLE | +1.63 |
| JJ Wetherholt | 2B/SS | STL | +1.61 |
| Ezequiel Duran | 3B/SS/2B/LF/CF/RF | TEX | +1.51 |
| Geraldo Perdomo | SS | AZ | +1.38 |
| Zach McKinstry | RF/2B/SS | DET | +1.37 |

### Fielding: bottom 10

| Player | Pos | Team | fielding |
|---|---|---|---|
| Luke Keaschall | 2B/RF/CF | MIN | -2.31 |
| Lane Thomas | CF/LF/RF | KC/ATL | -2.01 |
| Jordan Walker | RF | STL | -1.82 |
| Mike Trout | CF/DH | LAA | -1.76 |
| Sam Antonacci | LF/2B | CWS | -1.65 |
| Kyle Tucker | RF | LAD | -1.58 |
| Jung Hoo Lee | RF/CF | SF | -1.46 |
| Lawrence Butler | RF/CF | ATH | -1.41 |
| Dane Myers | CF/DH | CIN | -1.37 |
| Cole Young | 2B | SEA | -1.37 |

### Baserunning: top 10

| Player | Pos | Team | baserunning |
|---|---|---|---|
| Pete Crow-Armstrong | CF | CHC | +1.36 |
| Bobby Witt Jr. | SS | KC | +1.30 |
| Jazz Chisholm Jr. | 2B | NYY | +1.08 |
| Elly De La Cruz | SS/DH | CIN | +1.04 |
| Jakob Marsee | CF | MIA | +1.01 |
| Jackson Merrill | CF | SD | +0.99 |
| Dansby Swanson | SS | CHC | +0.97 |
| Christian Yelich | DH | MIL | +0.89 |
| Myles Straw | LF/CF/RF | TOR | +0.86 |
| Jeremy Peña | SS | HOU | +0.85 |

### Baserunning: bottom 10

| Player | Pos | Team | baserunning |
|---|---|---|---|
| Yordan Alvarez | LF/DH | HOU | -0.70 |
| Francisco Lindor | SS | NYM | -0.58 |
| Ryan Kreidler | SS/CF/2B | MIN | -0.55 |
| Hunter Goodman | C/DH | COL | -0.55 |
| Junior Caminero | 3B | TB | -0.50 |
| Connor Wong | C | BOS | -0.48 |
| Victor Caratini | C/1B | MIN | -0.47 |
| Heriberto Hernández | LF | MIA | -0.46 |
| Isaac Collins | LF | KC | -0.46 |
| Patrick Bailey | C | CLE/SF | -0.45 |

### Pitchers: top 10

| Player | Pos | Team | pitching | fielding | trad_pit |
|---|---|---|---|---|---|
| Adrian Morejon | P | SD | +4.43 | +0.31 | +3.60 |
| Louis Varland | P | TOR | +4.25 | -0.31 | +3.97 |
| Cristopher Sánchez | P | PHI | +4.24 | +0.26 | +3.96 |
| Cam Schlittler | P | NYY | +3.91 | -0.15 | +3.73 |
| Chris Sale | P | ATL | +3.76 | +0.10 | +3.24 |
| Brock Burke | P | CIN | +3.47 | -0.18 | +1.91 |
| Drew Rasmussen | P | TB | +3.45 | -0.08 | +4.23 |
| Reid Detmers | P | LAA | +3.36 | +0.05 | +2.81 |
| Jesús Luzardo | P | PHI | +3.35 | +0.08 | +3.48 |
| Jacob Misiorowski | P | MIL | +3.29 | -0.06 | +4.45 |

### Pitchers: bottom 10

| Player | Pos | Team | pitching | fielding | trad_pit |
|---|---|---|---|---|---|
| Kyle Freeland | P | COL | -4.14 | +0.02 | -3.83 |
| Michael Lorenzen | P | COL/TOR | -4.00 | +0.16 | -4.46 |
| Jeffrey Springs | P | ATH | -2.54 | +0.03 | -2.93 |
| Miles Mikolas | P | WSH | -2.42 | +0.11 | -2.40 |
| Brady Singer | P | CIN | -2.32 | -0.13 | -3.17 |
| Tomoyuki Sugano | P | COL | -2.06 | +0.03 | -1.38 |
| Ryan Feltner | P | COL | -1.92 | -0.03 | -2.10 |
| Luis Castillo | P | SEA/CWS | -1.81 | +0.00 | -2.49 |
| Mike Burrows | P | HOU | -1.52 | -0.12 | -2.12 |
| Steven Matz | P | TB | -1.50 | +0.00 | -0.69 |

### Pitchers hurt most by their defense (our pitching credit above traditional WPA: fielders took some blame)

| Player | Pos | Team | gap | pitching | trad_pit |
|---|---|---|---|---|---|
| Andrew Morris | P | MIN | +2.31 | +1.36 | -0.94 |
| Bradgley Rodriguez | P | SD | +1.60 | +1.54 | -0.07 |
| Brock Burke | P | CIN | +1.56 | +3.47 | +1.91 |
| Matthew Liberatore | P | STL | +1.54 | -0.80 | -2.35 |
| Bubba Chandler | P | PIT | +1.45 | +0.22 | -1.23 |
| Joe Ryan | P | MIN | +1.30 | +0.81 | -0.49 |
| Will Warren | P | NYY | +1.29 | +0.95 | -0.34 |
| Kyle Bradish | P | BAL | +1.28 | +0.47 | -0.81 |
| Connor Prielipp | P | MIN | +1.27 | +0.17 | -1.10 |
| Bryan Woo | P | SEA | +1.26 | +1.47 | +0.21 |

### Pitchers helped most by their defense (our pitching credit below traditional WPA: fielders took some credit)

| Player | Pos | Team | gap | pitching | trad_pit |
|---|---|---|---|---|---|
| Michael McGreevy | P | STL | -1.43 | -0.31 | +1.12 |
| Michael King | P | SD | -1.40 | +1.36 | +2.76 |
| Brent Headrick | P | NYY | -1.29 | +1.10 | +2.38 |
| Grant Holmes | P | ATL | -1.23 | -0.39 | +0.85 |
| Sean Newcomb | P | CWS | -1.21 | +1.49 | +2.70 |
| Javier Assad | P | CHC | -1.17 | +0.51 | +1.69 |
| Ranger Suarez | P | BOS | -1.17 | +1.23 | +2.40 |
| Jacob Misiorowski | P | MIL | -1.16 | +3.29 | +4.45 |
| Nick Martinez | P | TB | -0.92 | +2.12 | +3.05 |
| Martín Pérez | P | ATL | -0.91 | +0.34 | +1.25 |

### Coaching (team)

| Team | bunt call | defensive indifference | intentional walk | positioning | total |
|---|---|---|---|---|---|
| TB | +0.15 | +0.04 | -0.17 | +4.80 | +4.82 |
| DET | +0.03 | -0.02 | -0.08 | +3.15 | +3.08 |
| PIT | -0.03 | -0.00 | -0.34 | +2.53 | +2.16 |
| NYY | +0.06 | -0.03 | -0.14 | +1.57 | +1.46 |
| WSH | +0.17 | -0.03 | -0.30 | +1.32 | +1.17 |
| SEA | +0.07 | -0.01 | -0.24 | +1.33 | +1.15 |
| NYM | -0.03 | -0.02 | -0.06 | +1.00 | +0.88 |
| MIL | +0.03 | -0.01 | -0.17 | +0.95 | +0.80 |
| ATL | +0.02 | -0.00 | -0.30 | +1.02 | +0.74 |
| TOR | +0.01 | -0.02 | -0.40 | +0.34 | -0.06 |
| SF | +0.11 | -0.01 | -0.19 | -0.06 | -0.15 |
| HOU | +0.05 | -0.01 | -0.02 | -0.21 | -0.19 |
| LAD | +0.07 | -0.01 | -0.45 | +0.12 | -0.27 |
| CHC | -0.01 | -0.01 | -0.14 | -0.16 | -0.32 |
| CWS | +0.19 | -0.01 | -0.20 | -0.48 | -0.49 |
| MIN | -0.05 | -0.03 | -0.15 | -0.50 | -0.72 |
| LAA | -0.03 | -0.01 | -0.45 | -0.29 | -0.79 |
| MIA | -0.09 | -0.01 | -0.08 | -0.69 | -0.86 |
| CLE | +0.23 | -0.01 | -0.17 | -1.25 | -1.20 |
| KC | +0.11 | -0.01 | -0.06 | -1.47 | -1.43 |
| ATH | -0.00 | -0.00 | -0.33 | -1.09 | -1.43 |
| BOS | -0.05 | -0.00 | -0.13 | -1.53 | -1.71 |
| COL | +0.22 | -0.01 | -0.17 | -1.81 | -1.76 |
| TEX | -0.15 | -0.01 | -0.63 | -1.19 | -1.97 |
| CIN | -0.03 | -0.01 | -0.22 | -1.74 | -2.00 |
| SD | -0.00 | -0.01 | -0.20 | -2.04 | -2.26 |
| STL | +0.18 | -0.03 | -0.16 | -2.35 | -2.35 |
| PHI | +0.00 | -0.05 | -0.14 | -2.47 | -2.66 |
| BAL | +0.10 | -0.00 | -0.20 | -2.97 | -3.08 |
| AZ | -0.29 | -0.02 | -0.29 | -3.21 | -3.81 |

### Bucket totals (league)

- def / coaching: -14.3
- def / fielding: -43.4
- def / pitching: +158.9
- off / baserunning: +61.2
- off / batting: -163.5
- off / coaching: +1.1
