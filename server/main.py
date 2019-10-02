from flask import Flask,render_template,Blueprint,request,json,Response
from . import db

main = Blueprint('main',__name__)

@main.route("/")
def homePage() :
    stops = db.session.execute("select bclass from bus_class")
    stops_data = [str(r[0]) for r in stops]
    print(stops_data)
    return render_template('index.html',stops = json.dumps(stops_data))

@main.route("/searchbus/")
def searchBusPage() :
    stops = db.session.execute("select stop_name from stops")
    return render_template("searchbus.html",jsonify(stops = stops), results = [])

@main.route("/searchbus_autocomplete/")
def searchbus_autocomplete() :
    search = request.args.get('term')
    stops = db.session.execute("select bclass from bus_class")
    stops_data = [str(r[0]) for r in stops]
    print(stops_data)
    return Response(json.dumps(stops_data))

@main.route("/searchbus/",methods=['POST'])
def searchBus() :
    source = request.form['source']
    dest = request.form['dest']
    jdate = request.form['jdate']
    bus_class = request.form['bus_class']
    SQL_final = "select * from ( select  * from (select * from busses where busno =  (select busno from bus_stops where stop_id = (select stop_id  from stops where stops.stop_name = :source or stops.stop_district = :source) intersect select busno from bus_stops where stop_id = (select stop_id from stops where stops.stop_name = :dest or stops.stop_district = :dest ))) as q1 inner join bus_class on q1.bclass = bus_class.bclass ) as q2 left outer join  (select * from bus_object where bus_date = :jdate) as q3 on q2.busno = q3.busno"
    results = db.session.execute(SQL_final,{'source':source ,'dest':dest,'jdate':jdate})
    return render_template('searchbus.html',formdetail = request.form,results = results)



# select *
# from ( select  *
# 	from (select * 
# 		from busses
# 		where busno =  (select busno
# 						 from bus_stops
# 						 where stop_id = (select stop_id 
# 										 from stops
# 										 where stops.stop_name = 'pune' or stops.stop_district = 'pune') 
# 						intersect 
# 						select busno 
# 						from bus_stops 
# 						where stop_id = (select stop_id 
# 										from stops 
# 										where stops.stop_name = 'mumbai' or stops.stop_district = 'mumbai' )
#         )) as q1 inner join bus_class on q1.bclass = bus_class.bclass
#     ) as q2 left outer join  
# (select * 
# from bus_object
# where bus_date = '10-08-2019') as q3
# on q2.busno = q3.bus_no 
