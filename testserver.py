#!/usr/bin/env python

from json import loads
from flask import Flask, request

from model import User, Datastore


app = Flask("codetest")
store = Datastore()


def start_with_flask_server(port):
    app.run(debug=True, port=port)


@app.route("/add_user", methods=["POST"])
def add_user():
    """ request.data -- the body of the request (as a string); will
                        be parsed as JSON.

                        Note that the request object (imported from
                        the flask package) is a context-local proxy
                        containing incoming request data. If you're
                        not familiar with how Flask uses context
                        locals to provide thread-safe objects via
                        a pseudo-global interface, don't worry about
                        it--it just works. (If you're interested,
                        you can read:
        http://flask.pocoo.org/docs/quickstart/#accessing-request-data
                        when you're done with the test.)

    """
    user = User(**loads(request.data))
    userid = store.add(user)
    return userid


@app.route("/users", methods=["GET"])
def list_users():
    return "\n".join([str(u) for u in store if isinstance(u, User)])


@app.route("/data_stats", methods=["GET"])
def data_stats():
    item_types = store.stats()
    return "\n".join([
        "There are {} {}s in the datastore.".format(count, item_type)
        for item_type, count in item_types.most_common()])

@app.route("/reset", methods=["GET"])
def reset():
    store.clear()
    return '{0}'.format(store.size())

@app.route("/size", methods=["GET"])
def size():
    return '{0}'.format(store.size())

@app.route("/count_dependents", methods=["GET"])
def count_dependents():
    return '{0}'.format(store.count_dependents())




if __name__ == "__main__":
    import sys
    port = 5000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    start_with_flask_server(port)
