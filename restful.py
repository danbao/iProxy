import flask
import sqlite3
from flask import Flask

app = Flask(__name__)


@app.route("/proxy")
def restful():
    try:
        conn = sqlite3.connect("./proxy.db")
        curs = conn.cursor()
        curs.execute("select * from proxy")
        addrs = curs.fetchall()
        curs.close()
        conn.close()
        return flask.jsonify(addrs)
    except sqlite3.Error:
        return "Wait a minute..."


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8083, debug=False)
