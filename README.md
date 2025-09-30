# HomeBundle

This website is used to sell stuff online. It was developed for a university project assignment.

## Compulsory Features:

These are the features that the homework requires for a full grade.

### Flask server & basic design

The websites features the following routes:
- homepage
- about
- cart
- cart/add-item
- cart/remove-item
- checkout

Bonus routes:
- login
- logout
- register
- account

### Front page
Features a basic design. All items are visible on the front page, and can be
added to cart. Each item features a photo, title, description, and price.
(Also an id and whether they are out of stock or not)

### Shopping Cart
This feature is functional regardless if the user is logged in or not. If the
user is logged in, the cart information will be saved inside the database, even
after logging out. You can also change the quantity of a particular item.

### Checkout page
Checkout page that asks for full name, email, phone number, address and the 
payment method. After clicking place order, the order information will be saved
inside a json file in the database (orders.json).

### Docker container
The Dockerfile is set up using python:3.13.3-alpine.

## Bonus Features:
- Login functionality
The website features a login and register page. When you register, you can do
so using a username and a password. The user and password will be saved inside
a json in the database. The password will NOT be saved as plain text.

I used python's bcrypt library for password hashing and password checking
for login. All of this is done in the scripts.py file.

By logging in, you are able to save your current cart. That means that the
id's of the items inside of one user's cart are also saved inside the database.

If logged in, you can go to the Account page and change your password (which
works, it updates the hash of the function in the database).

Also, during the checkout, if the user is logged in, it auto completes some of
the data (seen inside the orders.json after placing the order)
