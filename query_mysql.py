import bcrypt
import json
import mysql.connector

USER = 'root'
PASSWORD = 'whoknows'
PORT = '3306'

cnx = mysql.connector.connect(
    user=USER,
    password=PASSWORD,
    host='127.0.0.1',
    port=PORT,
    database='tft'
)
cursor = cnx.cursor(dictionary=True)

def print_exec(query):
    cursor.execute(query)
    res = cursor.fetchall()
    # print(f"Response: {json.dumps(res, indent=4)}")
    print(res)
    return

def add_item_details_to_db():
    add_item = (
        "INSERT INTO item_details (Item_ID, Description, Name)"
        "VALUES (%s, %s, %s)"
    )

    item_data = (
        15,
        'This is a sample item.',
        'Sample'
    )

    cursor.execute("delete from item_details")

    items = json.load(open("item_details.json", "r"))
    for index, item in enumerate(items):
        print(f"Adding {item['name']} . . .")
        item_data = (
            index,
            item["description"],
            item["name"]
        )
        cursor.execute(add_item, item_data)

    cursor.fetchall()
    cnx.commit()
    return

def add_champion_details_to_db():
    add_champion = (
        "INSERT INTO champion_details (Champion_ID, Name, Skill_Description)"
        "VALUES (%s, %s, %s)"
    )

    champion_data = (
        15,
        'Sample',
        'This is a sample champion.'
    )

    cursor.execute("delete from champion_details")

    champions = json.load(open("champion_details.json", "r"))
    for index, champion in enumerate(champions):
        print(f"Adding {champion['Name']} . . .")
        champion_data = (
            index,
            champion["Name"],
            champion["Description"]
        )
        cursor.execute(add_champion, champion_data)

    cursor.fetchall()
    cnx.commit()
    return

def add_trait_details_to_db():
    add_trait = (
        "INSERT INTO trait_details (Trait_ID, Name, Description, Activation)"
        "VALUES (%s, %s, %s, %s)"
    )

    trait_data = (
        15,
        'Sample',
        'This is a sample trait.',
        '3 >> This is a sample activation.'
    )

    cursor.execute("delete from trait_details")

    traits = json.load(open("trait_details.json", "r"))
    for index, trait in enumerate(traits):
        print(f"Adding {trait['name']} . . .")
        trait_data = (
            index,
            trait["name"],
            trait["description"],
            trait["activation"]
        )
        cursor.execute(add_trait, trait_data)

    cursor.fetchall()
    cnx.commit()
    return

def add_trait_to_db():
    add_trait = (
        "INSERT INTO trait (Trait_ID, Champion_ID)"
        "VALUES (%s, %s)"
    )

    trait_data = (
        15,
        0
    )

    traits = json.load(open("trait_details.json", "r"))
    champions = json.load(open("champion_details.json", "r"))

    for i, trait in enumerate(traits):
        for champ in trait['champions']:
            for j, champion in enumerate(champions):
                if champ == champion['Name']:
                    trait_data = (
                        i,
                        j
                    )
                    cursor.execute(add_trait, trait_data)
                    break

    cursor.fetchall()
    cnx.commit()
    return

def get_hashed_password(username):
    query = f"SELECT Encrypted_Password FROM User " \
            f"WHERE Username = '{username}'"
    cursor.execute(query)
    res = cursor.fetchall()
    ret = res[0]['Encrypted_Password']
    return ret

def add_authentication_system_to_db(system_id):
    cursor.execute(
        "INSERT INTO authentication_system (System_ID)"
        f"VALUES ({system_id})"
    )

    cursor.fetchall()
    cnx.commit()
    return

def check_password(password, hashed_password):
    ret = bcrypt.checkpw(
        password.encode(),
        hashed_password.encode()
    )
    return ret

def check_credentials(username, password):
    ret = False
    try:
        ret = check_password(
            password,
            get_hashed_password(username)
        )
    except:
        ret = False
    return ret

def add_user_to_db(username, system_id, password):
    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt(13)
    ).decode()
    cursor.execute(
        "INSERT INTO user (Username, System_ID, Encrypted_Password)"
        f"VALUES ('{username}', {system_id}, '{hashed_password}')"
    )

    cursor.fetchall()
    cnx.commit()
    return

def add_board_to_db(board_id, username):
    cursor.execute(
        "INSERT INTO board (Board_ID, Username)"
        f"VALUES ({board_id}, '{username}')"
    )

    cursor.fetchall()
    cnx.commit()
    return

def add_champion_to_db(champion_id, slot_id, board_id):
    cursor.execute(
        "INSERT INTO champion (Champion_ID, Slot_ID, Board_ID)"
        f"VALUES ({champion_id}, {slot_id}, {board_id})"
    )

    cursor.fetchall()
    cnx.commit()
    return

def add_item_to_db(item_id, champion_id, slot_id, board_id):
    cursor.execute(
        "INSERT INTO item (Item_ID, Champion_ID, Slot_ID, Board_ID)"
        f"VALUES ({item_id}, {champion_id}, {slot_id}, {board_id})"
    )

    cursor.fetchall()
    cnx.commit()
    return

def get_champion_details():
    cursor.execute("SELECT * FROM champion_details")
    ret = cursor.fetchall()
    return ret

def get_item_details():
    cursor.execute("SELECT * FROM item_details")
    ret = cursor.fetchall()
    return ret

def get_board_list(username):
    cursor.execute(
        "SELECT b.Board_ID, c.Champion_ID "
        f"FROM (SELECT * FROM board WHERE Username='{username}') AS b "
        "JOIN champion AS c "
        "ON b.Board_ID=c.Board_ID"
    )
    tmp = cursor.fetchall()
    ret = {}
    for t in tmp:
        if t['Board_ID'] not in ret:
            ret[t['Board_ID']] = []
        ret[t['Board_ID']].append(t['Champion_ID'])
    return ret

def get_champion_list(board_id):
    req = "SELECT champ.Slot_ID, champ.Champion_ID, item.Item_ID "\
        f"FROM (SELECT * FROM champion WHERE champion.Board_ID = {board_id}) AS champ "\
        f"LEFT JOIN item "\
        "ON champ.Slot_ID = item.Slot_ID AND champ.Board_ID = item.Board_ID"
    cursor.execute(req)
    ret = cursor.fetchall()
    return ret

def reset_board(board_id):
    cursor.execute(f"DELETE FROM item WHERE Board_ID={board_id}")
    cursor.execute(f"DELETE FROM champion WHERE Board_ID={board_id}")

    cursor.fetchall()
    cnx.commit()
    return

def create_new_board(username):
    cursor.execute(f"SELECT COUNT(Board_ID) FROM board")
    board_id = cursor.fetchall()[0]['COUNT(Board_ID)']
    cursor.execute(
        "INSERT INTO board (Board_ID, Username)"
        f"VALUES ({board_id}, \"{username}\")"
    )
    cursor.fetchall()
    cnx.commit()
    return board_id

def update_board(board_id, board_data):
    reset_board(board_id)
    for slot_id, slot in enumerate(board_data):
        if slot['champion_id']:
            add_champion_to_db(slot['champion_id'], slot_id,  board_id)
            for item in slot['items_ids']:
                add_item_to_db(item, slot['champion_id'], slot_id, board_id)
    return

def get_owner(board_id):
    cursor.execute(f"SELECT Username FROM board WHERE Board_ID={board_id}")
    username = cursor.fetchall()[0]['Username']
    cnx.commit()
    return username

# add_authentication_system_to_db(19020060)
# add_user_to_db("duongoku", 19020060, "Lucario3011")
# add_board_to_db(0, "duongoku")
# add_champion_to_db(0, 0, 0)
# add_item_to_db(0, 0, 0, 0)
# add_item_to_db(1, 0, 0, 0)
# add_item_to_db(1, 2, 0, 0)

# add_item_details_to_db()
# add_champion_details_to_db()
# add_trait_details_to_db()
# add_trait_to_db()

# try:
#     cursor.execute(add_item, item_data)
# except:
#     pass

# cursor.execute("DESCRIBE item_details")

# responses = cursor.fetchall()

# for response in responses:
#     response['Type'] = response['Type'].decode()

# print(json.dumps(responses, indent=4))

# print_exec("SELECT * FROM item_details LIMIT 3")
# print_exec("SELECT * FROM champion_details LIMIT 3")
# print_exec("SELECT * FROM trait_details LIMIT 3")
# print_exec("DESCRIBE user")

