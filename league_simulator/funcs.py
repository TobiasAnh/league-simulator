import random
import string
import pandas as pd


def handleInput(prompt, default_output, decimal=False):

    while True:
        try:
            output = input(prompt) or default_output

            if decimal:
                return float(output)
            else:
                return int(output)
        except ValueError:
            print("Invalid input. Please enter a number")


def generate_unique_names(n, name_length=1):
    """
    Generates a specified number of unique names.

    Args:
        num_names (int): The number of unique names to generate.
        name_length (int): The length of each name. default = 1

    Returns:
        list: A list of unique names.
    """
    unique_names = set()

    while len(unique_names) < n:
        # Generate a random name
        name = "".join(random.choices(string.ascii_letters, k=name_length))
        unique_names.add(name)

    return list(unique_names)


class team:
    """
    Generates a team with a name and various attributes
    """

    def __init__(self, team_name, potential_std):
        # Assigns pre-season attributes to a team such as games played, points, goals , etc.
        self.team_name = team_name
        self.points_total = 0
        self.scored_total = 0
        self.received_total = 0
        self.games_total = 0

        # Also adds a random potential to induce variance in teams strengs across the league
        # Spreach of this variance can be changed

        self.potential = random.normalvariate(0.5, potential_std)

    def game(self, scored, received):
        """
        A description of what this method does.

        Returns:
            type: Description of the return value.
        """
        self.scored_total += scored
        self.received_total += received

        if scored == received:
            self.points_total += 1
        if scored > received:
            self.points_total += 3
        if scored < received:
            self.points_total += 0

        self.games_total += 1

    def show_stats(self):
        self.stats = {
            "Team": self.team_name,
            "Games": self.games_total,
            "Points": self.points_total,
            "Scored": self.scored_total,
            "Received": self.received_total,
        }
        return self.stats


# Create matchdays
def generateMatchdays(league):
    """
    A short description of what this class represents.

    Attributes:
        attribute1 (type): Description of attribute1.
        attribute2 (type): Description of attribute2.
    """

    matches_per_matchday = int(len(league) / 2)
    n_matchdays = (len(league) - 1) * 2  #

    # print(f"Initiate match schedule for {len(league)} Teams.")
    # print(f"Preparing 2 x {n_matchdays} matchdays ... ")

    # Accumulating matches in a set until its filled up
    matches = set()
    while len(matches) < (matches_per_matchday * n_matchdays):
        match = tuple(random.sample(league.keys(), 2))
        matches.add(match)

    return matches


def simulate_matches(league):
    matches = generateMatchdays(league)

    for match in matches:
        # Teams playing
        team_0 = league.get(match[0]).team_name
        team_1 = league.get(match[1]).team_name

        # Reassigning potentials
        potential_0 = league.get(match[0]).potential
        potential_1 = league.get(match[1]).potential

        # Besides potential, each team has a daily performance fluctuation
        tagesform_0 = random.normalvariate(0, 0.05)
        tagesform_1 = random.normalvariate(0, 0.05)

        # Match performance
        performance_0 = potential_0 + tagesform_0
        performance_1 = potential_1 + tagesform_1

        # Anpfiff !
        # Simple simulation of a game having up to 5 chances per game
        # If a goal per chance is succesful depends on performace (potential + tagesform) and another luck component
        goal_0, goal_1 = 0, 0
        for chances in range(random.randint(0, 5)):
            expected_result = (
                performance_0 - performance_1 + random.normalvariate(0, 0.1)
            )
            if expected_result > 0:
                goal_0 += 1
            if expected_result < 0:
                goal_1 += 1

        # goal_0, goal_1

        league.get(team_0).game(goal_0, goal_1)
        league.get(team_1).game(goal_1, goal_0)

    return league


def simulate_season(
    n_teams,
    potential_std,
    rank_of_interest,
    show_each_simulation=False,
):

    teams = generate_unique_names(n_teams)
    # Initiate league
    league = {}
    for team_name in teams:
        oTeam = team(team_name, potential_std)
        league[team_name] = oTeam

    # Start league
    league_finished = simulate_matches(league)

    # Analyse results
    status_list = []
    for team_name, team_object in league_finished.items():
        status_list.append(team_object.show_stats())

    table = pd.DataFrame(status_list)
    table["Diff"] = table["Scored"] - table["Received"]
    table = table.sort_values(
        ["Points", "Diff"],
        ascending=False,
    )
    table = table.reset_index(drop=True)
    table.index = table.index + 1
    points = table[(rank_of_interest - 1) : rank_of_interest]["Points"].item()

    if show_each_simulation:
        print(table)

    return points
