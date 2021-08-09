from flask import Flask
app = Flask(__name__)

from santak import ray_setup

import santak.routes