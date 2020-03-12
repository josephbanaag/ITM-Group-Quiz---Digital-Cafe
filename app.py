from flask import Flask,redirect
from flask import render_template
from flask import request
from flask import session
import database as db
import authentication
import logging

app = Flask(__name__)

# Set the secret key to some random bytes.
# Keep this really secret!
app.secret_key = b's@g@d@c0ff33!'


logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.INFO)

navbar = """
         <a href='/'>Home</a> | <a href='/products'>Products</a> |
         <a href='/branches'>Branches</a> | <a href='/aboutus'>About Us</a>
         <p/>
         """

# Basic Pages
@app.route('/')
def index():
    return render_template('index.html', page="Index")

@app.route('/products')
def products():
    product_list = db.get_products()
    return render_template('products.html', page="Products", product_list=product_list)

@app.route('/productdetails')
def productdetails():
    code = request.args.get('code', '')
    product = db.get_product(int(code))

    return render_template('productdetails.html', code=code, product=product)

@app.route('/branches')
def branches():
	branch_list = db.get_branches()
	return render_template('branches.html', page="Branches", branch_list=branch_list)

@app.route('/branchdetails')
def branchdetails():
	code = request.args.get('code', '')
	branch = db.get_branch(int(code))

	return render_template('branchdetails.html', code=code, branch=branch)
	
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html', page="About Us")

@app.route('/privacy')
def privacy():
    return render_template('privacy.html', page="Privacy")

# Login and Logout
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/login2', methods=['GET', 'POST'])
def login2():
    return render_template('login2.html')

@app.route('/auth', methods = ['GET', 'POST'])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')

    is_successful, user = authentication.login(username, password)
    app.logger.info('%s', is_successful)
    if(is_successful):
        session["user"] = user
        return redirect('/')
    else:
        return redirect('/login2')

@app.route('/logout')
def logout():
    session.pop("user",None)
    session.pop("cart",None)
    return redirect('/')

# Order Management
@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/addtocart')
def addtocart():
    code = request.args.get('code', '')
    product = db.get_product(int(code))
    item=dict()
    # A click to add a product translates to a 
    # quantity of 1 for now

    item["code"] = code
    item["qty"] = 1
    item["name"] = product["name"]
    item["subtotal"] = product["price"]*item["qty"]

    if(session.get("cart") is None):
        session["cart"]={}

    cart = session["cart"]
    cart[code]=item
    session["cart"]=cart
    return redirect('/cart')

@app.route('/removecartitem')
def removecartitem():
    cart = session["cart"]
    code = request.args.get('code')
    
    del cart[code]

    session["cart"]=cart
    return redirect('/cart')
