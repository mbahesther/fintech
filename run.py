
import datetime
from flask import render_template
from apps import *
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



balancee = 10

@app.route('/deposit')
def deposit():
    email = input('enter email')
    my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
    my_cursor.execute('SELECT * FROM register WHERE email = %s', [email])
    query = my_cursor.fetchone() 
    if query:
        amount = int(input('Enter the amount to deposit:')) 
        pin =input('enter pin')
        typ = "deposit"
        total = balancee + amount
        now = datetime.datetime.now()
        dt_now = now.strftime("%d-%m-%Y %H:%M:%S")
        my_cursor.execute('SELECT * FROM register WHERE email = %s', [email])
        queryy = my_cursor.fetchone()  
        if queryy and sha256.verify(pin, queryy[4]):

            my_cursor.execute("""UPDATE register SET balance=%s WHERE email = %s""", [total, email])  
            my_cursor.execute("INSERT INTO  transactions (email,amount,type,date) VALUES(%s,%s,%s,%s)", [email, amount, typ, dt_now])  
            mydb.commit()
            return jsonify(str(amount) + " withdraw " + str(total) + ' your account account')
        else:
            return jsonify("invalid pin")
    else:
        return jsonify('email doesnt exits')
           
            
           
        
 

#checkingapi
@app.route('/depositt', methods=['POST'])
def depositt():
     data = request.json
     amount = data['amount']
     total = data['amount'] + balancee
     return str(total)
   

@app.route('/withdraw')   
def withdraw():
    email = input('enter email')

    my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
    my_cursor.execute('SELECT * FROM register WHERE email = %s', [email])
    query = my_cursor.fetchone() 
    if query:
        amount = int(input('Enter the amount to withdraw:')) 
        pin =input('enter pin')
        typ = "withdraw"
        my_cursor.execute('SELECT balance FROM register WHERE email = %s', [email])
        query = my_cursor.fetchone()
        print(query)
        
        carry = ''.join(map(str, query))  #change the tuple to string
        change_query = int(carry)     #change the string to int
       
        if amount >= change_query :
            return jsonify('insufficient account')
        else:

            total = change_query - amount
            now = datetime.datetime.now()
            dt_now = now.strftime("%d-%m-%Y %H:%M:%S")
            my_cursor.execute('SELECT * FROM register WHERE email = %s', [email])
            queryy = my_cursor.fetchone()  
        if queryy and sha256.verify(pin, queryy[4]):
            print(queryy)

            my_cursor.execute("""UPDATE register SET balance=%s WHERE email = %s""", [total, email])  
            my_cursor.execute("INSERT INTO  transactions (email,amount,type,date) VALUES(%s,%s,%s,%s)", [email, amount, typ, dt_now])  
            mydb.commit()
            return jsonify ( str(amount) + " withdraw " + str(total)+' your account account')
        else:
            return jsonify("invalid pin")
    else:
        return jsonify('email doesnt exits')
           
               

#checkingapi
@app.route('/withdraww', methods=['POST'])   
def withdraww():
    data = request.json
    amount = data['amount']
    if amount > balancee:
        return jsonify('Insufficient Balance')
    else:
       total = balancee - data['amount']
       return str(total)        


@app.route('/history')
def history():
    pass


if __name__ == '__main__':
    app.run(debug=True)

    