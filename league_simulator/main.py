from league_simulator.funcs import simulate_season, handleInput
import pandas as pd


n_teams = handleInput("How many teams are in the league (default 18)? ", 18)
potential_std = handleInput("League spread (default 0.1)? ", 0.1, decimal=True)
rank_of_interest = handleInput("Rank of interest? (default 1st)", 1)
n_simulations = handleInput("How many simulations (default 1000)? ", 1000)


points_required = list()
for simulation in range(n_simulations):
    points = simulate_season(
        n_teams,
        potential_std,
        rank_of_interest,
        show_each_simulation=True,
    )
    points_required.append(points)
    print(f"Simulation #{simulation + 1} done.")

points_required.sort()
points_required.reverse()

print(
    f"{n_simulations} simulations suggest: Rank >> {rank_of_interest} << was achieved by as low as {points_required[-1]} and as high as {points_required[0]} points"
)
