import socket
import sys
import threading
from ttkbootstrap import *
import tkinter as tk
from tkinter import ttk, scrolledtext
import time
from datetime import datetime
from plyer import notification
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs import *
import re


class Peer:
    def __init__(self, my_ip, my_port):
        self.my_ip = my_ip
        self.my_port = my_port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((my_ip, my_port))
        self.start_thread = True

        try:
            self.receiveThread = threading.Thread(target=self.receive_message)
            self.receiveThread.start()
        except threading.ThreadError:
            print("Error: unable to start thread")
        else:
            print("Thread started")

        # self.agreement = noStupidAgreement()
        # self.agreement.root.wait_window()

        self.uiroot = Window(themename='darkly')
        self.uiroot.title("simplezchat")
        self.uiroot.geometry("800x600")
        self.uiroot.resizable(False, False)
        self.chat_ui = ChatUI(self.uiroot, connection=self)
        self.uiroot.protocol("WM_DELETE_WINDOW", self.on_close)
        self.uiroot.mainloop()

    def on_close(self):
        print('buh bye!')
        self.start_thread = False
        self.receiveThread.join()
        print("Thread closed")
        self.s.close()
        print("Socket closed")
        self.uiroot.destroy()
        print("UI closed")
        sys.exit(0)

    def send_message(self, target_ip, target_port, messageContents):
        print(f"Sending '{messageContents}' to {target_ip}:{target_port}")
        self.s.sendto(messageContents.encode(), (target_ip, target_port))



class ChatUI:
    def __init__(self, uiroot, connection):
        self.root = uiroot
        self.connectpeer = connection

        Label(self.root, text="Simple LAN Chat", font=('Helvetica', 16, 'bold')).pack(pady=10, anchor='center')

        self.chat_scrollframe = ScrolledFrame(self.root)
        self.chat_scrollframe.pack(fill="both", expand=True, padx=10, pady=10)

        self.ip_frame = Frame(self.root)
        self.ip_frame.pack(fill="x", padx=20, anchor='n')

        self.ip_label = Label(self.ip_frame, text="Send to: ")
        self.ip_label.pack(side="left")

        self.ip_entry = Entry(self.ip_frame)
        self.ip_entry.pack(side="left", padx=5, fill="x", expand=True)

        self.entered_ip = ""

        self.message_entry_frame = Frame(self.root)
        self.message_entry_frame.pack(fill="x", padx=20, pady=(10, 20), anchor='s')

        self.message_entry = ScrolledText(self.message_entry_frame, height=5, wrap="word")
        self.message_entry.pack(fill="x", side="left", expand=True)
        self.message_entry.bind("<Return>", self.handle_return)

        self.send_button = Button(self.message_entry_frame, text="Send")
        self.send_button.pack(side="right", anchor='n', padx=5)
        self.send_button.bind("<Button-1>", lambda event: self.send_event())

    def handle_return(self, event):
        if event.state & 0x1:
            pass
        else:
            self.send_event()
            return 'break'

    def send_event(self):
        print("Button Clicked")

        self.formattedcontents = self.message_entry.get(1.0, 'end-1c')




class messageBox:
    def __init__(self, uiroot, messageContents, senderIP):
        self.root = uiroot
        self.messageContents = messageContents

        self.contentsFrame = Frame(self.root)
        self.contentsFrame.pack(fill="both", expand=True, padx=5, pady=5, anchor='n')

        self.senderInfo = Frame(self.contentsFrame)
        self.senderInfo.pack(fill="x", expand=True, anchor='n')

        self.senderHostName = Label(self.senderInfo, text=socket.gethostbyaddr(senderIP)[0])
        self.senderHostName.pack(side="left")

        self.senderIP = Label(self.senderInfo, text=f' ({senderIP})', font=('Helvetica', 8, 'bold'))
        self.senderIP.pack(side="left")

        self.timeSent = Label(self.senderInfo, text=f'{datetime.now().strftime("%H:%M:%S")}',
                              font=('Helvetica', 8, 'italic'))
        self.timeSent.pack(side="right", padx=5)

        self.message = Label(self.contentsFrame, wraplength=(self.contentsFrame.winfo_width() - 10),
                             text=messageContents)
        self.message.pack(fill="both", expand=True, padx=5, pady=5, anchor='n')

if __name__ == "__main__":
    print(socket.gethostname())
    peer = Peer(my_ip=socket.gethostbyname(socket.gethostname()), my_port=12345)
