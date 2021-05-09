
from flask import Flask, render_template, request, json, redirect,url_for
from flaskext.mysql import MySQL
from flask import session
from flask import jsonify
import math
import pymysql

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


@app.route('/showProfile')
def showProfile():
    if not session.get('user_id'):
        return redirect('/')

    _userid =session.get('user_id')

    try:
        con = mysql.connect()
        cursor = con.cursor()
        
        cursor.execute("SELECT * FROM tbl_user WHERE id = %s", (_userid))

        data = cursor.fetchall()

        if len(data) > 0:
            return render_template('profile.html', data = data[0])
        else:
            flash("Sorry, user does not exist")
            return redirect('/')

    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()

@app.route('/showPurchases')
def showPurchases():
    if not session.get('user_id'):
        return redirect('/')

    _userid =session.get('user_id')

    try:
        con = mysql.connect()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        
        cursor.execute("SELECT * FROM tbl_order WHERE user_id = %s", (_userid))

        orders = cursor.fetchall()

        return render_template('orders.html', orders = orders)

    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()

@app.route("/viewOrderDetail/<order_id>", methods=['POST','GET'])
def viewOrderDetail(order_id):
    if not session.get('user_id'):
        return redirect('/')
    try:
        con = mysql.connect()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        
        # get that specific order from tbl_order //for total price and date
        print("first")
        cursor.execute("SELECT * FROM tbl_order WHERE order_id = %s", (order_id))
        order = cursor.fetchone()

        # get all the items/products and quantity from tbl_order_detail
        cursor.execute("SELECT * FROM tbl_order_detail WHERE order_id = %s", (order_id))
        items = cursor.fetchall()

        products = []
        #get the detail of each product
        for item in items:
            print(item['product_id'])
            cursor.execute("SELECT * FROM tbl_product WHERE id = %s", (item['product_id']))
            product = cursor.fetchone()
            print(product)
            product['num'] = item['num']
            products.append(product)

        return render_template('orderDetail.html', order = order, products = products)

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
    try:
        if session.get('user_id'):
            _userid =session.get('user_id')
        if request.method == 'GET':
            product_id=request.args.get('_id')
            session['product_id']= product_id

            conn = mysql.connect()
            cursor = conn.cursor()
        
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


@app.route('/addToCart',methods=['POST', 'GET'])
def addToCart():
    if session.get('user_id'):
        _userid =session.get('user_id')
        qty = 1
        # qty = int(request.form['inputQty'])
        product_id = int(request.args.get('_id'))

        all_total_price =0
        all_tatal_quantity =0

        conn = mysql.connect()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tbl_product where id= %s ",(product_id))                                                                                                      
        row = cursor.fetchall()

        itemArray = {row['id']:{'name': row['name'], 'quantity':qty, 'price':row['price'],'image':row['picture_url'],'total_price':qty*row['price']}}
 
        
        
        session.modifed =True
        if 'cart_item' in session:
            if row['id'] in seesion ['cart_item']:
                for key,value in session['cart_item'].items():
                    if row[0] ==key:
                        old_quantity = int(session['cart_item'][key]['quantity'])
                        total_quantity = old_quantity + qty
                        session['cart_item'][key]['quantity']=total_quantity
                        session['cart_item'][key]['total_price']= total_quantity*row['price']
                
            else:
                session['cart_item'] = array_merge(session['car_item'],itemArray)
            
            for key, value in session['cart_item'].items():
                ind_quantity = int(session['cart_item'][key]['quantity'])
                ind_price = float(session['cart_item'][key]['price']) 
                all_total_quantity = all_total_quantity + ind_quantity
                all_total_price = all_total_price + ind_quantity
            

        else:
            session['cart_item'] = itemArray
            all_tatal_quantity = all_tatal_quantity + qty
            all_total_price = all_total_price + qty*row['price']

        session['all_total_quantity'] = all_tatal_quantity
        session['a''_total_price'] = all_total_price
        # flash('Item successfully added to cart!!','success')
        return redirect('/')
    else:
        return redirect('/showSignin')

@app.route('/cart',methods=['POST', 'GET'])
def cart():
    if session.get('user_id'):
        _userid =session.get('user_id')
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM tbl_product where id= %s ",(_userid))                                                                                                      
        _UserName = cursor.fetchall()


        if 'cart_item' in session:
            return render_template('cart.html',UserName = _UserName)
        else:
            return render_template('home.html', message = 'Cart is empty, choose your Gourmet !!!')
    else: return redirect('/showSignin')


@app.route('/removeFromCart',methods=['POST', 'GET'])
def removeFromCart():
    product_id=int(request.args.get('_id'))

    try:
        all_total_price =0
        all_total_quantity =0
        session.modified = True

        for item in session['cart_item'].items():
            if item[0] == product_id:
                session['cart_item'].pop(item[0],None)
                if 'cart_item' in session:
                    for key, value in session['cart_item'].items():
                        ind_quantity = session['cart_item'][key]['quantity']
                        ind_price = session['cart_item'][key]['price'] 
                        all_total_quantity = all_total_quantity + ind_quantity
                        all_total_price = all_total_price + ind_quantity
                break
        if all_total_quantity ==0:
            session['cart_item'].clear()
        else:
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price

        return render_template('/cart.html')
    except Exception as e:
        return render_template('error.html',error = str(e))

@app.route('/emptyCart',methods=['POST', 'GET'])
def emptyCart():
    try:
        session['cart_items'].clear()
        return redirect('/')
    
    except Exception as e:
        return render_template('error.html',error = str(e))

def array_merge(first_array, second_array):
    if isinstance( first_array,list) and isinstance(second_array, list):
        return first_array + second_array
    elif isinstance(first_array, dict) and isinstance(second_array, dict):
        return dict( list(first_array.items())+ list(second_array.items()) )
    elif isinstance(first_array, set) and isinstance(second_array, set):
         return first_array.union (second_array)
    return False


if __name__ == "__main__":
    app.run(debug=True)  
    # app.run()




