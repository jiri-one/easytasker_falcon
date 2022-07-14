import falcon
from falcon import testing, inspect
import pytest
from uuid import uuid4
from tinydb import TinyDB, JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer
from datetime import datetime, timedelta
# internal imports
from easytasker import app
import db, login
from path_serializer import PathSerializer
from helpers import templatelookup

serialization = SerializationMiddleware(JSONStorage)
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
serialization.register_serializer(PathSerializer(), 'TinyPath')


class FakeDB(object):
    def __init__(self, tmp_path):
        self.tmp_path = tmp_path
        self.test_cookie = str(uuid4())
        (tmp_path / "files/test").mkdir(parents=True, exist_ok=True) 
        self.db_users = TinyDB(tmp_path / 'files/db_users.json')
        self.db_users.insert({'name': 'test',
                              'password':  db.get_hashed_password("test"),
                              'cookie_uuid': self.test_cookie})
        self.main_fake_db = TinyDB(self.tmp_path / 'files/test/db.json', storage=serialization)
        self.create_fake_tasks_in_db()
    
    def fake_db_init(self, user):
        return self.main_fake_db
    
    def create_fake_tasks_in_db(self):  
        self.active_task = db.Task(title="TEST TITLE",
                        content="TEST CONTENT",
                        time_expired=datetime.now() + timedelta(days=7),
                        attach=None,
                        db=self.main_fake_db,
                        )
        self.active_task.write_to_db()
        assert self.active_task.id == 1
        self.finished_task = db.Task(title="TEST FINISHED TITLE",
                        content="TEST FINISHED CONTENT",
                        time_finished=datetime.now() + timedelta(days=3),
                        time_expired=datetime.now() + timedelta(days=7),
                        attach=None,
                        db=self.main_fake_db,
                        )
        self.finished_task.write_to_db()
        assert self.finished_task.id == 2
        self.expired_task = db.Task(title="TEST EXPIRED TITLE",
                        content="TEST EXPIRED CONTENT",
                        time_expired=datetime.now() - timedelta(days=1),
                        attach=None,
                        db=self.main_fake_db,
                        )
        self.expired_task.write_to_db()
        assert self.expired_task.id == 3



@pytest.fixture
def fake_db(tmp_path):
    return FakeDB(tmp_path)

@pytest.fixture
def client(fake_db, monkeypatch):
    monkeypatch.setattr(login, "db_init", fake_db.fake_db_init)
    monkeypatch.setattr(login, "db_users", fake_db.db_users)
    return testing.TestClient(app)

# TESTS FOR GET METHODS
def test_all_GET_to_status_303_without_logged_user(client):
    """All GET methods have to redirect (status 303) to /login page (except /login and /register page), if user is not logged in."""
    for route in inspect.inspect_routes(app):
       for method in route.methods:
            if method.function_name[:6] == "on_get" and route.path not in ["/login", "/register"]:
                if route.path == "/{task_id:int}": route.path = "/1"
                response = client.simulate_get(f'{route.path}')
                assert response.status == falcon.HTTP_303


def test_all_GET_status_200_with_logged_user(client, fake_db):
    """All pages and their GET methods have to return code 200 OK (except /login and /logout page) if user is logged in."""
    for route in inspect.inspect_routes(app):
       for method in route.methods:
            if method.function_name[:6] == "on_get" and route.path not in ["/login", "/logout"]:
                if route.path == "/{task_id:int}": route.path = "/1"
                response = client.simulate_get(f'{route.path}', cookies={"user": "test", 'cookie_uuid': fake_db.test_cookie})
                assert response.status == falcon.HTTP_OK
                

def test_index_with_all_task_types(client, fake_db):
    mytemplate = templatelookup.get_template("index.mako")
    for task_type in [None, "finished", "expired"]: # None is default view for active tasks
        tasks = db.get_tasks(fake_db.main_fake_db, task_type)
        rendered_template = mytemplate.render(data={"tasks": tasks, "tasks_type": task_type})
        response = client.simulate_get(f'/?tasks={task_type}', cookies={"user": "test", 'cookie_uuid': fake_db.test_cookie})
        assert rendered_template == response.content
        assert response.status == falcon.HTTP_OK

def test_register_page_with_logged_user(client, fake_db):
    response = client.simulate_get('/register', cookies={"user": "test", 'cookie_uuid': fake_db.test_cookie})
    mytemplate = templatelookup.get_template("register.mako")
    rendered_template = mytemplate.render(data={"error": """Přihlášení uživatelé nemohou provádět registrace! Musíte se nejdříve <a href="/logout">odhlásit.</a>"""})
    assert rendered_template == response.content
    assert response.status == falcon.HTTP_OK

def test_new_task_page_with_logged_user(client, fake_db):
    response = client.simulate_get('/new_task', cookies={"user": "test", 'cookie_uuid': fake_db.test_cookie})
    mytemplate = templatelookup.get_template("new_task.mako")
    rendered_template = mytemplate.render(data={})
    assert rendered_template == response.content
    assert response.status == falcon.HTTP_OK

def test_task_page_with_three_testing_tasks(client, fake_db):
    """Combined test, that take three task from FakeDB and compare them with task with same id from db (function get_task_from_db), then try to render those tasks via /{task_id}"""
    for task in [fake_db.active_task, fake_db.finished_task, fake_db.expired_task]:
        task_from_db = db.get_task_from_db(fake_db.main_fake_db, task.id)
        assert task_from_db == task # test, that function get_task_from_db works
        mytemplate = templatelookup.get_template("task.mako")
        rendered_template = mytemplate.render(data=task_from_db)
        response = client.simulate_get(f'/{task_from_db.id}', cookies={"user": "test", 'cookie_uuid': fake_db.test_cookie})
        assert rendered_template == response.content
        assert response.status == falcon.HTTP_OK

def test_task_page_bad_task_number(client, fake_db):
    response = client.simulate_get('/999999', cookies={"user": "test", 'cookie_uuid': fake_db.test_cookie})
    assert response.json == {"title": "Neexistující ID tasku, používejte pouze tlačítka a odkazy na stránce!"}

def test_task_page_task_number_is_not_int(client, fake_db):
    response = client.simulate_get('/XXXX', cookies={"user": "test", 'cookie_uuid': fake_db.test_cookie})
    assert response.status == falcon.HTTP_404
    # in the future, this should be handled better
