# protocol_DB.py
import json
import Users_db

REG_LOGIN_CMD = ("REG", "SIGNIN")

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
                return json.dumps({"success": True, "msg": f"User {login} registered"})
            return json.dumps({"success": False, "error": "User already exists"})

        if cmd == "SIGNIN":
            ok = Users_db.check_user(login, password)
            if ok:
                return json.dumps({"success": True, "msg": f"Welcome {login}"})
            return json.dumps({"success": False, "error": "Wrong login/password"})

        return json.dumps({"success": False, "error": "Unknown DB cmd"})

    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})

