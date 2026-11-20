"""
Project 28: Sports Tournament Performance Analysis
--------------------------------------------------
Uses only pandas and numpy.

How to run
    1. Put 28_tournament_match_stats.csv in the same folder as this file.
    2. pip install pandas numpy
    3. python tournament_analysis.py

Results are printed on the screen and also saved as files in a folder
called "output" (created next to this file).

About the data
    - Each row is one team's record for one match: Match_ID, Team, Opponent,
      Player_Name, Player_Points, Match_Duration_Mins, Result (Win/Loss/Draw).
    - Some rows are exact copies of other rows, so Match_ID repeats.
      After removing the copies, every Match_ID appears once, so every
      match is counted once.
"""

import os

import numpy as np
import pandas as pd


# ---------------------------------------------------------------
# Settings
# ---------------------------------------------------------------
FILE_NAME = "28_tournament_match_stats.csv"
OUTPUT_FOLDER = "output"

# Some rows have the same team in Team and Opponent (a team playing itself).
# They are reported in Task 2 but kept by default. Set this to True to
# remove them from the analysis.
REMOVE_SELF_MATCHES = False


# ---------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------
def win_percentage(team, wins_by_team, matches_by_team):
    """Task 12: win percentage = wins / matches played * 100."""
    played = matches_by_team.get(team, 0)
    if played == 0:
        return 0.0
    return wins_by_team.get(team, 0) / played * 100


def iqr_upper_fence(values):
    """Task 14: anything above this number is unusually high (IQR method)."""
    q1 = np.percentile(values, 25)
    q3 = np.percentile(values, 75)
    return q3 + 1.5 * (q3 - q1)


def performance_group(total_points, low_limit, high_limit):
    """Task 14: put a player into Low / Average / High."""
    if total_points <= low_limit:
        return "Low"
    if total_points > high_limit:
        return "High"
    return "Average"


class Player:
    """Task 15: a simple Player class."""

    def __init__(self, name, team, points):
        self.name = name
        self.team = team
        self.points = points

    def summary(self):
        return f"{self.name} ({self.team}) scored {self.points:.0f} points in total."


def heading(text):
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)


# ---------------------------------------------------------------
# Task 1: Load the data and look at it
# ---------------------------------------------------------------
heading("TASK 1: Load the dataset")

folder = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(folder, FILE_NAME)
if not os.path.exists(csv_path):
    raise SystemExit("Cannot find " + FILE_NAME + " in " + folder)

output_path = os.path.join(folder, OUTPUT_FOLDER)
os.makedirs(output_path, exist_ok=True)

data = pd.read_csv(csv_path)

print("Rows and columns:", data.shape)
print("\nColumn names and data types:")
print(data.dtypes)
print("\nFirst 5 rows:")
print(data.head())


# ---------------------------------------------------------------
# Task 2: Missing values and duplicate Match_ID records
# ---------------------------------------------------------------
heading("TASK 2: Missing values and duplicates")

print("Missing values in each column:")
print(data.isna().sum())

print("\nRows in file:", len(data))
print("Unique Match_IDs:", data["Match_ID"].nunique())
print("Match_IDs that appear more than once:",
      int((data["Match_ID"].value_counts() > 1).sum()))
print("Exact duplicate rows:", int(data.duplicated().sum()))

# Remove rows that are exact copies of an earlier row.
data = data.drop_duplicates()

# Safety check: if a Match_ID still repeats (same ID, different details),
# keep the first one so that every match is counted only once.
still_repeated = int(data["Match_ID"].duplicated().sum())
if still_repeated > 0:
    print("Match_IDs still repeated after removing copies:", still_repeated)
    data = data.drop_duplicates(subset="Match_ID", keep="first")

data = data.reset_index(drop=True)
print("Rows after removing duplicates:", len(data))

# A team cannot play itself, so these rows look wrong. Report them.
same_team = data["Team"] == data["Opponent"]
print("\nRows where Team and Opponent are the same team:", int(same_team.sum()))
if REMOVE_SELF_MATCHES:
    data = data[~same_team].reset_index(drop=True)
    print("These rows were removed. Rows left:", len(data))
else:
    print("These rows are kept (set REMOVE_SELF_MATCHES = True to remove them).")


# ---------------------------------------------------------------
# Task 3: Fill missing Player_Points and Match_Duration_Mins
# ---------------------------------------------------------------
heading("TASK 3: Fill missing values with the median")

data["Player_Points"] = pd.to_numeric(data["Player_Points"], errors="coerce")
data["Match_Duration_Mins"] = pd.to_numeric(data["Match_Duration_Mins"], errors="coerce")

missing_points = int(data["Player_Points"].isna().sum())
missing_duration = int(data["Match_Duration_Mins"].isna().sum())

# Why the median? It is not pulled up or down by very high or very low
# values, so it is a safe "typical" value. Filling with it keeps the
# overall average almost unchanged.
points_median = data["Player_Points"].median()
duration_median = data["Match_Duration_Mins"].median()

data["Player_Points"] = data["Player_Points"].fillna(points_median)
data["Match_Duration_Mins"] = data["Match_Duration_Mins"].fillna(duration_median)

print("Missing Player_Points filled:", missing_points, "with median", points_median)
print("Missing Match_Duration_Mins filled:", missing_duration, "with median", duration_median)


# ---------------------------------------------------------------
# Task 4: Dates -> month and weekday
# ---------------------------------------------------------------
heading("TASK 4: Convert Match_Date and add month and weekday")

data["Match_Date"] = pd.to_datetime(data["Match_Date"], errors="coerce")
print("Dates that could not be converted:", int(data["Match_Date"].isna().sum()))

data["Match_Month"] = data["Match_Date"].dt.month
data["Match_Weekday"] = data["Match_Date"].dt.day_name()

print(data[["Match_ID", "Match_Date", "Match_Month", "Match_Weekday"]].head())

data.to_csv(os.path.join(output_path, "cleaned_data.csv"), index=False)


# ---------------------------------------------------------------
# Task 5: Total matches, total points, average match duration
# ---------------------------------------------------------------
heading("TASK 5: Tournament totals")

# Each Match_ID is now on one row only, so each match is counted once.
total_matches = data["Match_ID"].nunique()
total_points = data["Player_Points"].sum()
average_duration = data["Match_Duration_Mins"].mean()

print("Total matches played:", total_matches)
print("Total points scored:", total_points)
print("Average match duration (minutes):", round(average_duration, 2))


# ---------------------------------------------------------------
# Task 11: A tuple of result labels and a set of teams
# ---------------------------------------------------------------
heading("TASK 11: Tuple of result labels and set of teams")

RESULT_LABELS = ("Win", "Loss", "Draw")          # fixed values -> tuple
participating_teams = set(data["Team"])           # unique values -> set

print("Result labels (tuple):", RESULT_LABELS)
print("Participating teams (set):", participating_teams)

for label in data["Result"].unique():
    if label not in RESULT_LABELS:
        print("Warning: unexpected result label found:", label)

print("\nHow many rows have each result:")
print(data["Result"].value_counts())


# ---------------------------------------------------------------
# Task 12: Dictionary of wins per team
# ---------------------------------------------------------------
heading("TASK 12: Dictionary of wins and win-percentage function")

# matches played by each team (each Match_ID counted once)
matches_by_team = data.groupby("Team")["Match_ID"].nunique().to_dict()

# start every team at 0 wins, then add one for each "Win" row
wins_by_team = {}
for team in participating_teams:
    wins_by_team[team] = 0

for team in data.loc[data["Result"] == "Win", "Team"]:
    wins_by_team[team] = wins_by_team[team] + 1

print("Wins by team (dictionary):")
for team in sorted(wins_by_team):
    print("  ", team, ":", wins_by_team[team])

example_team = sorted(participating_teams)[0]
print("\nExample: win percentage of", example_team, "=",
      round(win_percentage(example_team, wins_by_team, matches_by_team), 2), "%")


# ---------------------------------------------------------------
# Tasks 6 and 9: Team ranking and win percentage
# ---------------------------------------------------------------
heading("TASKS 6 and 9: Team ranking and win percentage")

points_by_team = data.groupby("Team")["Player_Points"].sum()

rows = []
for team in participating_teams:
    rows.append({
        "Team": team,
        "Total_Points": points_by_team[team],
        "Matches_Played": matches_by_team[team],
        "Matches_Won": wins_by_team[team],
        "Win_Percentage": round(win_percentage(team, wins_by_team, matches_by_team), 2),
    })

team_table = pd.DataFrame(rows)

# Rank by total points first; if two teams tie, the one with more wins is higher.
team_table = team_table.sort_values(["Total_Points", "Matches_Won"],
                                    ascending=[False, False]).reset_index(drop=True)
team_table.insert(0, "Rank_By_Points", np.arange(1, len(team_table) + 1))
team_table["Rank_By_Wins"] = team_table["Matches_Won"].rank(
    method="min", ascending=False).astype(int)

print("Teams ranked by total points (and matches won):")
print(team_table.to_string(index=False))

win_table = team_table[["Team", "Matches_Played", "Matches_Won", "Win_Percentage"]]
win_table = win_table.sort_values("Win_Percentage", ascending=False)
print("\nWin percentage comparison (draws count as played, not as wins):")
print(win_table.to_string(index=False))

team_table.to_csv(os.path.join(output_path, "team_ranking.csv"), index=False)
win_table.to_csv(os.path.join(output_path, "win_percentage_comparison.csv"), index=False)


# ---------------------------------------------------------------
# Task 7: Top 10 players by total points
# ---------------------------------------------------------------
heading("TASK 7: Top 10 players")

# In this file every player appears for several teams, so players are
# grouped by NAME only.
player_totals = data.groupby("Player_Name")["Player_Points"].agg(["sum", "count"]).reset_index()
player_totals.columns = ["Player_Name", "Total_Points", "Matches_Played"]

# Main team = the team the player scored the most points for.
points_by_player_team = data.groupby(["Player_Name", "Team"])["Player_Points"].sum().reset_index()
points_by_player_team = points_by_player_team.sort_values("Player_Points", ascending=False)
main_team = points_by_player_team.drop_duplicates(subset="Player_Name")
main_team = main_team.set_index("Player_Name")["Team"]
player_totals["Main_Team"] = player_totals["Player_Name"].map(main_team)

player_totals = player_totals.sort_values("Total_Points", ascending=False).reset_index(drop=True)
player_totals.insert(0, "Rank", np.arange(1, len(player_totals) + 1))

top_10_players = player_totals.head(10)
print(top_10_players.to_string(index=False))

top_10_players.to_csv(os.path.join(output_path, "top_10_players.csv"), index=False)


# ---------------------------------------------------------------
# Task 8: Average points by match type and by tournament round
# ---------------------------------------------------------------
heading("TASK 8: Average points by match type and round")

avg_by_type = data.groupby("Match_Type")["Player_Points"].mean().round(2)
avg_by_type = avg_by_type.sort_values(ascending=False)
print("Average points by Match_Type:")
print(avg_by_type)

avg_by_round = data.groupby("Tournament_Round")["Player_Points"].mean().round(2)
avg_by_round = avg_by_round.sort_values(ascending=False)
print("\nAverage points by Tournament_Round:")
print(avg_by_round)

avg_by_type.to_csv(os.path.join(output_path, "avg_points_by_match_type.csv"))
avg_by_round.to_csv(os.path.join(output_path, "avg_points_by_round.csv"))


# ---------------------------------------------------------------
# Task 10: Longest and shortest matches
# ---------------------------------------------------------------
heading("TASK 10: Longest and shortest matches")

longest_value = data["Match_Duration_Mins"].max()
shortest_value = data["Match_Duration_Mins"].min()

show_columns = ["Match_ID", "Match_Date", "Team", "Opponent", "Match_Duration_Mins"]

# Several matches can have the same duration, so all ties are shown.
longest_matches = data[data["Match_Duration_Mins"] == longest_value][show_columns]
shortest_matches = data[data["Match_Duration_Mins"] == shortest_value][show_columns]

print("Longest match(es):", longest_value, "minutes")
print(longest_matches.to_string(index=False))
print("\nShortest match(es):", shortest_value, "minutes")
print(shortest_matches.to_string(index=False))

duration_summary = pd.concat([
    longest_matches.assign(Type="Longest"),
    shortest_matches.assign(Type="Shortest"),
])
duration_summary.to_csv(os.path.join(output_path, "match_duration_summary.csv"), index=False)


# ---------------------------------------------------------------
# Task 13: NumPy mean, median, standard deviation of player points
# ---------------------------------------------------------------
heading("TASK 13: NumPy statistics for Player_Points")

points = data["Player_Points"].to_numpy()

points_mean = np.mean(points)
points_median = np.median(points)
points_std = np.std(points, ddof=1)     # ddof=1 -> sample standard deviation

print("Mean   :", round(points_mean, 2))
print("Median :", round(points_median, 2))
print("Std dev:", round(points_std, 2))


# ---------------------------------------------------------------
# Task 14: Outliers (IQR method) and performance groups
# ---------------------------------------------------------------
heading("TASK 14: High scores (IQR) and performance groups")

# Part 1: unusually high single-match scores
fence = iqr_upper_fence(points)
high_scores = data[data["Player_Points"] > fence]
high_scores = high_scores[["Match_ID", "Player_Name", "Team", "Player_Points"]]

print("Q1 =", np.percentile(points, 25), " Q3 =", np.percentile(points, 75))
print("Upper fence (Q3 + 1.5 * IQR) =", fence)
print("Single-match scores above the fence:", len(high_scores))
if len(high_scores) > 0:
    print(high_scores.sort_values("Player_Points", ascending=False).to_string(index=False))
else:
    print("No single-match score is unusually high.")

# Extra check: the same rule on each player's TOTAL points
total_fence = iqr_upper_fence(player_totals["Total_Points"].to_numpy())
high_totals = player_totals[player_totals["Total_Points"] > total_fence]
print("\nPlayer TOTALS above their upper fence (", round(total_fence, 1), "):", len(high_totals))
if len(high_totals) > 0:
    print(high_totals[["Player_Name", "Total_Points"]].to_string(index=False))

high_scores.to_csv(os.path.join(output_path, "score_outliers.csv"), index=False)

# Part 2: performance groups based on each player's total points.
# Thresholds (documented):
#   Low     = total points at or below the 25th percentile of player totals
#   Average = above the 25th percentile and up to the 75th percentile
#   High    = above the 75th percentile
totals = player_totals["Total_Points"].to_numpy()
low_limit = np.percentile(totals, 25)
high_limit = np.percentile(totals, 75)
print("\nGroup limits -> Low: <=", low_limit, "| Average: up to", high_limit, "| High: above", high_limit)

player_totals["Performance_Group"] = [
    performance_group(p, low_limit, high_limit) for p in player_totals["Total_Points"]
]
print(player_totals["Performance_Group"].value_counts())

player_totals.to_csv(os.path.join(output_path, "player_performance_groups.csv"), index=False)


# ---------------------------------------------------------------
# Task 15: Player class objects and five observations
# ---------------------------------------------------------------
heading("TASK 15: Player objects and observations")

top_players = []
for name, team, pts in zip(player_totals["Player_Name"].head(5),
                           player_totals["Main_Team"].head(5),
                           player_totals["Total_Points"].head(5)):
    top_players.append(Player(name, team, pts))

print("Top 5 players (Player objects):")
for p in top_players:
    print(" -", p.summary())

best_points_team = team_table.iloc[0]
best_win_team = win_table.iloc[0]
best_player = top_players[0]

observations = [
    f"The tournament has {total_matches} matches, {len(participating_teams)} teams and "
    f"{data['Player_Name'].nunique()} players, with {total_points:.0f} points scored in total.",

    f"{best_points_team['Team']} scored the most points ({best_points_team['Total_Points']:.0f}) "
    f"and won {best_points_team['Matches_Won']} of {best_points_team['Matches_Played']} matches.",

    f"{best_win_team['Team']} has the best win percentage "
    f"({best_win_team['Win_Percentage']:.1f}%). Draws count as matches played but not as wins.",

    f"{best_player.name} is the top player with {best_player.points:.0f} points. "
    f"The average player score per match is {points_mean:.1f}.",

    f"{avg_by_type.index[0]} matches have the highest average points ({avg_by_type.iloc[0]}) and "
    f"{avg_by_round.index[0]} is the highest-scoring round ({avg_by_round.iloc[0]}). "
    f"There are {len(high_scores)} unusually high single-match scores.",
]

print("\nFive observations:")
for number, text in enumerate(observations, start=1):
    print(f"{number}. {text}")

with open(os.path.join(output_path, "five_observations.txt"), "w", encoding="utf-8") as f:
    f.write("Five Tournament Performance Observations\n\n")
    for number, text in enumerate(observations, start=1):
        f.write(f"{number}. {text}\n")


heading("DONE")
print("All result files are saved in:", output_path)
