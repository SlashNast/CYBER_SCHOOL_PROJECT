



import json
from cryptography.fernet import Fernet

DB_NAME = "Users.db"
TABLE_USERS = "Users"

REG_LOGIN_CMD = ("REG", "SIGNIN")


def create_response_msg_DB(cmd: str, args: list):
    pass


def generate_key() -> bytes:
    return Fernet.generate_key()


def save_client_data(client_data):
    # Here should be code to save data to DB
    print("Client data saved:", client_data)


def handle_registration(client_socket) -> str:
    data = client_socket.recv(1024).decode()
    registration_data = json.loads(data)

    login = registration_data.get('login')
    password = registration_data.get('password')

    if is_valid(login, password):
        encryption_key = generate_key().decode()
        client_data = {'login': login, 'encryption_key': encryption_key}
        save_client_data(client_data)

        response = {'success': True, 'encryption_key': encryption_key}
    else:
        response = {'success': False, 'error': 'Invalid credentials'}

    client_socket.send(json.dumps(response).encode())


def is_valid(login, password):
    return len(login) > 0 and len(password) > 0
