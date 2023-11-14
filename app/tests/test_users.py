from app import models, CONTESTS, USERS
from http import HTTPStatus
import requests
from uuid import uuid4


ENDPOINT = "http://127.0.0.1:5000"


def create_user_payload():
    return {
        "first_name": "Vasya" + str(uuid4()),
        "last_name": "Pupkin" + str(uuid4()),
        "email": "test@test.ru",
        "sport": "sport",
    }


def create_contest_payload():
    return {
        "name": "name" + str(uuid4()),
        "sport": "sport" + str(uuid4()),
        "participants": [],
        "status": models.Contest_status.STARTED.value,
        "winner": models.Contest_winner.NOT_DEFINED.value,
    }


def test_users_create():
    payload = create_user_payload()
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.CREATED
    user_data = create_response.json()
    user_id = user_data['id']

    assert user_data["first_name"] == payload["first_name"]
    assert user_data["last_name"] == payload["last_name"]
    assert user_data["email"] == payload["email"]
    assert user_data["sport"] == payload["sport"]

    get_response = requests.get(f"{ENDPOINT}/users/{user_id}")
    assert get_response.json()["first_name"] == payload["first_name"]
    assert get_response.json()["last_name"] == payload["last_name"]
    assert get_response.json()["email"] == payload["email"]
    assert get_response.json()["sport"] == payload["sport"]


def test_users_create_wrong_data():
    payload = create_user_payload()
    payload["email"] = "testtest.ru"
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.BAD_REQUEST


def test_users_leaderboard():
    # it's enough to create only one user without assigning any contest to him
    # because it's necessary to check if the graph is created
    payload = create_user_payload()
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.CREATED
    payload = {
        "type": "list",
        "sort": "desc"
    }
    get_response = requests.get(f"{ENDPOINT}/users/leaderboard", json=payload)
    leaderboard = get_response.json()["users"]
    assert (isinstance(leaderboard, list))


def test_users_assigncont():
    payload_user = create_user_payload()
    payload_contest = create_contest_payload()
    create_response_user = requests.post(
        f"{ENDPOINT}/users/create", json=payload_user)
    assert create_response_user.status_code == HTTPStatus.CREATED
    create_response_contest = requests.post(
        f"{ENDPOINT}/contests/create", json=payload_contest)
    assert create_response_contest.status_code == HTTPStatus.CREATED
    user_id = create_response_user.json()["id"]
    contest_id = create_response_contest.json()["id"]
    payload_contest_id = {"id": contest_id}
    create_response_assign = requests.post(
        f"{ENDPOINT}/users/{user_id}/assigncont", json=payload_contest_id)
    assert create_response_assign.status_code == HTTPStatus.CREATED
    assert payload_contest_id in USERS[user_id].contests
    assert user_id in CONTESTS[contest_id].participants


def test_user_contests():
    payload_user = create_user_payload()
    create_response_user = requests.post(
        f"{ENDPOINT}/users/create", json=payload_user)
    assert create_response_user.status_code == HTTPStatus.CREATED
    payload_contest = create_contest_payload()
    create_response_contest = requests.post(
        f"{ENDPOINT}/contests/create", json=payload_contest)
    assert create_response_contest.status_code == HTTPStatus.CREATED
    user_id = create_response_user.json()["id"]
    get_response = requests.get(f"{ENDPOINT}/users/{user_id}/contests")
    for contest_dict in get_response.json()["contests"]:
        # we just need to check if the following dict keys exist
        # other tests guaranteed that the values of these keys are correct
        assert "id" in contest_dict
        assert "name" in contest_dict
        assert "sport" in contest_dict
        assert "participants" in contest_dict
        assert "winner" in contest_dict
        assert "status" in contest_dict
