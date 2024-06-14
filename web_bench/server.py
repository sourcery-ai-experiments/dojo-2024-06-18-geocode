#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from time import sleep

import bjoern
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world() -> str:
    sleep(1e-6)
    return "Hello world!\n"


if __name__ == "__main__":

    bjoern.run(app, "127.0.0.1", 8000)
