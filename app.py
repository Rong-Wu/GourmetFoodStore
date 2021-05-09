
from flask import Flask, render_template, request, json, redirect,url_for,flash
from flaskext.mysql import MySQL
from flask import session
from flask import jsonify
import math
import pymysql
import time
import os
import re
import bcrypt

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'GourmetFood'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 8889
mysql.init_app(app) 

# app.config['MYSQL_DATABASE_USER'] = 'dotasks'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'task123456'
# app.config['MYSQL_DATABASE_DB'] = 'tasks'
# app.config['MYSQL_DATABASE_HOST'] = '49.233.184.42'
# app.config['MYSQL_DATABASE_PORT'] = 3306

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
            return render_template('error.html', error='no products')

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
        if not password_check(_password):
            return render_template('signup.html', error = 'password is too weak')
        else:
            salt = bcrypt.gensalt()
            _hashedPass = bcrypt.hashpw(_password.encode('utf-8'),salt)
            try:
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
                cursor.execute("INSERT INTO tbl_user(name, email, password,is_admin) VALUES (%s, %s, %s, %s)", (_name, _email, _hashedPass, _isadmin))
                data = cursor.fetchall() 
                
                if len(data) == 0:
                    conn.commit()
                    return render_template('signup.html', message = 'User created successfully !')
                else:
                    return json.dumps({'error':str(data[0])})
            except Exception as e:
                return render_template('error.html',error = str(e))
            finally:
                cursor.close()
                conn.close()
    else:
        return render_template('signup.html', error = "Enter the required fields!")



@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')


@app.route('/admin', methods=['GET'])
def admin():
    try:
        con = mysql.connect()
        cursor = con.cursor()
        if session.get('is_admin', None):
            cursor.execute("SELECT * FROM tbl_product")
            data = cursor.fetchall()
            return render_template('adminportal.html', products=data)
        else:
            return render_template('signin.html', error="You don't have permission")

    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()

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
            hashed = data[0][2]
            if bcrypt.checkpw(_password.encode('utf-8'), hashed.encode('utf-8')):
            # if str(data[0][2]) == _password:
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
    session.pop('is_admin', None)
    return redirect('/')


@app.route('/addToCart',methods=['POST', 'GET'])
def addToCart():
    if not session.get('user_id'):
        return redirect('/')
    try:
        qty = int(request.form['inputQty'])
        product_id = request.form['productID']

        if qty and product_id and request.method =='POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM tbl_product where id= %s ",(product_id)) 
            row = cursor.fetchone()

            all_total_price = 0
            all_total_quantity = 0 

            itemArray = {str(row['id']):{'name': row['name'], 'quantity':qty, 'price':row['price'],'image':row['picture_url'],'total_price':qty*row['price']}}
        
            session.modified =True
            # if cart is not empty
            if 'cart_item' in session:
                # if item already in cart
                if str(row['id']) in session ['cart_item']:
                    for key,value in session['cart_item'].items():
                        if str(row['id']) == key:
                            old_quantity = int(session['cart_item'][key]['quantity'])
                            total_quantity = old_quantity + qty
                            session['cart_item'][key]['quantity']=total_quantity
                            session['cart_item'][key]['total_price']= total_quantity*row['price']
                
                # if item not in the cart
                else:
                    session['cart_item'] = array_merge(session['cart_item'],itemArray)
                
                for key, value in session['cart_item'].items():
                    ind_quantity = int(session['cart_item'][key]['quantity'])
                    ind_price = float(session['cart_item'][key]['total_price']) 
                    all_total_quantity = all_total_quantity + ind_quantity
                    all_total_price = all_total_price + ind_price
            
            # if cart is empty
            else:
                session['cart_item'] = itemArray
                all_total_quantity = all_total_quantity + qty
                all_total_price = all_total_price + qty*row['price']

            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price
            # flash('Item successfully added to cart!!','success')
            return redirect('/')
        else:
            return 'Error while adding item to cart'
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()



@app.route('/cart',methods=['POST', 'GET'])
def cart():
    if session.get('user_id'):
        _userid =session.get('user_id')
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM tbl_user where id= %s ",(_userid))                                                                                                      
        _username = cursor.fetchone()


        return render_template('cart.html', username=_username[0])
    else: 
        return redirect('/showSignin')


@app.route('/removeFromCart',methods=['POST', 'GET'])
def removeFromCart():
    if session.get('user_id'):
        _userid =session.get('user_id')

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM tbl_user where id= %s ",(_userid))                                                                                                      
        _username = cursor.fetchone()

        product_id=request.args.get('_id')

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
                session.pop('cart_item')  
            else:
                session['all_total_quantity'] = all_total_quantity
                session['all_total_price'] = all_total_price

            return render_template('cart.html', username=_username[0])
        except Exception as e:
            return render_template('error.html',error = str(e))
    else:
        return redirect('/showSignin')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    try:
        _userid =session.get('user_id')
        if 'cart_item' in session:
            all_total_price = session['all_total_price']
            all_total_quantity = session['all_total_quantity']
            
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tbl_order (user_id, total_price) VALUES '(%s,%s)' ",(_userid, all_total_price)) 
            _orderid = cursor.fetchone()
            # for key, value in session['cart_item'].items():
            #     _price = session['cart_item'][key]['price']
            #     _num = session['cart_item'][key]['quantity']
            #     cursor.execute("INSERT INTO tbl_order_detail(order_id, product_id, price,num) value (%s,%s,%s,%s) ",(_order_id,_userid, _price,_num))                                                                                                   
            

           
        
            cursor.execute("SELECT * FROM tbl_user WHERE id = %s", (_userid))
            data = cursor.fetchall()

            if len(data) > 0:
                # empty the shop cart
                session.pop('cart_item') 

                return render_template('checkout.html',data=data[0], order_id=_orderid,num= all_total_quantity, all_total_price= all_total_price)
            return render_template('checkout.html')
        else:           
            return redirect('/') 
        

    except Exception as e:
        return render_template('error.html',error = str(e))    



@app.route('/emptyCart')
def emptyCart():
    try:
        session.pop('cart_item')   
        return redirect('/cart')   
    except Exception as e:
        return render_template('error.html',error = str(e))



@app.route('/addproduct', methods=['GET', 'POST'])
def add_product():
    con = mysql.connect()
    cursor = con.cursor()
    try:
        if request.method == 'GET':
            return render_template('addproduct.html')
        else:

            name = request.form['inputname']
            description = request.form['inputDescription']
            inventory = request.form['inputInventory']
            price = request.form['inputPrice']
            picture = request.files.get('inputPicture')
            cate = request.form['cate']
            img_db_path = 'static/img/' + str(time.time()).replace('.', '') + '.' + picture.filename.split('.')[-1]
            cursor.execute('insert into tbl_product(name, description, inventory, price, picture_url,category_id) value '
                           '("%s", "%s", %s, %s, "%s", %s)' % (name,description, inventory, price, img_db_path, cate))
            con.commit()
            picture.save('%s/%s' % (basedir, img_db_path))
            cursor.close()
            con.close()
            return redirect('/admin')
    except Exception as e:
        cursor.close()
        con.close()
        return render_template('error.html', error=str(e))

@app.route('/editproduct', methods=['GET', 'POST'])
def edit_item():
    con = mysql.connect()
    cursor = con.cursor()
    p_id = request.args.get('_id')
    try:
        if request.method == 'GET':
            cursor.execute("SELECT * FROM tbl_product where id= %s ", p_id)
            product = cursor.fetchall()
            if product:
                return render_template('editproduct.html', product=product[0])
            else:
                return render_template('error.html', error='There is no such product!')
        else:
            name = request.form['inputname']
            description = request.form['inputDescription']
            inventory = request.form['inputInventory']
            price = request.form['inputPrice']
            picture = request.files.get('inputPicture', None)
            cate = request.form['cate']
            if picture:
                img_db_path = 'static/img/' + str(time.time()).replace('.', '') + '.' + picture.filename.split('.')[-1]
                cursor.execute('update tbl_product set name="%s", description="%s", inventory=%s, price=%s, picture_url="%s",category_id=%s where id=%s' % (name,description, inventory, price, img_db_path, cate, p_id))
                con.commit()
                picture.save('%s/%s' % (basedir, img_db_path))
            else:
                cursor.execute(
                    'update tbl_product set name="%s", description="%s", inventory=%s, price=%s,category_id=%s where id=%s' % (
                    name, description, inventory, price, cate, p_id))
                con.commit()
            cursor.close()
            con.close()
            return redirect('/admin')
    except Exception as e:
        cursor.close()
        con.close()
        return render_template('error.html', error=str(e))

@app.route('/deleteprod')
def delete_item():
    product_id = request.args.get('_id')

    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute("delete from tbl_product where id = %s" % product_id)

    con.commit()
    return redirect('/admin')


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
