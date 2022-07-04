from tinydb import TinyDB, Query, JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
import bcrypt
# internal imports
from path_serializer import PathSerializer

# set current working directory
cwd = Path(__file__).parent

# set DB files and queries
serialization = SerializationMiddleware(JSONStorage)
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
serialization.register_serializer(PathSerializer(), 'TinyPath')
db = TinyDB(cwd / 'db.json', storage=serialization)
db_users = TinyDB(cwd / 'db_users.json')
query = Query()


@dataclass
class Task:
    title: str
    content: str
    time_expired: datetime
    time_created: datetime = datetime.now()
    time_finished: datetime = None
    attach: Path = None
    id: int = None

    def write_to_db(self):
        self.id = db.insert({ 'title': self.title,
                    'content': self.content,
                    'time_expired': self.time_expired,
                    'time_created': self.time_created,
                    'time_finished': self.time_finished,
                    'attach': self.attach,
                    })
    
    def update_in_db(self, id):
        db.update({ 'title': self.title,
                    'content': self.content,
                    'time_expired': self.time_expired,
                    'time_created': self.time_created,
                    'time_finished': self.time_finished,
                    'attach': self.attach,
                    }, doc_ids=[id])


def create_task_class(el):
    return Task(title=el["title"],
                content=el["content"],
                time_expired=el["time_expired"],
                time_created=el["time_created"],
                time_finished=el["time_finished"],
                attach=el["attach"],
                id=el.doc_id
                )

def get_task_from_db(doc_id):
    el = db.get(doc_id=doc_id)
    return create_task_class(el)

def remove_task_from_db(doc_id):
    db.remove(doc_ids=[doc_id])


def get_tasks(expired=None, finished=None):
    if expired:
        for el in db.search(query.time_expired > datetime.now()):
            yield create_task_class(el)
    if finished:
        for el in db.search(query.time_finished != None):
            yield create_task_class(el)
    for el in db.all():
        yield create_task_class(el)


# pasword hash helpers
def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())


def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password, hashed_password)


# db_users.insert({'name': 'USER_NAME', 'password': get_hashed_password("XXXXX")})

print(db_users.search(query.name == 'deso')[0]["password"])

print(check_password("heslo", db_users.search(query.name == 'deso')[0]["password"]))
