import subprocess
from authentication import password_system
from time import sleep
import socket
from database import DatabasePG
from network import Network
from telegram import Bot


def main():
    vm_name = socket.gethostname()
    while True:
        msg = ''
        db = DatabasePG("bot")
        vm = db.get_select(f"SELECT id FROM webcontrolbot_vmmodel WHERE name_vm = '{vm_name}'")
        rows = db.get_select(f"SELECT id, active, phone, api_id, api_hash, vpn_id, doge, ltc, zec, date_close FROM"
                             f" webcontrolbot_accounttelegrammodel WHERE market_id = 2 and vm_id = " + str(vm[0][0]))
        accounts = []

        for row in rows:
            account = {}
            if not row[1] or len(row) < 10 or not row[5]:
                continue
            account['id'] = row[0]
            account['phone'] = row[2]
            account['api_id'] = row[3]
            account['api_hash'] = row[4]
            account['doge'] = row[6]
            account['ltc'] = row[7]
            account['zec'] = row[8]
            account['last_active'] = row[9]
            account['vpn'] = str(
                db.get_select(f"SELECT name_vpn FROM webcontrolbot_vpnmodel WHERE id = {row[5]}")[0][0])
            accounts.append(account)
        for account in accounts:
            index = 1
            while index <= 10:
                proc = subprocess.Popen('sudo -S sudo killall openvpn', shell=True, stdin=subprocess.PIPE)
                proc.communicate(password_system.encode('UTF-8'))
                proc.wait()
                sleep(2)
                nt = Network(account['vpn'], account['id'], db)
                if nt.open_vpn():
                    print('network state True')
                    break
                index += 1
            else:
                continue

            print(account['phone'])
            tel = Bot(account['phone'], account['api_id'], account['api_hash'], 'CNHungry', db)
            if not tel.search_dialog():
                print('подписываемся')
                tel.join_channel()
            link = tel.get_link()
            tel.watch_message(link)
        db.close_db()


if __name__ == '__main__':
    main()
