from datetime import datetime

import rethinkdb as r
from flask import Flask, redirect, url_for, g, request
from rethinkdb import RqlRuntimeError

from .api import bp as api
from .config import config
from .logs import bp as logs
from .templates import bp as templates
from .tokens import bp as tokens

app = Flask(__name__)

RDB_HOST = config.database.host
RDB_PORT = config.database.port
RDB_DATABASE = config.database.database
timezone = config.r_timezone


def db_setup():
    conn = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db_create(RDB_DATABASE).run(conn)
    except RqlRuntimeError:
        print('Database already exists.')
    try:
        r.table_create('logs').run(conn)
    except RqlRuntimeError:
        print('Logs table already exists.')
    try:
        r.table_create('tokens').run(conn)
    except RqlRuntimeError:
        print('Tokens table already exists.')
    try:
        r.table_create('templates').run(conn)
    except RqlRuntimeError:
        print('Templates table already exists.')


db_setup()


@app.before_request
def setup_rdb():
    g.rdb_conn = r.connect(host=RDB_HOST, port=RDB_PORT, db=RDB_DATABASE)


@app.teardown_request
def teardown_rdb(exception):
    auth = request.headers.get('authorization')
    if auth:
        r.table('tokens').filter({'id': auth}).update({'last_used': datetime.now(timezone)}).run(g.rdb_conn)
    g.rdb_conn.close()


@app.route('/')
def hello_world():
    return redirect(url_for('remotelogging.server.tokens.tokens'))


app.register_blueprint(tokens, url_prefix='/tokens')
app.register_blueprint(templates, url_prefix='/templates')
app.register_blueprint(logs, url_prefix='/logs')
app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run()
