
import socket
import subprocess
import time
import datetime

def main_loop():
    sleep_till_full_min()
    while True:
        dev = run_nmap()
        print('\r\n' * 1000)
        dtn = f'[{datetime.datetime.now():%H:%M}]'
        for x in dev:
            print(f'''{dtn} ip {x['ip']:>15}     device {x['device_name']:>15}     mac {x['mac']}''')
        print()
        print(f'{dtn} {len(dev)} devices are connected')
        sleep_till_full_min()

def run_nmap():
    cmd = f'nmap -sn {get_local_ip()}/24'
    cmd_out = str(subprocess.run(cmd, capture_output = True))
    device_list = cmd_out.split(r'\r\n')[1:-4]
    devices = []
    for x in range(0, len(device_list), 3):
        ip = device_list[x][21:]
        mac = device_list[x+2][13:]
        devices.append({'ip':ip, 'device_name':get_device_name_by_ip(ip), 'mac':mac})
    return devices

def get_device_name_by_ip(ip):
    res = socket.getfqdn(ip)
    return res

def sleep_till_full_min():
    while int(f'{datetime.datetime.now():%S}') != 0:
        time.sleep(1)

def get_local_ip():
    local_ip=socket.gethostbyname(socket.gethostname())   
    return local_ip

if __name__ == '__main__':
    main_loop()