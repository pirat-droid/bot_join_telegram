import psutil
from telethon import TelegramClient, sync, events
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from time import sleep, timezone
from telethon.tl.functions.messages import GetHistoryRequest
from pyvirtualdisplay import Display
import shlex
import subprocess
import Xlib.display


class Bot:

    def __init__(self, phone, api_id, api_hash, channel, db):
        self.client = TelegramClient(phone, api_id, api_hash)
        self.channel = channel
        self.db = db

    def __get_mes(self, channel_entity):
        post = self.client(GetHistoryRequest(
            peer=channel_entity,
            limit=1,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0))
        return post

    @staticmethod
    def __kill_proc_chromium():
        for proc in psutil.process_iter():
            if proc.name() == 'chromium':
                proc.kill()

    def search_dialog(self):
        client = self.client.start()
        for dialog in self.client.iter_dialogs():
            try:
                if dialog.name == self.channel:
                    client.disconnect()
                    return True
            except:
                client.disconnect()
        client.disconnect()
        return False

    def join_channel(self):
        client = self.client.start()
        try:
            client(JoinChannelRequest(f'@{self.channel}'))
        except Exception as e:
            print(e)
            client.disconnect()

    def get_link(self):
        client = self.client.start()
        try:
            channel_entity = client.get_entity(self.channel)
            messages = self.__get_mes(channel_entity)
            id = messages.messages[0].id
            link = f'https://t.me/{self.channel}/{str(id)}'
        except:
            client.disconnect()
        client.disconnect()
        return link

    def watch_message(self, link):
        disp = Display(visible=False, size=(1366, 768), backend="xvfb", color_depth=24).start()
        command = '/usr/bin/chromium-browser "' + link + '"'
        args = shlex.split(command)
        run_browser = subprocess.Popen(args)
        sleep(5)
        run_browser.kill()
        disp.stop()





