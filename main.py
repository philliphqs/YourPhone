from flask import Flask, jsonify, request, redirect

from dearpygui.dearpygui import *
import webbrowser
import urllib.request
from datetime import date
import os
from PIL import Image
import win32clipboard
import socket

app = Flask(__name__)

localip = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
           [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]


@app.route('/test', methods=['GET'])
def test():
    return jsonify({"result": "SUCCESS"})


@app.route('/show_window', methods=['get'])
def show_window():
    text = request.args.get('text', 'ERROR:TEXT')

    text = text.replace('_DOPPELPUNKT_', ':')
    text = text.replace('_SLASH_', '/')
    text = text.replace('_FRAGEZEICHEN_', '?')
    text = text.replace('_PERCENT_', '%')
    text = text.replace('_BINDESTRICH_', '-')
    text = text.replace('_EMPTY_', ' ')

    def viewport_init():
        vp = create_viewport()
        setup_dearpygui(viewport=vp)
        configure_viewport(0, height=500, width=500, x_pos=600, y_pos=200)
        set_viewport_title("Clipboard")
        set_viewport_always_top(True)
        set_viewport_resizable(False)
        set_viewport_maximized_box(False)
        set_viewport_small_icon('icons/clipboard.ico')
        set_viewport_large_icon('icons/clipboard.ico')
        show_viewport(vp)

    with window(label="window", width=500, height=500) as main_window:
        add_input_text(id=1, width=470, height=445, multiline=True, readonly=False,
                       default_value=text, label=' ')

    viewport_init()
    set_primary_window(main_window, True)
    start_dearpygui()

    return '...'


@app.route('/open_url', methods=['get'])
def open_url():
    url = request.args.get('url', 'ERROR:URL')

    url = url.replace('_DOPPELPUNKT_', ':')
    url = url.replace('_SLASH_', '/')
    url = url.replace('_FRAGEZEICHEN_', '?')
    url = url.replace('_PERCENT_', '%')
    url = url.replace('_BINDESTRICH_', '-')

    webbrowser.open(url)
    return '...'


@app.route('/show_image', methods=['get'])
def show_image():
    url = request.args.get('url', 'ERROR:URL')

    url = url.replace('_DOPPELPUNKT_', ':')
    url = url.replace('_SLASH_', '/')
    url = url.replace('_FRAGEZEICHEN_', '?')
    url = url.replace('_PERCENT_', '%')
    url = url.replace('_BINDESTRICH_', '-')

    path = f"C:/Users/{os.getlogin()}/Downloads/drop_{date.today()}.png"

    urllib.request.urlretrieve(url, path)

    img = Image.open(path)
    img.show()

    return '...'


# Anything towards phone
@app.route('/phone/open_url', methods=['get'])
def phone_open_url():
    try:
        win32clipboard.OpenClipboard()
        c = win32clipboard.GetClipboardData()
        win32clipboard.EmptyClipboard()
        c = c.replace('\n', ' ')
        c = c.replace('\r', ' ')
        while c.find('  ') != -1:
            c = c.replace('  ', ' ')
        win32clipboard.SetClipboardText(c)
        win32clipboard.CloseClipboard()

        return jsonify({
            "url": c
        })
    except:
        return jsonify({
            "url": "Clipboard is empty or there is no copied url"
        })


@app.route('/phone/get_clipboard', methods=['get'])
def phone_get_clipboard():
    try:
        win32clipboard.OpenClipboard()
        c = win32clipboard.GetClipboardData()
        win32clipboard.EmptyClipboard()
        c = c.replace('\n', ' ')
        c = c.replace('\r', ' ')
        while c.find('  ') != -1:
            c = c.replace('  ', ' ')
        win32clipboard.SetClipboardText(c)
        win32clipboard.CloseClipboard()

        return jsonify({
            "clipboard": c
        })
    except:
        return jsonify({
            "clipboard": "Clipboard is empty"
        })


def init_app():
    pass


def main():
    init_app()
    app.run(host=localip, port=528, debug=False)


if __name__ == '__main__':
    main()