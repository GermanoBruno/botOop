import requests
import json

LINK_URL = "http://localhost:8080"

class Event():
	def __init__(self, eventId='', nome='', dias=[], nantes='', ndepois='', pessoas={}):
		self.eventId = eventId
		self.nome = nome
		self.dias = dias
		self.nantes = nantes
		self.ndepois = ndepois
		self.pessoas = pessoas


	def set(self, eventId, nome, dias, nantes, ndepois, pessoas):
		self.eventId = eventId
		self.nome = nome
		self.dias = dias
		self.nantes = nantes
		self.ndepois = ndepois
		self.pessoas = pessoas

	def getFromJson(self, id):
		req = requests.get(LINK_URL + "/evento/" + id)

		if req.status_code == 200:
			# pega o json
			eventJson = json.loads(req.text)
		else:
			# evento não existente
			return None


		self.set(
			eventJson["id"], 
			eventJson["nome"], 
			eventJson["dias_da_semana"],
			eventJson["nao_antes"],
			eventJson["nao_depois"],
			eventJson["pessoas"]
			)

	def createJson(self):
		eventDict = {
			"id":  self.eventId,
			"nome": self.nome,
			"dias_da_semana": self.dias,
			"nao_antes": self.nantes,
			"nao_depois": self.ndepois,
			"pessoas": self.pessoas
		}

		eventJson = json.dumps(eventDict, indent=4)

		return eventJson

	def addPessoa(self, pessoa):
		self.pessoas.append(pessoa)

class Pessoa():
	def __init__(self, nome='', horas=[]):
		self.nome = nome
		self.horas = horas

	def set(self, nome, horas):
		self.nome = nome
		self.horas = horas

	def addDisponivel(self, disponivel):
		self.horas.append(disponivel)

	def __str__(self):
		return str({"nome":self.nome, "horas_disponiveis":self.horas})


class HorasDisponiveis():
	def __init__(self, dia='', horarios=[]):
		self.dia = dia
		self.horarios = horarios

	def set(self, dia, horarios):
		self.dia = dia
		self.horarios = horarios


print(Pessoa("rubens", ["13:00:00", "14:00:00"]))