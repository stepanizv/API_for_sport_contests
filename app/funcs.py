import numpy as np
from matplotlib import pyplot as plt
from app import models, USERS


def get_valid_users(USERS=USERS):
    # returns the list of all USERS that are NOT DELETED
    users_valid = [user for user in USERS if models.User.is_valid_id(user.id)]
    return users_valid


def get_users_leaderboard(sort = 'desc'):
    # creates an array of users' leaderboard
    users_list = get_valid_users()
    if sort == "asc":
        users_list.sort(key=lambda user: len(user.contests))
    else:
        users_list.sort(key=lambda user: len(user.contests), reverse=True)
    return users_list


def create_graph():
    # creates a graph of users' leaderboard
    users_list = get_valid_users()
    x = np.array(
        [f"{user.id}# {user.last_name}" for user in users_list])
    y = np.array([len(user.contests) for user in users_list])
    plt.figure()
    plt.xticks(ticks=np.array([users_list.index(user) for user in users_list]), rotation=10)
    plt.yticks(ticks=np.arange(min(y), max(y)+1))
    plt.xlabel("users' ids and last names")
    plt.ylabel("number of contests")
    plt.grid()
    plt.bar(x, y, width=0.1)
    plt.savefig("app/static/leaderboard.png")
