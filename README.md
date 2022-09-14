**EasyTasker - Simple web based tasker.**

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
- [Falcon](https://falcon.readthedocs.io/en/stable/) (WSGI framework)
- [TinyDB](https://tinydb.readthedocs.io/en/latest/index.html) (pure Python NoSQL database)
- [BCrypt](https://github.com/pyca/bcrypt/) (password hashing tool and crypto algorithm)
- [Mako](https://www.makotemplates.org/) (fast html template system for Python)

**Dependencies for default local run:**
- [hupper](https://github.com/Pylons/hupper)
- [waitress](https://github.com/Pylons/waitress)

Every dependencies are included in requirements.txt. If you want to use another server and you don't need reloader, then you can uninstall or don't need to install hupper and waitress (in this case you will need to change local_run() function in [easytasker.py](https://github.com/jiri-one/easytasker_falcon/blob/main/easytasker.py) file maybe, for local development/run).

**Login:**
Three accounts are created for preview and tests, so you can use them:

```
deso:heslo
deso2:heslo
deso3:heslo
```
But you can (and you should) register your own account.

**Tests:** 
- [![Tests (PyTest)](https://github.com/jiri-one/easytasker_falcon/actions/workflows/tests.yml/badge.svg)](https://github.com/jiri-one/easytasker_falcon/actions/workflows/tests.yml)
- created in pytest (install it with `pip install pytest`)
- helpers for pytest are flacon.inspect and flacon.testing
- tests are completely independent of main db or user db
- NOT FINISHED YET (more test will come later)
