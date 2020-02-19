"""

- A simple application that allows the user to pull time from Toggl for import (by gui automation into a timer application)
- Features:
    - allow the user to define their own API key
        - this key should be saved on user side
    - allow user to view their workspaces and to choose one to pull time from
    - allow user to specify their own parser plugin or gui automation tool
- Implementation
    - define controller on python side
    - define single screen for user interaction
- Look into
    - can we make writing the HTML easy? Templating lang? Drag and drop?



"""

from flask import Flask, Response, request
from typing import List, Tuple, Iterable
from requests import get

app = Flask(__name__)


@app.route("/workspaces")
def get_workspaces():
    pass

"""
Taken from a comment I made on 2020-02-18:
Just a thought here: what if we could add values to container classes on the
 Python side then, when a request came in, we could use those containers to populate
  values in some HTML and respond with the updated HTML? 
  That would solve our problem, right? There'd be control references on the 
  Python side, and the client wouldn't have to do more than request some new information
   for a particular control or group of controls.

TODO : TRY THIS FOR THE WORKSPACES ENDPOINT

"""


@app.route("/apiKey", methods=['GET', 'PUT'])
def api_key():
    if request.method == 'PUT':
        pass  # TODO save the key