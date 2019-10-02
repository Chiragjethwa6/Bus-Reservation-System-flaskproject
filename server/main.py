from flask import Flask,render_template,Blueprint,request,json,Response
from . import db

main = Blueprint('main',__name__)

def getStopsData() :

    stops = db.session.execute("select stop_name from stops")
    stops_data = [str(r[0]) for r in stops]
    return json.dumps(stops_data)

@main.route("/")
def homePage() :
    return render_template('index.html', stops = getStopsData())

@main.route("/searchbus/")
def searchBusPage() :
    return render_template("searchbus.html",stops = getStopsData(), results = [])


@main.route("/searchbus/",methods=['POST'])
def searchBus() :
    source = request.form['source']
    dest = request.form['dest']
    jdate = request.form['jdate']
    bus_class = request.form['bus_class']
    SQL_final = "select * from ( select  * from (select * from busses where busno in  (select busno from bus_stops where stop_id in (select stop_id  from stops where stops.stop_name = :source or stops.stop_district = :source) intersect select busno from bus_stops where stop_id in (select stop_id from stops where stops.stop_name = :dest or stops.stop_district = :dest ))) as q1 inner join bus_class on q1.bclass = bus_class.bclass ) as q2 left outer join  (select * from bus_object where bus_date = :jdate) as q3 on q2.busno = q3.busno"
    SQL_final2 = "select * from ( select  * from (select * from busses where busno in  (select busno from bus_stops where stop_id in (select stop_id  from stops where stops.stop_name = :source or stops.stop_district = :source) intersect select busno from bus_stops where stop_id in (select stop_id from stops where stops.stop_name = :dest or stops.stop_district = :dest ))) as q1 inner join ( select * from bus_class where bclass = :busclass) as q4 on q1.bclass = q4.bclass ) as q2 left outer join  (select * from bus_object where bus_date = :jdate) as q3 on q2.busno = q3.busno"
 
    if bus_class  != "ANY" :
        results = db.session.execute(SQL_final2,{'source':source ,'dest':dest,'jdate':jdate ,'busclass' : bus_class})
    else :
        results = db.session.execute(SQL_final,{'source':source ,'dest':dest,'jdate':jdate})
    return render_template('searchbus.html',formdetails = request.form,results = results,stops = getStopsData())

# select *
# from ( select  *
# 	from (select * 
# 		from busses
# 		where busno in  (select busno
# 						 from bus_stops
# 						 where stop_id in (select stop_id 
# 										 from stops
# 										 where stops.stop_name = 'pune' or stops.stop_district = 'pune') 
# 						intersect 
# 						select busno 
# 						from bus_stops 
# 						where stop_id in (select stop_id 
# 										from stops 
# 										where stops.stop_name = 'mumbai' or stops.stop_district = 'mumbai' )
#         )) as q1 inner join (select * from bus_class where bclass = :busclass) as q5 on q1.bclass = q5.bclass
#     ) as q2 left outer join  
# (select * 
# from bus_object
# where bus_date = '10-08-2019') as q3
# on q2.busno = q3.bus_no 
