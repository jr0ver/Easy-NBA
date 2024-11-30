import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use Agg backend (non-interactive)
import matplotlib.pyplot as plt
import seaborn as sns


def find_top_teams(reg: pd.DataFrame) -> list[str]:
    teams = reg["Team"].value_counts()
    all_teams = teams.index.tolist()[:-1]

    if "Total" in all_teams:
        all_teams.remove("Total")
    if len(all_teams) > 3:
        return all_teams[:3]

    return ", ".join(all_teams)


def show_graph(reg: pd.DataFrame) -> None:
    sns.jointplot(x=reg.index, y=reg["Points"], data=reg, kind="hex")
    plt.xlabel("Season Number")
    plt.ylabel("Points")
    plt.savefig("abd.png")
