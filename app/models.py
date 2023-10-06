import re
from app import USERS, CONTESTS
import numpy as np
from matplotlib import pyplot as plt


class User:
    def __init__(self, id, first_name, last_name, email, sport, contests):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.sport = sport
        self.contests = contests

    def repr(self):
        return f"{self.id}) {self.first_name} {self.last_name}"

    def convert_to_dict(self):
        # creates a dict of the class attributes for json.dumps when required
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "contests": self.contests,
        }

    @staticmethod
    def is_valid_id(id):
        return id >= 0 and id < len(USERS)

    @staticmethod
    def is_valid_email(email):
        if (
            re.match(
                r"[^@]+@[^@]+\.[^@]+",
                email,
            )
            != None
        ):
            return True
        return False

    @staticmethod
    def is_email_occupied(email):
        return any(user.email == email for user in USERS)


class Contest:
    def __init__(self, id, name, sport, participants, status, winner):
        self.name = name
        self.sport = sport
        self.participants = participants
        self.id = id
        self.status = status
        self.winner = winner

    def repr(self):
        return f"{self.id}) {self.name}"

    def convert_to_dict(self):
        # creates a dict of the class attributes for json.dumps when required
        return {
            "id": self.id,
            "name": self.name,
            "sport": self.sport,
            "status": self.status,
            "participants": self.participants,
            "winner": self.winner,
        }

    def is_finished(self):
        return self.status == "FINISHED"

    def is_valid_winner(self, winner):
        return winner in self.participants

    @staticmethod
    def is_valid_id(id):
        return id >= 0 and id < len(CONTESTS)


def remove_finished_contest(USERS, contest_id):
    for user in USERS:
        if contest_id in user.contests:
            user.contests.pop(user.contests.index(contest_id))


def create_graph(USERS):
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
