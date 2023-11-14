import re
from app import USERS, CONTESTS
from enum import Enum
import json
from flask import Response
from http import HTTPStatus
from abc import ABC, abstractmethod


class Object(ABC):

    @abstractmethod
    def convert_to_dict():
        pass

    def get_response_json(self, response_method):
        # forms the response in json view of object
        if response_method == "OK":
            response = Response(
                json.dumps(self.convert_to_dict()),
                HTTPStatus.OK,
                mimetype="application/json",
            )
        if response_method == "CREATED":
            response = Response(
                json.dumps(self.convert_to_dict()),
                HTTPStatus.CREATED,
                mimetype="application/json",
            )
        return response


class User(Object):

    def __init__(self, first_name, last_name, email, sport):
        self.id = len(USERS)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.sport = sport
        self.contests = []
        self.status = User_status.CREATED.value

    def repr(self):
        # the representation of a User-object
        if self.status == User_status.CREATED.value:
            return f"{self.id}) {self.first_name} {self.last_name}"
        return f"DELETED{id}"

    def create_list_of_contests(self):
        # creates the list of user's contests (not ids but the Contest objects!)
        user_contests = []
        for contest in CONTESTS:
            if (self.id in contest.participants) and (Contest.is_valid_id(contest.id)):
                user_contests.append(contest)
        return user_contests

    def get_contests_json(self):
        user_contests = self.create_list_of_contests()
        response = Response(
            json.dumps(
                {
                    "contests": [
                        contest.convert_to_dict() for contest in user_contests
                    ]
                }
            ),
            HTTPStatus.OK,
            mimetype="application/json",
        )
        return response

    def convert_to_dict(self):
        # creates a dict of the class attributes for json.dumps when required
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "sport": self.sport,
            "contests": self.contests,
            "status": self.status,
        }

    @staticmethod
    # checks the id for validity
    def is_valid_id(id):
        return (id >= 0 and id < len(USERS) and (USERS[id].status != User_status.DELETED.value))

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


class Contest(Object):

    def __init__(self, name, sport):
        self.name = name
        self.sport = sport
        self.participants = []
        self.id = len(CONTESTS)
        self.status = Contest_status.STARTED.value
        self.winner = Contest_winner.NOT_DEFINED.value

    def repr(self):
        # the representation of a Contest-object
        return f"{self.id}) {self.name} ({self.status})"

    def convert_to_dict(self):
        # creates a dict of the class attributes for json.dumps when required
        return {
            "id": self.id,
            "name": self.name,
            "sport": self.sport,
            "participants": self.participants,
            "status": self.status,
            "winner": self.winner,
        }

    def create_list_of_participants(self):
        # creates a list of the contest participants (not ids but the User objects!)
        contest_participants = []
        for user in USERS:
            if (self.id in user.contests) and (User.is_valid_id(user.id)):
                contest_participants.append(user)
        return contest_participants

    def get_participants_json(self):
        cont_participants = self.create_list_of_participants()
        response = Response(
            json.dumps(
                {
                    "participants": [
                        participant.convert_to_dict() for participant in cont_participants
                    ]
                }
            ),
            HTTPStatus.OK,
            mimetype="application/json",
        )
        return response

    def is_finished(self):
        # checks if the contest is finished
        return self.status == Contest_status.FINISHED.value

    def finish(self, winner_id):
        if not self.is_finished():
            self.winner = winner_id
            self.status = Contest_status.FINISHED.value

    def is_valid_winner(self, winner_id):
        # checks if the user, being assigned as the winner, in the list of participants
        return (winner_id in self.participants) and (USERS[winner_id].status == User_status.CREATED.value)

    @staticmethod
    # checks the contest id for validity
    def is_valid_id(id):
        return 0 <= id < len(CONTESTS)

    @staticmethod
    def is_valid_name(name):
        return all(contest.name != name for contest in CONTESTS)


# the classes below are responsible for objects' statuses (deleted, created, etc.)
class Contest_status(Enum):
    STARTED = "Started"
    FINISHED = "Finished"


class Contest_winner(Enum):
    NOT_DEFINED = "Not defined"


class User_status(Enum):
    CREATED = "Created"
    DELETED = "Deleted"
