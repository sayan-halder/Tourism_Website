import mysql.connector
from flask import Flask, request, render_template

app = Flask(__name__)

dataBase = mysql.connector.connect(host="localhost", user="root", password="")
cursorObject = dataBase.cursor()
cursorObject.execute("CREATE DATABASE IF NOT EXISTS Tourism")
dataBase.close()

db_connection = mysql.connector.connect(host="localhost", user="root", password="", database="Tourism")

cid = 9
bid = 999


def generateCustomerID():
    global cid

    cursor = db_connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM customerregistration')
    row_count = cursor.fetchone()[0]

    if row_count > 0:
        query = "SELECT Customer_ID from customerregistration"
        cursor.execute(query)
        result_set = cursor.fetchall()
        for row in result_set:
            x = row
        cid = int(x[-1]) + 1
        return cid
    else:
        cid += 1
        return cid


def generateBookingID():
    global bid

    cursor = db_connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM touristcity')
    row_count = cursor.fetchone()[0]

    if row_count > 0:
        query = "SELECT Booking_ID from touristcity"
        cursor.execute(query)
        result_set = cursor.fetchall()
        for row in result_set:
            x = row
        bid = int(x[-1]) + 1
        return bid
    else:
        bid += 1
        return bid


@app.route('/')
def index():
    table_cursor = db_connection.cursor()
    table_query = """
        CREATE TABLE IF NOT EXISTS CustomerRegistration (
            Customer_ID VARCHAR(255) PRIMARY KEY,
            First_Name VARCHAR(255),
            Last_Name VARCHAR(255),
            Email_ID VARCHAR(255),
            Password VARCHAR(255)
        )
        """
    table_cursor.execute(table_query)

    table_query = """
                    CREATE TABLE IF NOT EXISTS TouristCity (
                        Booking_ID VARCHAR(255) PRIMARY KEY,
                        Customer_Name VARCHAR(255),
                        Departing_City VARCHAR(255),
                        Destination_City VARCHAR(255),
                        Traveling_Mode VARCHAR(255),
                        Departure_Date VARCHAR(255),
                        Tourist_Spot VARCHAR(255),
                        Total_Price VARCHAR(255),
                        Customer_ID VARCHAR(255)
                    )
                    """
    table_cursor.execute(table_query)
    table_cursor.close()
    return render_template('index.html')


@app.route('/adminLogin')
def adminLogin():
    return render_template('adminLogin.html')


@app.route('/adminLogin_', methods=['POST'])
def adminLogin_():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == "admin@gmail.com" and password == "admin":
            select_cursor = db_connection.cursor()
            select_query = "SELECT * FROM TouristCity"
            select_cursor.execute(select_query)
            result_set = select_cursor.fetchall()
            select_cursor.close()
            return render_template('adminAllBookings.html', result_set=result_set)
        else:
            return render_template('adminLoginpopup1.html')


@app.route('/adminAllBookings')
def adminAllBookings():
    select_cursor = db_connection.cursor()
    select_query = "SELECT * FROM TouristCity"
    select_cursor.execute(select_query)
    result_set = select_cursor.fetchall()
    select_cursor.close()
    return render_template('adminAllBookings.html', result_set=result_set)


@app.route('/adminViewBill/<string:booking_id>')
def adminViewBill(booking_id):
    cursor = db_connection.cursor()

    query = "SELECT * from touristcity"
    cursor.execute(query)
    result_set = cursor.fetchall()

    for row in result_set:
        if booking_id == row[0]:
            return render_template('adminViewBill.html', row=row)


@app.route('/adminDelete/<string:booking_id>')
def adminDelete(booking_id):
    cursor = db_connection.cursor()

    query = "SELECT * from touristcity"
    cursor.execute(query)
    result_set = cursor.fetchall()

    for row in result_set:
        if booking_id == row[0]:
            delete_query = "DELETE FROM touristcity WHERE booking_id = %s"
            cursor.execute(delete_query, (booking_id,))
            db_connection.commit()
            return render_template('adminDeletepopup.html', row=row)


@app.route('/adminLoginpopup1')
def adminLoginpopup1():
    return render_template('adminLoginpopup1.html')


@app.route('/adminLoginpopup2')
def adminLoginpopup2():
    return render_template('adminLoginpopup2.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/destinations')
def destinations():
    return render_template('destinations.html', customer_name=customer_name)


@app.route('/bangalore')
def bangalore():
    return render_template('bangalore.html', customer_name=customer_name)


@app.route('/chennai')
def chennai():
    return render_template('chennai.html', customer_name=customer_name)


@app.route('/delhi')
def delhi():
    return render_template('delhi.html', customer_name=customer_name)


@app.route('/hyderabad')
def hyderabad():
    return render_template('hyderabad.html', customer_name=customer_name)


@app.route('/jaipur')
def jaipur():
    return render_template('jaipur.html', customer_name=customer_name)


@app.route('/kolkata')
def kolkata():
    return render_template('kolkata.html', customer_name=customer_name)


@app.route('/lucknow')
def lucknow():
    return render_template('lucknow.html', customer_name=customer_name)


@app.route('/mumbai')
def mumbai():
    return render_template('mumbai.html', customer_name=customer_name)


@app.route('/pune')
def pune():
    return render_template('pune.html', customer_name=customer_name)


@app.route('/udupi')
def udupi():
    return render_template('udupi.html', customer_name=customer_name)


@app.route('/bookings')
def bookings():
    return render_template('bookings.html')


@app.route('/indexpopup3')
def indexpopup3():
    return render_template('indexpopup3.html')


@app.route('/indexpopup4')
def indexpopup4():
    return render_template('indexpopup4.html')


@app.route('/CustomerRegistration', methods=['POST'])
def CustomerRegistration():
    insert_cursor = db_connection.cursor()
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        customer_id = generateCustomerID()

        insert_query = "INSERT INTO CustomerRegistration (Customer_ID, First_Name, Last_Name, Email_ID, Password) " \
                       "VALUES (%s, %s, %s, %s, %s)"
        insert_cursor.execute(insert_query, (customer_id, fname, lname, email, password))
        db_connection.commit()
        insert_cursor.close()

    return render_template('registerpopup.html')


@app.route('/Login', methods=['POST'])
def Login():
    check_cursor = db_connection.cursor()

    query = "SELECT customer_id, first_name, last_name, email_id, password from customerregistration"
    check_cursor.execute(query)
    result_set = check_cursor.fetchall()

    global customer_name

    if request.method == 'POST':
        emid = request.form['email']
        pwd = request.form['password']

    global cust_id

    for row in result_set:
        cust_id, first_name, last_name, email_id, password = row
        if email_id == emid and password == pwd:
            customer_name = f"{first_name} {last_name}"
            return render_template('indexpopup1.html')
    else:
        return render_template('indexpopup2.html')

    check_cursor.close()


@app.route('/BangaloreTourist', methods=['POST', 'PATCH'])
def BangaloreTourist():
    insert_cursor = db_connection.cursor()
    if request.method == 'POST':
        dept_city = request.form['departing-city']
        des_city = "Bangalore"
        trav_mode = request.form['vehicle']
        dept_date = request.form['departure-date']
        tourist_spot = request.form.getlist('tourist-spot')
        total_price = request.form.get('total-price-input')

        spot = ""
        for ts in tourist_spot:
            spot += ts + ","

        booking_ID = generateBookingID()

        result = []
        result.append(booking_ID)
        result.append(customer_name)
        result.append(dept_city)
        result.append(des_city)
        result.append(trav_mode)
        result.append(dept_date)
        result.append(tourist_spot)
        result.append(total_price)

        insert_query = "INSERT INTO TouristCity (Booking_ID, Customer_Name, Departing_City, Destination_City, " \
                       "Traveling_Mode, Departure_Date, Tourist_Spot, Total_Price, Customer_ID) VALUES (%s, %s, " \
                       "%s, %s, %s, %s, %s, %s, %s)"
        insert_cursor.execute(insert_query,
                              (booking_ID, customer_name, dept_city, des_city, trav_mode, dept_date, spot, total_price,
                               cust_id))

        db_connection.commit()
        insert_cursor.close()

    return render_template('bookings.html', result=result)


@app.route('/ChennaiTourist', methods=['POST', 'PATCH'])
def ChennaiTourist():
    insert_cursor = db_connection.cursor()
    if request.method == 'POST':
        dept_city = request.form['departing-city']
        des_city = "Chennai"
        trav_mode = request.form['vehicle']
        dept_date = request.form['departure-date']
        tourist_spot = request.form.getlist('tourist-spot')
        total_price = request.form.get('total-price-input')

        spot = ""
        for ts in tourist_spot:
            spot += ts + ","

        booking_ID = generateBookingID()

        result = []
        result.append(booking_ID)
        result.append(customer_name)
        result.append(dept_city)
        result.append(des_city)
        result.append(trav_mode)
        result.append(dept_date)
        result.append(tourist_spot)
        result.append(total_price)

        insert_query = "INSERT INTO TouristCity (Booking_ID, Customer_Name, Departing_City, Destination_City, " \
                       "Traveling_Mode, Departure_Date, Tourist_Spot, Total_Price, Customer_ID) VALUES (%s, %s, " \
                       "%s, %s, %s, %s, %s, %s, %s)"
        insert_cursor.execute(insert_query,
                              (booking_ID, customer_name, dept_city, des_city, trav_mode, dept_date, spot, total_price,
                               cust_id))

        db_connection.commit()
        insert_cursor.close()

    return render_template('bookings.html', result=result)


@app.route('/DelhiTourist', methods=['POST', 'PATCH'])
def DelhiTourist():
    insert_cursor = db_connection.cursor()
    if request.method == 'POST':
        dept_city = request.form['departing-city']
        des_city = "Delhi"
        trav_mode = request.form['vehicle']
        dept_date = request.form['departure-date']
        tourist_spot = request.form.getlist('tourist-spot')
        total_price = request.form.get('total-price-input')

        spot = ""
        for ts in tourist_spot:
            spot += ts + ","

        booking_ID = generateBookingID()

        result = []
        result.append(booking_ID)
        result.append(customer_name)
        result.append(dept_city)
        result.append(des_city)
        result.append(trav_mode)
        result.append(dept_date)
        result.append(tourist_spot)
        result.append(total_price)

        insert_query = "INSERT INTO TouristCity (Booking_ID, Customer_Name, Departing_City, Destination_City, " \
                       "Traveling_Mode, Departure_Date, Tourist_Spot, Total_Price, Customer_ID) VALUES (%s, %s, " \
                       "%s, %s, %s, %s, %s, %s, %s)"
        insert_cursor.execute(insert_query,
                              (booking_ID, customer_name, dept_city, des_city, trav_mode, dept_date, spot, total_price,
                               cust_id))

        db_connection.commit()
        insert_cursor.close()

    return render_template('bookings.html', result=result)


@app.route('/HyderabadTourist', methods=['POST', 'PATCH'])
def HyderabadTourist():
    insert_cursor = db_connection.cursor()
    if request.method == 'POST':
        dept_city = request.form['departing-city']
        des_city = "Hyderabad"
        trav_mode = request.form['vehicle']
        dept_date = request.form['departure-date']
        tourist_spot = request.form.getlist('tourist-spot')
        total_price = request.form.get('total-price-input')

        spot = ""
        for ts in tourist_spot:
            spot += ts + ","

        booking_ID = generateBookingID()

        result = []
        result.append(booking_ID)
        result.append(customer_name)
        result.append(dept_city)
        result.append(des_city)
        result.append(trav_mode)
        result.append(dept_date)
        result.append(tourist_spot)
        result.append(total_price)

        insert_query = "INSERT INTO TouristCity (Booking_ID, Customer_Name, Departing_City, Destination_City, " \
                       "Traveling_Mode, Departure_Date, Tourist_Spot, Total_Price, Customer_ID) VALUES (%s, %s, " \
                       "%s, %s, %s, %s, %s, %s, %s)"
        insert_cursor.execute(insert_query,
                              (booking_ID, customer_name, dept_city, des_city, trav_mode, dept_date, spot, total_price,
                               cust_id))

        db_connection.commit()
        insert_cursor.close()

    return render_template('bookings.html', result=result)


@app.route('/JaipurTourist', methods=['POST', 'PATCH'])
def JaipurTourist():
    insert_cursor = db_connection.cursor()
    if request.method == 'POST':
        dept_city = request.form['departing-city']
        des_city = "Jaipur"
        trav_mode = request.form['vehicle']
        dept_date = request.form['departure-date']
        tourist_spot = request.form.getlist('tourist-spot')
        total_price = request.form.get('total-price-input')

        spot = ""
        for ts in tourist_spot:
            spot += ts + ","

        booking_ID = generateBookingID()

        result = []
        result.append(booking_ID)
        result.append(customer_name)
        result.append(dept_city)
        result.append(des_city)
        result.append(trav_mode)
        result.append(dept_date)
        result.append(tourist_spot)
        result.append(total_price)

        insert_query = "INSERT INTO TouristCity (Booking_ID, Customer_Name, Departing_City, Destination_City, " \
                       "Traveling_Mode, Departure_Date, Tourist_Spot, Total_Price, Customer_ID) VALUES (%s, %s, " \
                       "%s, %s, %s, %s, %s, %s, %s)"
        insert_cursor.execute(insert_query,
                              (booking_ID, customer_name, dept_city, des_city, trav_mode, dept_date, spot, total_price,
                               cust_id))

        db_connection.commit()
        insert_cursor.close()

    return render_template('bookings.html', result=result)


@app.route('/KolkataTourist', methods=['POST', 'PATCH'])
def KolkataTourist():
    insert_cursor = db_connection.cursor()
    if request.method == 'POST':
        dept_city = request.form['departing-city']
        des_city = "Kolkata"
        trav_mode = request.form['vehicle']
        dept_date = request.form['departure-date']
        tourist_spot = request.form.getlist('tourist-spot')
        total_price = request.form.get('total-price-input')

        spot = ""
        for ts in tourist_spot:
            spot += ts + ","

        booking_ID = generateBookingID()

        result = []
        result.append(booking_ID)
        result.append(customer_name)
        result.append(dept_city)
        result.append(des_city)
        result.append(trav_mode)
        result.append(dept_date)
        result.append(tourist_spot)
        result.append(total_price)

        insert_query = "INSERT INTO TouristCity (Booking_ID, Customer_Name, Departing_City, Destination_City, " \
                       "Traveling_Mode, Departure_Date, Tourist_Spot, Total_Price, Customer_ID) VALUES (%s, %s, " \
                       "%s, %s, %s, %s, %s, %s, %s)"
        insert_cursor.execute(insert_query,
                              (booking_ID, customer_name, dept_city, des_city, trav_mode, dept_date, spot, total_price,
                               cust_id))

        db_connection.commit()
        insert_cursor.close()

    return render_template('bookings.html', result=result)


@app.route('/LucknowTourist', methods=['POST', 'PATCH'])
def LucknowTourist():
    insert_cursor = db_connection.cursor()
    if request.method == 'POST':
        dept_city = request.form['departing-city']
        des_city = "Lucknow"
        trav_mode = request.form['vehicle']
        dept_date = request.form['departure-date']
        tourist_spot = request.form.getlist('tourist-spot')
        total_price = request.form.get('total-price-input')

        spot = ""
        for ts in tourist_spot:
            spot += ts + ","

        booking_ID = generateBookingID()

        result = []
        result.append(booking_ID)
        result.append(customer_name)
        result.append(dept_city)
        result.append(des_city)
        result.append(trav_mode)
        result.append(dept_date)
        result.append(tourist_spot)
        result.append(total_price)

        insert_query = "INSERT INTO TouristCity (Booking_ID, Customer_Name, Departing_City, Destination_City, " \
                       "Traveling_Mode, Departure_Date, Tourist_Spot, Total_Price, Customer_ID) VALUES (%s, %s, " \
                       "%s, %s, %s, %s, %s, %s, %s)"
        insert_cursor.execute(insert_query,
                              (booking_ID, customer_name, dept_city, des_city, trav_mode, dept_date, spot, total_price,
                               cust_id))

        db_connection.commit()
        insert_cursor.close()

    return render_template('bookings.html', result=result)


@app.route('/MumbaiTourist', methods=['POST', 'PATCH'])
def MumbaiTourist():
    insert_cursor = db_connection.cursor()
    if request.method == 'POST':
        dept_city = request.form['departing-city']
        des_city = "Mumbai"
        trav_mode = request.form['vehicle']
        dept_date = request.form['departure-date']
        tourist_spot = request.form.getlist('tourist-spot')
        total_price = request.form.get('total-price-input')

        spot = ""
        for ts in tourist_spot:
            spot += ts + ","

        booking_ID = generateBookingID()

        result = []
        result.append(booking_ID)
        result.append(customer_name)
        result.append(dept_city)
        result.append(des_city)
        result.append(trav_mode)
        result.append(dept_date)
        result.append(tourist_spot)
        result.append(total_price)

        insert_query = "INSERT INTO TouristCity (Booking_ID, Customer_Name, Departing_City, Destination_City, " \
                       "Traveling_Mode, Departure_Date, Tourist_Spot, Total_Price, Customer_ID) VALUES (%s, %s, " \
                       "%s, %s, %s, %s, %s, %s, %s)"
        insert_cursor.execute(insert_query,
                              (booking_ID, customer_name, dept_city, des_city, trav_mode, dept_date, spot, total_price,
                               cust_id))

        db_connection.commit()
        insert_cursor.close()

    return render_template('bookings.html', result=result)


@app.route('/PuneTourist', methods=['POST', 'PATCH'])
def PuneTourist():
    insert_cursor = db_connection.cursor()
    if request.method == 'POST':
        dept_city = request.form['departing-city']
        des_city = "Pune"
        trav_mode = request.form['vehicle']
        dept_date = request.form['departure-date']
        tourist_spot = request.form.getlist('tourist-spot')
        total_price = request.form.get('total-price-input')

        spot = ""
        for ts in tourist_spot:
            spot += ts + ","

        booking_ID = generateBookingID()

        result = []
        result.append(booking_ID)
        result.append(customer_name)
        result.append(dept_city)
        result.append(des_city)
        result.append(trav_mode)
        result.append(dept_date)
        result.append(tourist_spot)
        result.append(total_price)

        insert_query = "INSERT INTO TouristCity (Booking_ID, Customer_Name, Departing_City, Destination_City, " \
                       "Traveling_Mode, Departure_Date, Tourist_Spot, Total_Price, Customer_ID) VALUES (%s, %s, " \
                       "%s, %s, %s, %s, %s, %s, %s)"
        insert_cursor.execute(insert_query,
                              (booking_ID, customer_name, dept_city, des_city, trav_mode, dept_date, spot, total_price,
                               cust_id))

        db_connection.commit()
        insert_cursor.close()

    return render_template('bookings.html', result=result)


@app.route('/UdupiTourist', methods=['POST', 'PATCH'])
def UdupiTourist():
    insert_cursor = db_connection.cursor()
    if request.method == 'POST':
        dept_city = request.form['departing-city']
        des_city = "Udupi"
        trav_mode = request.form['vehicle']
        dept_date = request.form['departure-date']
        tourist_spot = request.form.getlist('tourist-spot')
        total_price = request.form.get('total-price-input')

        spot = ""
        for ts in tourist_spot:
            spot += ts + ","

        booking_ID = generateBookingID()

        result = []
        result.append(booking_ID)
        result.append(customer_name)
        result.append(dept_city)
        result.append(des_city)
        result.append(trav_mode)
        result.append(dept_date)
        result.append(tourist_spot)
        result.append(total_price)

        insert_query = "INSERT INTO TouristCity (Booking_ID, Customer_Name, Departing_City, Destination_City, " \
                       "Traveling_Mode, Departure_Date, Tourist_Spot, Total_Price, Customer_ID) VALUES (%s, %s, " \
                       "%s, %s, %s, %s, %s, %s, %s)"
        insert_cursor.execute(insert_query,
                              (booking_ID, customer_name, dept_city, des_city, trav_mode, dept_date, spot, total_price,
                               cust_id))

        db_connection.commit()
        insert_cursor.close()

    return render_template('bookings.html', result=result)


@app.route('/bookingsall')
def bookingsall():
    select_cursor = db_connection.cursor()
    select_query = "SELECT * FROM TouristCity where Customer_ID = %s"
    select_cursor.execute(select_query, (cust_id,))
    result_set = select_cursor.fetchall()
    select_cursor.close()
    return render_template('bookingsall.html', result_set=result_set)


if __name__ == '__main__':
    app.run(debug=True)
