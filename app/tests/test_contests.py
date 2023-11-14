from http import HTTPStatus
from app import CONTESTS
import requests
from uuid import uuid4


ENDPOINT = "http://127.0.0.1:5000"


def create_contest_payload():
    return {
        "name": "name" + str(uuid4()),
        "sport": "sport" + str(uuid4()),
    }


def create_user_payload():
    return {
        "first_name": "Vasya" + str(uuid4()),
        "last_name": "Pupkin" + str(uuid4()),
        "email": "test@test.ru",
        "sport": "sport",
    }


def test_contests_create():
    payload = create_contest_payload()
    create_response = requests.post(
        f"{ENDPOINT}/contests/create", json=payload)
    assert create_response.status_code == HTTPStatus.CREATED
    contest_data = create_response.json()
    contest_id = contest_data["id"]

    assert contest_data["name"] == payload["name"]
    assert contest_data["sport"] == payload["sport"]

    get_response = requests.get(f"{ENDPOINT}/contests/{contest_id}")
    assert get_response.json()["name"] == payload["name"]
    assert get_response.json()["sport"] == payload["sport"]


def test_contests_create_wrong_data():
    payload = create_contest_payload()
    create_response_contest = requests.post(
        f"{ENDPOINT}/contests/create", json=payload)
    assert create_response_contest.status_code == HTTPStatus.CREATED
    contest_id = create_response_contest.json()["id"]
    payload["name"] = CONTESTS[contest_id].name
    create_response_wrong_data = requests.post(
        f"{ENDPOINT}/contests/create", json=payload)
    assert create_response_wrong_data.status_code == HTTPStatus.BAD_REQUEST


def test_contest_finish():
    payload_contest = create_contest_payload()
    create_response_contest = requests.post(
        f"{ENDPOINT}/contests/create", json=payload_contest)
    assert create_response_contest.status_code == HTTPStatus.CREATED
    payload_user = create_user_payload()
    create_response_user = requests.post(
        f"{ENDPOINT}/users/create", json=payload_user)
    assert create_response_user.status_code == HTTPStatus.CREATED
    contest_id = create_response_contest.json()["id"]
    user_id = create_response_user.json()["id"]
    create_response_assignuser = requests.post(
        f"{ENDPOINT}/contests/{contest_id}/assignuser", json={"id": user_id})
    assert create_response_assignuser.status_code == HTTPStatus.CREATED
    create_response_finish = requests.post(
        f"{ENDPOINT}/contests/{contest_id}/finish", json={"winner": user_id})
    response_data = create_response_finish.json()
    contest = CONTESTS[contest_id]
    assert create_response_finish.status_code == HTTPStatus.CREATED
    assert response_data["winner"] == contest.winner
    assert response_data["status"] == contest.status


def test_contests_assignuser():
    payload_contest = create_contest_payload()
    create_response_contest = requests.post(
        f"{ENDPOINT}/contests/create", json=payload_contest)
    assert create_response_contest.status_code == HTTPStatus.CREATED
    payload_user = create_user_payload()
    create_response_user = requests.post(
        f"{ENDPOINT}/users/create", json=payload_user)
    assert create_response_user.status_code == HTTPStatus.CREATED
    contest_id = create_response_contest.json()["id"]
    user_id = create_response_user.json()["id"]
    create_response_assignuser = requests.post(
        f"{ENDPOINT}/contests/{contest_id}/assignuser", json={"id": user_id})
    response_data = create_response_assignuser.json()
    contest = CONTESTS[contest_id]
    assert response_data["participants"] == contest.participants
    assert user_id in response_data["participants"]


def test_get_contest_participants():
    payload_contest = create_contest_payload()
    create_response_contest = requests.post(
        f"{ENDPOINT}/contests/create", json=payload_contest)
    assert create_response_contest.status_code == HTTPStatus.CREATED
    payload_user = create_user_payload()
    create_response_user = requests.post(
        f"{ENDPOINT}/users/create", json=payload_user)
    assert create_response_user.status_code == HTTPStatus.CREATED
    contest_id = create_response_contest.json()["id"]
    user_id = create_response_user.json()["id"]
    create_response_assignuser = requests.post(
        f"{ENDPOINT}/contests/{contest_id}/assignuser", json={"id": user_id})
    assert create_response_assignuser.status_code == HTTPStatus.CREATED
    get_response = requests.get(
        f"{ENDPOINT}/contest/{contest_id}/participants")
    for participant_dict in get_response.json()["participants"]:
        # we just need to check if the following dict keys exist
        # other tests guaranteed that the values of these keys are correct
        assert "id" in participant_dict
        assert "first_name" in participant_dict
        assert "last_name" in participant_dict
        assert "email" in participant_dict
        assert "sport" in participant_dict
        assert "contests" in participant_dict
        assert "status" in participant_dict
