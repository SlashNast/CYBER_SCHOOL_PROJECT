#serverBL.py
import threading
from protocol import *
import Users_db
from crypto_utils import generate_rsa_keys, serialize_public_key, rsa_decrypt, aes_encrypt, aes_decrypt




class CServerBL:

    def __init__(self,host,port):

        # Open the log file in write mode, which truncates the file to zero length
        with open(LOG_FILE,'w'):
            pass  # This block is empty intentionally

        self._host = host
        self._port = port
        self._server_socket = None
        self._is_srv_running = True
        self._client_handlers = []

        self.private_key, self.public_key = generate_rsa_keys()
        self.public_pem = serialize_public_key(self.public_key)


        Users_db.ensure_db()
        Users_db.ensure_db_materials()
        Users_db.seed_materials()
        Users_db.ensure_db_favorites()


    def stop_server(self):
        try:
            self._is_srv_running = False
            # Close server socket
            if self._server_socket is not None:
                self._server_socket.close()
                self._server_socket = None

            if len(self._client_handlers) > 0:
                # Waiting to close all opened threads
                for client_thread in self._client_handlers:
                    client_thread.join()
                write_to_log(f"[SERVER_BL] All Client threads are closed")

        except Exception as e:
            write_to_log("[SERVER_BL] Exception in Stop_Server fn : {}".format(e))

    def start_server(self):
        try:
            self._server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self._server_socket.bind((self._host,self._port))
            self._server_socket.listen(5)
            write_to_log(f"[SERVER_BL] listening...")

            while self._is_srv_running and self._server_socket is not None:
                # Accept socket request for connection
                client_socket,address = self._server_socket.accept()
                write_to_log(f"[SERVER_BL] Client connected {client_socket}{address} ")

                # Start Thread
                cl_handler = CClientHandler(client_socket,address, self)
                cl_handler.start()
                self._client_handlers.append(cl_handler)
                write_to_log(f"[SERVER_BL] ACTIVE CONNECTION {threading.active_count() - 1}")

        except Exception as e:
            write_to_log("[SERVER_BL] Exception in start_server fn : {}".format(e))
        finally:
            write_to_log(f"[SERVER_BL] Server thread is DONE")


class CClientHandler(threading.Thread):
    _client_socket = None
    _address = None

    def __init__(self,client_socket,address, server):
        super().__init__()

        self._client_socket = client_socket
        self._address = address
        self._server = server
        self._aes_key = None



    def run(self):
        # This code run in separate thread for every client
        connected = True

        write_to_log(f"[SERVER_BL] sending public key to {self._address}")
        self._client_socket.send(self._server.public_pem)

        write_to_log(f"[SERVER_BL] waiting for encrypted AES key from {self._address}")
        encrypted_aes_key = self._client_socket.recv(4096)

        write_to_log(f"[SERVER_BL] encrypted AES key received from {self._address}")
        self._aes_key = rsa_decrypt(encrypted_aes_key, self._server.private_key)

        write_to_log(f"[SERVER_BL] AES key decrypted for {self._address}: {self._aes_key.hex()}")

        write_to_log(f"[SERVER_BL] AES key received for {self._address}")

        while connected:
            encrypted_data = self._client_socket.recv(4096)

            if not encrypted_data:
                connected = False
                break

            try:
                # 1. расшифровываем AES
                decrypted_data = aes_decrypt(self._aes_key, encrypted_data)
                buf = decrypted_data.decode(FORMAT)

                # 2. разбираем обычное сообщение
                cmd, args = get_cmd_and_args(buf)
                write_to_log(f"[SERVER_BL] received decrypted from {self._address} - cmd: {cmd}, args: {args}")

                # 3. создаём ответ
                if check_cmd(cmd) == 1:
                    response = create_response_msg(cmd)
                elif check_cmd(cmd) == 2:
                    response = create_response_msg_27(cmd, args)
                elif check_cmd(cmd) == 3:
                    payload = create_response_msg_DB(cmd, args)
                    response = f"{len(payload):04d}{payload}"
                else:
                    response = '{"success": true, "msg":"ok"}'
                    response = f"{len(response):04d}{response}"

                # 4. шифруем ответ через AES
                write_to_log("[SERVER_BL] send - " + response)
                encrypted_response = aes_encrypt(self._aes_key, response.encode(FORMAT))
                self._client_socket.send(encrypted_response)

                # 5. отключение
                if cmd == DISCONNECT_MSG:
                    connected = False

            except Exception as e:
                write_to_log(f"[SERVER_BL] decrypt/handle error: {e}")
                connected = False

        self._client_socket.close()
        write_to_log(f"[SERVER_BL] Thread closed for : {self._address} ")


if __name__ == "__main__":

    server = CServerBL(SERVER_HOST,PORT)
    server.start_server()
