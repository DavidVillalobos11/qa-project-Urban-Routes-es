from sender_stand_request import post_new_user, post_new_client_kit
import data

def get_auth_token():
    response = post_new_user()
    return response.json()["authToken"]


# 1
def test_kit_name_1_char():
    token = get_auth_token()
    kit_body = data.kit_body.copy()
    kit_body["name"] = "a"

    response = post_new_client_kit(kit_body, token)

    assert response.status_code == 201
    assert response.json()["name"] == kit_body["name"]


# 2
def test_kit_name_511_chars():
    token = get_auth_token()
    kit_body = data.kit_body.copy()
    kit_body["name"] = "a" * 511

    response = post_new_client_kit(kit_body, token)

    assert response.status_code == 201
    assert response.json()["name"] == kit_body["name"]


# 3
def test_kit_name_empty():
    token = get_auth_token()
    kit_body = data.kit_body.copy()
    kit_body["name"] = ""

    response = post_new_client_kit(kit_body, token)

    assert response.status_code == 400


# 4
def test_kit_name_512_chars():
    token = get_auth_token()
    kit_body = data.kit_body.copy()
    kit_body["name"] = "a" * 512

    response = post_new_client_kit(kit_body, token)

    assert response.status_code == 400


# 5
def test_kit_special_chars():
    token = get_auth_token()
    kit_body = data.kit_body.copy()
    kit_body["name"] = "№%@,"

    response = post_new_client_kit(kit_body, token)

    assert response.status_code == 201
    assert response.json()["name"] == kit_body["name"]


# 6
def test_kit_spaces():
    token = get_auth_token()
    kit_body = data.kit_body.copy()
    kit_body["name"] = " A Aaa "

    response = post_new_client_kit(kit_body, token)

    assert response.status_code == 201
    assert response.json()["name"] == kit_body["name"]


# 7
def test_kit_numbers():
    token = get_auth_token()
    kit_body = data.kit_body.copy()
    kit_body["name"] = "123"

    response = post_new_client_kit(kit_body, token)

    assert response.status_code == 201
    assert response.json()["name"] == kit_body["name"]


# 8
def test_kit_no_name():
    token = get_auth_token()
    kit_body = data.kit_body.copy()
    kit_body.pop("name")

    response = post_new_client_kit(kit_body, token)

    assert response.status_code == 400


# 9
def test_kit_wrong_type():
    token = get_auth_token()
    kit_body = data.kit_body.copy()
    kit_body["name"] = 123

    response = post_new_client_kit(kit_body, token)

    assert response.status_code == 400