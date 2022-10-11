
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
            my_cursor.execute('''INSERT INTO register(fullname, email, password, transaction_pin) VALUES (%s, %s, %s, %s)  ''' , (fullname, email, hash_password, hash_pin))
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
    my_cursor.execute('SELECT * FROM register WHERE email = %s', [email])  #check db if the email exist
    query = my_cursor.fetchone()
    if query and sha256.verify(password, query[3]):
   
      return jsonify('you are logged in')
    else:
        return jsonify('email or password is incorrect')  




#deposit route
@app.route('/deposit', methods=['GET'])
def deposit():
    data = request.json
    email = data['email']
    
    my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
    my_cursor.execute('SELECT * FROM register WHERE email = %s', [email])
    query = my_cursor.fetchone() 
    if query:
        amount = data['amount']
        pin = data['pin']
        typ = "deposit"             # type of transaction  
        now = datetime.datetime.now()
        dt_now = now.strftime("%d-%m-%Y %H:%M:%S")

        my_cursor.execute('SELECT balance FROM register WHERE email = %s', [email])
        user = my_cursor.fetchone()

        carry = ''.join(map(str, user))      #change the tuple from the database to string
        change_user = int(carry)             #change the string to int
        total = change_user + amount

        my_cursor.execute('SELECT * FROM register WHERE email = %s', [email])
        queryy = my_cursor.fetchone()  
        if queryy and sha256.verify(pin, queryy[4]):

            my_cursor.execute("""UPDATE register SET balance=%s WHERE email = %s""", [total, email])  
            my_cursor.execute("INSERT INTO  transactions (email,amount,type,date) VALUES(%s,%s,%s,%s)", [email, amount, typ, dt_now])  
            mydb.commit()
            return jsonify(str(amount) + " Deposited " + " Remain " + str(total) + ' your account account')
        else:
            return jsonify("invalid pin")
    else:
        return jsonify('email doesnt exits')
           
            
           
        
#withdraw route
@app.route('/withdraw', methods=['GET'])   
def withdraw():
    data = request.json
    email = data['email']

    my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
    my_cursor.execute('SELECT * FROM register WHERE email = %s', [email])
    query = my_cursor.fetchone() 
    if query:
        amount = data['amount']
        pin = data['pin']
        typ = "withdraw"       #type of transaction
        now = datetime.datetime.now()
        dt_now = now.strftime("%d-%m-%Y %H:%M:%S")

        my_cursor.execute('SELECT balance FROM register WHERE email = %s', [email])
        user = my_cursor.fetchone()
        
        carry = ''.join(map(str, user))  #change the tuple from the database to string
        change_user = int(carry)     #change the string to int
       
        if amount >= change_user :
            return jsonify('insufficient account')
        else:

            total = change_user - amount
            my_cursor.execute('SELECT * FROM register WHERE email = %s', [email])
            queryy = my_cursor.fetchone()  
        if queryy and sha256.verify(pin, queryy[4]):
        
            my_cursor.execute("""UPDATE register SET balance=%s WHERE email = %s""", [total, email])  
            my_cursor.execute("INSERT INTO  transactions (email,amount,type,date) VALUES(%s,%s,%s,%s)", [email, amount, typ, dt_now])  
            mydb.commit()
            return jsonify ( str(amount) + " withdraw, " + " Remain " + str(total)+' your account account')
        else:
            return jsonify("invalid pin")
    else:
        return jsonify('email doesnt exits')
           
               


@app.route('/history', methods=['GET'])
def history():
    data = request.json
    email = data['email']
   
    my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
    my_cursor.execute('SELECT * FROM register WHERE email = %s', [email])
    query = my_cursor.fetchone()
    if query:
        my_cursor.execute('SELECT * FROM transactions WHERE email = %s', [email])
        user = my_cursor.fetchall()
        return jsonify(user)
    else:
        return jsonify('email is not registered')



if __name__ == '__main__':
    app.run(debug=True)

    