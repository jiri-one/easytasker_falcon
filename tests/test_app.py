import falcon
from falcon import testing, inspect
import pytest
from uuid import uuid4
from pathlib import Path
from tinydb import TinyDB, Query, JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer
# internal imports
from easytasker import app
import db
from path_serializer import PathSerializer

serialization = SerializationMiddleware(JSONStorage)
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
serialization.register_serializer(PathSerializer(), 'TinyPath')

class FakeDB(object):
    def __init__(self, tmp_path):
        print("XXXXXXXXXXXXXXXX",tmp_path)
        self.tmp_path = tmp_path
        self.test_cookie = str(uuid4())
        (tmp_path / "files/test").mkdir(parents=True, exist_ok=True) 
        self.db_users = TinyDB(tmp_path / 'files/db_users.json')
        self.db_users.insert({'name': 'test',
                              'password':  db.get_hashed_password("test"),
                              'cookie_uuid': self.test_cookie})

    def fake_db_init(self, user):
        return TinyDB(self.tmp_path / 'files/test/db.json', storage=serialization)


@pytest.fixture
def fake_db(tmp_path):
    return FakeDB(tmp_path)

@pytest.fixture
def client():
    return testing.TestClient(app)


def test_index_without_login(client):
    """Test that index have to redirect to login page withou proper authorization"""
    response = client.simulate_get('/')
    assert response.status == falcon.HTTP_303


def test_index_with_login(client, fake_db, monkeypatch):
    monkeypatch.setattr(db, "db_init", fake_db.fake_db_init)
    monkeypatch.setattr(db, "db_users", fake_db.db_users)
    response = client.simulate_get('/', cookies={"user": "test", 'cookie_uuid': fake_db.test_cookie})
    assert response.status == falcon.HTTP_OK
