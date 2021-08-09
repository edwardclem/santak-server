from santak import app
import pytest
import json

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_match(client):
    res = client.post("/match", data={'image': open('tests/imgs/73728_CuneiformComposite_96_dpi_300_150.png', 'rb')})

    data = json.loads(res.data)
    assert data["msg"] == "success"
    assert len(data["matches"]) == 5

def test_match_params(client):

    for n_matches in [1, 5, 10, 15]:
        res = client.post(f"/match?num={n_matches}", data={'image': open('tests/imgs/73728_CuneiformComposite_96_dpi_300_150.png', 'rb')})

        data = json.loads(res.data)
        assert data["msg"] == "success"
        assert len(data["matches"]) == n_matches
