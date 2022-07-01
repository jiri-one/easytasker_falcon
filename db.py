from tinydb import TinyDB, Query, JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
# internal imports
from helpers import file_path, get_hashed_password, check_password

# set current working directory
cwd = Path(__file__).parent

# set DB files and queries
db_users = TinyDB(cwd / 'db_users.json')
# db_users.insert({'name': 'USER_NAME', 'password': get_hashed_password("XXXXX")})
serialization = SerializationMiddleware(JSONStorage)
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')

@dataclass
class Task:
    title: str
    content: str
    time_expired: datetime
    time_created: datetime = datetime.now()
    time_finished: datetime = None
    attachement: Path = None
    db = TinyDB(cwd / 'db.json', storage=serialization)
    query = Query()


print(Path(__file__).parent)
print(db_users.search(query.name == 'deso')[0]["password"])

print(check_password("heslo", db_users.search(query.name == 'deso')[0]["password"]))
