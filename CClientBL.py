from protocol import *
from crypto_utils import load_public_key
from crypto_utils import generate_aes_key
from crypto_utils import rsa_encrypt
from crypto_utils import aes_encrypt, aes_decrypt




class CClientBL:

    def __init__(self, host: str, port: int):

        self._client_socket = None
        self._host = host
        self._port = port
        self._aes_key = None



    def connect(self) -> socket:
        try:
            self._client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self._client_socket.connect((self._host,self._port))
            # 1. получить публичный ключ сервера
            public_pem = self._client_socket.recv(4096)
            server_public_key = load_public_key(public_pem)

            # 2. сгенерировать AES-ключ
            self._aes_key = generate_aes_key()

            # 3. зашифровать AES-ключ публичным ключом сервера
            encrypted_key = rsa_encrypt(self._aes_key, server_public_key)

            # 4. отправить серверу зашифрованный AES-ключ
            self._client_socket.send(encrypted_key)

            write_to_log("[CLIENT_BL] connected to server")

            public_pem = self._client_socket.recv(4096)
            write_to_log("[CLIENT_BL] public key received from server")

            server_public_key = load_public_key(public_pem)
            write_to_log("[CLIENT_BL] public key loaded")

            self._aes_key = generate_aes_key()
            write_to_log(f"[CLIENT_BL] AES key generated: {self._aes_key.hex()}")

            encrypted_key = rsa_encrypt(self._aes_key, server_public_key)
            write_to_log("[CLIENT_BL] AES key encrypted with RSA")

            self._client_socket.send(encrypted_key)
            write_to_log("[CLIENT_BL] encrypted AES key sent to server")

            write_to_log(f"[CLIENT_BL] {self._client_socket.getsockname()} connected")
            return self._client_socket
        except Exception as e:
            write_to_log("[CLIENT_BL] Exception on connect: {}".format(e))
            return None

    def disconnect(self) -> bool:
        try:
            write_to_log(f"[CLIENT_BL] {self._client_socket.getsockname()} closing")
            self.send_data(DISCONNECT_MSG)
            self._client_socket.close()
            return True
        except Exception as e:
            write_to_log("[CLIENT_BL] Exception on disconnect: {}".format(e))
            return False

    def send_data(self, cmd: str, args: str = '') -> bool:
        try:
            request = create_request_msg(cmd, args)
            encrypted = aes_encrypt(self._aes_key, request.encode(FORMAT))
            self._client_socket.send(encrypted)
            write_to_log(f"[CLIENT_BL] send {self._client_socket.getsockname()} {cmd} ")
            return True
        except Exception as e:
            write_to_log("[CLIENT_BL] Exception on send_data: {}".format(e))
            return False

    def receive_data(self) -> str:
        try:
            encrypted_response = self._client_socket.recv(4096)
            decrypted_response = aes_decrypt(self._aes_key, encrypted_response)
            msg = decrypted_response.decode(FORMAT)

            write_to_log(f"[CLIENT_BL] received decrypted {self._client_socket.getsockname()} {msg}")
            return msg
        except Exception as e:
            write_to_log("[CLIENT_BL] Exception on receive: {}".format(e))
            return ""
