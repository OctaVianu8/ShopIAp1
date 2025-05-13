import json
import bcrypt # type: ignore

def hash_password(plain_text_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_text_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(plain_text_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))

def update_password(username: str, new_password: str) -> bool:
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
        
        for user in users:
            if user["username"] == username:
                user["pass"] = hash_password(new_password)
                break
        else:
            return False  # User not found

        with open("users.json", "w") as f:
            json.dump(users, f)
        return True
    except Exception as e:
        print(f"Error updating password: {e}")
        return False
    
def add_to_cart_in_account(username: str, item: str):
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
        for user in users:
            if user["username"] == username:
                if item in user["cart"]:
                    user["cart"][item] += 1
                else:
                    user["cart"][item] = 1
                break
        else:
            return False  # User not found

        with open("users.json", "w") as f:
            json.dump(users, f)
        return True
    except Exception as e:
        print(f"Error updating cart: {e}")
        return False
    
def remove_from_cart_in_account(username: str, item: str):
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
        
        for user in users:
            if user["username"] == username:
                if item in user["cart"]:
                    user["cart"][item] -= 1
                    if user["cart"][item] <= 0:
                        del user["cart"][item]
                else:
                    return False
                break
        else:
            return False  # User not found

        with open("users.json", "w") as f:
            json.dump(users, f)
        return True
    except Exception as e:
        print(f"Error updating cart: {e}")
        return False