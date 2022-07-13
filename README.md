**This is simple web based tasker named shortly EasyTasker.**

After download files from this repository, you can install and run it this way:
```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python easytasker.py
```

Features of EasyTasker:
- user registration
- user login/logout
- NoSQL database backend
- passwords hashed over bcrypt
- task you can: add, delete, search, mark them as finished
- you can add one file to every task like attachement (upload/download both is working)
- you can see expired tasks
- and some more functions ...

EasyTasker is based on:
- Falcon
- TinyDB
- BCrypt
- Mako

For default local run:
- hupper
- waitress

Every dependencies are included in requirements.txt. If you want to use another server and you don't need reloader, then you can uninstall or don't need to install hupper and waitress.

Three accounts are created for preview and tests, so you can use them:

```
deso:heslo
deso2:heslo
deso3:heslo
```


What is not completed for now:
- tests (I am working on them, some of them are ready in test folder)
