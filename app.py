
from flask import Flask, render_template, request, json, redirect,url_for
from flaskext.mysql import MySQL
from flask import session
from flask import jsonify
import math

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'GourmetFood'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 8889
mysql.init_app(app) 


app.secret_key = 'secret key'

@app.route("/") # define an url "/" home page
def main():
    try:
        if session.get('user_id'):
            _userid =session.get('user_id')
        
        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tbl_product")
        data = cursor.fetchall()

        if len(data)>= 0 :
            conn.commit()
            return render_template('home.html',products=data)
        else:
            return render_template ('error.html', error='no products')
       
    except Exception as e:
        return render_template('error.html',error = str(e))
	

@app.route('/showSignUp') 
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp',methods=['POST']) 
def signUp():
    
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    _isadmin = 0
 
    # validate the received values
    if _name and _email and _password:

        conn = mysql.connect()
        cursor = conn.cursor() 

        #check if user name or email already exist
        cursor.execute("SELECT * FROM tbl_user WHERE name = %s", (_name))
        if cursor.fetchone() is not None:   
            return render_template('signup.html', error = "That username is already taken, please choose another")
        
        cursor.execute("SELECT * FROM tbl_user WHERE email = %s", (_email))
        if cursor.fetchone() is not None:   
            return render_template('signup.html', error = "That email is already taken, please choose another")

        # create new user
        cursor.execute("INSERT INTO tbl_user(name, email, password,is_admin) VALUES (%s, %s, %s, %s)", (_name, _email, _password, _isadmin))
        data = cursor.fetchall() 
        
        if len(data) == 0:
            conn.commit()
            return render_template('signup.html', message = 'User created successfully !')
        else:
            return json.dumps({'error':str(data[0])})

    else:
        return json.dumps({'error':'Enter the required fields!'})


@app.route('/showSignin') 
def showSignin():
    return render_template('signin.html')


@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    try:
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        con = mysql.connect()
        cursor = con.cursor()
        

        cursor.execute("SELECT * FROM tbl_user WHERE email = %s", (_email))

        data = cursor.fetchall()


        if len(data) > 0:
            if str(data[0][2]) == _password:
                session['user_id'] = data[0][0]
                return redirect('/') #login success
            else:
                return render_template('signin.html', error = 'Password incorrect, please try enter correct password')
        else:
            return render_template('signin.html', error = 'Email incorrect, please enter correct email')

    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()

@app.route("/search", methods=['POST', 'GET'])
def search():
    try:
        if session.get('user_id'):
            _userid =session.get('user_id')
        
        _keyword = request.form['search']
            
        
        conn = mysql.connect()
        cursor = conn.cursor()
        #SearchContent = "SELECT * FROM tbl_product where name like %{}% ".formet(_keyword)
        #cursor.execute(SearchContent)
        cursor.execute("SELECT * FROM tbl_product where name like %s ",('%'+_keyword+'%'))                                                                                                       
        data = cursor.fetchall()

        if len(data)>= 0 :
            conn.commit()
            return render_template('SearchResult.html',result=data)
        else:
            return render_template ('error.html', error='no search result')
       
    except Exception as e:
        return render_template('error.html',error = str(e))


@app.route("/Category", methods=['POST', 'GET'])
def Category():
    try:
        if session.get('user_id'):
            _userid =session.get('user_id')
        
        if request.method == 'GET':
            cate_id=request.args.get('_id')
        
        conn = mysql.connect()
        cursor = conn.cursor()
        #SearchContent = "SELECT * FROM tbl_product where name like %{}% ".formet(_keyword)
        #cursor.execute(SearchContent)
        cursor.execute("SELECT * FROM tbl_product where category_id= %s",(cate_id))                                                                                                    
        data = cursor.fetchall()

        if len(data)>= 0 :
            conn.commit()
            return render_template('SearchResult.html',result=data)
        else:
            return render_template ('error.html', error='no search result')
       
    except Exception as e:
        return render_template('error.html',error = str(e))

@app.route("/productinfo", methods=['POST', 'GET'])
def productinfo():
    if session.get('user_id'):
        _userid =session.get('user_id')
    try:
        if request.method == 'GET':
            product_id=request.args.get('_id')
            session['product_id']= product_id

            conn = mysql.connect()
            cursor = conn.cursor()
        #SearchContent = "SELECT * FROM tbl_product where name like %{}% ".formet(_keyword)
        #cursor.execute(SearchContent)
            cursor.execute("SELECT * FROM tbl_product where id= %s ",(product_id))                                                                                                      
            data = cursor.fetchall()

        if len(data)>= 0 :
            conn.commit()
            return render_template('productinfo.html',result=data)
        else:
            return render_template ('error.html', error='no search result')
       
    except Exception as e:
        return render_template('error.html',error = str(e))


@app.route('/logout')
def logout():
    session.pop('user_id',None) #destroy the session
    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)  
    # app.run()




