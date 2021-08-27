import subprocess
import requests
from decouple import config
import os

IP_NETWORK = config('IP_NETWORK')
IP_DEVICE = config('IP_DEVICE')


proc = subprocess.Popen(["ping", IP_NETWORK], stdout=subprocess.PIPE)
print("Scanning for new IPs...")

while True:
    line = proc.stdout.readline()
    if not line:
        break
    # the real code does filtering here
    connected_ip = line.decode('utf-8').split()[3].split(":")[0]

    if connected_ip == IP_DEVICE:
        print("New IP detected!")
        os.system(f"nslookup {connected_ip} > dns.txt")
        with open("dns.txt", "r") as f:
            lines = f.readlines()
            dns_name = lines[-2].split()[-1].split('.')[0]
        requests.get('https://api.telegram.org/bot1996090749:AAGTqqw06z7_Y0DwpynzrjEKxUEEWs9eGms/sendMessage?chat_id'
                     '=-499444156&text="{} has been connected to your network!"'.format(dns_name))
        break

