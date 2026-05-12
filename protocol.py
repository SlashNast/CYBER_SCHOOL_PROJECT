#protocol
import ipaddress
from datetime import datetime
import socket
import random
import logging


from protocol_DB import *

SERVER_HOST: str = "0.0.0.0"
CLIENT_HOST: str = "127.0.0.1"
PORT: int = 12345
BUFFER_SIZE: int = 1024
HEADER_LEN: int = 4
FORMAT: str = 'utf-8'

DISCONNECT_MSG: str = "EXIT"
STANDARD_CMD = ("TIME","NAME","RAND",DISCONNECT_MSG)

COMMAND_SEPARATOR = '>'
PARAMETER_SEPARATOR = '<'



LOG_FILE = 'LOG.log'
logging.basicConfig(filename=LOG_FILE,level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')


def check_cmd(data) -> int:
    data = data.upper()
    if data in STANDARD_CMD:
        return 1

    if data in REG_LOGIN_CMD:
        return 3

    return 0


def create_request_msg(cmd: str,args: str) -> str:

    if args is None:
        args = []
    request = ''

    if check_cmd(cmd) == 1:  # commands "TIME"....
        request = cmd


    if check_cmd(cmd) == 3:  # commands DB
        request = cmd
        if args:
            request += COMMAND_SEPARATOR + args

    return f"{len(request):04d}{request}"


def create_response_msg(cmd: str,args: list) -> str:
    response = "Non-supported cmd"

    if cmd == DISCONNECT_MSG:
        response = "Exit request accepted"

    response = f"{len(response):04d}{response}"
    return response


def receive_msg(my_socket: socket) -> (bool,str):
    str_header = my_socket.recv(HEADER_LEN).decode(FORMAT)
    length = int(str_header)
    if length > 0:
        buf = my_socket.recv(length).decode(FORMAT)
    else:
        return False, "Error"

    return True, buf


def get_cmd_and_args(buf: str) -> (str, list):
    split_request = buf.split(COMMAND_SEPARATOR, 1)
    cmd = split_request[0]
    args = []
    if len(split_request) > 1:
        rest = split_request[1]

        if cmd.upper() in REG_LOGIN_CMD:
            args = [rest]
        else:
            args = rest.split(PARAMETER_SEPARATOR)

    return cmd, args


def write_to_log(msg):
    logging.info(msg)
    print(msg)
