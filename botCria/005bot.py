import json
import logging
from sys import argv, stdout

import requests

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from utils import *
from classes import *


import matplotlib.pyplot as plt
import numpy as np

LINK_URL = "http://localhost:8080"

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
	update.message.reply_text('Implementation command:\nA) /start\nB) /week\nC) /freeday\nD) /plot')
	

def week(update, context):

	_file = open('data01.json')
	data = json.load(_file)

   # print(type(data)) => this is a dictionary
   # print(type(data['week'])) => this is a fucking list!

	for x in data['week']:
		#update.message.reply_text(x)

		if(x['hora'] != None and len(x['hora']) != 0):
				
			
			msg = " ,".join(x['hora'])

			msg2 ="Empresa: " + str(x['emp_name']) + "\nDia: " + str(x['day']) + "\nHorario: " + msg
			update.message.reply_text(msg2)
		
		


	_file.close()


def freeday(update,context):
	_file = open('data01.json')
	data = json.load(_file)

	for x in data['week']:
	
		if(x['hora'] == None or len(x['hora']) == 0):
			msg ="\nDia: " + str(x['day']) + "\nHorario: <VAGO>"
			
			update.message.reply_text(msg)
		
		


	_file.close()


def plot_01(update, context):
		
	height = []

	_file = open('data01.json')
	data = json.load(_file)
	for x in data['week']:
		if(x['hora'] != None):
			height.append(len(x['hora'])*10)
		else:
			height.append(0)

	_file.close()
	
	#print(height)

	bars = ('Mon','Tues','Wed','Thurs','Fri','Sat')
	x_pos = np.arange(len(bars))

	plt.bar(x_pos,height)

	plt.yticks(np.arange(0,110,10))
	
	plt.xticks(x_pos,bars)
	plt.ylabel("%")
	plt.xlabel("Week")
	
	
	plt.savefig('mgraph.png')

	img_filename_new = 'mgraph.png'
	update.message.reply_photo(open(img_filename_new,'rb'))


def createEvento(evento):
	eventJson = evento.createJson()

	# Request do create aqui
	req = requests.post(LINK_URL + "/evento",json=json.loads(eventJson))
	
	print(req.json())

	eventJson = json.loads(req.text)

	# print(eventJson)
	return eventJson["id"]

def create(update, context):
	# /create dias nearly nlater
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

	dp.add_handler(CommandHandler('week', week)) #run:: def week
	dp.add_handler(CommandHandler('freeday', freeday)) #run:: def freeday

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


	

