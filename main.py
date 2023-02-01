import json
import datetime
from bson import ObjectId
from flask import Flask, render_template, request, session
import pymongo
import os
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = APP_ROOT + "/static"

myClient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myClient["Smart_BNB"]

app = Flask(__name__)
app.secret_key = "edvarrwrvsdvrge"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/alogin")
def alogin():
    return render_template("alogin.html")

@app.route("/hlogin")
def hlogin():
    return render_template("hlogin.html")

@app.route("/clogin")
def clogin():
    return render_template("clogin.html")


@app.route('/alogin1', methods=['post'])
def alogin1():
    Username = request.form.get("Username")
    Password = request.form.get("Password")
    session['role'] = 'admin'
    if Username == 'admin' and Password == 'admin':
        return render_template("ahome.html")
    else:
        return render_template("msg.html", msg='Invalid Login Details', color='bg-danger')

@app.route("/ahome")
def ahome():
    return render_template("ahome.html")


@app.route("/logout")
def logout():
    return render_template("index.html")

@app.route("/hostReg")
def hostReg():
    return render_template("hostReg.html")

@app.route("/hostReg1",methods = ['post'])
def hostReg1():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    phone  = request.form.get("phone")
    about  = request.form.get("about")
    mycol = mydb["Hosts"]
    total_count = mycol.count_documents({'$or': [{"email": email}, {"phone": phone}]})
    if total_count > 0:
        return render_template("msg.html", msg='Details Already Exists', color='bg-info')
    else:
        mydb.Hosts.insert_one( {"name": name, "email": email, "password": password, "phone": phone, "about": about,"isVerified": "not Verified"})
        return render_template('msg.html', msg='Host Registered  successfully', color='bg-success')



@app.route("/hlogin1", methods=['post'])
def hlogin1():
    email = request.form.get("email")
    password = request.form.get("password")
    mycol = mydb["Hosts"]
    myquery = {"email": email, "password": password}
    total_count = mycol.count_documents(myquery)
    if total_count > 0:
        results = mycol.find(myquery)
        for result in results:
            if result['isVerified'] == 'Verified':
                session['Host_id'] = str(result['_id'])
                session['role'] = 'Host'
                return render_template("hHome.html")
            else:
                return render_template("msg.html", msg=" Your Account Is Not Verified", color='bg-info')
    else:
        return render_template("msg.html", msg="Invalid login details", color='bg-danger')

@app.route("/hHome")
def hHome():
    return render_template("hHome.html")


@app.route("/customerReg")
def customerReg():
    return render_template("customerReg.html")



@app.route("/customerReg1",methods = ['post'])
def customerReg1():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    phone  = request.form.get("phone")
    address  = request.form.get("address")
    mycol = mydb["Customers"]
    total_count = mycol.count_documents({'$or': [{"email": email}, {"phone": phone}]})
    if total_count > 0:
        return render_template("msg.html", msg='Details Already Exists', color='bg-info')
    else:
        mydb.Customers.insert_one(
            {"name": name, "email": email, "password": password, "phone": phone, "address": address})
        return render_template('msg.html', msg='Customer Registered  successfully', color='bg-success')

@app.route("/clogin1", methods=['post'])
def clogin1():
    email = request.form.get("email")
    password = request.form.get("password")
    mycol = mydb["Customers"]
    myquery = {"email": email, "password": password}
    total_count = mycol.count_documents(myquery)
    if total_count > 0:
        results = mycol.find(myquery)
        for result in results:
                session['Customer_id'] = str(result['_id'])
                session['role'] = 'Customer'
                return render_template("chome.html")
    else:
        return render_template("msg.html", msg="Invalid login details", color='bg-danger')

@app.route("/viewHosts")
def viewHosts():
    mycol = mydb["Hosts"]
    query = {}
    Hosts = mycol.find(query)
    return render_template("viewHosts.html",Hosts=Hosts)



@app.route("/HostStatus")
def HostStatus():
    Host_id = ObjectId(request.args.get("Host_id"))
    mycol = mydb["Hosts"]
    query2 = {'$set': {"isVerified": 'Verified'}}
    result = mycol.update_one({'_id': Host_id}, query2)
    return viewHosts()

@app.route("/HostStatus1")
def HostStatus1():
    Host_id = ObjectId(request.args.get("Host_id"))
    mycol = mydb["Hosts"]
    query2 = {'$set': {"isVerified": 'not Verified'}}
    result = mycol.update_one({'_id': Host_id}, query2)
    return viewHosts()


@app.route("/addCategory")
def addCategory():
    return render_template("addCategory.html")

@app.route("/addCategory1",methods=['post'])
def addCategory1():
    categoryName = request.form.get("categoryName")
    categoryIcon = request.form.get("categoryIcon")
    mycol = mydb["Categories"]
    total_count = mycol.count_documents({'$or': [{"categoryName": categoryName}]})
    if total_count > 0:
        return render_template("amsg.html", msg='Details Already Exists', color='bg-info')
    else:
        mydb.Categories.insert_one(
            {"categoryName": categoryName, "categoryIcon": categoryIcon})
        return render_template('amsg.html', msg='Category Added  successfully', color='bg-success')

@app.route("/viewCategories")
def viewCategories():
    mycol = mydb["Categories"]
    query = {}
    Categories = mycol.find(query)
    return render_template("viewCategories.html",Categories=Categories)


@app.route("/viewPlaces")
def viewPlaces():
    mycol = mydb["Places"]
    query = {}
    Places  = mycol.find(query)
    return render_template("viewPlaces.html",Places = Places)

@app.route("/addPlace")
def addPlace():
    return render_template("addPlace.html")

@app.route("/addPlace1",methods=['post'])
def addPlace1():
    placeName = request.form.get("placeName")
    country = request.form.get("country")
    image = request.files["image"]
    path = APP_ROOT + "/Places/" + image.filename
    image.save(path)
    mycol = mydb["Places"]
    total_count = mycol.count_documents({"placeName": placeName, "country":country})
    if total_count > 0:
        return render_template("amsg.html", msg='Details Already Exists', color='bg-info')
    else:
        mydb.Places.insert_one(
            {"placeName": placeName, "country": country,"image":image.filename})
        return render_template('amsg.html', msg='Place Added  successfully', color='bg-success')

@app.route("/postHouseRent")
def postHouseRent():
    mycol = mydb["Categories"]
    query = {}
    Categories = mycol.find(query)
    mycol2 = mydb["Places"]
    query = {}
    Places = mycol2.find(query)
    return render_template("postHouseRent.html",Categories=Categories,Places=Places)

@app.route("/postApartmentRent")
def postApartmentRent():
    mycol = mydb["Categories"]
    query = {}
    Categories = mycol.find(query)
    mycol2 = mydb["Places"]
    query = {}
    Places = mycol2.find(query)
    return render_template("postApartmentRent.html", Categories=Categories,Places=Places)

@app.route("/postCondosRent")
def postCondosRent():
    mycol = mydb["Categories"]
    query = {}
    Categories = mycol.find(query)
    mycol2 = mydb["Places"]
    query = {}
    Places = mycol2.find(query)
    return render_template("postCondosRent.html", Categories=Categories, Places=Places)

@app.route("/postHouseRent1",methods=['post'])
def postHouseRent1():
    Category_id = request.form.get("Category_id")
    Place_id = request.form.get("Place_id")
    houseNumber = request.form.get("houseNumber")
    phone = request.form.get("phone")
    numberOfBedRooms = request.form.get("numberOfBedRooms")
    numberOfRestRooms = request.form.get("numberOfRestRooms")
    propertyType = request.form.get("propertyType")
    areaOccupied = request.form.get("areaOccupied")
    ownerName = request.form.get("ownerName")
    pricePerDay = request.form.get("pricePerDay")
    pricePerMonth = request.form.get("pricePerMonth")
    Pictures = request.files.getlist("Pictures")
    Pictures2 = []
    for Picture in Pictures:
        path = APP_ROOT + "/pictures/" + Picture.filename
        Picture.save(path)
        Pictures2.append(Picture.filename)
    mycol = mydb["Property"]
    mydb.Property.insert_one({"Category_id": ObjectId(Category_id), "Place_id":ObjectId(Place_id),"houseNumber":houseNumber,"phone":phone,
                              "numberOfBedRooms":numberOfBedRooms,"numberOfRestRooms":numberOfRestRooms,
                              "propertyType":propertyType,"areaOccupiede":areaOccupied,"ownerName":ownerName,"pricePerDay":pricePerDay,"pricePerMonth":pricePerMonth,"Pictures":Pictures2,
                              "isAvailableForBooking":"True","Host_id":ObjectId(session['Host_id'])})
    return render_template("Hmsg.html", msg='Property Posted ', color='bg-success')



@app.route("/postApartmentRent1",methods=['post'])
def postApartmentRent1():
    Category_id = request.form.get("Category_id")
    Place_id = request.form.get("Place_id")
    apartmentNumber = request.form.get("apartmentNumber")
    phone = request.form.get("phone")
    numberOfBedRooms = request.form.get("numberOfBedRooms")
    numberOfRestRooms = request.form.get("numberOfRestRooms")
    propertyType = request.form.get("propertyType")
    areaOccupied = request.form.get("areaOccupied")
    carParkingSlots = request.form.get("carParkingSlots")
    pricePerDay = request.form.get("pricePerDay")
    pricePerMonth = request.form.get("pricePerMonth")
    area = request.form.get("area")
    Pictures = request.files.getlist("Pictures")
    Pictures2 = []
    for Picture in Pictures:
        path = APP_ROOT + "/pictures/" + Picture.filename
        Picture.save(path)
        Pictures2.append(Picture.filename)
    mycol = mydb["Property"]
    mydb.Property.insert_one({"Category_id": ObjectId(Category_id), "Place_id":ObjectId(Place_id),"apartmentNumber":apartmentNumber,"phone":phone,
                              "numberOfBedRooms":numberOfBedRooms,"numberOfRestRooms":numberOfRestRooms,
                              "propertyType":propertyType,"areaOccupiede":areaOccupied,"carParkingSlots":carParkingSlots,"pricePerDay":pricePerDay,"pricePerMonth":pricePerMonth,"Pictures":Pictures2,
                              "isAvailableForBooking":"True","area":area,"Host_id":ObjectId(session['Host_id'])})
    return render_template("Hmsg.html", msg='Property Posted ', color='bg-success')


@app.route("/postCondosRent1",methods=['post'])
def postCondosRent1():
    Category_id = request.form.get("Category_id")
    Place_id = request.form.get("Place_id")
    numberOfGuest = request.form.get("numberOfGuest")
    numberOfBedRooms = request.form.get("numberOfBedRooms")
    numberOfRestRooms = request.form.get("numberOfRestRooms")
    propertyType = request.form.get("propertyType")
    numberofBathRooms = request.form.get("numberofBathRooms")
    numberofbeds = request.form.get("numberofbeds")
    pricePerDay = request.form.get("pricePerDay")
    pricePerMonth = request.form.get("pricePerMonth")
    specialities = request.form.get("specialities")
    Pictures = request.files.getlist("Pictures")
    Pictures2 = []
    for Picture in Pictures:
        path = APP_ROOT + "/pictures/" + Picture.filename
        Picture.save(path)
        Pictures2.append(Picture.filename)
    mycol = mydb["Property"]
    mydb.Property.insert_one({"Category_id": ObjectId(Category_id), "Place_id":ObjectId(Place_id),"numberOfGuest":numberOfGuest,
                              "numberOfBedRooms":numberOfBedRooms,"numberOfRestRooms":numberOfRestRooms,
                              "propertyType":propertyType,"numberofBathRooms":numberofBathRooms,"numberofbeds":numberofbeds,"pricePerDay":pricePerDay,"pricePerMonth":pricePerMonth,"Pictures":Pictures2,
                              "isAvailableForBooking":"True","specialities":specialities,"Host_id":ObjectId(session['Host_id'])})
    return render_template("Hmsg.html", msg='Property Posted ', color='bg-success')


@app.route("/ViewHostPosts")
def ViewHostPosts():
    role = session['role']
    mycol = mydb["Categories"]
    query = {}
    Categories = mycol.find(query)
    search = request.args.get("search")
    Category_id = request.args.get("Category_id")
    mycol2 = mydb["Places"]
    query2 = {}
    if search ==None and Category_id ==None:
        Places = mycol2.find(query2)
    elif search !=None and Category_id ==None:
        import re
        rgx = re.compile(".*" + search + ".*", re.IGNORECASE)
        mycol3 = mydb["Places"]
        query3 = {"placeName":rgx}
        Places = mycol3.find(query3)
    elif search ==None and Category_id !=None:
        print("hiiii")
        col = mydb["Property"]
        Properties =col.find({'Category_id': ObjectId(Category_id)})
        col2 = mydb["Places"]
        Places = []
        PlaceIds = []
        for Property in Properties:
            print(Property)
            Place = col2.find_one({"_id":Property['Place_id']})
            if str(Place['_id']) not in PlaceIds:
                Places.append(Place)
                PlaceIds.append(str(Place['_id']))
        print(Places)

    return render_template("ViewHostPosts.html", Categories=Categories, Places=Places, str=str, search=search,role=role)

@app.route("/viewProperty")
def viewProperty():
    role = session['role']
    Place_id = ObjectId(request.args.get("Place_id"))
    propertyType = request.args.get("propertyType");
    if propertyType==None or propertyType=='all':
        query = {"Place_id": Place_id}
    else:
        query = {"Place_id": Place_id,"propertyType":propertyType}
    mycol = mydb["Property"]
    Properties = mycol.find(query)
    return render_template("viewProperty.html",Properties=Properties,getPlace=getPlace,role=role,Place_id=Place_id,propertyType=propertyType)


def getPlace(_id):
    mycol = mydb["Places"]
    query = {"_id": ObjectId(_id)}
    Places = mycol.find_one(query)
    return Places


@app.route("/reserveProperty")
def reserveProperty():
    Property_id = ObjectId(request.args.get("Property_id"))
    pricePerDay = request.args.get("pricePerDay")
    pricePerMonth = request.args.get("pricePerMonth")
    return render_template("reserveProperty.html",Property_id=Property_id,pricePerDay=pricePerDay,pricePerMonth=pricePerMonth)

@app.route("/reserveProperty1",methods=['post'])
def reserveProperty1():
    Property_id = ObjectId(request.form.get("Property_id"))
    pricePerDay = request.form.get("pricePerDay")
    pricePerMonth = request.form.get("pricePerMonth")
    fromDate = request.form.get("fromDate")
    toDate = request.form.get("toDate")
    fromDate2 = fromDate
    toDate2 = toDate
    fromDate = datetime.datetime(*[int(v) for v in fromDate.replace('T', '-').replace(':', '-').split('-')])
    toDate = datetime.datetime(*[int(v) for v in toDate.replace('T', '-').replace(':', '-').split('-')])
    difference =toDate-fromDate
    days_diiference = difference.days
    print(days_diiference)
    month_difference = int(days_diiference/30)
    print(month_difference)
    remain_dates = days_diiference%30
    print(remain_dates)
    month_price = int(pricePerMonth)*month_difference
    print(month_price)
    days_price =int(pricePerDay)*remain_dates
    print(days_diiference)
    total_price = month_price+days_price
    print(total_price)
    if fromDate>toDate:
        return render_template("cmsg.html", msg='Invalid Dates', color='bg-info')
    if checkReserved(fromDate, toDate,Property_id):
        return render_template("cmsg.html", msg='You can not book in these date', color='bg-info')

    return render_template("reserveProperty1.html",total_price=total_price,Property_id=Property_id,fromDate=fromDate2,toDate=toDate2,pricePerMonth=pricePerMonth,pricePerDay=pricePerDay,month_difference=month_difference,remain_dates=remain_dates,int=int)

@app.route("/reserveProperty2",methods=['post'])
def reserveProperty2():
    Property_id = ObjectId(request.form.get("Property_id"))
    total_price = request.form.get("total_price")
    print(total_price)
    fromDate = request.form.get("fromDate")
    toDate = request.form.get("toDate")
    mycol = mydb["Bookings"]
    mydb.Bookings.insert_one(
        {"Property_id": ObjectId(Property_id), "total_price": total_price, "fromDate": fromDate,
         "toDate": toDate, "BookedDate": datetime.datetime.now(),"status":"Property Reserved",
         "Customer_id": ObjectId(session['Customer_id'])})
    return render_template("cmsg.html",msg='Property Reserved',color='bg-success')


@app.route("/chome")
def chome():
    return render_template("chome.html")

@app.route("/viewReservations")
def viewReservations():
    mycol = mydb["Bookings"]
    query = {"Customer_id":ObjectId(session['Customer_id'])}
    details = mycol.find(query)
    details = list(details)
    list.reverse(details)
    return render_template("viewReservations.html",getCustomers=getCustomers,details=details,getProperty=getProperty,getPlaces=getPlaces,str=str,getPlace=getPlace)

def getProperty(Property_id):
    mycol = mydb["Property"]
    query = {"_id": ObjectId(Property_id)}
    properties = mycol.find_one(query)
    print("-----------")
    print(properties)
    return properties


def getCustomers(Customer_id):
    mycol = mydb["Customers"]
    query = {"_id": Customer_id}
    customers = mycol.find_one(query)
    print(customers)
    return customers

def getPlaces(Place_id):
    mycol = mydb["Places"]
    query = {"_id": Place_id}
    places = mycol.find(query)
    print(places)
    return places


@app.route("/viewCustomerReservations")
def viewCustomerReservations():
    Host_id = ObjectId(session['Host_id'])
    mycol2 = mydb["Property"]
    query2 = {"Host_id":Host_id}
    properties = mycol2.find(query2)
    details = []
    for property in properties:
        print(property)
        Property_id = property['_id']
        print(Property_id)
        mycol3 = mydb['Bookings']
        query3 = {"Property_id":Property_id}
        print(query3)
        bookings = mycol3.find(query3)
        for booking in bookings:
            details.append(booking)
        list.reverse(details)
    return render_template("viewCustomerReservations.html",getCustomers=getCustomers,details=details,getProperty=getProperty,getPlaces=getPlaces,getPlace=getPlace)

@app.route("/vacateProperty")
def vacateProperty():
    Booking_id = ObjectId(request.args.get("Booking_id"))
    mycol = mydb["Bookings"]
    query2 = {'$set': {"status": 'Property Vacated'}}
    result = mycol.update_one({'_id': Booking_id}, query2)
    return viewReservations()


@app.route("/vacationConfirmation")
def vacationConfirmation():
    Booking_id = ObjectId(request.args.get("Booking_id"))
    mycol = mydb["Bookings"]
    query2 = {'$set': {"status": 'Property Vacation Confirmed'}}
    result = mycol.update_one({'_id': Booking_id}, query2)
    return viewCustomerReservations()

@app.route("/viewReservedDates")
def viewReservedDates():
    Property_id = request.args.get('Property_id')
    mycol = mydb["Bookings"]
    query = {"Property_id": ObjectId(Property_id), "status": "Property Reserved"}
    Bookings = mycol.find(query)
    return render_template("viewReservedDates.html", Bookings=Bookings)

def checkReserved(fromDate,toDate,Property_id):
    mycol = mydb["Bookings"]
    query = {"Property_id": ObjectId(Property_id), "status": "Property Reserved"}
    print(type(fromDate))
    Bookings = mycol.find(query)
    for Booking in Bookings:
        print('inside')
        fromDateBooked = datetime.datetime(*[int(v) for v in Booking['fromDate'].replace('T', '-').replace(':', '-').split('-')])
        toDateBooked = datetime.datetime(*[int(v) for v in Booking['toDate'].replace('T', '-').replace(':', '-').split('-')])
        if fromDate>=fromDateBooked and fromDate<=toDateBooked:
            return True
        elif toDate>=fromDateBooked and toDate<=toDateBooked:
            return True
        elif fromDate < fromDateBooked and toDate > toDateBooked:
            return True
        print(fromDate>=fromDateBooked)
    return False

app.run(debug=True)