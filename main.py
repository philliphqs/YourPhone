from flask import Flask, jsonify, request, redirect

from dearpygui.dearpygui import *
import os

import socket

import ctypes
import tinyWinToast.tinyWinToast
import time

app = Flask(__name__)

config = tinyWinToast.tinyWinToast.Config()
config.APP_ID = "YourPhone"


localip = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
           [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]


@app.route('/test', methods=['GET'])
def test():
    return jsonify({"result": "SUCCESS"})


@app.route('/automation/mailbox', methods=['POST'])
def mailbox():
    message = request.headers.get('message')
    print(message)

    toast = tinyWinToast.tinyWinToast.Toast(config)
    toast.setTitle("Mailbox", maxLines=1)
    toast.setMessage(message, maxLines=1)
    # toast.setIcon('icons/battery.jpg')
    toast.show()

    return jsonify({"result": "SUCCESS"})


@app.route('/automation/sms_code', methods=['POST'])
def sms_code():
    message = request.headers.get('message')
    print(message)

    toast = tinyWinToast.tinyWinToast.Toast(config)
    toast.setTitle("SMS-Code", maxLines=1)
    toast.setMessage(message, maxLines=1)
    # toast.setIcon('icons/battery.jpg')
    toast.show()

    return jsonify({"result": "SUCCESS"})


@app.route('/automation/lock', methods=['POST'])
def lock():
    print('lock')

    toast = tinyWinToast.tinyWinToast.Toast(config)
    toast.setTitle("Locking PC in 10 seconds", maxLines=1)
    toast.setMessage('This PC will get locked in 10 seconds', maxLines=1)
    # toast.setIcon('icons/battery.jpg')
    toast.show()    

    time.sleep(10)

    ctypes.windll.user32.LockWorkStation()

@app.route('/automation/battery_low', methods=['POST'])
def battery_low():
    print("battery low")


    toast = tinyWinToast.tinyWinToast.Toast(config)
    toast.setTitle("Your phone is under 15%", maxLines=1)
    toast.setMessage("Charge your phone before it's to late", maxLines=1)
    # toast.setIcon('icons/battery.jpg')
    toast.show()
    return jsonify({"result": "SUCCESS"})


@app.route('/automation/wind_down', methods=['POST'])
def wind_down():
    print("wind down")


    toast = tinyWinToast.tinyWinToast.Toast(config)
    toast.setTitle("Winddown started", maxLines=1)
    toast.setMessage("TEST MESSAGE", maxLines=1)
    # toast.setIcon('icons/health.jpg')
    
    toast.show()
    

def init_app():
    pass


def main():
    init_app()
    app.run(host=localip, port=528, debug=False)


if __name__ == '__main__':
    main()