import os
import time
import threading
import webbrowser


def server():
    os.system('python manage.py runserver localhost:80')


threading.Thread(target=server).start()
webbrowser.get().open('http://localhost/console/')
