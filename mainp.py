from flask import Flask, render_template, flash, request , url_for, session, jsonify
from dbConnect import connection
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc



class onlinedriver(object):

    def __init__(self, username, latitude, longitude):
        
        self.username = username
        self.latitude = latitude
        self.longitude = longitude


app = Flask(__name__)

@app.route('/')
def main():
    return "index"

@app.route('/register', methods = ['GET','POST'])
def register():

    try:
       
        if request.method == "POST":
            entered_full_name = request.form['username']
            entered_license_number = request.form['license_number'] 
            entered_address = request.form['address'] 
            entered_mobile_number = request.form['mobile_number'] 
            entered_username = request.form['username'] 
            entered_password = request.form['password'] 
            entered_taxi_number = request.form['taxi_number'] 
            c, conn = connection()
            #x = c.execute("SELECT * FROM Drivers WHERE username = (%s)", (entered_username))
            

            #if int(x) == 1:
             #   return render_template('register.html')
                
            #else:
            #c.execute("INSERT INTO Driver (full_name,license_number,address,mobile_number,username,password,taxi_number) VALUES (%s,%s,%s,%s,%s,%s,%s)",thwart(entered_full_name), thwart(entered_license_number),thwart(entered_address),thwart(entered_mobile_number),thwart(entered_username),thwart(entered_password),thwart(entered_taxi_number))
            c.execute("""INSERT INTO Driver (full_name,license_number,address,mobile_number,username,password,taxi_number) VALUES (%s,%s,%s,%s,%s,%s,%s)""",(entered_full_name, entered_license_number,entered_address,entered_mobile_number,entered_username,entered_password,entered_taxi_number))
            conn.commit()
                
            c.close()
            conn.close()
            gc.collect()
            
                #session['logged_in'] = True
                #session['username'] = entered_username 
            return "Register bhayo." + entered_full_name
            
        else:    
            return render_template("register.html")
            
            
    except Exception as e:
        
        return render_template("register.html")

   
@app.route('/login', methods = ['GET','POST'])
def login():
   
    try:
        if request.method == "POST":
            attempted_username = request.form['username']
            attempted_password = request.form['password']
                   
            if attempted_username == "admin" and attempted_password == "password":
                return "you are correct my boy"
                
            else:
                flash('Login failed. Please enter the correct username and password.')
                return render_template("login.html")
                
        else:
           return render_template("login.html")
                
    except Exception as e:
        
        return render_template("login.html")



@app.route('/findmeataxi')
def findmeataxi():

    c , conn = connection()
    c.execute("SELECT * FROM OnlineDriver")
    results = c.fetchall()
    for row in results:

        username = row[0]
        longitude = row[1]
        latitude = row[2]


    conn.commit()         
    c.close()
    conn.close()
    gc.collect()
       
    list = [
          {
          "mobile":"9845153645"
          },
        
          {
             "username":username,
             "longitude": longitude,
             "latitude": latitude,
             
          }
                     
    ]
    #return "hello"
    return jsonify(results =list)

    

@app.route('/goonline')
def goonline():
    username = "sudip235"
    longitude = 27.6956
    latitude = 85.8495

    c, conn = connection()
    
    c.execute("""INSERT INTO OnlineDriver (username,longitude,latitude) VALUES (%s,%s,%s)""",(username,longitude,latitude))
    conn.commit()
        
    c.close()
    conn.close()
    gc.collect()

    return "went online"



@app.route('/gooffline')
def gooffline():
    username = "sudip235"
    c, conn = connection()
    
    c.execute("""DELETE FROM OnlineDriver WHERE username = %s""",(username,))
   
    conn.commit()
        
    c.close()
    conn.close()
    gc.collect()


    return "went offline"



@app.route('/updateme')
def updateme():
    username = "sudip235"
    longitude = 27.695545
    latitude = 85.849534534

    c, conn = connection()
    c.execute("""UPDATE OnlineDriver SET longitude =%s  , latitude =%s  WHERE username = %s""",(longitude,latitude,username,))
    conn.commit()
        
    c.close()
    conn.close()
    gc.collect()




    return "updated location"






if __name__ == "__main__":
    app.run()
