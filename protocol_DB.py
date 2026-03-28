# protocol_DB.py
import json
import Users_db

REG_LOGIN_CMD = ("REG", "SIGNIN")
USERS_BASKET = ("USER_ID", "MATERIAL_ID")

def create_response_msg_DB(cmd: str, args: list) -> str:
    try:
        if not args:
            return json.dumps({"success": False, "error": "Missing args"})

        data = json.loads(args[0])
        login = (data.get("login") or "").strip()
        password = (data.get("password") or "").strip()

        if not login or not password:
            return json.dumps({"success": False, "error": "Empty login/password"})

        if cmd == "REG":
            ok = Users_db.add_user(login, password)
            if ok:
                user_id = Users_db.get_user_id(login)
                return json.dumps({"success": True,
                                   "msg": f"User {login} registered", "user_id": user_id}, )
            return json.dumps({"success": False, "error": "User already exists"})

        if cmd == "SIGNIN":
            ok = Users_db.check_user(login, password)
            if ok:
                user_id = Users_db.get_user_id(login)
                return json.dumps({"success": True, "msg": f"Welcome {login}", "user_id": user_id})
            return json.dumps({"success": False, "error": "Wrong login/password"})

        if cmd == "ADD_FAVORITE":
            user_id = data.get("user_id")
            material_id = data.get("material_id")

            ok = Users_db.add_to_favorites(user_id, material_id)

            return json.dumps({"success": ok})

        if cmd == "REMOVE_FAVORITES":
            user_id = data.get("user_id")
            material_id = data.get("material_id")

            ok = Users_db.remove_from_favorites(user_id, material_id)

            return json.dumps({"success": ok})

        if cmd == "GET_USER_FAVORITES":
            user_id = data.get("user_id")

            ok = Users_db.get_user_favorite_materials(user_id)

            return json.dumps({"success": ok})

        return json.dumps({"success": False, "error": "Unknown DB cmd"})

    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

