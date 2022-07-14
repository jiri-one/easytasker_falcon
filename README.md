**EasyTasker
Simple web based tasker.**

**Instalation:**
After download files from this repository, you can install and run it this way:
```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python easytasker.py
```

**Features of EasyTasker:**
- user registration
- user login/logout
- NoSQL database backend
- passwords hashed over bcrypt
- task you can: add, delete, search, mark them as finished
- you can add one file to every task like attachement (upload/download both is working)
- you can see expired tasks
- and some more functions ...

**EasyTasker is based on:**
- Falcon
- TinyDB
- BCrypt
- Mako

**Dependencies for default local run:**
- hupper
- waitress

Every dependencies are included in requirements.txt. If you want to use another server and you don't need reloader, then you can uninstall or don't need to install hupper and waitress.

**Login:**
Three accounts are created for preview and tests, so you can use them:

```
deso:heslo
deso2:heslo
deso3:heslo
```
But you can (and you should) register your own account.

**Tests:**
- NOT FINISHED YET
- created in pytest (install it with `pip install pytest`)
- helpers for pytest are flacon.inspect and flacon.testing
- tests are completely independent on main db or user_db
