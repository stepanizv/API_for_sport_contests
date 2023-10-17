import numpy as np
from matplotlib import pyplot as plt


def remove_finished_contest(USERS, contest_id):
    # removes the finished contest from the CONTEST list
    for user in USERS:
        if contest_id in user.contests:
            user.contests.pop(user.contests.index(contest_id))


def create_graph(USERS):
    # creates a graph of users' leaderboard
    x = np.arange([f"{user.id}, {user.first_name} {user.last_name}" for user in USERS])
    y = np.array([len(user.contests) for user in USERS])
    plt.figure()
    plt.xticks(ticks=np.array([user.id for user in USERS]), rotation=40)
    plt.yticks(ticks=np.arange(min(y), max(y)))
    plt.ylim(max(y) + 1)
    plt.xlim((max(x) + 1))
    plt.title("The leaderboard of all users by numbers of contests")
    plt.xlabel("users' ids")
    plt.ylabel("numbers of contests")
    plt.grid()
    plt.bar(x, y, width=0.1)
    plt.savefig("app/leaderboard.png")
