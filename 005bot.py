import logging
from sys import argv, stdout

import json
import requests

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from utils import *


import matplotlib.pyplot as plt
import numpy as np


#1904764847:AAGXkcxU_DOSh3vhIWr9eHjJVSeO2TMmkRI
#token key from my bot: this will be a token key from the API_bot!


#logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',                       level=logging.INFO);


logger = logging.getLogger(__name__);




def start(update,context):
	''' /start sentive from the commandHandler
	'''

	logMessageReceived(update,context,logger);
	msg = "Bem Vindo ao Agend\n\n\nPara Criar um evento,digite:\n/create <empresa> <horario> <dia_da_semana>\n\nDigite /help, para mais ajuda!";
	update.message.reply_text(msg,parse_mode='Markdown');
	logMessageSent(update,context,logger,"TXT", msg);
	



def help(update,context):
	'''
		send a commdn /help
	'''
	update.message.reply_text('Did you need some help?');
	update.message.reply_text('Implementation command:\nA) /start\nB) /week\nC) /freeday\nD) /plot');
	

def week(update, context):

	_file = open('data01.json');
	data = json.load(_file);

   # print(type(data)); => this is a dictionary
   # print(type(data['week'])); => this is a fucking list!

	for x in data['week']:
		#update.message.reply_text(x);

		if(x['hora'] != None and len(x['hora']) != 0):
				
			
			msg = " ,".join(x['hora']);

			msg2 ="Empresa: " + str(x['emp_name']) + "\nDia: " + str(x['day']) + "\nHorario: " + msg;
			update.message.reply_text(msg2);
		
		


	_file.close();


def freeday(update,context):
	_file = open('data01.json');
	data = json.load(_file);

	for x in data['week']:
	
		if(x['hora'] == None or len(x['hora']) == 0):
			msg ="\nDia: " + str(x['day']) + "\nHorario: <VAGO>";
			
			update.message.reply_text(msg);
		
		


	_file.close();


def plot_01(update, context):
		
	height = [];

	_file = open('data01.json');
	data = json.load(_file);
	for x in data['week']:
		if(x['hora'] != None):
			height.append(len(x['hora'])*10);
		else:
			height.append(0);

	_file.close();
	
	#print(height);

	bars = ('Mon','Tues','Wed','Thurs','Fri','Sat');
	x_pos = np.arange(len(bars));

	plt.bar(x_pos,height);

	plt.yticks(np.arange(0,110,10));
	
	plt.xticks(x_pos,bars);
	plt.ylabel("%");
	plt.xlabel("Week");
	
	
	plt.savefig('mgraph.png');

	img_filename_new = 'mgraph.png';
	update.message.reply_photo(open(img_filename_new,'rb'));



def createEvento(dias, nearly, nlater):
	dias = [for dia in dias: dia.upper()]
	nearly = str(nearly) + ':00'
	nlater = str(nlater) + ':00'

	# Request do create aqui
	#requests.get()

def create(update, context):
	# /create dias nearly nlater
	user_input = update.message.text.split()[1:]

	nlater = user_input[-1]
	nearly = user_input[-2]

	dias = user_input[:-2]

	update.message.reply_text('Evento de ' + str(dias) + ' das ' + nearly + ' as ' + nlater + 'criado!')

	createEvento(dias, nearly, nlater)

def join(update, context):
	# /join <id do evento> 

	user_input = update.message.text.split()[1]
	update.message.reply_text('O id do evento é: ' + user_input)
    #jsonEvento = getEvento(user_input)

    # tratar erro

    # Pegar horarios dos dias do evento
    for dia in dias:
    	update.message.reply_text('Horarios da ' + dia)
    	# get horarios do input

	# updateEvento() com a entrada do usuario

	

def main():
	updater = Updater(token = '1904764847:AAGXkcxU_DOSh3vhIWr9eHjJVSeO2TMmkRI', use_context = True);
	
	dp = updater.dispatcher;


	dp.add_handler(CommandHandler('start', start)); #run:: def start
	dp.add_handler(CommandHandler('help', help));   #run:: def help

	dp.add_handler(CommandHandler('week', week)); #run:: def week
	dp.add_handler(CommandHandler('freeday', freeday)); #run:: def freeday

	dp.add_handler(CommandHandler('join', join)); #run:: def join
	dp.add_handler(CommandHandler('create', create)); #run:: def create

	dp.add_handler(CommandHandler('plot',plot_01));#run :: def plot_01

	updater.start_polling()

	logging.info("=====================BOT version: 0.0.1==============");
	updater.idle()



if __name__ == '__main__':
	
	#print("Let see what is gonna do!!");
 
	logger = logging.getLogger(__name__);
	
	logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
						handlers=[logging.FileHandler("bot.log", "a", "UTF-8"), logging.StreamHandler()])
	main(); 


	

