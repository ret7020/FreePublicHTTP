#!/usr/bin/env python

import subprocess
import logging
import signal, os
import requests
import time

def finish(*_):
    global serveo_process
    logging.warning("Closing process")
    os.kill(serveo_process.pid, 9)
    serveo_process.stdout.close()
    exit(0)

def change_dns_url(api_url: str, api_token: str, url: str):
    requests.post(api_url, json={"token": api_token, "new_url": url}, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"
    })

def start_tunnel(host_port: int = 8000):
    serveo_process = subprocess.Popen(['ssh', '-ttR', f'80:localhost:{host_port}', 'serveo.net'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True)
    public_url = None

    while serveo_process.poll() is None and not public_url:
        tmp = serveo_process.stdout.readline().decode("utf-8")
        tmp = tmp.replace("Forwarding HTTP traffic from ", "")
        if tmp:
            public_url = tmp[5:-1].strip()
    # print(public_url, serveo_process.pid)
    return public_url, serveo_process


if __name__ == "__main__":
    url_update_token = os.getenv("URL_UPDATE_TOKEN")
    api_url = os.getenv("URL_UPDATE_API")
    signal.signal(signal.SIGALRM, handler=finish)
    logging.basicConfig(filename="events.log",
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    logging.info(f"Process of public_ip_handler.py started")

    while True:
        url, serveo_process = start_tunnel(8000)
        change_dns_url(api_url, url_update_token, url)
        logging.info(f"Tunnel started: {url}; serveo pid: {serveo_process.pid}")
        while serveo_process.poll() is None: # Process still alive, tunnel works
            time.sleep(5)
        logging.info("Restarting tunnel...")
