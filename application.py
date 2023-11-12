from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import sys
import hashlib


application = Flask(__name__, static_url_path='/static', static_folder='static')
DB = DBhandler()





if __name__ == "__main__":
 application.run(host='0.0.0.0', debug=True)