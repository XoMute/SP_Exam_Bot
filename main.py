import telebot;
from telebot import types
from subprocess import call
bot = telebot.TeleBot('838535643:AAFqEVm3RXjszzemWqIBF6bPCfy4Pqjj0Hw')

kb = types.ReplyKeyboardMarkup()
kb.add('USE16','USE32')

usecache = {}

@bot.message_handler(content_types=['text'])
def get_text_messages(message):


    if message.text.startswith('USE'):
        usecache[message.chat.id] = message.text
        print(usecache)
        bot.send_message(message.chat.id,'Send me your asm', reply_markup=kb)
        return

    if message.text == '/start' or not usecache.get(message.chat.id):
        bot.send_message(message.chat.id,'Hi', reply_markup=kb)
        return;

    process_asm(message.chat.id,message.text,usecache[message.chat.id])

    

def process_asm(id,code,use):

    print('processing asm')
    print(code)
    with open('/home/ddone/Code/masm/BOT.ASM','w') as o:
        o.write(''' .386
DATA SEGMENT USE32
a db 1
b dw 2
c dd 3
w dq 4
DATA ENDS
CODE SEGMENT {}
assume cs:code, ds:data
{}
code ends
end
                '''.format(use,code))
    call(''' dosbox -c "TASM.EXE /l BOT.ASM" -c "exit" ''',shell=True)

    with open('/home/ddone/Code/masm/BOT.LST') as i:
        bot.send_message(id,'```{}```'.format(i.read()))





bot.polling(none_stop = True, interval = 0)
