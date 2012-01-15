PRAGMA foreign_keys = ON;

-- Since we're prototyping, let's drop the tables
-- if they already exist.

--DROP TABLE IF EXISTS set_member_questions;
--DROP TABLE IF EXISTS set_questions;
--DROP TABLE IF EXISTS set_members;
--DROP TABLE IF EXISTS sets;

CREATE TABLE IF NOT EXISTS sets(
	id INTEGER PRIMARY KEY,
	name CHAR(255));

CREATE TABLE IF NOT EXISTS set_questions(
	id INTEGER PRIMARY KEY,
	set_id INTEGER NOT NULL,
	question_phrase TEXT,
	FOREIGN KEY(set_id) REFERENCES sets(id));

CREATE TABLE IF NOT EXISTS set_members(
	id INTEGER PRIMARY KEY,
	set_id INTEGER NOT NULL,
	FOREIGN KEY(set_id) REFERENCES sets(id));

CREATE TABLE IF NOT EXISTS set_member_questions(
	id INTEGER PRIMARY KEY,
	set_id INTEGER NOT NULL,
	question_id INTEGER NOT NULL,
	member_id INTEGER NOT NULL,
	answer TEXT,
	FOREIGN KEY(member_id) REFERENCES set_members(id)
	FOREIGN KEY(question_id) REFERENCES set_questions(id),
	FOREIGN KEY(set_id) REFERENCES sets(id));
