#VoltWay - EV Charging Hub Finder
import os
from PIL import Image
from DBConnection import Db
from datetime import datetime
from evchargingfinderlib.booking import booking_success
from flask import Flask, render_template, url_for, request, redirect, session, jsonify, flash
import requests


application = Flask(__name__)
app=application
app.secret_key="123"





@app.route('/')
def home():
    session.pop('username',None)
    session.pop('user_type',None)
    session.pop('log',None)
    session.pop('usertype',None)
    return render_template('index.html')


@app.route('/find_your_charger')
def find_your_charger():
    if  'user_type' in session and session['user_type'] != "admin":
        return render_template('find_your_charger.html')
    else:
        return render_template('login.html')


@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        feedback = request.form['message']
        db = Db()
        sql = db.insert("INSERT INTO contact_us (Name, Email, feedback_date, feedback) VALUES (%s, %s, NOW(), %s)", (name, email, feedback))
        return render_template('contact_us.html', message='Thank you for your feedback!')
    else:
        return render_template('contact_us.html')



@app.route('/login',methods=['GET', 'POST'])
def login():
    if  'user_type' in session and session['user_type'] == "admin":
        return redirect('/admin-home')

    if request.method == "POST":
        print('form ', request.form)
        username = request.form['username']
        password = request.form['password']
        db = Db()
        ss = db.selectOne("select * from login where username='" + username + "'and password='" + password + "'")
        
        user_email=ss['email']
        if ss is not None:
            session['head'] = ""
            session['username'] = username # set the username key in the session
            session['email'] = user_email 
            if ss['usertype'] == 'admin':
                session['user_type'] = 'admin'
                return redirect('/admin-home')

            elif ss['usertype'] == 'user':
                session['user_type'] = 'user'
                session['uid'] = ss['login_id']
                return redirect('/user-dashboard')
            else:
                return '''<script>alert('user not found');window.location="/login"</script>'''
        else:
            return '''<script>alert('user not found');window.location="/login"</script>'''
    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop('username',None)
    session.pop('user_type',None)
    session.pop('log',None)
    session.pop('usertype',None)
    session.pop('email',None)

    return redirect('/login')



    # =========================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['signupUsername']
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']

        # Perform form validation
        if username.strip() == '':
            return redirect(url_for('register', error='Please enter a username', form_id='createAccount'))

        if email.strip() == '':
            return redirect(url_for('register', error='Please enter an email address', form_id='createAccount'))

        if password.strip() == '':
            return redirect(url_for('register', error='Please enter a password', form_id='createAccount'))

        if confirmPassword.strip() == '':
            return redirect(url_for('register', error='Please confirm the password', form_id='createAccount'))

        if password != confirmPassword:
            return redirect(url_for('register', error='Passwords do not match', form_id='createAccount'))

        db = Db()
        qry = db.insert("INSERT INTO login (username, email, password, usertype) VALUES (%s, %s, %s, 'user')", (username,  email, password))

        return '<script>alert("User registered"); window.location.href="/login";</script>'
    else:
        error = request.args.get('error')  # Get the error message from the URL parameters
        return render_template("login.html", error=error , form_id='createAccount')






#////////////////////////////////////////////////////////////ADMIN///////////////////////////////////////////////////////////////////////////////////////////////////////////////////


@app.route('/admin-home')
def admin_home():
    if 'user_type' not in session:
        return redirect('/')
    else:
        if session['user_type'] == 'admin':
            username = session['username'] # get the username from the session
            return render_template('admin/admin-login-dashboard.html', username=username)
        else:
            return redirect('/')


@app.route('/Manage_station')
def Manage_station():
    if 'user_type' not in session:
        return redirect('/')
    else:
        if session['user_type'] == 'admin':
            username = session['username']
            db=Db()
            qry=db.select("select station_id, station_name, address, city, charger_type, available_ports, status from admin_charging_station_list")
            return render_template("admin/Manage_station.html",data=qry,username=username)
        else:
            return redirect('/')


@app.route('/addstationpage')
def addstationpage():
    if 'user_type' not in session:
        return redirect('/')
    else:
        if session['user_type'] == 'admin':
            username = session['username'] # get the username from the session
            return render_template('admin/add_station.html', username=username)
        else:
            return redirect('/')


#image exe
ALLOWED_EXTENSIONS = {'jpg'}
def allowed_file(filename):
  return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/addchargingstation', methods=['POST'])
def addchargingstation():
    if 'user_type' not in session:
        return redirect('/')
    else:
        if session['user_type'] == 'admin':
            username = session['username']
            savepath = 'images'
            file = None
            file = request.files['file']
            # imagepath = os.path.join(savepath,file.filename)
            # image.save(imagepath)
            if file and allowed_file(file.filename):
                stationname = request.form['stationname']
                address = request.form['address']
                city = request.form['city']
                chargetype = request.form['chargetype']
                ports = str(request.form['ports'])
                image = Image.open(file)
                imagepath = os.path.join(savepath,file.filename)
                image.save(imagepath)
                # file_name = imagepath 
                # bucket_name = "evlocator"      
                # upload_file_to_s3(file_name, bucket_name)

            status = 'active'
            db = Db()
            qry = db.insert("INSERT INTO admin_charging_station_list VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)", (stationname,address,city,chargetype,ports,imagepath,status))

            return render_template('admin/add_station.html', username=username, successmsg="Charging Station Added Successfully !!!")


        else:
            return redirect('/')



# =============================contact_us
@app.route('/view_feedback')
def view_feedback():
    if 'user_type' not in session:
        return redirect('/')
    else:
        #print('session ', session)
        if session['user_type'] == 'admin':
            username = session['username']
            db=Db()
            ss=db.select("select * from contact_us")
            return render_template("admin/view_feedback.html",data=ss, username=username)
        else:
            return redirect('/')

# 


# ==================delete station=======
@app.route("/adm_delete_station/<station_name>")
def adm_delete_station(station_name):
    if 'user_type' not in session:
        return redirect('/')
    else:
        #print('session ', session)
        if session['user_type'] == 'admin':
            username = session['username']
            db = Db()
            qry = db.delete("DELETE FROM admin_charging_station_list WHERE Station_name = %s", (station_name,))
            return '''<script>alert('station deleted');window.location="/Manage_station"</script>'''
        else:
            return redirect('/')
# =======================================





@app.route("/adm_delete_feedback/<feedback>")
def adm_delete_feedback(feedback):
    if 'user_type' not in session:
        return redirect('/')
    else:
        #print('session ', session)
        if session['user_type'] == 'admin':
            username = session['username']
            db = Db()
            qry = db.delete("delete from contact_us where Sl_no='"+feedback+"'")
            return '''<script>alert('feedback deleted');window.location="/view_feedback"</script>'''
        else:
            return redirect('/')



@app.route('/user-list')
def user_list():
    if 'user_type' not in session:
        return redirect('/')
    else:
        if session['user_type'] == 'admin':
            username = session['username']
            db=Db()
            qry = db.select("SELECT * FROM `login` WHERE usertype='user'")
            return render_template("admin/user-list.html",data=qry,username=username)
        else:
            return redirect('/')


# ==================delete user===========
@app.route("/adm_delete_user/<login_id>")
def adm_delete_user(login_id):
    if 'user_type' not in session:
        return redirect('/')
    else:
        #print('session ', session)
        if session['user_type'] == 'admin':
            username = session['username']
            db = Db()
            qry = db.delete("delete from login   where login_id='"+login_id+"'")
            return '''<script>alert('user deleted');window.location="/user-list"</script>'''
        else:
            return redirect('/')
# ==============view booking=========================

@app.route('/view_booking')
def view_booking():
    if 'user_type' not in session:
        return redirect('/')
    else:
        #print('session ', session)
        if session['user_type'] == 'admin':
            username = session['username']
            db=Db()
            bookings = db.select("select Booking_id	, Booking_date, Time_from, Time_to, City, Station_name, Available_ports, login_id  from booking  order by Booking_date desc;")
            return render_template('admin/view_booking.html', bookings=bookings,username=username)
        else:
            return redirect('/')

# ===========delete booking

@app.route("/adm_delete_booking/<Booking_id>")
def adm_delete_booking(Booking_id):
    if 'user_type' not in session:
        return redirect('/')
    else:
        #print('session ', session)
        if session['user_type'] == 'admin':
            db = Db()
            qry = db.delete("delete from booking where Booking_id='"+Booking_id+"'")
            return '''<script>alert('booking deleted');window.location="/view_booking"</script>'''
        else:
            return redirect('/')



#//////////////////////////////////////////////////////////////USER//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# -----------

@app.route('/user-dashboard')
def user_dashboard():
    if 'user_type' in session and session['user_type'] == "user":
        username = session['username'] # get the username from the session
        db = Db()
        bookings = db.select("select * from booking where login_id = '%s' order by Booking_date desc;", (session['uid'],))
        # print(bookings)  # print out the value of the bookings variable
        return render_template("user/user-login-dashboard.html", bookings=bookings, username=username)
    else:
        return redirect('/')


@app.route('/usr_delete_booking/<int:booking_id>')
def usr_delete_booking(booking_id):
    if 'user_type' in session and session['user_type'] == "user":
        username = session['username']
        if 'user_type' in session and session['user_type'] == "user":
            db = Db()
            
            # Delete the booking for the specific user and booking_id
            db.delete("DELETE FROM booking WHERE booking_id = %s AND login_id = %s", (booking_id, session['uid']))
            
            return '''<script>alert('Booking deleted');window.location="/user-dashboard"</script>'''
        else:
            return redirect('/user-dashboard')
    
    else:
        return redirect('/')



@app.route('/user_find_your_charger', methods=['GET', 'POST'])
def user_find_your_charger():
    if 'user_type' in session and session['user_type'] == 'user':
        username = session['username']
        if request.method == 'POST':
            city = request.form.get('City')
            charger_type = request.form.get('Charger_type')
            db = Db()
            qry = db.select("select Station_name, Address, Charger_type, Available_ports from admin_charging_station_list where City = %s and Charger_type = %s", (city, charger_type))
            return render_template('user/station_search.html', data=qry, username=username)       
        else:
            return render_template('user/user_find_your_charger.html', username=username)
    else:
        return redirect('/')




@app.route('/search_stations', methods=['POST'])
def search_stations():
    if 'user_type' in session and session['user_type'] == 'user':
        username = session['username']
        # Get the form data
        City = request.form.get('City')
        Charger_type = request.form.get('Charger_type')

        # Redirect to the station_list page with the city and charger_type as URL parameters
        return redirect(url_for('station_search', City=City, Charger_type=Charger_type, username=username))
    else:
        return redirect('/')


@app.route('/station_search', methods=['GET'])
def station_search():
    if 'user_type' in session and session['user_type'] == 'user':
        username = session['username']
        City = request.args.get('City')
        Charger_type = request.args.get('Charger_type')
        # Query your MySQL database using the city and charge_type variables
        db = Db()
        sql = "select * from admin_charging_station_list where City = %s and Charger_type = %s"
        ss = db.select(sql, (City, Charger_type))

        # Return the results to the user in a new template
        return render_template('user/station_search.html', data=ss, City=City, Charger_type=Charger_type, username=username)
    else:
        return redirect('/')

# ==============from station_search to booking page====================
@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if 'user_type' in session and session['user_type'] == 'user':
        username = session['username']
        if request.method == 'POST':
            Station_name = request.form['Station_name']
            City = request.form['City']
            Available_ports = request.form['Available_ports']
            db = Db()
            sql = "select filepath from admin_charging_station_list where Station_name = %s"
            ss = db.select(sql, (Station_name,))
            #print(ss[0]['filepath'])
            imgfilename = str(ss[0]['filepath'])
            imgfilename = imgfilename.split('/')[-1]
            return redirect(url_for('booking_form',  Station_name=Station_name, City=City, Available_ports=Available_ports, outputimgpath=imgfilename))
        else:
            # handle GET request to display the form
            Station_name = request.args.get('Station_name')
            City = request.args.get('City')
            Available_ports = request.args.get('Available_ports')
            db = Db()
            sql = "select filepath from admin_charging_station_list where Station_name = %s"
            ss = db.select(sql, (Station_name,))
            imgfilename = str(ss[0]['filepath'])
            imgfilename = imgfilename.split('/')[-1]
            imgfilename = f'static\image\ {imgfilename}'
            return redirect(url_for('booking_form', Station_name=Station_name, City=City, Available_ports=Available_ports, username=username, outputimgpath=imgfilename))
    else:
        return redirect('/')


@app.route('/booking-form', methods=['GET'])
def booking_form():
    if 'user_type' in session and session['user_type'] == 'user':
        username = session['username']
        city = request.args.get('City')
        available_ports = request.args.get('Available_ports')
        station_name = request.args.get('Station_name')
        db = Db()
        station_data = db.select("select * from admin_charging_station_list where Station_name = %s", (station_name,))
        db = Db()
        sql = "select filepath from admin_charging_station_list where Station_name = %s"
        ss = db.select(sql, (station_name,))
        imgfilename = str(ss[0]['filepath'])
        imgfilename = imgfilename.split('/')[-1]
        imgfilename = f'images/{imgfilename}'
        session['station_data'] = station_data[0] if station_data else None
        if 'station_data' in session and session['station_data']:
            
            return render_template('/user/booking_form.html', city=city, available_ports=available_ports, username=username, outputimgpath=imgfilename)
        else:
            return redirect(url_for('station_search'))
    else:
        return redirect('/')


# ====================from booking to dashboard

@app.route('/book', methods=['POST'])
def book():
    if 'user_type' not in session and session['user_type'] != 'user':
        return redirect('/')
    
    else:
        username = session['username']
        # get the form data submitted by the user
        station_name = request.form['Station_name']
        city = request.form['City']
        available_ports = request.form['Available_ports']
        booking_date = request.form['Booking_date']
        time_from = request.form['Time_from']
        time_to = request.form['Time_to']
        login_id = session['uid']


        db = Db()

        # get the current timestamp
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # insert the booking data into the MySQL table
        sql = "insert into booking (Station_name, City, Available_ports, Booking_date, Time_from, Time_to, Created_id, login_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        booking_id = db.insert(sql, (station_name, city, available_ports, booking_date, time_from, time_to, created_at, login_id))
        booksuccessmsg = booking_success()
        #     #calling smpt api for email
        to_hr,to_min=time_to.split(":")
        to_hr,to_min=int(to_hr),int(to_min)
        from_hr,from_min=time_from.split(":")
        from_hr,from_min=int(from_hr),int(from_min)
        global duration
        duration=(abs(to_hr-from_hr)*60)+(abs(to_min-from_min))

        # global API_URL1,API_URL2
        

        #call api for conversion
        


        API_URL='http://x23337818-calculateapi.eba-xdnngu8m.ap-southeast-1.elasticbeanstalk.com/calculator'
        
        json_data={"duration":duration}
        try:
            response=requests.get(API_URL,json=json_data,stream=True)
            if response.status_code == 200:
                data = response.json()
                calculated_amt=data.get('calculated_amt')
                converted_usd=data.get('converted_usd')
                print(f"generated value --------> {calculated_amt} and in usd {converted_usd}")
            else:
                print(response)
                print("Failed to email")
        except Exception as e:
            calculated_amt = f"An error occurred: {str(e)}"
            converted_usd = f"An error occurred: {str(e)}"
        


            # redirect the user to their dashboard
        # print(booksuccessmsg=booksuccessmsg,cal_amt=calculated_amt,con_usd=converted_amt,duration=duration)
        return render_template('/user/booking_form.html', booksuccessmsg=booksuccessmsg,cal_amt=calculated_amt,con_usd=converted_usd,duration=duration,bookingdate=booking_date,time=time_from)


@app.route('/mail',methods=['GET','POST'])
def mail():
    usd=request.form['usd']
    duration=request.form['duration']
    euro=request.form['euros']
    date=request.form['date']
    time=request.form['time']
    API_URL = "http://x23324902-scalableapi.eba-euagxqry.us-west-2.elasticbeanstalk.com/email"
    try:
        subject='Booking for ev charging  '
        message=f"Your booking has been confirmed for {date} at {time} .Total duration of {duration}min which costs € {euro}. Thankyou for booking!"
        email=session['email']
        ##translating the name
        json_data = {"subject": subject,"body":message,"email":email }
        response = requests.get(API_URL, json=json_data, stream=True)
        if response.status_code == 200:
            
            print("Mail delivered Successfully ")
            return redirect(url_for('user_dashboard'))
        else:
            print(response)
            print("Failed to email")
            return redirect(url_for('user_dashboard'))
    except Exception as e:
        converted_amt = f"An error occurred: {str(e)}"
        return redirect(url_for('user_dashboard'))



if __name__ == '__main__':        
    app.run(host='0.0.0.0', port=5000)




