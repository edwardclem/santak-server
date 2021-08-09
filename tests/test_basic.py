from santak import app
import pytest
import json

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_basic(client):
    res = client.get("/")

    assert b"test index page" in res.data


def test_img_post(client):
    res = client.post("/img_debug", data={'image': open('tests/imgs/73728_CuneiformComposite_96_dpi_300_150.png', 'rb')})

    data = json.loads(res.data)
    assert data["size"] == [312, 312]
