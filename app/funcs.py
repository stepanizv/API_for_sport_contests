import numpy as np
from matplotlib import pyplot as plt
from app import USERS


def get_users_leaderboard(sort):
    # creates an array of users' leaderboard
    users_actual = [user for user in USERS if user.is_valid_id(user.id)]
    if sort == "asc":
        users_actual.sort(key=lambda user: len(user.contests))
    else:
        users_actual.sort(key=lambda user: len(user.contests), reverse=True)
    return users_actual


def create_graph():
    # creates a graph of users' leaderboard
    users_actual = [user for user in USERS if user.is_valid_id(user.id)]
    x = np.array(
        [f"{user.id}, {user.last_name}" for user in users_actual])
    y = np.array([len(user.contests) for user in users_actual])
    plt.figure()
    plt.xticks(ticks=np.array([user.id for user in users_actual]), rotation=20)
    plt.yticks(ticks=np.arange(min(y), max(y)))
    plt.title("The leaderboard of all users by numbers of contests")
    plt.xlabel("users' ids and last names")
    plt.ylabel("number of contests")
    plt.grid()
    plt.bar(x, y, width=0.1)
    plt.savefig("app/leaderboard.png")
