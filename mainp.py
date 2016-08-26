import os
from flask import Flask, g, render_template, flash, request , url_for, session, jsonify ,redirect, session , escape
from dbConnect import connection
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc
import json
from decimal import *
from jinja2 import Template
from distance import calculatedistance
from random import randint
from sparrow import sparrow , sparrow2
from functools import wraps
from authentication import login_required
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import urllib
import datetime
from pyfcm import FCMNotification

app = Flask(__name__)

# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "AIzaSyAZzeHhs-8JZ7i18MjFuM35dJHq70n3Hx4"

# you can also pass key here
GoogleMaps(app, key="AIzaSyAZzeHhs-8JZ7i18MjFuM35dJHq70n3Hx4")

os.environ['CLOUDINARY_URL']="cloudinary://418193537422982:ayEj_qE71n2sYdQWcgg3qi9YWjo@instantum"

# for firebase cloud messaging push notification

push_service = FCMNotification(api_key="AIzaSyDCJW73vGwn1OGYGbDltO3dKmPaHjdnZKY")

#push_service = FCMNotification(api_key="AIzaSyALZyuZDchNjC1dL-0pXy9ReqZd5D36j-0")

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("login"))

    return wrap


# for website

 
@app.route('/register', methods = ['GET','POST'])
@login_required
def register():

    try:
       
        if request.method == "POST":
            
            entered_full_name = request.form['full_name']
            entered_license_number = request.form['license_number'] 
            entered_address = request.form['address'] 
            entered_mobile_number = request.form['mobile_number']                        
            entered_username = request.form['username'] 
            entered_password = request.form['password'] 
            entered_taxi_number = request.form['taxi_number']
            file = request.files['file']
            
            
            c, conn = connection()
            c.execute("""Select * From Driver where mobile_number = %s""",[entered_mobile_number])
            x= c.fetchone()
            c.close() 
            conn.commit()              
            gc.collect()

            if x:
                flash("This Mobile Number is already taken")
                return render_template("register.html")

            else:
                pass

            
            c, conn = connection()
            c.execute("""Select * From Driver where username = %s""",[entered_username])
            x=c.fetchone()
            conn.commit()              
            c.close()
            gc.collect()
            if x:
                flash("This Username is already taken")
                return render_template("register.html")

            else:
                pass

            c, conn = connection()
            c.execute("""Select * From Driver where taxi_number = %s""",[entered_taxi_number])
            x=c.fetchone()
            conn.commit()              
            c.close()
            gc.collect()

            if x:
                flash("This Taxi Number is already taken")
                return render_template("register.html")

            else:
                pass 


            
            if file: 
                upload_result = upload(file, public_id = entered_username)
                photo_url1 = str(cloudinary_url(entered_username+ ".jpg"))
                photo_url = photo_url1[2:-6]               
                c, conn = connection()
                c.execute("""INSERT INTO Driver (full_name,license_number,address,mobile_number,username,password,taxi_number,profile_photo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",(entered_full_name, entered_license_number,entered_address,entered_mobile_number,entered_username,entered_password,entered_taxi_number,photo_url))
                conn.commit()              
                c.close()
                gc.collect()
                return redirect(url_for(".dashboard"))  

            else:    

                return render_template("register.html") 
 
   

        else:    

            return render_template("register.html")
            
            
    except Exception as e:
        
        return e


@app.route("/", methods = ['GET','POST'])
@app.route('/login', methods = ['GET','POST'])
def login():
   
    try:
        users = [{"username":"sandesh","password":"kandel"},
        {"username":"sujit","password":"bhandari"},
        {"username":"sankalpa","password":"aryal"},
        {"username":"sudip","password":"paudel"}]


        if request.method == "POST":
            attempted_username = request.form['username']
            attempted_password = request.form['password']
            
            for i in users:       
                if attempted_username == i['username'] and attempted_password == i['password']:
                    session['username'] = attempted_username
                    #session['logged_in'] = True
                    #return "Hello " + attempted_username
                    return redirect(url_for(".dashboard"))

                    #return render_template("dashboard.html", username = i['username'] , password = i['password'])
             
            return render_template("login.html")   
               
                
        else:
           return render_template("login.html")
                
    except Exception as e:
        
        return render_template("login.html")


@app.route('/logout')
@login_required
def logout():

    session.pop('username', None)
    #session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    try:

        username = session['username']
        return render_template('dashboard.html',username = username)
    
           

    except Exception as e:
        
        return "error"




@app.route('/listofdrivers/', methods = ['GET','POST'])
@login_required
def listofdrivers():
    try:
        if request.method == "GET":  
            c , conn = connection()
            c.execute("SELECT * from Driver ")
            drivers = []
            
            x = c.fetchall()
            
            for row in x:
                z= {
                "full_name": row[0],
                "license_number": row[1],
                "address": row[2],
                "mobile_number": row[3],
                "username": row[4],
               "password": row[5],
                "taxi_number": row[6]
                }
                drivers.append(z)

            conn.commit()
            c.close()
           
            gc.collect()
            return render_template("listofdrivers.html", drivers = drivers)

        else:
            info = request.form['x']
            c , conn = connection()
            c.execute("SELECT * from Driver where full_name = %s or mobile_number = %s or taxi_number = %s or username = %s",(info,info,info,info))
            drivers = []
            
            x = c.fetchall()
            
            for row in x:
                z= {
                "full_name": row[0],
                "license_number": row[1],
                "address": row[2],
                "mobile_number": row[3],
                "username": row[4],
                "password": row[5],
                "taxi_number": row[6]
                }
                drivers.append(z)

            conn.commit()
            c.close()
            
            gc.collect()
            return render_template("listofdrivers.html", drivers = drivers)



    except Exception as e:
        
        return "error"


@app.route('/listofcustomers/', methods = ['GET','POST'])
@login_required
def listofcustomers():
    try:
        if request.method == "GET":  
            c , conn = connection()
            c.execute("SELECT * from Customer")
            customers = []
            x = c.fetchall()
            
            for row in x:
                z= {
                "full_name": row[0],
                "mobile_number": row[1]
                
                }
                customers.append(z)

            conn.commit()
            c.close()
            
            gc.collect()
            return render_template("listofcustomers.html", customers = customers)

        else:
            info = request.form['x']
            c , conn = connection()
            c.execute("SELECT * from Customer where full_name = %s or mobile_number = %s",(info,info))
            customers = []
            
            x = c.fetchall()
            
            for row in x:
                z= {
                "full_name": row[0],                
                "mobile_number": row[1]
                
                }
                customers.append(z)

            conn.commit()
            c.close()
            
            gc.collect()
            return render_template("listofcustomers.html", customers = customers)



    except Exception as e:
        
        return "error"


@app.route('/delete/<username>')
@login_required
def delete(username):

    c,conn = connection()
    c.execute("SELECT * from Driver where username = %s ",[username])
    x=c.fetchone()
    conn.commit()
    c.close()
    gc.collect()
    return render_template("delete.html", driver = x)


@app.route('/finaldelete/<username>')
@login_required
def finaldelete(username):

    c,conn = connection()
    c.execute("DELETE from Driver where username = %s ",[username])
    conn.commit()
    c.close()
    gc.collect()
    return redirect(url_for(".listofdrivers"))


@app.route('/details/<username>')
@login_required
def details(username):

    c,conn = connection()
    c.execute("SELECT * from Driver where username = %s ",[username])
    x=c.fetchone()
    conn.commit()
    c.close()
    gc.collect()
    photo_url = x[7]
    return render_template("details.html", driver = x, photo_url = photo_url)


@app.route('/update/<username>', methods = ["POST","GET"])
@login_required
def update(username):
    if request.method == "POST":
        entered_license_number = request.form['license_number'] 
        entered_address = request.form['address'] 
        entered_mobile_number = request.form['mobile_number'] 
        entered_password = request.form['password'] 
        entered_taxi_number = request.form['taxi_number'] 

        c, conn = connection()
        c.execute("""Select * From Driver where mobile_number = %s""",[entered_mobile_number])
        x= c.fetchone()
        c.close() 
        conn.commit()              
        gc.collect()

        if x:
            flash("This Mobile Number is already taken")
            return render_template("register.html")

        else:
            pass

        
        c, conn = connection()
        c.execute("""Select * From Driver where taxi_number = %s""",[entered_taxi_number])
        x=c.fetchone()
        conn.commit()              
        c.close()
        gc.collect()
        if x:
            flash("This Taxi Number is already taken")
            return render_template("register.html")

        else:
            pass

        c, conn = connection()
        c.execute("""UPDATE Driver SET license_number = %s , address  = %s , mobile_number  = %s , password  = %s , taxi_number  = %s where username = %s""",(entered_license_number,entered_address,entered_mobile_number,entered_password,entered_taxi_number,username))
        conn.commit()              
        c.close()
        
        gc.collect()
        return redirect(url_for(".details", username = username ))
           
    else:
        return render_template("update.html", username = username)     
            
            


@app.route('/listofonlinedrivers/')
@login_required
def listofonlinedrivers(): 
    try:

        c , conn = connection()
        c.execute("SELECT * from OnlineDriver")
        onlinedrivers = []
        x = c.fetchall()
        conn.commit()
        c.close()
        gc.collect()
        for row in x:
            z= {
            "username": row[0]
                }
            onlinedrivers.append(z)

        #correct upto above line. Any mistakes that will occur will be from below here

        onlinedriversinfo = []
        for a in onlinedrivers:
            c,conn = connection()
            username = a['username']
            
            c.execute("SELECT * from Driver where username = %s ",[username])
            y=c.fetchone()
            conn.commit()
            c.close()
            gc.collect()
            d={
                "full_name": y[0],
                "mobile_number": y[3],
                "license_number": y[1],    
                "taxi_number": y[6]
            }
            onlinedriversinfo.append(d)      
         

        
        return render_template("listofonlinedrivers.html", drivers = onlinedriversinfo)


    except Exception as e:
        
        return "error"



# Here lies the code for displaying online drivers in map:

@app.route('/onlinedriversmap')
@login_required
def onlinedriversmap():
    try:
        c , conn = connection()
        c.execute("""SELECT * FROM OnlineDriver""")
        y = []
        x = c.fetchall()
        for row in x:
            username = row[0]
            c , conn = connection()
            c.execute("""SELECT * FROM Driver where username = %s""",[username])
            x=c.fetchone()
            conn.commit()
            c.close()
            gc.collect()
            full_name = x[0]
            address = x[2]
            mobile_number = x[3]
            photo_url = x[7]
            z= {
            'icon': '//maps.google.com/mapfiles/ms/icons/green-dot.png',
            'title': 'Information Of Driver',
            'lat': row[2],
            'lng': row[1],
            'infobox': (
                "<b>Name:</b> " +full_name + "<br/>" +
                "<b>Address:</b> " +address + "<br/>" +
                "<b>Mobile Number:</b> " + mobile_number + "<br/>"
                "<img src = "+photo_url+" height=""126"" width=""150"">"
                )
            }
            y.append(z)
        
        conn.commit()         
        c.close()
        
        gc.collect()
             
        


        fullmap = Map(
            identifier="fullmap",
            varname="fullmap",
            style=(
                "height:100%;"
                "width:100%;"
                "top:10;"
                "left:0;"
                "position:absolute;"
                "z-index:200;"
            ),
            lat=27.7,
            lng=85.2891,
            markers=y,
            #maptype = "TERRAIN",
            #zoom="100"
        )
        return render_template('onlinedriversmap.html', fullmap=fullmap)

    except Exception as e:
        
        return "error"


#Here ends the code for displaying online drivers in map:






@app.route('/listofblockedcustomer/')
@login_required
def listofblockedcustomer(): 
    try:

        c , conn = connection()
        c.execute("SELECT * from Block")
        blocked = []
        x = c.fetchall()
        conn.commit()
        c.close()
        gc.collect()
        for row in x:
            z= {
            "mobile_number": row[0]
                }
            blocked.append(z)

      

        blockedcustomers = []
        for a in blocked:
            c,conn = connection()
            mobile_number = a['mobile_number']
            
            c.execute("SELECT * from Customer where mobile_number = %s ",[mobile_number])
            y=c.fetchone()
            conn.commit()
            c.close()
            gc.collect()
            d={
                "full_name": y[0],                 
                "mobile_number": y[1]
            }
            blockedcustomers.append(d)      
         

        #return json.dumps(blockedcustomers , indent = 0)
        return render_template("listofblockedcustomer.html", blockedcustomers = blockedcustomers)


    except Exception as e:
        
        return "error"


@app.route('/listofrequestedblock/')
@login_required
def listofrequestedblock(): 
    try:

        c , conn = connection()
        c.execute("SELECT * from RequestToBlock")
        block = []
        x = c.fetchall()
        conn.commit()
        c.close()
        gc.collect()
        for row in x:
            z= {
            "mobile_number": row[0],
            "username": row[1]
                }
            block.append(z)

      
        info = []
        for a in block:
            mobile_number = a['mobile_number']
            username = a['username']
            c,conn = connection()
            c.execute("SELECT * from Customer where mobile_number = %s ",[mobile_number])
            y=c.fetchone()
            conn.commit()
            c.close()
            gc.collect()
            c,conn = connection()
            c.execute("SELECT * from Driver where username = %s ",[username])
            z=c.fetchone()
            conn.commit()
            c.close()
            gc.collect()
            d={
                "full_name": y[0],           
                
                "dfull_name": z[0]
            }
            info.append(d)      
         

        #return json.dumps(info , indent = 0)
        return render_template("listofrequestedblock.html", info = info)


    except Exception as e:
        
        return "error"


#-----------------------------------------------------------------------------------------------------------
# for android chalak costumer app



#done
@app.route('/getmeacode',methods = ['POST'])
def getmeacode():
    mobile_number = request.form['mobile_number']
    c,conn = connection()
    c.execute("SELECT * from Block where mobile_number = %s",[mobile_number])
    x= c.fetchone()
    conn.commit()
    c.close()
    gc.collect()

    if x:
        return "Your number is in the block list."

    else:
        c, conn = connection()
        c.execute("SELECT * from Customer where mobile_number = %s",[mobile_number])
        x= c.fetchone()
        conn.commit()
        c.close()
        gc.collect()

        if x:
            full_name = x[0]
            return "Your number is already registered in the name of " + full_name   

        else:
            code= randint(10000,99999)
            c = str(code)
            sparrow(mobile_number , c)
            c, conn = connection()
            c.execute("DELETE from ForCode where mobile_number = %s",[mobile_number])
            conn.commit()
            c.close()
            gc.collect()
            c,conn = connection()
            c.execute("INSERT INTO ForCode (mobile_number, code) VALUES (%s,%s)",(mobile_number, code))
            conn.commit()
            c.close()
            gc.collect()
            return "success"
        
#done
@app.route('/forgotpassword',methods = ['POST'])
def forgotpassword():
    mobile_number = request.form['mobile_number']
    c, conn = connection()
    c.execute("SELECT * from Customer where mobile_number = %s",[mobile_number])
    x= c.fetchone()
    conn.commit()
    c.close()
    gc.collect()


    if x:
        password = x[2]
        sparrow2(mobile_number , password)
        return "Password is sent to your mobile number."
    else:
        return "Your number is not registered." 
              


#done
@app.route('/registeracustomer' , methods = ["POST"])
def registeracustomer():
    full_name = request.form['full_name']
    mobile_number = request.form['mobile_number']
    password = request.form['password']
    code = int(request.form['code'])

    c,conn = connection()
    c.execute("SELECT * from ForCode WHERE mobile_number = %s",[mobile_number])
    x = c.fetchone()
    conn.commit()
    c.close()
    gc.collect()
    if int(x[1]) == code:
        c,conn = connection()
        c.execute("INSERT INTO Customer (full_name, mobile_number, password) VALUES (%s, %s, %s)",(full_name , mobile_number ,password) )
        conn.commit()
        c.close()
        gc.collect()
        return "success"
    else:
        return "failed"

#done
@app.route('/customerlogin', methods = ["POST"])
def customerlogin():
    mobile_number = request.form['mobile_number']
    password = request.form['password']
    token = request.form['token']

    if mobile_number== "" or password == "":
        return "Enter Username and Password"

    else:
        pass

    c,conn = connection()
    c.execute("SELECT * from Block where mobile_number = %s",[mobile_number])
    x= c.fetchone()
    conn.commit()
    c.close()
    gc.collect()

    if x:
        return "Your number is in the Block List."

    c,conn = connection()
    c.execute("SELECT * from Customer where mobile_number = %s",[mobile_number])
    x= c.fetchone()
    c.close()
    conn.commit()
    gc.collect()

    if x:
        if x[2] == password:

            c,conn = connection()
            c.execute("SELECT * from ForCustomerToken where mobile_number =%s",[mobile_number])
            x= c.fetchone()
            c.close()
            conn.commit()
            gc.collect()

            if x:
                c,conn = connection()
                c.execute("DELETE from ForCustomerToken where mobile_number =%s",[mobile_number])
                c.close()
                conn.commit()
                gc.collect()

            c,conn = connection()
            c.execute("SELECT * from ForCustomerToken where token =%s",[token])
            x= c.fetchone()
            c.close()
            conn.commit()
            gc.collect()

            if x:
                c,conn = connection()
                c.execute("DELETE from ForCustomerToken where token =%s",[token])
                c.close()
                conn.commit()
                gc.collect()



            c,conn = connection()
            c.execute("INSERT into ForCustomerToken (mobile_number, token) values(%s,%s)",(mobile_number,token))
            c.close()
            conn.commit()
            gc.collect()
        
            return "success"
        else:
            return "failed"

    else:
        return "Username not correct"



# done!
@app.route('/willselectataxi', methods = ['POST','GET'])
def willselectataxi():
    try:
        if request.method == "POST":
            mobile_number = request.form['mobile_number']
            latitude = float(request.form['latitude'])
            longitude = float(request.form['longitude'])

        else:
            latitude = float(request.args['latitude'])
            longitude = float(request.args['longitude'])

        c,conn = connection()
        c.execute("SELECT * from OnlineCustomer where mobile_number = %s",[mobile_number])
        x=c.fetchone()
        c.close()
        conn.commit()
        gc.collect()

        if x:
            c,conn = connection()
            c.execute("DELETE from OnlineCustomer where mobile_number = %s",[mobile_number])
            c.close()
            conn.commit()
            gc.collect()

        else:
            pass
        
        c,conn = connection()
        c.execute("INSERT into OnlineCustomer values(%s,%s,%s)",(mobile_number,latitude,longitude))
        c.close()
        conn.commit()
        gc.collect()



        w = latitude + float(0.018087434)
        x = latitude - float(0.018087434)
        y = longitude + float(0.018087434)
        z = longitude - float(0.018087434)

        c , conn = connection()
        c.execute("""SELECT * FROM OnlineDriver WHERE longitude BETWEEN %s AND %s AND latitude BETWEEN %s AND %s and with_customer = %s """,(z,y,x,w,False))
        #c.execute("""SELECT * FROM OnlineDriver where with_customer = %s""",[False])
        y = []
        x = c.fetchall()
        #for each in x:

        if len(x) == 0:
            return "No Drivers."


        else:
            pass

        for row in x:
            z= {
            "username": row[0],
            "longitude": row[1],
            "latitude": row[2]
            }
            y.append(z)

        w= {"markers":y}
        
        conn.commit()         
        c.close()
       
        gc.collect()
        return json.dumps(w, indent=0)
             
               
    except Exception as e:
            
            return e


#done          
@app.route('/findmeataxi', methods = ['POST'])
def findmeataxi():
    try:
        
        mobile_number = request.form['mobile_number']
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])

        c,conn = connection()
        c.execute("SELECT * from OnlineCustomer where mobile_number = %s",[mobile_number])
        x=c.fetchone()
        c.close()
        conn.commit()
        gc.collect()

        if x:
            c,conn = connection()
            c.execute("DELETE from OnlineCustomer where mobile_number = %s",[mobile_number])
            c.close()
            conn.commit()
            gc.collect()

        else:
            pass

        c,conn = connection()
        c.execute("INSERT into OnlineCustomer values(%s,%s,%s)",(mobile_number,latitude,longitude))
        c.close()
        conn.commit()
        gc.collect()
            
        w = latitude + float(0.018087434)
        x = latitude - float(0.018087434)
        y = longitude + float(0.018087434)
        z = longitude - float(0.018087434)

        c , conn = connection()
        c.execute("""SELECT * FROM OnlineDriver WHERE longitude BETWEEN %s AND %s AND latitude BETWEEN %s AND %s and with_customer = %s """,(z,y,x,w,False))
        #c.execute("""SELECT * FROM OnlineDriver where with_customer = %s""",[False])
        x = c.fetchall()
        conn.commit()         
        c.close()
        gc.collect()


        shortest_distance = 10000

        if len(x)==0:
            return "No Drivers"

        else:
            pass
        
        for row in x:
            d = calculatedistance(longitude,latitude,row[1],row[2])
            if d < shortest_distance:
                shortest_distance = d
                nearest_user = row[0]

            else:
                pass

        c , conn = connection()
        c.execute("""SELECT * FROM Driver WHERE username = %s """,[nearest_user])               
        x = c.fetchone()
        conn.commit()         
        c.close()
        gc.collect()
        driver1 = []
        driver= {
        "full_name": x[0],
        "license_number": x[1],
        "address": x[2],
        "mobile_number": x[3],
        "taxi_number" : x[6],
        "username": x[4]
        }

        driver1.append(driver)
           

        w= {"driver":driver1}      
        return json.dumps(w, indent=0)
        
                
               
    except Exception as e:            
        return e



#done if certain error occurs it is easy

@app.route('/showprofile', methods = ['POST'])
def showprofile():
    
    try:
        
        username = request.form['username']
        c,conn = connection()
        c.execute("SELECT * FROM Driver where username = %s",[username])
        x= c.fetchone()
           
        driver = []
        driver1 = {
                    "full_name" : x[0],
                    "license_number" : x[1],
                    "address" : x[2],
                    "mobile_number" : x[3],
                    "taxi_number" : x[6],
                    "username" : x[4]

        }
        driver.append(driver1)
        jsdriver = {"driver":driver}

        conn.commit()
        c.close()
        gc.collect()
        return json.dumps(jsdriver,indent = 0)

    except Exception as e:

        return e


@app.route('/callnow', methods = ["POST"])
def callnow():
    if request.method == "POST":
        mobile_number = request.form['mobile_number']
        username = request.form['username']

    c , conn = connection()
    c.execute("""SELECT * FROM OnlineDriver WHERE username = %s and with_customer = %s""",(username,False))              
    x = c.fetchone()
    conn.commit()         
    c.close()
    
    c,conn = connection()
    c.execute("SELECT * from ForToken where username = %s",[username])
    x=c.fetchone()
    c.close()
    conn.commit()
    gc.collect()


    registration_id = x[1]
    message_title = mobile_number
    message_body = "Hi " + username + " Did you get call from "+ mobile_number + " ?"
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)


    c,conn = connection()
    c.execute("""UPDATE OnlineDriver SET with_customer = %s where username = %s""",(True,username))
    c.close()
    conn.commit()

    c,conn = connection()
    timeofride = str(datetime.datetime.now())
    c.execute("INSERT INTO Ride (mobile_number, username, timeofride, status) values (%s,%s,%s,%s)",(mobile_number, username,timeofride, "UNKNOWN"))
    conn.commit()
    c.close()
    gc.collect()
    return "success"

@app.route('/mydrivers',methods = ["POST"])
def mydrivers():
    mobile_number = request.form['mobile_number']
    c,conn = connection()
    c.execute("SELECT * FROM Ride where mobile_number = %s)",[mobile_number])
    x = c.fetchall()
    conn.commit()
    c.close()
    gc.collect()
    
    driver = []
    for row in x:
        z= {
            "username": row[1],
            "timeofride": row[2]
                }
        driver.append(z)
 

    driversinfo = []
    for a in driver:
        c,conn = connection()
        username = a['username']
        
        c.execute("SELECT * from Driver where username = %s ",[username])
        y=c.fetchone()
        conn.commit()
        c.close()
        gc.collect()
        d={
            "full_name": y[0],
            "mobile_number": y[3],
            "taxi_number": y[6],
            "timeofride": a['timeofride']
        }
        driversinfo.append(d)  

    drivers = {"drivers": driversinfo}    

    return json.dumps(drivers,indent = 0)



@app.route('/showinformationofride' , methods =["POST"])
def showinformationofride():
    mobile_number = request.form['mobile_number']

    c, conn = connection()
    c.execute("SELECT * from Ride where mobile_number = %s ORDER BY timeofride DESC  ",[mobile_number])
    x=c.fetchone()
    conn.commit()
    c.close()
    gc.collect()
    informationofride2 = []
    informationofride1={
    "current_driver" : x[0],
    "started_time" : x[1],
    "distance" : x[2],
    "duration_of_ride" : x[3],
    "fare" : x[4]
    }
    informationofride2.append(informationofride1)

    informationofride = {"informationofride":informationofride2}

    return json.dumps(informationofride,indent = 0)

@app.route('/customerlogout', methods = ['POST'])
def customerlogout():
    mobile_number = request.form['mobile_number']
    c, conn = connection()
    c.execute("DELETE from ForToken where mobile_number = %s ",[mobile_number])
    conn.commit()
    c.close()
    gc.collect()
    return "logged out"


#-----------------------------------------------------------------------------------------------------------

#for android app chalak driver

@app.route('/driverlogin', methods = ["POST"])
def driverlogin():
    username = request.form['username']
    password = request.form['password']
    token = request.form['token']
    
    c,conn = connection()
    c.execute("SELECT * from Driver where username = %s",[username])
    x= c.fetchone()
    c.close()
    conn.commit()
    gc.collect()
    if x:
        if x[5] == password:
            c,conn = connection()
            c.execute("SELECT * from ForToken where username =%s",[username])
            x= c.fetchone()
            c.close()
            conn.commit()
            gc.collect()

            if x:
                c,conn = connection()
                c.execute("DELETE from ForToken where username =%s",[username])
                c.close()
                conn.commit()
                gc.collect()



            c,conn = connection()
            c.execute("INSERT into ForToken (username, token) values(%s,%s)",(username,token))
            c.close()
            conn.commit()
            gc.collect()
            
            return "success"
        else:
            return "failed"

    else:
        return "Not a registered user"
        
@app.route('/driverforgotpassword',methods = ['POST'])
def driverforgotpassword():
    username = request.form['username']
    c, conn = connection()
    c.execute("SELECT * from Driver where username = %s",[username])
    x= c.fetchone()
    conn.commit()
    c.close()
    gc.collect()


    if x:
        password = x[5]
        mobile_number = x[3]
        sparrow2(mobile_number , password)
        return "Password is sent to your mobile number."
    else:
        return "Your number is not registered." 
              





#works fine
@app.route('/goonline',methods= ['POST'])
def goonline():
    username = request.form['username']
    latitude = float(request.form['latitude'])
    longitude = float(request.form['longitude']) 


    c, conn =connection()
    c.execute("SELECT * from OnlineDriver where username = %s",[username])
    x = c.fetchone()
    c.close()
    conn.commit()
    gc.collect()

    if x:
        c, conn =connection()
        c.execute("DELETE from OnlineDriver where username = %s",[username])
        c.close()
        conn.commit()
        gc.collect()

    else:
        pass

    c, conn = connection()    
    c.execute("""INSERT INTO OnlineDriver (username,longitude,latitude,with_customer) VALUES (%s,%s,%s,%s)""",(username,longitude,latitude,False))
    conn.commit()        
    c.close()
    
    gc.collect()
    return "online"

@app.route('/gotapassenger', methods = ['POST'])
def gotapassenger():
    username = request.form['username']
    c, conn = connection()
    c.execute("UPDATE OnlineDriver SET with_costumer = %s  WHERE username = %s ",(True, username))
    c.close()
    conn.commit()
    gc.collect()
    return "You have a costumer"

#currently working on
@app.route('/completedaride', methods = ['POST'])
def completedaride():
    username = request.form['username']
    distance = request.form['distance']
    time = request.form['time']
    fare = request.form['fare']

    c, conn = connection()
    c.execute("SELECT * from Ride where username = %s ORDER BY timeofride DESC  ",[username])
    x=c.fetchone()
    
    c.close()
    conn.commit()
    gc.collect()
    current_customer = x[5]
    
    c,conn = connection()
    c.execute("UPDATE Ride set distance = %s , time = %s , fare = %s where username = %s and mobile_number = %s ",(distance,time,fare,username,current_customer))
    conn.commit()
    c.close()    
    gc.collect()


    c, conn = connection()
    c.execute("UPDATE OnlineDriver SET with_costumer = %s  WHERE username = %s ",(False, username))
    conn.commit()
    c.close()
    
    gc.collect()
    return "You completed a ride."  



@app.route('/callyes', methods = ['POST'])
def callyes():
    username = request.form['username']

    c, conn = connection()
    c.execute("SELECT * from Ride where username = %s ORDER BY timeofride DESC  ",[username])
    x=c.fetchone()
    conn.commit()
    c.close()
    gc.collect()
    username = x[0]
    calledtimeofride = x[1]
    mobile_number = x[4]


    c,conn = connection()
    timeofride = datetime.datetime.now()
    c.execute("UPDATE Ride set status = %s WHERE username = %s and mobile_number = %s and timeofride = %s",("ACCEPTED", username,mobile_number , calledtimeofride))
    conn.commit()
    c.close()
    gc.collect()
    


    #c,conn = connection()
    #c.execute("""UPDATE OnlineDriver SET with_customer = %s where username = %s""",(True,username))
    #c.close()
    #conn.commit()

    return "callyes"

@app.route('/callno', methods = ['POST'])
def callno():
    username = request.form['username']
    c, conn = connection()
    c.execute("SELECT * from Ride where username = %s ORDER BY timeofride DESC  ",[username])
    x=c.fetchone()
    conn.commit()
    c.close()
    gc.collect()

    username = x[0]
    calledtimeofride = x[1]
    mobile_number = x[4]


    c,conn = connection()
    timeofride = str(datetime.datetime.now())
    c.execute("UPDATE Ride set status = %s WHERE username = %s and mobile_number = %s and timeofride = %s",("CANCELLED", username,mobile_number , calledtimeofride))
    conn.commit()
    c.close()
    gc.collect()
    

    c,conn = connection()
    c.execute("""UPDATE OnlineDriver SET with_customer = %s where username = %s""",(False,username))
    c.close()
    conn.commit()

    return "callNo"



@app.route('/alertcustomer',methods = ['POST'])
def alertcustomer():
    username = request.form['username']
    c, conn = connection()
    c.execute("SELECT * from Ride where username = %s ORDER BY timeofride DESC  ",[username])
    x=c.fetchone()
    conn.commit()
    c.close()
    gc.collect()
    mobile_number = x[4]

    #c,conn = connection()
    #c.execute("SELECT * from ForCustomerToken where mobile_number = %s",[mobile_number])
    #x=c.fetchone()
    #conn.commit()
    #gc.collect()

    #registration_id = x[1]
    #message_title = "Driver Arrival!"
    #message_body = "The driver you requested has arrived. Have a safe ride !"
    #result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

    return mobile_number



@app.route('/gooffline', methods = ['POST'])
def gooffline():
    username = request.form['username']
    c, conn = connection()    
    c.execute("""DELETE FROM OnlineDriver WHERE username = %s""",(username,))   
    conn.commit()        
    c.close()
    
    gc.collect()
    return "You went offline."



@app.route('/updateme', methods = ['POST'])
def updateme():
    username = request.form['username']
    latitude = float(request.form['latitude'])
    longitude = float(request.form['longitude']) 
    c, conn =connection()
    c.execute("DELETE from OnlineDriver where username = %s",[username])
    c.close()
    conn.commit()
    gc.collect()
    c, conn = connection()
    c.execute("""UPDATE OnlineDriver SET longitude =%s  , latitude =%s , with_costumer = %s WHERE username = %s""",(longitude,latitude,False ,username,))
    conn.commit()
    c.close()
    
    gc.collect()
    return "Your location has been updated."



@app.route('/mycustomers',methods = ["POST"])
def mycustomers():
    username = request.form['username']
    c,conn = connection()
    c.execute("SELECT * FROM Ride where username = %s",[username])
    x = c.fetchall()
    conn.commit()
    c.close()
    gc.collect()
    
    if len(x) == 0:
        return "Not a single ride"
    else:
        pass

    customer = []
    for row in x:
        z= {
            "mobile_number": row[4],
            "timeofride": str(row[1]),
            "status" : row[6]
            }
        customer.append(z)
   
    customersinfo = []
    for a in customer:
        c,conn = connection()
        mobile_number = a['mobile_number']
        c.execute("SELECT * from Customer where mobile_number = %s ",[mobile_number])
        y=c.fetchone()
        c.close()
        conn.commit()
        gc.collect()
        m={
            "full_name" : y[0],
            "mobile_number": mobile_number,
            "timeofride": a['timeofride'],
            "status" : a['status']  
        }
        customersinfo.append(m)  

    customers = {"customers": customersinfo}    

    return json.dumps(customers,indent = 0)


@app.route('/requesttoblock',methods = ['POST'])
def requesttoblock():

    username = request.form['username']
    mobile_number = request.form['mobile_number']
    c, conn = connection()
    c.execute("SELECT * from RequestToBlock where mobile_number = %s ",[mobile_number])
    x= c.fetchall()
    conn.commit()
    c.close()
    gc.collect()
    if len(x) == 4:
        c,conn = connection()
        c.execute("INSERT into Block (mobile_number) values (%s)",(mobile_number))
        conn.commit()
        c.close()
        gc.collect()

    
    else:
        c,conn = connection()
        c.execute("INSERT into RequestToBlock (mobile_number, requested_by) values (%s,%s)",(mobile_number,username))
        conn.commit()
        c.close()
        gc.collect()


    return "Your request to block "+ mobile_number + "has been considered."


@app.route('/driverlogout', methods = ['POST'])
def driverlogout():
    username = request.form['username']
    c, conn = connection()
    c.execute("DELETE from ForToken where username = %s ",[username])
    conn.commit()
    c.close()
    gc.collect()
    return "logged out" + username



if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')
    app.run(debug=True, use_reloader=True)
