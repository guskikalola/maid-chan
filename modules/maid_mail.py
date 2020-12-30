#############################################
#                                           #
#                  [MODULE]                 #
#               Mail Listener               #
#                                           #
#############################################
import imaplib
from playsound import playsound
from time import sleep
from email import message_from_string
from email.header import decode_header
from threading import Thread
from PyQt5.Qt import QObject,QThread, QTextDocument, QAudio
# Load mail config from the config.json
import json
with open('./config.json') as configFile_data:
    mail_cfg = json.load(configFile_data)
mail_cfg = mail_cfg["email"]
# Email listening will be addressed to a separated thread
class worker(QObject):
    def work(self,callback):
        callback()

class mailListener(Thread):
    def __init__(self, username, password):
        super(mailListener, self).__init__()
        self.username = username
        self.password = password
        self.mail = imaplib.IMAP4_SSL("imap.gmail.com")
        self.newMailSound = "../resources/sounds/newmail.mp3"

    def login(self):
        if(self.mail.state == "NONAUTH"): # Only login if there is no auth already
            self.mail.login(self.username, self.password)
        data = self.mail.list()

    def read(self):
        self.mail.select(mail_cfg["mailbox_name"]) # Selects the mailbox to work on
        email_data = {}
        result, data = self.mail.search(None, "ALL")
        if(result == "OK"):
            ID = data[0].split()
            self.lastLength = ID[-1]  # [LAST_LENGTH SET]
            result, data = self.mail.fetch(ID[-1], "(RFC822)") # Fetch last email
            if(result == "OK"):
                raw_email = data[0][1]
                msg = message_from_string(str(raw_email, "utf-8"))
                # [GET SENDER]
                sender = []
                data = decode_header(msg.get("From"))
                for a, b in data:
                    if(type(a) == bytes):
                        sender.append(str(a, "utf-8"))
                    else:
                        sender.append(a)
                email_data["from"] = "".join(sender)  # [FROM(Sender) SET]

                # If the sender is ignored, then just ignore the mail
                if(mail_cfg["ignoredSenders"].count(email_data["from"]) == 0):
                    # Set the email_data fields with the retrieved information
                    # [GET SUBJECT]
                    subject = []
                    data = decode_header(msg.get("Subject"))
                    for a, b in data:
                        if(type(a) == bytes):
                            subject.append(str(a, "utf-8"))
                        else:
                            subject.append(a)
                    email_data["subject"] = ''.join(subject)
                    email_data["from"] = ''.join(sender)  # [FROM(Sender) SET]
                else:
                    return False
        return "Ha recibido un correo de: \n" + email_data["from"] + "\nAsunto:\n" + email_data["subject"]

    def start(self, maid_thread):   # Runs the listener in a separated thread
        # t = Thread(target=self.listen, args=[callback])
        # t.start()
        # self.main_thead = worker()
        # self.main_thead.moveToThread(maid_thread)
        worker_thread = QThread()
        self.slave = worker()
        self.slave.moveToThread(worker_thread)
        listenThread = Thread(target=self.listen, args=[maid_thread])
        listenThread.start()
        # print(maid_thread)
        # maid_thread.thread.connect(listen)
        # self.maid_thread = maid_thread
    def listen(self,maid_thread):
        if(self.mail.state != "AUTH"): # Prevent running without session logged
           self.login() 
        while(True):
            if(self.mail.state == "SELECTED"): # Prevent running before selecting mailbox
                result, data = self.mail.search(None, "ALL")
                currentLength = data[0].split()[-1]
                data = self.read()
                if(int(currentLength) < int(self.lastLength)):
                    def playSound():
                        Thread(target=playsound,args=['resources/sounds/newmail.mp3']).start()
                    def notify():
                        maid_thread.notificationQueue.append(data)
                        if(maid_thread.working == False):
                            playSound()
                            maid_thread.createNotification()
                        else:
                            looping = True
                            while(looping):
                                if(maid_thread.working == False):
                                    playSound()
                                    maid_thread.createNotification()
                                    looping = False
                    self.slave.work(notify)
listener = mailListener(mail_cfg["username"],mail_cfg["password"])
