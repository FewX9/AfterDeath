import re
from flask import *
from datetime import datetime
import mysql.connector
import os
import requests

try:
    db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="afterdeath"
    )
except:
    print('===========================')
    print('database is not connected!!')
    print('===========================')
    os._exit(0)

app = Flask(__name__)

@app.route('/')
def home():
    sql = "SELECT * FROM item WHERE collection = 'set'"
    cursor = db.cursor()
    cursor.execute(sql)
    i_set = cursor.fetchall()

    sql = "SELECT * FROM item WHERE recommend = 'true' AND collection = 'coffin' AND stock != '0'"
    cursor = db.cursor()
    cursor.execute(sql)
    i_coffin = cursor.fetchall()
    msg = None
    
    return render_template('index.html',data_set=i_set,data_coffin=i_coffin , msg=msg)

@app.route('/coffin')
def coffin():
    sql = "SELECT * FROM item WHERE collection = 'coffin' AND stock != '0'"
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return render_template('coffin.html', data = result)

@app.route('/flower')
def flower():
    sql = "SELECT * FROM item WHERE collection = 'flower' AND stock != '0'"
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return render_template('flower.html', data = result)

@app.route('/food')
def food():
    sql = "SELECT * FROM item WHERE collection = 'food' AND stock != '0'"
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return render_template('food.html', data = result)

@app.route('/gift')
def gift():
    sql = "SELECT * FROM item WHERE collection = 'gift' AND stock != '0'"
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return render_template('gift.html', data = result)

@app.route('/check')
def check():
    return render_template('check.html')

@app.route('/backend/cancle_order/<postID>')
def cancle_order(postID):
    if session.get('logged_in'):
        sql = "UPDATE c_order set status= 'ยกเลิก' WHERE id = '%s' " % (postID)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()

        msg = 'cancle'

        return redirect(url_for('order_list',msg=msg))
    else:
        return redirect(url_for('backend_login'))

@app.route('/backend/delete_order/<postID>')
def delete_order(postID):
    if session.get('logged_in'):
        sql = "DELETE FROM c_order WHERE id='%s'"%(postID)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()

        msg = 'delete'

        return redirect(url_for('order_list',msg=msg))
    else:
        return redirect(url_for('backend_login'))

@app.route('/backend/order_success/<postID>')
def order_success(postID):
    if session.get('logged_in'):
        sql = "UPDATE c_order set status= 'จัดส่งสำเร็จ'  WHERE id = '%s' " % (postID)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()

        msg = 'success'

        return redirect(url_for('order_list',msg=msg))
    else:
        return redirect(url_for('backend_login'))

@app.route('/backend/order_list')
def order_list():
    if session.get('logged_in'):
        sql = "SELECT * FROM c_order"
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        if request.args.get('msg') != None:
            msg = request.args.get('msg')
        else:
            msg = None
        return render_template('/backend/order.html',data=result,msg=msg)
    else:
        return redirect(url_for('backend_login'))

@app.route('/backend/item_edit/<postID>',methods=['POST', 'GET'])
def item_edit(postID):
    if session.get('logged_in'):
        sql = "SELECT * FROM item WHERE id = '%s'"%(postID)
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        msg = None
        return render_template('backend/item_edit.html',data=result,msg=msg)
    else:
        return redirect(url_for('backend_login'))

@app.route('/status', methods=['POST'])
def status():
    _phone = request.form.get('phone')
    sql = "SELECT * FROM c_order WHERE phone = '%s'"%(_phone)
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    
    if result:
        status = "warning"
        if result[6] == 'ยกเลิก':
            status = "danger"
        elif  result[6] == 'จัดส่งสำเร็จ':
            status = "secondary"
        else:
            status = "warning"
        return render_template('status.html',data=result,status=status)
    else:
        return render_template('status.html',data='no-data')

@app.route('/login') 
def backend_login():
    session['logged_in'] = False
    msg = None
    return render_template('backend/login-backend.html',msg=msg)

@app.route('/backend/add_confirm', methods=['POST'])
def add_confirm():
    if session.get('logged_in'):
        _name = request.form.get('i_name')
        _price = request.form.get('i_price')
        _stock = request.form.get('i_stock')
        _col = request.form.get('collection')
        _rec = request.form.get('recommend')
        _img = request.files['i_img']

        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        UPLOAD_FOLDER = 'static/img/item'
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        _filename = '%s_%s'%(now,_img.filename)
        _img.save(os.path.join (app.config['UPLOAD_FOLDER'],_filename))

        sql = "INSERT INTO item (name, price, count, img, collection, recommend, stock) VALUES ('%s', '%s', '0', '%s', '%s', '%s', '%s');" % (_name,_price,_filename,_col,_rec,_stock)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        message = 'success'
        return render_template('backend/item_add.html', message=message)
    else:
        return redirect(url_for('backend_login'))

@app.route('/backend/add_item')
def add_item():
    if session.get('logged_in'):
        message = None
        return render_template('backend/item_add.html', message=message)
    else:
        return redirect(url_for('backend_login'))
    

@app.route('/backend/item_delete/<postID>/<coll>')
def item_delete(postID,coll):
    sql = "DELETE FROM item WHERE id='%s'"%(postID)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    if coll == 'coffin':
        return redirect(url_for('edit_coffin'))
    elif coll == 'food':
        return redirect(url_for('edit_food'))
    elif coll == 'gift':
        return redirect(url_for('edit_gift'))
    else:
        return 'Error'

@app.route('/backend/edit_confirm/<postID>', methods=['POST'])
def edit_confirm(postID):
    if session.get('logged_in'):
        _id = postID
        _name = request.form.get('edit_name')
        _price = request.form.get('edit_price')
        _sell = request.form.get('edit_sell')
        _stock = request.form.get('edit_stock')

        if not request.files.get('edit_img', None):
            sql = "UPDATE item set name= '%s', price= '%s', count= '%s', stock = '%s' WHERE id = '%s' " % (_name, _price, _sell, _stock, _id)
        else:
            _img = request.files['edit_img']
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            UPLOAD_FOLDER = 'static/img/item'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            _filename = '%s_%s'%(now,_img.filename)
            _img.save(os.path.join (app.config['UPLOAD_FOLDER'],_filename))

            sql = "UPDATE item set name= '%s', price= '%s', count= '%s', stock = '%s', img = '%s' WHERE id = '%s' " % (_name, _price, _sell, _stock, _filename, _id)

        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()

        sql = "SELECT * FROM item WHERE id = '%s'"%(postID)
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        msg = 'edit'
        
        return render_template('backend/item_edit.html',data=result,msg=msg)
    else:
        return redirect(url_for('backend_login'))

@app.route('/backend/edit_coffin')
def edit_coffin():
    if session.get('logged_in'):
        sql = "SELECT * FROM item WHERE collection = 'coffin'"
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        return render_template('backend/edit_coffin.html', data=result)
    else:
        return redirect(url_for('backend_login'))

@app.route('/backend/edit_gift')
def edit_gift():
    if session.get('logged_in'):
        sql = "SELECT * FROM item WHERE collection = 'gift'"
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        return render_template('backend/edit_gift.html', data=result)
    else:
        return redirect(url_for('backend_login'))

@app.route('/backend/edit_flower')
def edit_flower():
    if session.get('logged_in'):
        sql = "SELECT * FROM item WHERE collection = 'flower'"
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        return render_template('backend/edit_flower.html', data=result)
    else:
        return redirect(url_for('backend_login'))

@app.route('/backend/edit_food')
def edit_food():
    if session.get('logged_in'):
        sql = "SELECT * FROM item WHERE collection = 'food'"
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        return render_template('backend/edit_food.html', data=result)
    else:
        return redirect(url_for('backend_login'))

@app.route('/backend/report')
def backend_report():
    if session.get('logged_in'):
        sql = "SELECT * FROM report"
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        return render_template('backend/report.html', data=result)
    else:
        return redirect(url_for('backend_login'))

@app.route('/backend/report_add', methods=['POST'])
def backend_report_add():
    if session.get('logged_in'):
        _date = request.form.get('date-in')
        _income = request.form.get('income-in')
        _payment = request.form.get('payment-in')
        _total = int(_income) - int(_payment)

        sql = "SELECT * FROM report WHERE date = '%s'"%(_date)
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            sql = "UPDATE report SET income = '%s', expenses='%s', total='%s' WHERE date = '%s';"%(_income,_payment,_total,_date)
        else:
            sql = "INSERT INTO report (date, income, expenses, total) VALUES ('%s', '%s', '%s', '%s');"%(_date,_income,_payment,_total)
        
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        return redirect(url_for('backend_report'))
    else:
        return redirect(url_for('backend_login'))

@app.route('/backend/home', methods=['GET','POST'])
def backend_home():
    username = request.form.get('username')
    password = request.form.get('password')

    sql = "SELECT * FROM account WHERE username  = '%s' and password = '%s'"%(username,password)
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()

    if not result:
        f_name = request.cookies.get('f_name')
        l_name = request.cookies.get('l_name')

        sql = "SELECT * FROM account WHERE f_name  = '%s' and l_name = '%s'"%(f_name,l_name)
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()

    if result:
        session['logged_in'] = True
        resp = make_response(render_template('backend/home.html', data=result))
        resp.set_cookie('role', result[9])
        resp.set_cookie('f_name', result[3])
        resp.set_cookie('l_name', result[4])
        resp.set_cookie('img', result[8])
        return resp
    else:
        session['logged_in'] = False
        msg='error'
        return render_template('backend/login-backend.html',msg=msg)

@app.route('/service')
def service():
    sql = "SELECT * FROM item WHERE collection = 'service'"
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return render_template('service.html',data=result)

@app.route('/api/check_otp', methods=['POST'])
def check_otp():
    _token = request.form.get('token')
    _pin = request.form.get('pin')
    url = 'https://otp.thaibulksms.com/v2/otp/verify'
    data = {
        "key" : "1731140603518261",
        "secret": "0f12f0d673ceb864003ea66b2af971ac",
        "token" : _token,
        "pin": _pin
        }
    x = requests.post(url, data = data)

    return x.json()

@app.route('/api/requests_otp', methods=['POST'])
def get_otp():
    _phone = request.form.get('phone')
    url = 'https://otp.thaibulksms.com/v2/otp/request'
    data = {
        "key" : "1731140603518261",
        "secret": "0f12f0d673ceb864003ea66b2af971ac",
        "msisdn" : _phone
        }

    x = requests.post(url, data = data)

    return x.json()
    
@app.route('/order_confirm', methods=['POST'])
def order_confirm():
    total = 0
    _date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _f_name = request.form.get('f_name')
    _l_name = request.form.get('l_name')
    _phone = request.form.get('phone')
    _slip = request.form.get('slip')
    _address = request.form.get('address')
    _session = request.form.get('session')
    _otp = request.form.get('otp')
    
    if _otp == None or _otp == '':
        prompay_phone = '0950960962'
        total = 0
        _session = request.form.get('session')
        cursor = db.cursor()
        cursor.execute("SELECT price,unit FROM cart WHERE session='%s'"%(_session))
        result = cursor.fetchall()
        for x in result:
            total += x[0]*x[1]
        msg = 'no_otp'
        return render_template('payment.html',total=total,session=_session,prompay_phone=prompay_phone,msg=msg)
    else:
        _status = 'รอยืนยัน'
        _s_name = 'รอระบุ'
        _s_phone = 'รอระบุ'
        
        cursor = db.cursor()
        cursor.execute("SELECT price,unit,i_id FROM cart WHERE session='%s'"%(_session))
        result = cursor.fetchall()

        for x in result:
            total += x[0]*x[1]
            cursor = db.cursor()
            cursor.execute("SELECT count,stock FROM item WHERE id='%s'"%(x[2]))
            data = cursor.fetchone()
            count = data[0] + x[1]
            stock = data[1] - x[1]
            sql = "UPDATE item SET count = '%s',stock = '%s' WHERE id = '%s';"%(count,stock,x[2])
            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()

        if _slip == None:
            sql = "INSERT INTO c_order (f_name, l_name, phone, total_price, time, status, s_name, s_phone, slip, session, address) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', 'cash', '{8}', '{9}');".format(_f_name,_l_name,_phone,total,_date,_status,_s_name,_s_phone,_session,_address)
        else:
            _img = request.files['slip']
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            UPLOAD_FOLDER = 'static/img/slip'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            _slip = _img
            _filename = '%s_%s_%s'%(now,_session,_img.filename)
            _img.save(os.path.join (app.config['UPLOAD_FOLDER'],_filename))
            sql = "INSERT INTO c_order (f_name, l_name, phone, total_price, time, status, s_name, s_phone, slip, session, address) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}');".format(_f_name,_l_name,_phone,total,_date,_status,_s_name,_s_phone,_filename,_session,_address)
        
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()

        sql = "SELECT * FROM item WHERE recommend = 'true' AND collection = 'set' AND stock != '0'"
        cursor = db.cursor()
        cursor.execute(sql)
        i_set = cursor.fetchall()

        sql = "SELECT * FROM item WHERE recommend = 'true' AND collection = 'coffin' AND stock != '0'"
        cursor = db.cursor()
        cursor.execute(sql)
        i_coffin = cursor.fetchall()

        msg = 'confirm'
        return render_template('index.html',data_set=i_set,data_coffin=i_coffin , msg=msg)

@app.route('/payment', methods=['POST'])
def payment():
    prompay_phone = '0950960962'
    total = 0
    _session = request.form.get('session')
    cursor = db.cursor()
    cursor.execute("SELECT price,unit FROM cart WHERE session='%s'"%(_session))
    result = cursor.fetchall()
    for x in result:
        total += x[0]*x[1]
    return render_template('payment.html',total=total,session=_session,prompay_phone=prompay_phone)

@app.route('/edit_cart', methods=['POST'])
def edit_cart():
    _id = request.form.get('id')
    _new_unit = int(request.form.get('new_unit'))
    _session = request.form.get('session')
    if _new_unit > 0:
        sql = "UPDATE cart SET unit = '%s' WHERE id = '%s' and session = '%s';"%(_new_unit,_id,_session)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
    elif _new_unit == 0:
        sql = "DELETE FROM cart WHERE id = '%s' and session = '%s';"%(_id,_session)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cart WHERE session='%s'"%(_session))
    result = cursor.fetchall()
    return Response(json.dumps(result),  mimetype='application/json')

@app.route('/backend/confirm_order/success')
def confirm_order_success():
    if session.get('logged_in'):
        sql = "SELECT * FROM c_order"
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        
        msg = 'confirm'
        return render_template('/backend/order.html',data=result,msg=msg)
    else:
        return redirect(url_for('backend_login'))

@app.route('/backend/confirm_order', methods=['POST'])
def confirm_order():
    _id = request.form.get('id')
    _name = request.form.get('name')
    _phone = request.form.get('phone')
    
    sql = "UPDATE c_order set status= 'รอจัดส่ง',s_name = '%s',s_phone = '%s'  WHERE id = '%s' " % (_name,_phone,_id)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    
    return 'success'

@app.route('/addtocart', methods=['POST'])
def add_tocart():
    _date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _id = request.form.get('id')
    _name = request.form.get('name')
    _price = request.form.get('price')
    _img = request.form.get('img')
    _session = request.form.get('session')
    _unit = 1
    sql = "INSERT INTO cart (i_id, session, item, price, unit, add_date, img) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s');"%(_id,_session,_name,_price,_unit,_date,_img)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    return 'success'

@app.route('/show_cart', methods=['POST'])
def show_cart():
    _session = request.form.get('session')
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cart WHERE session='%s'"%(_session))
    result = cursor.fetchall()
    return Response(json.dumps(result),  mimetype='application/json')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route("/ajaxlivesearch",methods=["POST","GET"])
def ajaxlivesearch():
    
    try:
        if request.method == 'POST':
            search_word = request.form['query']
        if search_word == '':
            query = "SELECT * from item ORDER BY name"
            cursor = db.cursor(dictionary=True)
            cursor.execute(query)
            employee = cursor.fetchall()
        else:    
            query = "SELECT * from item WHERE name LIKE '%{}%' ORDER BY id DESC LIMIT 20".format(search_word)
            cursor = db.cursor(dictionary=True)
            cursor.execute(query)
            numrows = int(cursor.rowcount)
            employee = cursor.fetchall()
        return jsonify({'htmlresponse': render_template('response.html', employee=employee, numrows=numrows)})
    except:
        return jsonify({'htmlresponse': render_template('response.html', data='nodata')})
            
@app.route("/account")
def account_user():
    sql = "SELECT * FROM account "
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return render_template('accountuser.html', data = result)

@app.route("/edit_account/<postID>")
def edit_account(postID):
    
    sql = "SELECT * FROM account WHERE id = '%s'"%(postID)
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    
    return render_template('editaccount.html', data= result)

@app.route("/add_account")
def add_account():
    return render_template('add_account.html')

@app.route("/add_account_confirm",methods=["POST"])
def add_account_confirm():
    if session.get('logged_in'):
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        _username = request.form.get('i_username')
        _password = request.form.get('i_password')
        _phone = request.form.get('i_phone')
        _mail = request.form.get('i_mail')
        _address = request.form.get('i_address')
        _permission = request.form.get('permissions')
        _img = request.files['i_img']

        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        UPLOAD_FOLDER = 'static/img/account'
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        _filename = '%s_%s'%(now,_img.filename)
        _img.save(os.path.join (app.config['UPLOAD_FOLDER'],_filename))

        sql = "INSERT INTO account (username, password, f_name, l_name, phone, address, mail, img, permission) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (_username,_password,f_name,l_name,_phone,_address,_mail,_filename,_permission)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()

        return redirect(url_for('account_user'))
    else:
        return redirect(url_for('backend_login'))

@app.route("/delete_account/<postID>")
def delete_account(postID):
    if session.get('logged_in'):
        sql = "DELETE FROM account WHERE id = '%s';"%(postID)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        
        return redirect(url_for('account_user'))
    else:
        return redirect(url_for('backend_login'))

@app.route("/update_account/<portID>", methods=["POST"])
def func(portID):
    if session.get('logged_in'):
        _username = request.form.get('edit_username')
        _password = request.form.get('edit_password')
        _name = request.form.get('edit_fname')
        _lname = request.form.get('edit_lname')
        _phone = request.form.get('edit_phone')
        _mail = request.form.get('edit_email')
        _address = request.form.get('edit_address')
        
        sql = "UPDATE account set username = '%s', password = '%s',f_name = '%s', l_name= '%s', phone= '%s', mail = '%s', address = '%s' WHERE id = '%s' " % (_username,_password,_name, _lname, _phone, _mail, _address, portID)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        print(portID)
        return redirect(url_for('account_user'))
    else:
        return redirect(url_for('backend_login'))
if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host="0.0.0.0", port=int("5000"), debug=True)