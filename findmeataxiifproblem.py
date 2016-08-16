@app.route('/findmeataxi')
def findmeataxi():

    latitude = 85.000
    longitude = 23.000
    w = latitude + 0.15060
    x = latitude - 0.15060
    y = longitude + 0.15060
    z = longitude - 0.15060

    c , conn = connection()
    #c.execute("""SELECT * FROM OnlineDriver WHERE longitude BETWEEN %s AND %s AND latitude BETWEEN %s AND %s""",(z,y,x,w))
    c.execute("""SELECT * FROM OnlineDriver""")
    y = []
    x = c.fetchall()
    #for each in x:
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
    conn.close()
    gc.collect()
     

   

    return json.dumps(w, indent=0)
