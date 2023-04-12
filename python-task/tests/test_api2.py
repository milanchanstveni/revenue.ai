import requests


base_url = "http://0.0.0.0:5001"
client = requests.Session()
client.auth = ('revenue', 'revenue')


def test__get_root() -> None:
    response = client.get(base_url)

    assert response.status_code == 200
    assert type(response.json()) == list
    assert len(response.json()) == 20


def test__get_docs() -> None:
    response = client.get(f"{base_url}/docs")

    assert response.status_code == 200
    assert len(response.text) > 2
