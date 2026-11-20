# HCLproject
# Project 28: Sports Tournament Performance Analysis

A Python program that analyses tournament match data and reports team rankings, player rankings, win percentages, match durations, unusually high scores and written observations. It uses only **pandas** and **NumPy**.

**Author:** Piyush Kumar
**Admission No.:** 2026B15410280
**College Email:** piyush.26b15410280@abes.ac.in

---

## Dataset

`28_tournament_match_stats.csv` has 609 rows and 10 columns. Each row is one team's record for one match.

| Column | Description |
| --- | --- |
| Match_ID | Match identifier |
| Match_Date | Date of the match |
| Team | Team the row belongs to (8 teams) |
| Opponent | Team played against |
| Player_Name | Player recorded for the match (79 players) |
| Player_Points | Points scored by the player |
| Match_Duration_Mins | Match length in minutes |
| Match_Type | Final, Semi-Final, Friendly or League |
| Tournament_Round | Round 1, Round 2, Quarter-Final, Semi-Final or Final |
| Result | Win, Loss or Draw for the team |

## What the program does

The script completes all 15 tasks of the assignment:

1. Loads the dataset and shows its size, columns and data types
2. Checks missing values and duplicate Match_ID records
3. Fills missing Player_Points and Match_Duration_Mins with the median
4. Converts Match_Date to a date and adds month and weekday
5. Calculates total matches, total points and average match duration
6. Ranks teams by total points and matches won
7. Finds the top 10 players by total points
8. Compares average points by match type and tournament round
9. Calculates each team's win percentage
10. Finds the longest and shortest matches
11. Stores result labels in a tuple and participating teams in a set
12. Stores team wins in a dictionary and uses a win-percentage function
13. Uses NumPy for the mean, median and standard deviation of player points
14. Finds unusually high scores with the IQR method and creates performance groups
15. Uses a simple `Player` class and writes five observations

## Project files

| File | Purpose |
| --- | --- |
| `tournament_analysis.py` | Main program |
| `28_tournament_match_stats.csv` | Input dataset |
| `output/` | Result files created by the program |
| SRS document (PDF) | Software Requirements Specification |
| `tournament_analysis_with_details.pdf` | Printout of the code |

## How to run

1. Install Python 3.8 or later.
2. Install the libraries:
   ```
   pip install pandas numpy
   ```
3. Keep `tournament_analysis.py` and `28_tournament_match_stats.csv` in the same folder.
4. Run the program:
   ```
   python tournament_analysis.py
   ```

The results are printed on the screen and saved in the `output` folder.

## Output files

| File | Content |
| --- | --- |
| `cleaned_data.csv` | Cleaned dataset with month and weekday columns |
| `team_ranking.csv` | Team points, matches played, wins, win percentage and ranks |
| `win_percentage_comparison.csv` | Teams sorted by win percentage |
| `top_10_players.csv` | Top 10 players by total points |
| `avg_points_by_match_type.csv` | Average points for each match type |
| `avg_points_by_round.csv` | Average points for each tournament round |
| `match_duration_summary.csv` | Longest and shortest matches |
| `score_outliers.csv` | Single-match scores above the IQR upper fence |
| `player_performance_groups.csv` | Each player's total points and performance group |
| `five_observations.txt` | Five observations about tournament performance |

## Key results

- 600 matches, 12,826 points in total, and an average match duration of 104.97 minutes
- Sharks scored the most points (2,025); Panthers have the best win percentage (38.89%)
- Player 43 is the top player with 381 points
- Player points: mean 21.38, median 21.0, sample standard deviation 12.66
- The IQR upper fence is 63.5, and no single-match score is above it

## Data handling notes

- The 9 repeated Match_ID values were exact duplicate rows. They were removed, which leaves one row per match.
- Draws count as matches played but not as wins.
- 81 matches list the same team as Team and Opponent. They are reported and kept. Set `REMOVE_SELF_MATCHES = True` at the top of the script to remove them.
- Every player appears under more than one team, so players are grouped by name only.
- Missing numbers are filled with the median because it is not pulled by very high or very low values.

## Technologies

Python 3, pandas, NumPy
