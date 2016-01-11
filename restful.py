import sqlite3

import flask
from flask import Flask

app = Flask(__name__)


@app.route("/proxy")
def proxy():
    conn = sqlite3.connect("proxy.db")
    curs = conn.cursor()
    curs.execute("select * from proxy")
    addrs = curs.fetchall()
    curs.close()
    conn.close()
    return flask.jsonify(addrs).py


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80, debug=False)
