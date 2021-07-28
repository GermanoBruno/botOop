import logging
from sys import argv, stdout

import json
import requests

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from utils import *


import matplotlib.pyplot as plt
import numpy as np
import datetime

#1904764847:AAGXkcxU_DOSh3vhIWr9eHjJVSeO2TMmkRI
#token key from my bot: this will be a token key from the API_bot!


#logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',                       level=logging.INFO)


logger = logging.getLogger(__name__)




def start(update,context):
    ''' /start sentive from the commandHandler
    '''

    logMessageReceived(update,context,logger)
    msg = "Bem Vindo ao Agend\n\n\nPara Criar um evento,digite:\n/create <empresa> <horario> <dia_da_semana>\n\nDigite /help, para mais ajuda!"
    update.message.reply_text(msg,parse_mode='Markdown')
    logMessageSent(update,context,logger,"TXT", msg)
    



def help(update,context):
    '''
        send a commdn /help
    '''
    update.message.reply_text('Did you need some help?')
    update.message.reply_text('Implementation command:\nA) /start\nB) /week\nC)/plot')
    

def week(update, context):
    _file = open('data02.json')

    data = json.load(_file)

    print(data['id'])
    print(data['nome'])
    print(data['dias_da_semana'])
    print(data['nao_antes'])
    print(data['nao_depois'])

    msg = "Reuniao "+str(data['nome'])
    
    update.message.reply_text(msg)

    for x in data['pessoas']:
        msg2 = "Integrante: " +str(x['nome'])
        update.message.reply_text(msg2)

        for z in x['horas_disponiveis']:
            msg3 = z['dia']
            msg4 = " ,".join(z['horarios'])
            endmsg = str(msg3) +",  Horarios: " + msg4 
            update.message.reply_text(endmsg)


    _file.close()


def float_date(str_line):

    a = int(str_line[0:2])
    b = int(str_line[3:5])

    return a + float(b/100)


def match(diaP,horarioP,diaT,horarioT):
    if diaP == diaT and horarioP == horarioT:
        return True
    else:
        return False





def plot_table_nosso(update, context):


    _file = open("data02.json")
    data = json.load(_file)
    
    # print(data)

    columns = data['dias_da_semana']
    rows = []



    horarioInicial = datetime.datetime(2000,1,1,hour=int(data['nao_antes'].split(":")[0]),minute=int(data['nao_antes'].split(":")[1]))
    horarioFinal = datetime.datetime(2000,1,1,hour=int(data['nao_depois'].split(":")[0]),minute=int(data['nao_depois'].split(":")[1]))

    intervalo = datetime.timedelta(minutes=15)
    
    # print(horarioInicial)


    while horarioInicial <= horarioFinal:
        rows.append(horarioInicial.strftime("%X"))
        horarioInicial += intervalo
        pass

    # print(rows)


    dataFrame = {}
    datarow = {}


    pessoas = data["pessoas"]

   
    for row in rows:
        for colum in columns:
            datarow[row] = 0
        dataFrame[colum] = datarow
        datarow = {}

    print(dataFrame)

    for pessoa in pessoas:
        for diasDisponiveisPessoa in pessoa["horas_dosponiveis"]:
            for horaDisponivel in  diasDisponiveisPessoa["horarios"]:
                dataFrame[diasDisponiveisPessoa["dia"]][horaDisponivel] += 1

    print(dataFrame)

    
    df2 = []
    df2_row = []



    for dfRow in dataFrame:
        for item in dataFrame[dfRow]:
            df2_row.append(str(dataFrame[dfRow][item]))
        df2.append(df2_row)
        df2_row = []

    print(df2)

    
    
    
    # fig, ax = plt.subplots(figsize=(8, 8))

    # # hide axes
    # fig.patch.set_visible(False)
    # ax.axis('off')
    

    # tab = ax.table(cellText=df2, rowLabels=rows, colLabels=columns, loc='center',cellLoc="center")
    # tab.get_celld()[(1,1)].set_color("#56b5fd")
    # # [t.auto_set_font_size(False) for t in tab]
    # # tab.auto_set_column_width(col=)
    
    
    # # fig.tight_layout()

    # plt.savefig('graph001.png')
    _file.close()
 

    pass



def plot_under(update, context):
    
    _file = open("data02.json")
    data = json.load(_file)
    
    columns = ('SEG', 'TER', 'QUA', 'QUI', 'SEX','SAB','')
    rows = [x['nome'] for x in data['pessoas']]


    values = np.arange(8,18,0.30)



    colors = plt.cm.BuPu(np.linspace(0,0.5,len(rows)))

    index = np.arange(len(columns))
    bar_width = 0.4
    
    y_offset = np.zeros(len(columns))

    print(columns)
    print(rows)
    print(values)
    x = 0
    for row1 in data['pessoas']:
        print(x)

        for row2 in row1['horas_disponiveis']:
        
            #print(y_offset)
            #k = row2['horarios']
            #print(float_date(k[0]))
            #y_offset[x] = y_offset[x] + float_date(k[0])

            
            if(row2['dia'] == 'SEG'):
                plt.bar(0,row2['horarios'],bar_width,bottom=y_offset,color= colors[x])
                k = row2['horarios']
                y_offset[x] = y_offset[x] + float_date(k[0])
        
            if(row2['dia'] == 'TER'):
                plt.bar(1,row2['horarios'],bar_width,bottom=y_offset,color= colors[x])
                k = row2['horarios']
                y_offset[x] = y_offset[x] + float_date(k[0])

            if(row2['dia'] == 'QUA'):
                plt.bar(2,row2['horarios'],bar_width,bottom=y_offset,color= colors[x])
                k = row2['horarios']
                y_offset[x] = y_offset[x] + float_date(k[0])

            if(row2['dia'] == 'QUI'):
                plt.bar(4,row2['horarios'],bar_width,bottom=y_offset,color= colors[x])
                k = row2['horarios']
                y_offset[x] = y_offset[x] + float_date(k[0])

        
            if(row2['dia'] == 'SEX'):
                plt.bar(5,row2['horarios'],bar_width,bottom=y_offset,color= colors[x])
                k = row2['horarios']
                y_offset[x] = y_offset[x] + float_date(k[0])
 
            if(row2['dia'] == 'SAB'):
                plt.bar(6,row2['horarios'],bar_width,bottom=y_offset,color= colors[x])
                k = row2['horarios']
                y_offset[x] = y_offset[x] + float_date(k[0])

 
            x +=1

    
    plt.yticks([val for val in values])
    plt.xticks(index,columns)           
    plt.savefig('graph001.png')
    _file.close()







def main():
    updater = Updater(token = '1904764847:AAGXkcxU_DOSh3vhIWr9eHjJVSeO2TMmkRI', use_context = True)
    
    dp = updater.dispatcher


    dp.add_handler(CommandHandler('start', start)) #run:: def start
    dp.add_handler(CommandHandler('help', help))   #run:: def help
    dp.add_handler(CommandHandler('week', week)) #run:: def week
    dp.add_handler(CommandHandler('plot',plot_table_nosso))#run :: def plot_01

    updater.start_polling()

    logging.info("=====================BOT version: 0.0.1==============")
    updater.idle()



if __name__ == '__main__':
    
    #print("Let see what is gonna do!!")
 
    logger = logging.getLogger(__name__)
    
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
                        handlers=[logging.FileHandler("bot.log", "a", "UTF-8"), logging.StreamHandler()])
    main() 


    

