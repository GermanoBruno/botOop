import json
import logging
from sys import argv, stdout

import requests

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from utils import *
from classes import *


import matplotlib.pyplot as plt
import numpy as np
import datetime

LINK_URL = "http://localhost:8080"

#1904764847:AAGXkcxU_DOSh3vhIWr9eHjJVSeO2TMmkRI
#token key from my bot: this will be a token key from the API_bot!


#logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',                       level=logging.INFO)


logger = logging.getLogger(__name__)


def plot_01(update, context):


    user_input = update.message.text.split()[1]

    idEvento = str(user_input)
    req = requests.get(LINK_URL + "/evento/" + idEvento)
    print(req)
    print(req.text)
    data = json.loads(req.text)
    
    # print(data)

    columns = data['dias_da_semana']
    rows = []


    horarioInicial = datetime.datetime(2000,1,1,hour=int(data['nao_antes'].split(":")[0]),minute=int(data['nao_antes'].split(":")[1]))
    horarioFinal = datetime.datetime(2000,1,1,hour=int(data['nao_depois'].split(":")[0]),minute=int(data['nao_depois'].split(":")[1]))

    intervalo = datetime.timedelta(minutes=15)



    while horarioInicial <= horarioFinal:
        rows.append(horarioInicial.strftime("%X"))
        horarioInicial += intervalo
        pass


    dataFrame = {}
    datarow = {}


    

   

    for colum in columns:
        for row in rows:
            datarow[row] = 0
        dataFrame[colum] = datarow
        datarow = {}




    pessoas = data["pessoas"]
    for pessoa in pessoas:
        for diasDisponiveisPessoa in pessoa["horas_disponiveis"]:
            for horaDisponivel in  diasDisponiveisPessoa["horarios"]:
                dataFrame[diasDisponiveisPessoa["dia"]][horaDisponivel] += 1


    
    df2 = []
    df2_row = []



    for dfRow in dataFrame:
        for item in dataFrame[dfRow]:
            df2_row.append(str(dataFrame[dfRow][item]))
        df2.append(df2_row)
        df2_row = []



    numpy_array = np.array(df2)
    transpose = numpy_array.T

    transpose_list = transpose.tolist()

    
    
    fig, ax = plt.subplots(figsize=(8, 8))

    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    

    tab = ax.table(cellText=transpose_list, rowLabels=rows, colLabels=columns, loc='center',cellLoc="center")
    
    colors =  plt.cm.BuPu(np.linspace(0, 0.5, len(pessoas)+1))

    
    for i in range(len(rows)):
        for j in range(len(columns)):
            tab.get_celld()[(i+1,j)].set_color(colors[int(transpose_list[i][j])])
    

    plt.savefig('graph001.png')
    img_filename_new = 'graph001.png'
    update.message.reply_photo(open(img_filename_new,'rb'))
 

    pass





def start(update,context):
	''' /start sentive from the commandHandler
	'''
	
	# /create nome do evento dias nearly nlater
	# /disponivel id_do_evento Dias horarios disp
	# /join id_do_evento

	logMessageReceived(update,context,logger)
	msg = "Bem Vindo ao Agendei\n\n\nPara Criar um evento,digite:\n/create <nome_do_evento> <dias_da_semana> <horario_min> <horario_max>\n\nDigite /help, para mais ajuda!"
	update.message.reply_text(msg,parse_mode='Markdown')
	logMessageSent(update,context,logger,"TXT", msg)
	



def help(update,context):
	'''
		send a commdn /help
	'''
	update.message.reply_text('Did you need some help?')
	update.message.reply_text('Implementation commands:')
	update.message.reply_text('/create <nome_do_evento> <dias_da_semana> <horario_min> <horario_max>')
	update.message.reply_text('/join <id_do_evento>')
	update.message.reply_text('/disponivel <id_do_evento> <dias> <horarios>')
	update.message.reply_text('/plot <id_do_evento>')
	

def createEvento(evento):
	eventJson = evento.createJson()

	# Request do create aqui
	req = requests.post(LINK_URL + "/evento",json=json.loads(eventJson))
	
	print(req.json())

	eventJson = json.loads(req.text)

	# print(eventJson)
	return eventJson["id"]

def create(update, context):
	# /create nome do evento dias nearly nlater
	user_input = update.message.text.split()[1:]

	nlater = str(user_input[-1])
	nearly = str(user_input[-2])

	nome = user_input[0]

	dias = user_input[1:-2]

	update.message.reply_text('Evento de ' + str(dias) + ' das ' + nearly + ' as ' + nlater + ' criado!')
	evento = Event(nome=nome,dias=dias, nantes=nearly, ndepois=nlater,pessoas=[])


	eventId = createEvento(evento)

	update.message.reply_text('Evento criado! Id do evento: ' + eventId)



def join(update, context):
	# /join <id do evento> 

	user_input = update.message.text.split()[1]
	user_name = update.message.from_user['username']
    
	#evento = Event()
	#evento.getFromJson(str(user_input))

	idEvento = str(user_input)
	userJson = json.dumps({"nome":user_name, "horas": []}, indent =4)
	print(idEvento)
	print(userJson)

	req = requests.post(LINK_URL + "/evento/" + idEvento + "/inserePessoa", json=json.loads(userJson))
	print(req)

	#eventJson = evento.createJson()

	update.message.reply_text('Entrou no evento de id: ' + user_input)
	#req = requests.put(LINK_URL + "/evento/" + id, eventJson)
	# updateEvento() com o usuario


def disponivel(update, context):
	# /disponivel DIA horarios

	user_input = update.message.text.split()[1:]
	user_name = update.message.from_user['username']

	idEvento = str(user_input[0])
	dia = str(user_input[1])
	horarios = user_input[2:]
	
	req = requests.get(LINK_URL + "/getPessoa/" + idEvento + "/" + user_name)
	userJson = json.loads(req.text)
	
	if userJson["horas_disponiveis"] == None:
		userJson["horas_disponiveis"] = []
	
	userJson["horas_disponiveis"].append({"dia":dia, "horarios":horarios})


	userJson = json.dumps(userJson, indent =4)

	req = requests.put(LINK_URL + "/evento/" + idEvento + "/updatehorarios/" + user_name,json=json.loads(userJson))
	print(req)
	print(req.text)

	update.message.reply_text("Dia cadastrado")
	

	

def main():
	updater = Updater(token = '1904764847:AAGXkcxU_DOSh3vhIWr9eHjJVSeO2TMmkRI', use_context = True)
	
	dp = updater.dispatcher


	dp.add_handler(CommandHandler('start', start)) #run:: def start
	dp.add_handler(CommandHandler('help', help))   #run:: def help

	dp.add_handler(CommandHandler('create', create)) #run:: def create
	
	dp.add_handler(CommandHandler('join', join)) #run:: def join
	dp.add_handler(CommandHandler('disponivel', disponivel)) #run:: def disponivel

	dp.add_handler(CommandHandler('plot',plot_01))#run :: def plot_01

	updater.start_polling()

	logging.info("=====================BOT version: 0.0.1==============")
	updater.idle()



if __name__ == '__main__':
	
	#print("Let see what is gonna do!!")
 
	logger = logging.getLogger(__name__)
	
	logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
						handlers=[logging.FileHandler("bot.log", "a", "UTF-8"), logging.StreamHandler()])
	main() 


	

