import rethinkdb as r
from flask import Blueprint, render_template, g, redirect, request, url_for

from remotelogging.server.util import requires_auth, variables

bp = Blueprint(__name__, __name__)


@bp.route('/')
@requires_auth
def list_templates():
    return render_template('templates.html', templates=r.table('templates').run(g.rdb_conn))


@bp.route('/new/', methods=['GET'])
@requires_auth
def add_template():
    return render_template('add_template.html', error=request.args.get('error', None))


@bp.route('/new/', methods=['POST'])
@requires_auth
def do_add_template():
    name = request.form.get('name', None)
    id = request.form.get('id', None)
    text = request.form.get('text', None)

    if name is None or len(name) < 4:
        return redirect(url_for('.add_template', error="Name too short or missing"))
    if id is None or len(id) < 4:
        return redirect(url_for('.add_template', error="Id too short or missing"))
    if r.table('templates').filter({'id': id}).count().run(g.rdb_conn):
        return redirect(url_for('.add_template', error="Duplicate id. try editing"))
    if text is None or len(text) < 2:
        return redirect(url_for('.add_template', error="Text too short or missing"))

    r.table('templates').insert({'id': id, 'name': name, 'text': text, 'vars': variables(text)}).run(g.rdb_conn)

    return redirect(url_for('.list_templates'))
