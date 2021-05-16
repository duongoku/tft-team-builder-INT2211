from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from markupsafe import escape

import json
import query_mysql
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_bytes(16)
print(f"Your secret key is {app.secret_key}")

authentication_system_id = 19020060

@app.route("/")
def index():
    if "username" in session:
        return render_template("index.html", username=session["username"])
    else:
        return render_template("index.html", username=None)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if valid_login(request.form["username"], request.form["password"]):
            session["username"] = request.form["username"]
            return render_template("checkpoint.html", login=True)
        else:
            return render_template("checkpoint.html", login=False)
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            query_mysql.add_user_to_db(
                request.form["username"],
                authentication_system_id,
                request.form["password"]
            )
            return render_template("checkpoint.html", login=True)
        except:
            return render_template("checkpoint.html", login=False)
    return render_template("register.html")
    
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

def valid_login(username, password):
    if query_mysql.check_credentials(username, password):
        return True
    else:
        return False

@app.route("/champions")
def champions():
    champion_details = query_mysql.get_champion_details()
    return render_template(
        "champions.html",
        champion_details=champion_details
    )

@app.route("/items")
def items():
    item_details = query_mysql.get_item_details()
    return render_template(
        "items.html",
        item_details=item_details
    )

@app.route("/boards")
def boards():
    if "username" in session:
        username = session["username"]
        board_list = query_mysql.get_board_list(username)
        return render_template("boards.html", boards=board_list)
    else:
        return render_template("not_logged_in.html")

@app.route("/newboard")
def newboard():
    if "username" in session:
        champion_details = query_mysql.get_champion_details()
        item_details = query_mysql.get_item_details()
        js_champion_details = reformat_to_json(champion_details)
        js_item_details = reformat_to_json(item_details)
        return render_template(
            "board.html",
            js_champion_details = js_champion_details,
            js_item_details = js_item_details,
            js_board_details = reformat_board_details([]),
            board_id = 9999999999
        )
    else:
        return render_template("not_logged_in.html")

def reformat_board_details(board_details):
    ret = [{'champion_id': None, 'items_ids': []} for i in range(28)]
    for board in board_details:
        ret[board['Slot_ID']]['champion_id'] = board['Champion_ID']
        if board['Item_ID'] is not None:
            ret[board['Slot_ID']]['items_ids'].append(board['Item_ID'])

    ret = (
        json.dumps(ret)
        .replace(u'<', u'\\u003c')
        .replace(u'>', u'\\u003e')
        .replace(u'&', u'\\u0026')
        .replace(u"'", u'\\u0027')
    )
    return ret

def reformat_to_json(detail):
    ret = (
        json.dumps(detail)
        .replace(u'<', u'\\u003c')
        .replace(u'>', u'\\u003e')
        .replace(u'&', u'\\u0026')
        .replace(u"'", u'\\u0027')
    )
    return ret

def save_board_to_db(board_id, board_data):
    print(f"DEBUG: {board_id} ==> {board_data}")
    if board_id == 9999999999:
        board_id = query_mysql.create_new_board(session["username"])
    query_mysql.update_board(board_id, board_data)
    return board_id

@app.route("/board/<int:board_id>", methods=["GET", "POST"])
def board(board_id = None):
    if "username" in session:
        if request.method == "GET":
            if board_id < 9999999999 and query_mysql.get_owner(board_id) != session["username"]:
                return render_template("permission.html")
            champion_details = query_mysql.get_champion_details()
            item_details = query_mysql.get_item_details()
            board_details = query_mysql.get_champion_list(board_id)
            js_champion_details = reformat_to_json(champion_details)
            js_item_details = reformat_to_json(item_details)
            js_board_details = reformat_board_details(board_details)
            return render_template(
                "board.html",
                js_champion_details = js_champion_details,
                js_item_details = js_item_details,
                js_board_details = js_board_details,
                board_id = board_id
            )
        elif request.method == "POST":
            if board_id == None:
                pass
            else:
                board_id = save_board_to_db(board_id, json.loads(request.form["board-data"]))
                return f"{board_id} OK, Received board-data"
    else:
        return render_template("not_logged_in.html")