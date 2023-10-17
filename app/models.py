import re
from app import USERS, CONTESTS
from enum import Enum

class User:
    def __init__(self, id, first_name, last_name, email, sport, contests):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.sport = sport
        self.contests = contests

    def repr(self):
        # the representation of a User-object
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
    # checks the id for validity
    def is_valid_id(id):
        return id >= 0 and id < len(USERS)

    @staticmethod
    # checks the email for validity
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
    # checks if the email is already occupied by another user
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
        # the representation of a Contest-object
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
        # checks if the contests is already finished
        return self.status == Status.FINISHED

    def is_valid_winner(self, winner):
        # checks if the user, being assigned as the winner, in the list of participants
        return winner in self.participants

    @staticmethod
    # checks the contest id for validity
    def is_valid_id(id):
        return id >= 0 and id < len(CONTESTS)

class Status(Enum):
    # status of contests
    STARTED = "Started"
    FINISHED = "Finished"