#!/usr/bin/python

import sqlite3

class DataInterfaceSet(object):
	def __init__(self, conn, sid, name):
		self._conn = conn
		self._sid = sid
		self.name = name 

	def addQuestion(self, question, existingMemberAnswers = {}):
		c = self._conn.cursor()
		c.execute("""INSERT INTO set_questions 
			(set_id, question_phrase) VALUES (?, ?)""",
			(self._sid, question))
		self._conn.commit()
		newQuestionId = c.lastrowid

		with self._conn as c:
			for key, value in existingMemberAnswers.items():
					c.execute("""INSERT INTO set_member_questions 
						(set_id, member_id, question_id, answer) 
						VALUES (?, ?, ?, ?)""",
						(self._sid, key, newQuestionId, value)) 

	def addMember(self, questionAnswers):
		c = self._conn.cursor()
		c.execute("""INSERT INTO set_members (set_id) VALUES (?)""",
			(self._sid, ))
		self._conn.commit()
		newMemberId = c.lastrowid

		with self._conn as c:
			for key,value in questionAnswers.items():
				c.execute("""INSERT INTO set_member_questions 
					(set_id, member_id, question_id, answer) 
					VALUES (?, ?, ?, ?)""",
					(self._sid, newMemberId, key, value)) 

	def deleteQuestion(self, question):
		with self._conn as c:
			c.execute("""DELETE FROM set_member_questions WHERE
				question_id = ?""", (question['id'], ))
			c.execute("""DELETE FROM set_questions WHERE
				id = ?""", (question['id'],))

	def deleteMember(self, member):
		with self._conn as c:
			c.execute("""DELETE FROM set_member_questions WHERE
				member_id = ?""", (member['id'], ))
			c.execute("""DELETE FROM set_members WHERE
				id = ?""", (memeber['id'], ))

	def listQuestions(self):
		c = self._conn.cursor()
		c.execute("""SELECT id, question_phrase FROM 
			set_questions WHERE set_id = ?""", (self._sid, ))
		return c.fetchall()

	def listMembers(self):
		c = self._conn.cursor()
		c.execute('SELECT id FROM set_members WHERE set_id = ?',
			(self._sid, )) 
		for r in c:
			cRow = self._conn.cursor()
			cRow.execute("""SELECT set_member_questions.answer as answer, 
				set_questions.question_phrase as question, set_questions.id 
				as qid FROM set_member_questions, set_questions 
				WHERE set_member_questions.question_id = 
				set_questions.id 
				AND set_member_questions.member_id = ?""", (r['id'], ))
			yield (r['id'], cRow.fetchall())

class DataInterface(object):
	def __init__(self):
		self._conn = sqlite3.connect("faceMaker.db")
		
		# This allows us to access rows by thier name
		self._conn.row_factory = sqlite3.Row
		# And ensure we are using ASCII representation, no need for UTF here
		self._conn.text_factory = str
		
		# Cache availiable sets internally
		self._setCache = {}
		self._setCacheIsValid = False

		try:
			self.initDatabase()
		except Exception:
			print 'Something has gone wrong initializing the database'
			quit()

	def initDatabase(self):
		c = self._conn.cursor()
		with open('database.sql', 'r') as f:
			buildUpQuery = f.read()
		# Create tables if they don't already exist	
		c.executescript(buildUpQuery)

	def sets(self):
		if not self._setCacheIsValid:
			c = self._conn.cursor()
			c.execute("SELECT * FROM sets")
			iterSets = [row for row in c if 
				(lambda a: a['id'] not in self_setCache)] 
			for row in iterSets:
				self._setCache[row['id']] = DataInterfaceSet(self._conn,
					row['id'], row['name'])
		return self._setCache

	def addSet(self, setTitle, setQuestions):
		c = self._conn.cursor()	
		c.execute('INSERT INTO sets (name) VALUES (?)', (setTitle,))
		newSetId = c.lastrowid
		self._conn.commit()

		with self._conn as c:
			for q in setQuestions:
				c.execute("""INSERT INTO set_questions 
					(set_id, question_phrase) VALUES (?, ?)"""
					, (newSetId, q))

		self._setCache[newSetId] = DataInterfaceSet(self._conn, 
			newSetId, setTitle)
		return self._setCache[newSetId]

	def deleteSet(self, setO):
		with self._conn as c:
			c.execute('DELETE FROM set_members WHERE set_id = ?'
				, (setO._sid,))
			c.execute('DELETE FROM set_questions WHERE set_id = ?'
				, (setO._sid, ))
			c.execute('DELETE FROM sets WHERE id = ?', (setO._sid, ))
		del self._setCache[setO._sid]
