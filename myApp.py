import json
import sqlite3
from flask import Flask, request
import re
app = Flask(__name__)
con = sqlite3.connect('example.db', check_same_thread=False)
cur = con.cursor()

try:
    cur.execute('''CREATE TABLE products (pic text, desc text, price int)''')
except:
    print('table already exist')
con.commit()
# cur.execute("INSERT INTO products VALUES ('milk.jpeg','Milk',15)")
# cur.execute("INSERT INTO products VALUES ('cola.gif','Cola',8)")



@app.route("/products/<id>", methods=['GET', 'DELETE', 'POST', 'PUT'])
@app.route("/products", methods=['GET', 'DELETE', 'POST', 'PUT'])
def products(id=-1):
    if request.method == "GET":
        if int(id) > -1:
            for prod in cur.execute(f'SELECT rowid,* FROM products where rowid={id}'):
                return json.dumps({"id": prod[0], "pic": prod[1], "desc": prod[2], 'price': prod[3]})
        else:
            prodLst = []
            for prod in cur.execute('SELECT rowid,* FROM products'):
                prodLst.append(
                    {"id": prod[0], "pic": prod[1], "desc": prod[2], 'price': prod[3]})
            return json.dumps(prodLst)

    if request.method == "POST":
        pic = request.get_json()['pic']
        desc = request.get_json()['desc']
        price = request.get_json()['price']
        validateJpeg = re.search(".*\.jpeg$", pic)
        validateGif = re.search(".*\.gif$", pic)
        if validateGif or validateJpeg:
            cur.execute(
                f"INSERT INTO products VALUES ('{pic}','{desc}',{price})")
            con.commit()
            return json.dumps({'create': f'{pic}'})
        else:
            return json.dumps({'error': f'{pic} should be only jpeg or gif file and cannot contain more than 10 characters.'})
    if request.method == "DELETE":
        if int(id) > -1:
            cur.execute(f'DELETE FROM products WHERE rowid={id}')
            con.commit()
            return {'DELETE': id}
        else:
            return json.dumps({'error': 'product not found'})
    if request.method == "PUT":
        pic = request.get_json()['pic']
        desc = request.get_json()['desc']
        price = request.get_json()['price']
        validateJpeg = re.search(".*\.jpeg$", pic)
        validateGif = re.search(".*\.gif$", pic)
        if validateGif or validateJpeg:
            cur.execute(
                f"UPDATE products SET pic = '{pic}', desc = '{desc}', price = {price} WHERE rowid={id}")
            return {'UPDATE': 'success'}


app.run(debug=True)
