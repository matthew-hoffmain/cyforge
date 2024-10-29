@app.route("/auth/register/")
def register():
    email = request.headers.get("email")
    username = request.headers.get("username")
    password = request.headers.get("password")
    confirm_password = request.headers.get("confirm_password")
    return {"message": "lmaoooo"}

@app.route("/auth/login/")
def login():
    temp_ledger = {"user1": "secrets",
                   "user2": "secrets"}

    username = request.headers.get("username")
    password = request.headers.get("password")
    print(f"LOG#: Attempted login - {username}")
    sessionKey = -1
    if username in temp_ledger:
        if password == temp_ledger[username]:
            sessionKey = random.randint(0, 10)
    return {"sessionKey": sessionKey}