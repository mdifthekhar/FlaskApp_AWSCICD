from bson import ObjectId
from flask import Flask, redirect, render_template, request, session
import pymongo
import os
import datetime
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

my_client = pymongo.MongoClient("mongodb://localhost:27017")
my_database = my_client["stadium_ticket_booking"]
admin_collection = my_database["admin_collection"]
event_host_collection = my_database["event_host_collection"]
customer_collection = my_database["customer_collection"]
schedule_collection = my_database["schedule_collection"]
teams_collection = my_database["teams_collection"]
bookings_collection = my_database["bookings_collection"]
payments_collection = my_database["payments_collection"]
tickets_collection = my_database["tickets_collection"]

app = Flask(__name__)
app.secret_key = "booking"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin_login")
def admin_login():
    return render_template("admin_login.html")


@app.route("/event_host_login")
def event_host_login():
    return render_template("event_host_login.html")


@app.route("/customer_login")
def customer_login():
    return render_template("customer_login.html")


@app.route("/customer_registration")
def customer_registration():
    return render_template("customer_registration.html")


@app.route("/event_host_registration")
def event_host_registration():
    return render_template("event_host_registration.html")


@app.route("/event_host_login_action", methods=['post'])
def event_host_login_action():
    email = request.form.get("email")
    password = request.form.get("password")
    query = {"email": email, "password": password}
    count = event_host_collection.count_documents(query)
    if count > 0:
        event_host = event_host_collection.find_one(query)
        if event_host['status'] == "Not verified":
            return render_template("message.html", message="Your are not verified")
        else:
            session["event_host_id"] = str(event_host['_id'])
            session['role'] = 'event_host'
            return redirect("/event_host_home")
    else:
        return render_template("message.html", message="Invalid Email or Password")


@app.route("/event_host_registration_action", methods=['post'])
def event_host_registration_action():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    address = request.form.get("address")
    password = request.form.get("password")
    query = {"email": email}
    count = event_host_collection.count_documents(query)
    if count > 0:
        return render_template("message.html", message="Email address already Registered")
    query = {"phone": phone}
    count = event_host_collection.count_documents(query)
    if count > 0:
        return render_template("message.html", message="Phone Number already Registered")
    event_host = {"name": name, "email": email, "phone": phone, "address": address, "password": password, "status":"Not verified"}
    event_host_collection.insert_one(event_host)
    return render_template("message.html", message="Event Registered Successfully")


@app.route("/verify_event_host")
def verify_event_host():
    event_host_id = request.args.get("event_host_id")
    _id = ObjectId(event_host_id)
    query = {"_id": _id}
    query2 = {"$set": {"status": "verified"}}
    event_host_collection.update_one(query, query2)
    return view_event_host()


query = {}
count = admin_collection.count_documents(query)
if count == 0:
    query = {"username": "admin", "password": "admin"}
    admin_collection.insert_one(query)


@app.route("/admin_login_action", methods=['post'])
def admin_login_action():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == "admin" and password == "admin":
        session['role'] = "admin"
        return redirect("/admin_home")
    else:
        return render_template("message.html", message="Invalid Email and password")


@app.route("/view_event_host")
def view_event_host():
    event_hosts = event_host_collection.find({})
    event_hosts = list(event_hosts)
    print(event_hosts)
    return render_template("view_event_host.html", event_hosts=event_hosts)


@app.route("/admin_home")
def admin_home():
    return render_template("admin_home.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/customer_home")
def customer_home():
    return render_template("customer_home.html")


@app.route("/customer_login_action", methods=['post'])
def customer_login_action():
    email = request.form.get("email")
    password = request.form.get("password")
    query = {"email": email, "password": password}
    count = customer_collection.count_documents(query)
    if count > 0:
        customer = customer_collection.find_one(query)
        session["customer_id"] = str(customer['_id'])
        session['role'] = 'customer'
        return redirect("/customer_home")
    else:
        return render_template("message.html", message=" Invalid Email or password")


@app.route("/customer_registration_action", methods=['post'])
def customer_registration_action():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    age = request.form.get("age")
    gender = request.form.get("gender")
    print(name)
    print(email)
    print(phone)
    query = {"email": email}
    count = customer_collection.count_documents(query)
    if count > 0:
        return render_template("message.html", message="Email address already Registered")
    query = {"phone": phone}
    count = customer_collection.count_documents(query)
    if count > 0:
        return render_template("message.html", message="Phone Number already Registered")
    event_host = {"name": name, "email": email, "phone": phone, "password": password, "age": age, "gender": gender}
    customer_collection.insert_one(event_host)
    return render_template("message.html", message="Customer Registered Successfully")


@app.route("/event_host_home")
def event_host_home():
    return render_template("event_host_home.html")


@app.route("/add_schedules")
def add_schedules():
    team_id = request.args.get("team_id")
    return render_template("add_schedules.html", team_id=team_id)


@app.route("/add_schedule_action", methods=['post'])
def add_schedule_action():
    team_id = request.form.get("team_id")
    address = request.form.get("address")
    zone_a_seats = request.form.get("zone_a_seats")
    zone_b_seats = request.form.get("zone_b_seats")
    zone_c_seats = request.form.get("zone_c_seats")
    zone_a_price = request.form.get("zone_a_price")
    zone_b_price = request.form.get("zone_b_price")
    zone_c_price = request.form.get("zone_c_price")
    from_date = request.form.get("from_date")
    to_date = request.form.get("to_date")
    from_date = datetime.datetime.strptime(from_date, "%Y-%m-%dT%H:%M")
    to_date = datetime.datetime.strptime(to_date, "%Y-%m-%dT%H:%M")
    add_schedule = {"team_id": ObjectId(team_id), "address": address, "from_date": from_date, "to_date":to_date, "zone_a_seats": zone_a_seats, "zone_b_seats": zone_b_seats, "zone_c_seats": zone_c_seats, "zone_a_price": zone_a_price, "zone_b_price": zone_b_price, "zone_c_price": zone_c_price}
    schedule_collection.insert_one(add_schedule)
    return render_template("event_host_message.html", message="Schedule Added Successfully")


@app.route("/view_schedules")
def view_schedules():
    team_id = request.args.get("team_id")
    if team_id == None:
        query = {}
    else:
        query = {"team_id": ObjectId(team_id)}
    schedules = schedule_collection.find(query)
    schedules = list(schedules)
    return render_template("view_schedules.html", schedules=schedules, get_team_by_team_id=get_team_by_team_id, datetime=datetime, get_booked_seats_by_schedule_id_and_zone=get_booked_seats_by_schedule_id_and_zone, int=int)


@app.route("/teams")
def teams():
    query = {}
    teams = teams_collection.find(query)
    teams = list(teams)
    return render_template("teams.html", teams=teams)


@app.route("/add_team")
def add_team():
    return render_template("add_team.html")


@app.route("/add_teams_action", methods=['post'])
def add_teams_action():
    game_title = request.form.get("game_title")
    coach_name = request.form.get("coach_name")
    number_of_players = request.form.get("number_of_players")
    number_of_players = int(number_of_players)
    players = []
    for i in range(number_of_players):
        players.append(request.form.get("player_name"+str(i)))

    add_teams = {"game_title": game_title, "coach_name": coach_name, "number_of_players": number_of_players, "players": players}
    teams_collection.insert_one(add_teams)
    return render_template("event_host_message.html", message=" Game added SuccessFully")


def get_team_by_team_id(team_id):
    query = {"_id": team_id}
    team = teams_collection.find_one(query)
    return team


@app.route("/book_tickets", methods=['post'])
def book_tickets():
    zone = request.form.get("zone")
    price = request.form.get("price")
    number_of_seats = request.form.get("number_of_seats")
    schedule_id = request.form.get("schedule_id")
    date = datetime.datetime.now()
    customer_id = session["customer_id"]
    seat_numbers = []
    for seat_number in range(1, int(number_of_seats) + 1):
        selected_seat = request.form.get("seat_number"+str(seat_number))
        if selected_seat!=None:
            seat_numbers.append(seat_number)
    total_price = int(len(seat_numbers)) * int(price)
    query = {"zone": zone, "schedule_id": ObjectId(schedule_id), "seat_numbers": seat_numbers, "customer_id": ObjectId(customer_id), "total_price": total_price, "status": "payment pending", "date": date}
    result = bookings_collection.insert_one(query)
    booking_id = result.inserted_id
    query = {"_id": booking_id}
    booking = bookings_collection.find_one(query)
    print(total_price)
    return render_template("book_tickets.html", booking=booking)


@app.route("/book_ticket_action", methods=['post'])
def book_ticket_action():
    booking_id = request.form.get("booking_id")
    card_type = request.form.get("card_type")
    card_number = request.form.get("card_number")
    holder_name = request.form.get("holder_name")
    cvv_number = request.form.get("cvv_number")
    expire_date = request.form.get("expire_date")
    date = datetime.datetime.now()
    customer_id = session["customer_id"]
    query = {"_id": ObjectId(booking_id)}
    booking = bookings_collection.find_one(query)
    amount =booking['total_price']
    query = {"card_type": card_type, "card_number": card_number, "holder_name": holder_name, "cvv_number": cvv_number, "expire_date":expire_date, "date": date, "customer_id": ObjectId(customer_id), "amount": amount, "booking_id": ObjectId(booking_id) }
    payments_collection.insert_one(query)
    for seat_number in booking['seat_numbers']:
        name = request.form.get("name"+str(seat_number))
        age = request.form.get("age"+str(seat_number))
        gender = request.form.get("gender"+str(seat_number))
        query = {"name": name, "age": age, "gender": gender, "seat_number": seat_number, "date": date, "booking_id": ObjectId(booking_id)}
        tickets_collection.insert_one(query)
    query1 = {"_id": ObjectId(booking_id)}
    query2 = {"$set": {"status": "Booked"}}
    bookings_collection.update_one(query1, query2)
    return render_template("customer_message.html", message="Ticket Booked SuccessFully")


@app.route("/view_layouts", methods=['post'])
def view_layouts():
    schedule_id = request.form.get("schedule_id")
    zone = request.form.get("zone")
    price = request.form.get("price")
    number_of_seats = request.form.get("number_of_seats")
    print(schedule_id)
    print(zone)
    print(price)
    print(number_of_seats)
    return render_template("view_layouts.html", schedule_id=schedule_id, zone=zone, price=price, number_of_seats=number_of_seats, int=int, if_seat_booked_in_schedule_of_time_zone=if_seat_booked_in_schedule_of_time_zone)


def if_seat_booked_in_schedule_of_time_zone(schedule_id, zone, seat_number):
    query = {"schedule_id": ObjectId(schedule_id), "zone": zone, "seat_numbers": seat_number, "status": "Booked"}
    print(query)
    count = bookings_collection.count_documents(query)
    print(count)
    if count > 0:
        return True
    else:
        return False


@app.route("/view_tickets")
def view_tickets():
    return render_template("view_tickets.html")


@app.route("/view_bookings")
def view_bookings():
    if session['role'] == 'event_host':
        schedule_id = request.args.get("schedule_id")
        zone = request.args.get("zone")
        query = {"schedule_id": ObjectId(schedule_id), "zone": zone}
    elif session['role'] == 'customer':
        customer_id = session['customer_id']
        query = {"customer_id": ObjectId(customer_id)}
    print(query)
    bookings = bookings_collection.find(query)
    bookings = list(bookings)
    bookings.reverse()
    print(bookings)
    return render_template("view_bookings.html", bookings=bookings, get_schedule_by_schedule_id=get_schedule_by_schedule_id, get_team_by_team_id=get_team_by_team_id, get_customer_by_customer_id=get_customer_by_customer_id, get_ticket_by_booking_id=get_ticket_by_booking_id, get_payment_by_booking_id=get_payment_by_booking_id)


def get_schedule_by_schedule_id(schedule_id):
    query = {"_id": schedule_id}
    schedule = schedule_collection.find_one(query)
    return schedule


def get_team_by_team_id(team_id):
    query = {"_id": team_id}
    team = teams_collection.find_one(query)
    return team


def get_customer_by_customer_id(customer_id):
    query = {"_id": customer_id}
    customer = customer_collection.find_one(query)
    return customer


def get_ticket_by_booking_id(booking_id):
    query = {"booking_id": booking_id}
    booking = bookings_collection.find_one(query)
    return booking


def get_payment_by_booking_id(booking_id):
    query = {"booking_id": booking_id}
    payment = payments_collection.find_one(query)
    return payment


@app.route("/cancel_bookings")
def cancel_bookings():
    booking_id = request.args.get("booking_id")
    query1 = {"_id": ObjectId(booking_id)}
    query2 = {"$set": {"status": "Cancelled"}}
    bookings_collection.update_one(query1, query2)
    query1 = {"booking_id": ObjectId(booking_id)}
    query2 = {"$set": {"status": "Payment Refunded"}}
    payments_collection.update_one(query1, query2)
    return render_template("customer_message.html", message=" Booking Cancelled")


def get_booked_seats_by_schedule_id_and_zone(schedule_id, zone):
    query = {"schedule_id": ObjectId(schedule_id), "zone": zone, "status": "Booked"}
    bookings = bookings_collection.find(query)
    bookings = list(bookings)
    print(bookings)
    booked_seats = 0
    for booking in bookings:
        booked_seats = booked_seats + len(booking['seat_numbers'])
    return booked_seats


#app.run(host="0.0.0.0", port=5000)

