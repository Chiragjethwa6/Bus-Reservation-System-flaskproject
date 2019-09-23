from flask import Flask,render_template,Blueprint,request
from . import db

main = Blueprint('main',__name__)

@main.route("/")
def homePage() :
    return render_template('index2.html')

@main.route("/searchbus")
def searchBusPage() :
    return render_template("searchbus.html")

@main.route("/searchbus",methods=['POST'])
def searchBus() :
    source = request.form['source']
    dest = request.form['dest']
    jdate = request.form['jdate']
    bus_class = request.form['bus_class']

    results = db.session.execute("select * from busses where busses.bus_no in(select bus_no from bus_stops where bus_stops.stop_id = (select stop_id from stops where stops.name = :source) intersect select bus_no from bus_stops where bus_stops.stop_id = (select stop_id from stops where stops.name = :dest))",{'source':source ,'dest':dest})
    
    return render_template('.html',results = results)



