#!/usr/bin/python

from datai import *
import prompts
import os
import random

class FlashCarder(object):
	def __init__(self):
		self.data = DataInterface()

	def formatAsQuestion(self, phrase):
		if phrase[-1] == 's':
			return "What are " + phrase + "?"
		else:
			return "What is " + phrase + "?"

	def formatAsAnswer(self, phrase, answer):
		if phrase[-1] == 's':
			return phrase.capitalize() + " are " + answer + "."
		else:
			return phrase.capitalize() + " is " + answer + "."

	def formatAsStatement(self, phrase):
		return phrase.capitalize()

	def validateSet(self, setString):
		val = setString.strip()
		try:
			val = int(val)
		except:
			return (False, 0)
		if val in self.data.sets():
			return (True, val)
		else:
			return (False, 0)	

	def retrieveSet(self, phrase):
		while True:
			value = raw_input(phrase)
			result = self.validateSet(value)
			if result[0] == True:
				return self.data.sets()[result[1]]
			else:
				print 'Invalid set'	

	def runSetMenu(self):
		setO = self.retrieveSet("Choose a set to run> ")
		self.runSet(setO)
		 
	def runSet(self, setO):
		print prompts.sPairs['runSet']

		questionDict = {}
		for q in enumerate(setO.listQuestions()):
			questionDict[q[0]] = q[1]['id']
			print '%d) %s' % (q[0], 
				self.formatAsStatement(q[1]['question_phrase']))
		
		while True:
			val = raw_input("Choose a question> ")
			try:
				val = int(val)
			except:
				print 'Invalid choice.'
				continue
			if val in questionDict:
				val = questionDict[val]
				break
		
		members = list(setO.listMembers())
		while True:
			random.shuffle(members)
			for m in members:
				aprompt = {}
				qprompt = []
				for x in m[1]:
					if x['qid'] == val:
						aprompt = x
					else:
						qprompt.append(x)	

				os.system('clear')
				print self.formatAsAnswer(aprompt['question'], 
					aprompt['answer']) + '\n'
				
				for q in qprompt:
					print self.formatAsQuestion(q['question']),
					raw_input()
					print q['answer']
				raw_input()
			if "n" in raw_input("Again? (Y/n)> "):
				return
			os.system('clear')

	def addItemsMenu(self):
		setO = self.retrieveSet("Choose a set to add to> ")
		while True:
			newQuestions = {}
			for q in setO.listQuestions():
				answer = raw_input(
					self.formatAsQuestion(q['question_phrase']) 
					+ "> ")
				newQuestions[q['id']] = answer
			setO.addMember(newQuestions)
			print 'Item added'
			cont = raw_input("Add another? (Y/n)> ")
			if "n" in cont:
				return
			
	def deleteSetMenu(self):
		setO = self.retrieveSet("Choose a set to delete> ")
		cont = raw_input("Warning: This cannot be undone, continue? (Y/n)> ")
		if "n" in cont:
			return
		self.data.deleteSet(setO)	

	def createSetMenu(self):
		value = raw_input("Choose a title for your new set> ")
		print prompts.sPairs['newSetQ']

		questionsToAdd = []
		questionNumber = 1
		while True:
			questionValue = raw_input("Question %d> " % questionNumber).strip()
			if(questionValue != ''):
				questionsToAdd.append(questionValue)
				questionNumber += 1
			else:
				self.data.addSet(value.strip(), questionsToAdd)
				return

	def mainMenu(self):
		os.system('clear')
		while True: 
			print prompts.sPairs['main']
			for sid, s in self.data.sets().items():
				print '%d - %s' % (sid, s.name)
			value = raw_input("Make a selection> ")
			if "1" in value:
				self.runSetMenu()	
				os.system('clear')
			elif "2" in value:
				self.addItemsMenu()
				os.system('clear')
			elif "3" in value:
				self.deleteSetMenu()
				os.system('clear')
			elif "4" in value:
				self.createSetMenu()
				os.system('clear')
			elif "5" in value:
				print 'Good-bye'
				quit()	
			else:
				os.system('clear')
				print 'Invalid menu choice.'

	def run(self):
		print 'FlashCarder Initializing'
		self.mainMenu()

if __name__ == "__main__":
	f = FlashCarder()
	f.run()
