# -*- coding: utf-8 -*-

import struct
from base64 import b64encode
from hashlib import sha1
from typing import Dict, Tuple
from uuid import uuid4
from socket import error as SocketError
import errno


from .logger import get_logger
from simple_http_server import Headers, WebsocketRequest, WebsocketSession

_logger = get_logger("http_request_handler")


'''
+-+-+-+-+-------+-+-------------+-------------------------------+
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-------+-+-------------+-------------------------------+
|F|R|R|R| opcode|M| Payload len |    Extended payload length    |
|I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
|N|V|V|V|       |S|             |   (if payload len==126/127)   |
| |1|2|3|       |K|             |                               |
+-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
|     Extended payload length continued, if payload len == 127  |
+ - - - - - - - - - - - - - - - +-------------------------------+
|                     Payload Data continued ...                |
+---------------------------------------------------------------+
'''

FIN = 0x80
OPCODE = 0x0f
MASKED = 0x80
PAYLOAD_LEN = 0x7f
PAYLOAD_LEN_EXT16 = 0x7e
PAYLOAD_LEN_EXT64 = 0x7f

OPCODE_CONTINUATION = 0x0
OPCODE_TEXT = 0x1
OPCODE_BINARY = 0x2
OPCODE_CLOSE_CONN = 0x8
OPCODE_PING = 0x9
OPCODE_PONG = 0xA

OPTYPES = {
    OPCODE_TEXT: "TEXT",
    OPCODE_PING: "PING",
    OPCODE_PONG: "PONE",
    OPCODE_BINARY: "BINARY"
}


def _msg_received(session, msg):
    if msg == "close":
        _logger.info("close session!")
        session.close("close session!")
    else:
        session.send(msg)
        _logger.info(f"receive message {msg}")


class WebsocketRequestHandler:

    GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

    def __init__(self, base_http_quest_handler) -> None:
        self.base_http_quest_handler = base_http_quest_handler
        self.request = base_http_quest_handler.request
        self.server = base_http_quest_handler.server
        self.send_response = base_http_quest_handler.send_response_only
        self.send_header = base_http_quest_handler.send_header
        self.rfile = base_http_quest_handler.rfile
        self.keep_alive = True
        self.handshake_done = False

        handler_class, path_values = self.server.get_websocket_handler(base_http_quest_handler.request_path)
        self.handler = handler_class() if handler_class else None
        self.ws_request = WebsocketRequest()
        self.ws_request.headers = base_http_quest_handler.headers
        self.ws_request.path = base_http_quest_handler.request_path
        self.ws_request.query_string = base_http_quest_handler.query_string
        self.ws_request.parameters = base_http_quest_handler.query_parameters
        self.ws_request.path_values = path_values
        if "cookie" in self.ws_request.headers:
            self.ws_request.cookies.load(self.ws_request.headers["cookie"])
        elif "Cookie" in self.ws_request.headers:
            self.ws_request.cookies.load(self.ws_request.headers["Cookie"])
        self.session = WebsocketSessionImpl(self, self.ws_request)
        self.close_reason = ""

    @property
    def response_headers(self):
        if hasattr(self.base_http_quest_handler, "_headers_buffer"):
            return self.base_http_quest_handler._headers_buffer
        else:
            return []

    def on_handshake(self) -> Tuple[int, Dict[str, str]]:
        if not hasattr(self.handler, "on_handshake") or not callable(self.handler.on_handshake):
            return None, {}
        res = self.handler.on_handshake(self.ws_request)
        http_status_code = None
        headers = {}
        if not res:
            pass
        elif isinstance(res, int):
            http_status_code = res
        elif isinstance(res, dict) or isinstance(res, Headers):
            headers = res
        elif isinstance(res, tuple):
            for item in res:
                if isinstance(item, int) and not http_status_code:
                    http_status_code = item
                elif isinstance(item, dict) or isinstance(item, Headers):
                    headers.update(item)
        else:
            _logger.warn(f"Endpoint[{self.ws_request.path}]")
        return http_status_code, headers

    def on_message(self, op_code, message):
        if hasattr(self.handler, "on_message") and callable(self.handler.on_message):
            self.handler.on_message(self.session, OPTYPES[op_code], message)
        
        if op_code == OPCODE_TEXT and hasattr(self.handler, "on_text_message") and callable(self.handler.on_text_message):
            self.handler.on_text_message(self.session, message)
        elif op_code == OPCODE_PING and hasattr(self.handler, "on_ping_message") and callable(self.handler.on_ping_message):
            self.handler.on_ping_message(self.session, message)
        elif op_code == OPCODE_PONG and hasattr(self.handler, "on_pong_message") and callable(self.handler.on_pong_message):
            self.handler.on_pong_message(self.session, message)

    def on_open(self):
        if hasattr(self.handler, "on_open") and callable(self.handler.on_open):
            self.handler.on_open(self.session)

    def on_close(self):
        if hasattr(self.handler, "on_close") and callable(self.handler.on_close):
            self.handler.on_close(self.session, self.close_reason)

    def handle(self):
        while self.keep_alive:
            if not self.handshake_done:
                self.handshake()
            else:
                self.read_next_message()

        self.on_close()

    def handshake(self):
        if self.handler:
            code, headers = self.on_handshake()
            if code and code != 101:
                self.keep_alive = False
                self.send_response(code)
            else:
                self.send_response(101, "Switching Protocols")
                self.send_header("Upgrade", "websocket")
                self.send_header("Connection", "Upgrade")
                self.send_header("Sec-WebSocket-Accept", self.calculate_response_key())
            if headers:
                for h_name, h_val in headers.items():
                    self.send_header(h_name, h_val)
        else:
            self.keep_alive = False
            self.send_response(404)

        ws_res_headers = b"".join(self.response_headers) + b"\r\n"
        _logger.debug(ws_res_headers)
        self.request.send(ws_res_headers)
        self.handshake_done = True
        if self.keep_alive == True:
            self.on_open()

    def calculate_response_key(self):
        _logger.debug(f"Sec-WebSocket-Key: {self.ws_request.headers['Sec-WebSocket-Key']}")
        key: str = self.ws_request.headers["Sec-WebSocket-Key"]
        hash = sha1(key.encode() + self.GUID.encode())
        response_key = b64encode(hash.digest()).strip()
        return response_key.decode('ASCII')

    def read_bytes(self, num):
        return self.rfile.read(num)

    def read_next_message(self):
        _logger.debug("read next message")
        try:
            b1, b2 = self.read_bytes(2)
        except SocketError as e:  # to be replaced with ConnectionResetError for py3
            if e.errno == errno.ECONNRESET:
                _logger.info("Client closed connection.")
                self.keep_alive = False
                self.close_reason = "Client closed connection."
                return
            b1, b2 = 0, 0
        except ValueError as e:
            b1, b2 = 0, 0

        fin = b1 & FIN
        opcode = b1 & OPCODE
        masked = b2 & MASKED
        payload_length = b2 & PAYLOAD_LEN

        if opcode == OPCODE_CLOSE_CONN:
            _logger.info("Client asked to close connection.")
            self.keep_alive = False
            self.close_reason = "Client asked to close connection."
            return
        if not masked:
            _logger.warn("Client must always be masked.")
            self.keep_alive = False
            self.close_reason = "Client is not masked."
            return
        if opcode == OPCODE_CONTINUATION:
            _logger.warn("Continuation frames are not supported.")
            return
        elif opcode == OPCODE_BINARY:
            _logger.warn("Binary frames are not supported.")
            return
        elif opcode == OPCODE_TEXT:
            opcode_handler = self.on_message
        elif opcode == OPCODE_PING:
            opcode_handler = self.on_message
        elif opcode == OPCODE_PONG:
            opcode_handler = self.on_message
        else:
            _logger.warn(f"Unknown opcode {opcode}.")
            self.keep_alive = False
            self.close_reason = f"Unknown opcode {opcode}."
            return

        if payload_length == 126:
            payload_length = struct.unpack(">H", self.rfile.read(2))[0]
        elif payload_length == 127:
            payload_length = struct.unpack(">Q", self.rfile.read(8))[0]

        masks = self.read_bytes(4)
        message_bytes = bytearray()
        for message_byte in self.read_bytes(payload_length):
            message_byte ^= masks[len(message_bytes) % 4]
            message_bytes.append(message_byte)
        opcode_handler(opcode, message_bytes.decode('utf8'))

    def send_message(self, message):
        self.send_text(message)

    def send_ping(self, message):
        self.send_text(message, OPCODE_PING)

    def send_pong(self, message):
        self.send_text(message, OPCODE_PONG)

    def send_text(self, message, opcode=OPCODE_TEXT):
        """
        Important: Fragmented(=continuation) messages are not supported since
        their usage cases are limited - when we don't know the payload length.
        """

        # Validate message
        if isinstance(message, bytes):
            message = self._try_decode_UTF8(message)  # this is slower but ensures we have UTF-8
            if not message:
                _logger.warning("Can\'t send message, message is not valid UTF-8")
                return False
        elif isinstance(message, str):
            pass
        else:
            _logger.warning('Can\'t send message, message has to be a string or bytes. Given type is %s' % type(message))
            return False

        header = bytearray()
        payload = self._encode_to_UTF8(message)
        payload_length = len(payload)

        # Normal payload
        if payload_length <= 125:
            header.append(FIN | opcode)
            header.append(payload_length)

        # Extended payload
        elif payload_length >= 126 and payload_length <= 65535:
            header.append(FIN | opcode)
            header.append(PAYLOAD_LEN_EXT16)
            header.extend(struct.pack(">H", payload_length))

        # Huge extended payload
        elif payload_length < 18446744073709551616:
            header.append(FIN | opcode)
            header.append(PAYLOAD_LEN_EXT64)
            header.extend(struct.pack(">Q", payload_length))

        else:
            raise Exception("Message is too big. Consider breaking it into chunks.")

        self.request.send(header + payload)

    def close(self, reason=""):
        self.send_text(reason, OPCODE_CLOSE_CONN)
        self.keep_alive = False
        self.close_reason = "Server asked to close connection."

    def _encode_to_UTF8(self, data):
        try:
            return data.encode('UTF-8')
        except UnicodeEncodeError as e:
            _logger.error("Could not encode data to UTF-8 -- %s" % e)
            return False
        except Exception as e:
            raise(e)
            return False

    def _try_decode_UTF8(self, data):
        try:
            return data.decode('utf-8')
        except UnicodeDecodeError:
            return False
        except Exception as e:
            raise(e)


class WebsocketSessionImpl(WebsocketSession):

    def __init__(self, handler: WebsocketRequestHandler, request: WebsocketRequest) -> None:
        self.__id = uuid4().hex
        self.__handler = handler
        self.__request = request

    @property
    def id(self):
        return self.__id

    @property
    def request(self):
        return self.__request

    @property
    def is_closed(self):
        return not self.__handler.keep_alive

    def send_ping(self, message: str):
        self.__handler.send_ping(message)

    def send(self, message: str):
        self.__handler.send_message(message)

    def send_pone(self, message: str):
        self.__handler.send_pong(message)

    def close(self, reason: str):
        self.__handler.close(reason)
