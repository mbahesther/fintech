import datetime
from run import *
from passlib.hash import pbkdf2_sha256 as sha256


@app.route('/')
def home():
    return "hello "

#registration route
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    fullname = data['fullname']
    email = data['email']
    password = data['password']
    confirm_password = data['confirm_password']
    transaction_pin = data['transaction_pin']
    confirm_pin = data['confirm_pin']
    my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
    my_cursor.execute(''' SELECT * FROM register WHERE email = %s''', [email])
    query = my_cursor.fetchone()
    if query :
       return jsonify('email already exit! choose a different email ')
    else:
       if password == confirm_password :
          hash_password = sha256.hash(password)
       else:
            return jsonify('password didnt match')

       if transaction_pin == confirm_pin:
         if len(transaction_pin) !=4:
            return jsonify('pin must be 4 digits')
         else:
            hash_pin = sha256.hash(transaction_pin)
            my_cursor.execute('''INSERT INTO register(fullname, email, password, transaction_pin) VALUES (%s, %s, %s, %s)  ''' , [fullname, email, hash_password, hash_pin])
            mydb.commit()
            return jsonify('Thanks for registering you can login now')
       else:
         return jsonify('your pin didn\'t match')


#login route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']
    my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
    my_cursor.execute('''SELECT * FROM register WHERE email = %s ''', [email])  #check db if the email exist
    query = my_cursor.fetchone()
    if query and sha256.verify(password, query[3]):
        access_token = create_access_token(identity=query)  
        return jsonify(access_token=access_token)
    else:
        return jsonify('email or password is incorrect'),401


@app.route('/balance', methods=['GET'])
@jwt_required()
def balance():
    
    verify = get_jwt_identity()
    user = verify[5]
   
    if user is None:
        return('token expired or tampared go generate a new token to reset your password')
    return jsonify(user)



#deposit route
@app.route('/deposit', methods=['POST'])
@jwt_required()
def deposit():
        current_user = get_jwt_identity()
        user_id = current_user[0]
        data = request.json
        amount = data['amount']
        pin = data['pin']
        typ = "deposit"             # type of transaction
        now = datetime.datetime.now()
        dt_now = now.strftime("%d-%m-%Y %H:%M:%S")


        my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)

        my_cursor.execute('SELECT balance FROM register WHERE id = %s', [user_id])
        user = my_cursor.fetchone()
        balance = ''.join(map(str, user))  #change the tuple from the database to string
        user_balance = int(balance)  #change the string to int

        total = user_balance + amount
        print(total)

        if current_user and sha256.verify(pin, current_user[4]):
            my_cursor.execute(""" UPDATE register SET balance=%s WHERE id = %s""", [total, user_id])
            my_cursor.execute("INSERT INTO  transactions (email,amount,type,date) VALUES(%s,%s,%s,%s)", [user_id, amount, typ, dt_now])
            mydb.commit()
            return jsonify(str(amount) + " Deposited " + " Remaining :  " + str(total) + ' balance')
        else:
            return jsonify("invalid pin")


#withdraw route
@app.route('/withdraw', methods=['POST'])
@jwt_required()
def withdraw():

        current_user = get_jwt_identity()
        user_id = current_user[0]

        data = request.json
        amount = data['amount']
        pin = data['pin']
        typ = "withdraw"       #type of transaction
        now = datetime.datetime.now()
        dt_now = now.strftime("%d-%m-%Y %H:%M:%S")
        my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
        my_cursor.execute('SELECT balance FROM register WHERE id = %s', [user_id])
        user = my_cursor.fetchone()
        carry = ''.join(map(str, user))  #change the tuple from the database to string
        change_user = int(carry)     #change the string to int

        if amount >= change_user :
            return jsonify('insufficient account')
        else:

           total = change_user - amount
           if current_user and sha256.verify(pin, current_user[4]):
               my_cursor.execute(""" UPDATE register SET balance=%s WHERE id =%s""", [total,user_id])
               my_cursor.execute("INSERT INTO  transactions (email,amount,type,date) VALUES(%s,%s,%s,%s)", [user_id, amount, typ, dt_now])
               mydb.commit()
               return jsonify ( str(amount) + " withdraw, " + " Remain " + str(total))
           else:
              return jsonify("invalid pin")


@app.route('/history', methods=['GET'])
@jwt_required()
def history():
        current_user = get_jwt_identity()
        user_id = current_user[0]
        if current_user is None:
                return jsonify('You have to login')
        else:
             my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
             my_cursor.execute('SELECT * FROM transactions WHERE email = %s', [user_id])
             user = my_cursor.fetchall()
             return jsonify(user)

#admin
@app.route('/admin', methods=['GET'])
@jwt_required()
def admin():
        current_user = get_jwt_identity()
        user_id = current_user[0]
        if  current_user is None:
          return jsonify("login to access")
        else:
           my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)

           my_cursor.execute('SELECT * FROM register')
           user = my_cursor.fetchall()
           return jsonify(user)



@app.route('/transactions', methods=['GET'])
@jwt_required()
def transactions():
    current_user = get_jwt_identity()
    user_id = current_user[0]
    if current_user  is None:
        return jsonify("login to access")
    else:
        my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
        my_cursor.execute('SELECT * FROM transactions ')
        user = my_cursor.fetchall()
        return jsonify(user)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

