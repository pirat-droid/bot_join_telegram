import requests
from os import system
import time
import threading
from signal import signal, alarm, SIGALRM


class Network:

    @staticmethod
    def vpn_connect(open_vpn):
        sudo_password = 'Dfkkf-123'
        command = open_vpn + ' --auth-user-pass authentication_vpn.txt'
        system('echo %s|sudo -S %s' % (sudo_password, command))

    def __init__(self, vpn, account, db):
        self.vpn = vpn
        self.account = account
        self.db = db

    def __handler(self, signum, frame):
        raise Exception('Время ожидания истекло \n')

    def my_ip(self):
        signal(SIGALRM, self.__handler)
        alarm(2)
        try:
            ip = requests.get('http://ifconfig.me/ip').text
            return ip
        except:
            return False
        finally:
            alarm(0)

    def open_vpn(self):
        try:
            requests.get('https://ya.ru/')
            if self.vpn != 'no':
                threading.Thread(target=self.vpn_connect, args=('openvpn --config /etc/openvpn/' + self.vpn,),
                                 daemon=True).start()
                i = 0
                while i < 6:
                    time.sleep(2)
                    if self.my_ip() != '31.163.196.69':
                        return True
                    i += 1
                else:
                    return False
            else:
                if self.my_ip() != '31.163.196.69':
                    return False
                else:
                    return True

        except requests.exceptions.ConnectionError:
            return False
