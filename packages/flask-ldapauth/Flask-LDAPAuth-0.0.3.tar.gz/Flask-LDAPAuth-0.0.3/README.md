# OS Dependencies

Debian

```bash
apt install python3-dev libldap2-dev libsasl2-dev
```

Centos

```bash
yum install python3-devel openldap-devel.x86_64 libgsasl-devel.x86_64
```

Alpine

```bash
apk add musl-dev openldap-dev gcc libgsasl-dev
```

# Install

```bash
pip install Flask-LDAPAuth
```

# Settings

App configs

| NAME              | Default |
| ----------------- | ------- |
| LDAP_URL          | None    |
| LDAP_ROOTDN       | None    |
| LDAP_USERDN       | None    |
| LDAP_GROUP        | False   |
| LDAP_START_TLS    | True    |
| LDAP_USER_FILTER  | 'cn'    |
| LDAP_TIMEOUT      | 10      |
| SECRET_KEY        | None    |
| LDAP_TOKEN_EXPIRE | 8       |

# Examples

## Simple User Authentication

```python
from flask import Flask, jsonify, make_response
from flask_ldapauth import LDAPAuth

app = Flask(__name__)

app.config['LDAP_URL'] = "ldap://localhost:389"
app.config['LDAP_ROOTDN'] = "dc=localhost"
app.config['LDAP_USERDN'] = "ou=People,dc=localhost"

auth = LDAPAuth(app)

@app.route('/login')
def index():
    user = auth.connect(username='nmacias',
                        password='password')

    if user is False:
        return jsonify({'mesg': 'invalid username or password'}), 401

    return jsonify({'mesg': 'login'})

def run():
    app.config['DEBUG'] = True
    app.config['ENV'] = 'development'
    app.run()


def main():
    run()


if __name__ == '__main__':
    main()
```

## Advance User Authenciation

- Only allow user if part of a group
- Create auth token cookies
- Protect routes
- Return JSON data on protected routes

```python
from flask import Flask, jsonify, make_response
from flask_ldapauth import LDAPAuth

app = Flask(__name__)


app.config['LDAP_URL'] = "ldap://localhost:389"
app.config['LDAP_ROOTDN'] = "dc=localhost"
app.config['LDAP_USERDN'] = "ou=People,dc=localhost"
app.config['LDAP_GROUP'] = "admins"

app.config['SECRET_KEY'] = 'supersecretkey'

auth = LDAPAuth(app)


@app.route('/protected', methods=['GET', 'POST'])
@auth.protected(data=True)
def propected(data):

    return jsonify({'mesg': 'Top secret', 'name': data['name']})


@app.route('/login')
def login():
    user = auth.connect(username='nmacias',
                        password='password', return_user=True)

    if user is False:
        return jsonify({'mesg': 'invalid username or password'}), 401

    token = auth.token.create(payload=user)

    response = make_response(jsonify({'token': token}))

    response.set_cookie('token', value=token, httponly=True)

    return response


@app.route('/logout')
def logout():

    response = make_response(jsonify({}))
    response.set_cookie('token', expires=0)

    return response


@app.route('/validate/<token>')
def validate(token):

    token_validate = auth.token.validate(token=token)

    if token_validate is False:
        return jsonify({'mesg': 'Invalid token'}), 401

    return jsonify({})


def run():
    app.config['DEBUG'] = True
    app.config['ENV'] = 'development'
    app.run()


def main():
    run()


if __name__ == '__main__':
    main()

```
