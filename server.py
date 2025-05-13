import json
from flask import Flask, request, render_template, redirect, session, flash
import scripts

# Note: static folder means all files from there will be automatically served over HTTP
app = Flask(__name__, static_folder="public")
app.secret_key = "TODO_task3"

@app.before_request
def init_defaults():
    session.setdefault("active_page", "home")
    session.setdefault("authenticated", False)
    session.setdefault("user", {
        "username": "",
        "cart": []
    })
    session.setdefault("error_msg", "")
    session.setdefault("error_message", "")
    
USERS_FILE = "users.json"

@app.route("/")
def index():
    products = []
    # Read products.json file
    with open("products.json", "r") as f:
        products = json.load(f)
    return render_template("index.html", products=products, current_page="home")

@app.route("/about")
def about():
    return render_template("about.html", current_page="about")

# LOGIN FUNCTION
@app.route("/login", methods=["GET", "POST"])
def login():
    error_msg = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        # import users.json to ALLOWED_USERS
        ALLOWED_USERS = []
        with open(USERS_FILE, "r") as f:
            ALLOWED_USERS = json.load(f)
        error_msg = "Invalid username or password"
        
        for user in ALLOWED_USERS:
            if user["username"] == username:
                if scripts.check_password(password, user["pass"]):
                    session["authenticated"] = True
                    session["user"]["username"] = username
                    session["user"]["cart"] = user["cart"]
                    error_msg = ""
                    return redirect("/")
        pass
    return render_template("login.html", error_msg=error_msg, current_page="login")

# REGISTER FUNCTION
@app.route("/register", methods=["GET", "POST"])
def register():
    error_msg = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        
        ALLOWED_USERS = []
        with open("users.json", "r") as f:
            ALLOWED_USERS = json.load(f)
            
        # Check if username already exists
        for user in ALLOWED_USERS:
            if user["username"] == username:
                error_msg = "Username already exists"
                break
        else:
            # Add new user to the list
            ALLOWED_USERS.append({"username": username, "pass": scripts.hash_password(password), "cart": []})
            # Save updated list to users.json
            with open("users.json", "w") as f:
                json.dump(ALLOWED_USERS, f)
            session["authenticated"] = True
            
            return redirect("/")
    # If we reach here, it means registration failed
    return render_template("register.html", error_msg=error_msg, current_page="register")

@app.route("/logout")
def logout():
    session["authenticated"] = False
    return redirect("/")

@app.route("/account", methods=["GET", "POST"])
def account():
    
    error_msg = ""
    
    if request.method == "POST":
        password = request.form.get("password")
        confirm = request.form.get("confirm_password")
        print(password, confirm)
        
        if password != confirm or not password:
            print("Passwords do not match.")
            error_msg = "Passwords do not match."
        else:
            # Update session or user in DB
            print("Updating password for user:", session["user"]["username"], password)
            success = scripts.update_password(session["user"]["username"], password)
            if success:
                error_msg = ""
                return redirect("/")
            else:
                error_msg = "Failed to update account."
    
    return render_template("account.html", current_page="account", error_msg=error_msg)

@app.errorhandler(404)
def error404(code):
    # bonus: make it show a fancy HTTP 404 error page, with red background and bold message ;) 
    return "HTTP Error 404 - Page Not Found :(("

@app.route("/cart/add/<product_id>", methods=["POST", "GET"])
def add_to_cart(product_id):
    user = session["user"]
    cart = session["user"]["cart"]
    
    if product_id in cart:
        print("Product already in cart")
        return redirect("/")
    
    scripts.add_to_cart_in_account(session["user"]["username"], product_id)
    
    cart.append(product_id)
    user["cart"] = cart
    session["user"] = user
    
    return redirect("/")

@app.route("/cart/remove/<product_id>", methods=["POST", "GET"])
def remove_from_cart(product_id):
    user = session["user"]
    cart = session["user"]["cart"]
    
    if product_id in cart:
        scripts.remove_from_cart_in_account(session["user"]["username"], product_id)
        cart.remove(product_id)
        user["cart"] = cart
        session["user"] = user
    return redirect("/cart")

@app.route("/cart")
def cart():
    
    # Filter the cart items based on the product IDs
    cart_items = []
    with open("products.json", "r") as f:
        products = json.load(f)
    print(session["user"])
    for id in session["user"]["cart"]:
        if id in products:
            cart_items.append(products[id])
            
    # Calculate the total price of the cart items
    total_price = sum(item["price"] for item in cart_items)
    
    return render_template("cart.html", cart_items=cart_items, current_page="cart", total_price=total_price)

# Run the webserver (port 5000 - the default Flask port)
if __name__ == "__main__":
    app.run(debug=True, port=5000)
