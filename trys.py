

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']
    my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
    my_cursor.execute('''SELECT * FROM register WHERE email = %s ''', [email]) >
    query = my_cursor.fetchone()
    if query and sha256.verify(password, query[3]):
        access_token = create_access_token(identity=query)
        return jsonify(access_token=access_token)
    else:
        return jsonify('email or password is incorrect'),401


@app.route('/balance', methods=['GET'])
@jwt_required()
def balance():
    # Access the identity of the current user with get_jwt_identity
    verify=  JWTT.decode('b5ee217d8764b9396c4bab0c84cec2e1', algorithms=['HS256>
    print(verify)
    if verify is None:
        return('token expired or tampared go generate a new token to reset your>
    else:
        email = verify['sub']
     #current_user = get_jwt_identity()
     #print(current_user)
     #return jsonify(logged_in_as=current_user), 200


#deposit route
@app.route('/deposit', methods=['POST'])
@jwt_required()
def deposit():
        data = request.json
        amount = data['amount']
        pin = data['pin']
        typ = "deposit"             # type of transaction
        now = datetime.datetime.now()
        dt_now = now.strftime("%d-%m-%Y %H:%M:%S")

        current_user = get_jwt_identity()
        my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
        my_cursor.execute("SELECT email FROM register")
        user = my_cursor.fetchone()
        print(user)
        return jsonify(user), 200



        #carry = ''.join(map(str, user))      #change the tuple from the databa>
        #change_user = int(carry)             #change the string to int
       # total = change_user + amount

        #my_cursor.execute('SELECT * FROM register WHERE email = %s', [email])
        #queryy = my_cursor.fetchone()

        if queryy and sha256.verify(pin, queryy[4]):

            my_cursor.execute("""UPDATE register SET balance=%s WHERE email = %>
            my_cursor.execute("INSERT INTO  transactions (email,amount,type,dat>
            mydb.commit()
            return jsonify(str(amount) + " Deposited " + " Remain " + str(total>
        else:
            return jsonify("invalid pin")





#withdraw route
@app.route('/withdraw', methods=['POST'])
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

        my_cursor.execute('SELECT balance FROM register WHERE email = %s', [ema>
        user = my_cursor.fetchone()


        carry = ''.join(map(str, user))  #change the tuple from the database to>
        change_user = int(carry)     #change the string to int

        if amount >= change_user :
            return jsonify('insufficient account')
        else:

            total = change_user - amount
            my_cursor.execute('SELECT * FROM register WHERE email = %s', [email>
            queryy = my_cursor.fetchone()
        if queryy and sha256.verify(pin, queryy[4]):

            my_cursor.execute("""UPDATE register SET balance=%s WHERE email = %>
            my_cursor.execute("INSERT INTO  transactions (email,amount,type,dat>
            mydb.commit()
            return jsonify ( str(amount) + " withdraw, " + " Remain " + str(tot>
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
        my_cursor.execute('SELECT * FROM transactions WHERE email = %s', [email>
        user = my_cursor.fetchall()
        return jsonify(user)
    else:
        return jsonify('email is not registered')

#admin

@app.route('/admin', methods=['GET'])
def admin():
    data = request.json
    email = data['email']

    my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
    my_cursor.execute('SELECT * FROM register WHERE email = %s', [email])
    query = my_cursor.fetchone()
    if query:
        my_cursor.execute('SELECT * FROM register')
        user = my_cursor.fetchall()
        return jsonify(user)
    else:
        return jsonify('email is not registered')


@app.route('/transactions', methods=['GET'])
def transactions():
    data = request.json
    email = data['email']
 my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
    my_cursor.execute('SELECT * FROM register WHERE email = %s', [email])
    query = my_cursor.fetchone()
    if query:
        my_cursor.execute('SELECT * FROM transactions ')
        user = my_cursor.fetchall()
        return jsonify(user)
    else:
        return jsonify('email is not registered')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

