import logging
import sys

import kik_unofficial.datatypes.xmpp.chatting as chatting
from kik_unofficial.client import KikClient
from kik_unofficial.callbacks import KikClientCallback
from kik_unofficial.datatypes.xmpp.errors import SignUpError, LoginError
from kik_unofficial.datatypes.xmpp.roster import FetchRosterResponse, PeersInfoResponse
from kik_unofficial.datatypes.xmpp.sign_up import RegisterResponse, UsernameUniquenessResponse
from kik_unofficial.datatypes.xmpp.login import LoginResponse, ConnectionFailedResponse
import requests
listfr = ['a', 'b', 'c', 'd', 'e', 'f']
listfn = ['0', '1', '2', '3', '4', '5', '6', '7', '8']

x = ''.join(random.choice(listfn + listfr) for _ in range(32)) #  Obsolete
y = ''.join(random.choice(listfn + listfr) for _ in range(16)) #  Obsolete
device_id = x #  Obsolete 
android_id = y #  Obsolete

OWNER = "JID"

username = sys.argv[1] if len(sys.argv) > 1 else input('Username: ')
password = sys.argv[2] if len(sys.argv) > 2 else input('Password: ')


def main():
    # set up logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter(KikClient.log_format()))
    logger.addHandler(stream_handler)

    # create the bot
    bot = RageBot()


class RageBot(KikClientCallback):
    def __init__(self):
        self.client = KikClient(self, username, password, android_id_override=android_id, device_id_override=device_id)

    def on_authenticated(self):
        print("Now I'm Authenticated, let's request roster")
        self.client.request_roster()

    def on_login_ended(self, response: LoginResponse):
        print("Full name: {} {}".format(response.first_name, response.last_name))

    def on_chat_message_received(self, chat_message: chatting.IncomingChatMessage):
        print("[+] '{}' says: {}".format(chat_message.from_jid, chat_message.body))

        default_dm = "This only works in group chats, say usage for help"

        if chat_message.body.lower() == 'usage' or 'commands':
            with open("txt_files/usage.txt", "r") as f:
                self.client.send_chat_message(chat_message.from_jid, f.read())

        elif chat_message.body.lower() == 'friend':
            self.client.add_friend(chat_message.from_jid)
            self.client.send_chat_message(chat_message.from_jid, "I'll be your friend! You can now add me to groups.")

        elif chat_message.body.lower() == 'premium usage':
            with open("txt_files/premium_commands.txt", "r") as f:
                self.client.send_chat_message(chat_message.from_jid, f.read())

        elif chat_message.body.lower() == 'wisdom':
            self.client.send_chat_message(chat_message.from_jid, "blank")

        elif chat_message.body.lower() == 'list':
            self.client.send_chat_message(chat_message.from_jid, default_dm)

        elif chat_message.body.lower() == 'talkers':
            self.client.send_chat_message(chat_message.from_jid, default_dm)

        elif chat_message.body.lower() == 'trigger -> response':
            self.client.send_chat_message(chat_message.from_jid, default_dm)

        elif chat_message.body.lower() == 'trigger ~> response':
            self.client.send_chat_message(chat_message.from_jid, default_dm)

        elif chat_message.body.lower().startswith('delete'):
            self.client.send_chat_message(chat_message.from_jid, default_dm)

        elif 'rules' in chat_message.body.lower()
            with open("txt_files/rules.txt", "r") as f:
                self.client.send_chat_message(chat_message.from_jid, f.read())

        # elif chat_message.body.lower() == 'donate':
            # self.client.send_chat_message(chat_message.from_jid, "blank")

        # elif chat_message.body.lower() == 'donators':
            # self.client.send_chat_message(chat_message.from_jid, "blank")

        elif '48 mode' in chat_message.body.lower():
            with open("txt_files/48_mode.txt", "r") as f:
                self.client.send_chat_message(chat_message.from_jid, f.read())

        elif chat_message.from_jid == 'OWNER' and chat_message.body.lower().startswith('alert'): # Not a public feature but it does exist
            alert_message = chat_message.body.replace('alert', ' ')
            self.client.send_chat_message(temp, alert_message) # Add GJIDs for temp, some function probably

        else:
            self.client.send_chat_message(chat_message.from_jid, "Say usage for help, say friend to add me to your chat")

    def on_group_message_received(self, chat_message: chatting.IncomingGroupChatMessage):
        if str(chat_message.raw_element).count("</alias-sender>") > 1 and "</alias-sender>" not in str(chat_message.body):
        print("[+] '{}' from group ID {} says: {}".format(chat_message.from_jid, chat_message.group_jid, chat_message.body))

        if chat_message.body.lower() == 'admins':

        elif chat_message.body.lower() == 'activity':

        elif chat_message.body.lower() == 'talkers':

        elif chat_message.body.lower() == 'usage':
             with open("txt_files/usage.txt", "r") as f:
                 self.client.send_chat_message(chat_message.group_jid, f.read())

    def on_roster_received(self, response: FetchRosterResponse):
        print("[+] Chat partners:\n" + '\n'.join([str(member) for member in response.peers]))

    def on_friend_attribution(self, response: chatting.IncomingFriendAttribution):
        print("[+] Friend attribution request from " + response.referrer_jid)

    def on_peer_info_received(self, response: PeersInfoResponse):
        print("[+] Peer info: " + str(response.users))

    def on_status_message_received(self, response: chatting.IncomingStatusResponse):
        pass

    def on_username_uniqueness_received(self, response: UsernameUniquenessResponse):
        print("Is {} a unique username? {}".format(response.username, response.unique))

    def on_sign_up_ended(self, response: RegisterResponse):
        print("[+] Registered as " + response.kik_node)

    # Error handling

    def on_connection_failed(self, response: ConnectionFailedResponse):
        print("[-] Connection failed: " + response.message)

    def on_login_error(self, login_error: LoginError):
        if login_error.is_captcha():
            login_error.solve_captcha_wizard(self.client)

    def on_register_error(self, response: SignUpError):
        print("[-] Register error: {}".format(response.message))


if __name__ == '__main__':
    main()
