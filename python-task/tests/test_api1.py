import requests


base_url = "http://0.0.0.0:5000"
client = requests.Session()
client.auth = ('revenue', 'revenue')


def test__get_root() -> None:
    response = client.get(base_url)

    assert response.status_code == 404
    assert type(response.json()) == dict
    assert response.json() == {"detail":"Not Found"}


def test__get_docs() -> None:
    response = client.get(f"{base_url}/docs")

    assert response.status_code == 200
    assert len(response.text) > 2


def test__get_countries() -> None:
    response1 = client.get(f"{base_url}/MasterData/Country")

    assert response1.status_code == 200
    assert type(response1.json()) == list
    assert len(response1.json()) == 250

    response2 = client.get(f"{base_url}/MasterData/Country?countryName=Canada")

    assert response2.status_code == 200
    assert type(response2.json()) == list
    assert len(response2.json()) == 1

    response3 = client.get(f"{base_url}/MasterData/Country?countryName=Invalid")

    assert response3.status_code == 200
    assert type(response3.json()) == list
    assert len(response3.json()) == 0