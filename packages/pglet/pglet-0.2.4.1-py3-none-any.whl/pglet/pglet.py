import os
import pathlib
import platform
import subprocess
import urllib.request
import zipfile
import tarfile
import re
import signal
from threading import Thread
from time import sleep
from .utils import is_windows, which
from .connection import Connection

PGLET_VERSION = "0.2.4"
pglet_exe = ""

def page(name='', web=False, server='', token='', no_window=False):

    pargs = [pglet_exe, "page"]

    if name != "":
        pargs.append(name)
    
    if web:
        pargs.append("--web")

    if server != "":
        pargs.append("--server")
        pargs.append(server)

    if token != "":
        pargs.append("--token")
        pargs.append(token)

    if no_window:
        pargs.append("--no-window")

    # execute pglet.exe and get connection ID
    exe_result = subprocess.check_output(pargs).decode("utf-8").strip()
    result_parts = re.split(r"\s", exe_result, 1)

    p = Connection(result_parts[0])
    p.url = result_parts[1]
    p.web = web
    return p

def app(name='', web=False, server='', token='', target=None, no_window=False):

    if target == None:
        raise Exception("target argument is not specified")

    pargs = [pglet_exe, "app"]

    if name != "":
        pargs.append(name)
    
    if web:
        pargs.append("--web")

    if server != "":
        pargs.append("--server")
        pargs.append(server)

    if token != "":
        pargs.append("--token")
        pargs.append(token)

    if no_window:
        pargs.append("--no-window")        

    # execute pglet.exe and get connection ID
    page_url = ""
    proc = subprocess.Popen(pargs, bufsize=0, stdout = subprocess.PIPE)
    for bline in proc.stdout:
        line = bline.decode('utf-8').rstrip()
        if page_url == "":
            # 1st is URL
            page_url = line
        else:
            # connection ID
            conn_id = line

            # create connection object
            p = Connection(conn_id)
            p.url = page_url
            p.web = web
            
            # start page session in a new thread
            thread = Thread(target = target, args = (p,))
            thread.start()


def install():
    global pglet_exe

    if is_windows():
        pglet_exe = "pglet.exe"
    else:
        pglet_exe = "pglet"

    # check if pglet.exe is in PATH already (development mode)
    pglet_in_path = which(pglet_exe)
    if pglet_in_path:
        pglet_exe = pglet_in_path
        return

    home = str(pathlib.Path.home())
    pglet_dir = os.path.join(home, ".pglet")
    pglet_bin = os.path.join(pglet_dir, "bin")

    if not os.path.exists(pglet_bin):
        os.makedirs(pglet_bin)
    
    if is_windows():
        pglet_exe = os.path.join(pglet_bin, pglet_exe)
    else:
        pglet_exe = os.path.join(pglet_bin, pglet_exe)

    ver = PGLET_VERSION

    installed_ver=None

    if os.path.exists(pglet_exe):
        # get installed pglet version
        installed_ver = subprocess.check_output([pglet_exe, "--version"]).decode("utf-8")
        #print(f'Found Pglet v{installed_ver}')
    
    if not installed_ver or installed_ver != ver:
        #print(f'Installing Pglet v{PGLET_VERSION}...')

        a = platform.machine().lower()
        if a == "x86_64" or a == "amd64":
            arch = "amd64"
        elif a == "arm64" or a == "aarch64":
            arch = "arm64"
        elif a.startswith("arm"):
            arch = "arm"
        else:
            raise Exception(f"Unsupported architecture: {a}")

        p = platform.system()
        if is_windows():
            plat = "windows"
            ext = "zip"
        elif p == "Linux":
            plat = "linux"
            ext = "tar.gz"
        elif p == "Darwin":
            plat = "darwin"
            ext = "tar.gz"
        else:
            raise Exception(f"Unsupported platform: {p}")

        # download archive
        pglet_url = f"https://github.com/pglet/pglet/releases/download/v{ver}/pglet-{ver}-{plat}-{arch}.{ext}"
        temp_arch = os.path.join(pglet_dir, f"pglet-{ver}-{plat}-{arch}.{ext}")

        #print (pglet_url)

        urllib.request.urlretrieve(pglet_url, temp_arch)

        if is_windows():
            with zipfile.ZipFile(temp_arch, 'r') as zip_arch:
                zip_arch.extractall(pglet_bin)
        else:
            with tarfile.open(temp_arch, 'r:gz') as tar_arch:
                tar_arch.extractall(pglet_bin)

        os.remove(temp_arch)

# install Pglet during import
install()

# Fix: https://bugs.python.org/issue35935
signal.signal(signal.SIGINT, signal.SIG_DFL)