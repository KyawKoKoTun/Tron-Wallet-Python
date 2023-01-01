from tkinter import *
from tkinter import messagebox as msg
from PIL import ImageTk, Image
import qrcode
from tronpy import Tron
from tronpy.keys import PrivateKey
import threading

client = Tron(network='trc-20')

WALLET_ADDRESS = ''
PRIVATE_KEY = ''


def trx(amt):
    return amt*1000000


def load_address(public, private):
    global WALLET_ADDRESS
    global PRIVATE_KEY
    WALLET_ADDRESS = public
    PRIVATE_KEY = private
    print(f'TRX Wallet loaded\npublic key - {WALLET_ADDRESS}\nprivate key - {PRIVATE_KEY}')
    print(f'Balance: f{account_balance(WALLET_ADDRESS)}')


def send_tron(amount, wallet):
    global WALLET_ADDRESS
    global PRIVATE_KEY
    try:
        priv_key = PrivateKey(bytes.fromhex(PRIVATE_KEY))
        txn = (
            client.trx.transfer(WALLET_ADDRESS, str(wallet), int(trx(amount)))
                .memo("Transaction Description")
                .build()
                .inspect()
                .sign(priv_key)
                .broadcast()
        )
        return txn.wait()
    except Exception as ex:
        return ex


def account_balance(address):
    balance = client.get_account_balance(str(address))
    return balance


def transation_detail(transaction_hash):
    info = client.get_transaction(str(transaction_hash))['raw_data']['contract'][0]['parameter']['value']
    return info


public = "" #public address
private = "" #private address
load_address(public, private)


def update():
    balance.configure(text=str(account_balance(WALLET_ADDRESS))+' trx')
    app.after(5000, update)


def send():
    threading.Thread(target=send1).start()
    msg.Message(title='Processing', message='Your request is processing\n if successful, your balance will be update shortly ').show()


def send1():
    am = amt.get().strip()
    ad = addr.get().strip()
    msg.Message(title='Send', message=send_tron(float(am), ad)).show()


img = qrcode.make(public)
img.save("qr.png")
app = Tk()
app.configure(bg='#111111')
app.wm_geometry('300x600')
app.wm_title('Tron wallet (by Kyaw Ko Ko Tun)')
frame = Frame(app, width=130, height=100, bg='#111111')
frame.pack()
img = Image.open("tron.png")
img = ImageTk.PhotoImage(img.resize((130, 100), Image.ANTIALIAS))
Label(frame, image=img).pack()
Label(app, text='Balance', fg='white', bg='#111111', font=('ariel', 25)).pack()
balance = Label(app, text=str(account_balance(WALLET_ADDRESS))+' trx', fg='red', bg='#111111', font=('ariel', 20))
balance.pack()
Label(app, text='Receive Tron', fg='yellow', bg='#111111', font=('ariel', 20)).pack()
Label(app, text=public, fg='red', bg='#111111', font=('ariel', 10)).pack()
img1 = Image.open("qr.png")
img1 = ImageTk.PhotoImage(img1.resize((100, 100), Image.ANTIALIAS))
Label(app, image=img1).pack()
Label(app, text='Send TRON (Fee will be charged)', fg='yellow', bg='#111111', font=('ariel', 14)).pack()
Label(app, text='Amount', fg='red', bg='#111111', font=('ariel', 15)).pack()
amt = Entry(app, width=180)
amt.pack()
Label(app, text='Address', fg='red', bg='#111111', font=('ariel', 15)).pack()
addr = Entry(app, width=180)
addr.pack()
Button(app, text='Send', bg='green', font=('ariel', 20), command=send).pack()
app.after(2000, update)
if __name__ == '__main__':
    app.mainloop()
