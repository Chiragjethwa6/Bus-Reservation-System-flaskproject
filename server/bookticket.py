from flask import Flask , render_template , Blueprint
from . import db

book = Blueprint('book',__name__)

@book.route('/bookticket/')
def bookticket():
    render_template("bookingticket.html",busdetail = request.form)