__author__ = 'med'

from bottle import route, run, template


@route('/perf/<hanachoo>')
def index(hanachoo):
    return template('<b>cpu usage: {{cpu}}</b>!', cpu=hanachoo)


c = 'controller'
run(host=c, port=8181, debug=True)