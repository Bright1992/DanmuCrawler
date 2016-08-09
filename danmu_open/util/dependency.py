import socket
import struct
import sys
import time
import threading
import os

host="openbarrage.douyutv.com"
port=8601
MAGICNUM_TO_SERVER=689
MAGICNUM_FROM_SERVER=690
KEEPALIVE_INTERVAL=40