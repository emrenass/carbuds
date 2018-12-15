from flask import Flask, request, make_response,render_template, Blueprint, jsonify, redirect
import psycopg2
import psycopg2.extras
import base64


app = Flask(__name__)


#image database
hostname = '35.205.45.78'
username = 'postgres'
password = 'postgres'
database = 'carbuds_backend'
portno = '5432'

#auth server for session confirmation
auth_hostname = '35.205.45.78'
auth_username = 'postgres'
auth_password = 'postgres'
auth_database = 'carbuds_backend'
auth_portno = '5432'

app.config['DEBUG'] = True

def check_session( user_id, session_token):
    #check at auth server
    return True

@app.route("/")
def hello_images():
    return "THIS IS AN IMAGE SERVER OF CARBUDS"

@app.route("/get_pfp", methods=["POST"])
def getspfp():
    user_id = request.json['user_id']

    if check_session(user_id, "") != True:
        return "SESSION DOES NOT EXIST"

    myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database, port=portno)

    qString = "SELECT id, image FROM user_pfp WHERE id =" + str(user_id)
    with myConnection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(qString)
        rows = cur.fetchall()
        myConnection.close()

        if( str(len(rows)) < 1 or rows[0]['image'] == None):
            return "NONE"

        bitmap_encoded = base64.b64encode(str(rows[0]['image']).decode('hex'))

        print(bitmap_encoded)
        return bitmap_encoded

    return "UNHANDLED ERROR AT GET_PFP"


@app.route("/set_pfp", methods=["POST"])
def setspfp():
    user_id = request.json['user_id']
    bitmap = request.json['bitmap']

    if check_session( user_id, "") != True:
        return "SESSION DOES NOT EXIST"

    bitmap_real = base64.b64decode(bitmap).encode('hex')

    myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database, port=portno)

    qString = "SELECT id, image FROM user_pfp WHERE id =" + str(user_id)
    with myConnection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(qString)
        rows = cur.fetchall()

        print(str(len(rows)))
        if( len(rows) < 1 ):
            #Insert if empty
            cur.execute("INSERT INTO user_pfp(id, image) VALUES(" + str(user_id) + ", %s )", (psycopg2.Binary(bitmap_real),))
            myConnection.commit()
        else:
            # Update if not
            cur.execute("UPDATE user_pfp SET image  = %s WHERE id = " + str(user_id), (psycopg2.Binary(bitmap_real),))
            myConnection.commit()
        myConnection.close()
        return str(0)

    return "UNHANDLED ERROR AT SET_PFP"


if __name__=='__main__':
    app.run(host='0.0.0.0', port=80)



