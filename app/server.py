#!/usr/bin/env python

from bottle import static_file, route, run
from threading import Thread

import asyncio
import websockets
import json
import bot
import re

clients = set()

#serving index.html file on "http://localhost:9000"
def httpHandler():
    while True:
        @route('/')
        def index():
            static_file('index.css', root='./app')
            static_file('client.js', root='./app')
            return static_file("index.html", root='./app')

        @route('/<filename>')
        def server_static(filename):
            return static_file(filename, root='./app')

        run(host='localhost', port=9000)


async def receive_send(websocket, path):
    # Please write your code here

    global clients
    clients.add(websocket)
    try:
        while True:
            msg = await websocket.recv()
            ans = {}
            ans['data'] = msg
            await asyncio.wait([ws.send(json.dumps(ans)) for ws in clients])
            if re.match(' *bot +.+ +.+ *', msg) != None:
                command_list = re.split(" +", msg)[1:]
                command_dic = {'command': command_list[0], 'data': command_list[1]}
                bt = bot.Bot(command_dic)
                bt.generate_hash()
                ans['data'] = bt.hash
                await asyncio.wait([ws.send(json.dumps(ans)) for ws in clients])

    except websockets.exceptions.ConnectionClosed:
        pass

    finally:
        clients.remove(websocket)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    start_server = websockets.serve(receive_send, '127.0.0.1', 3000)
    server = loop.run_until_complete(start_server)
    print('Listen')

    t = Thread(target=httpHandler)
    t.daemon = True
    t.start()

    try:
        loop.run_forever()
    finally:
        server.close()
        start_server.close()
        loop.close()
