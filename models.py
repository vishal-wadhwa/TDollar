from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

from app import db

SQLALCHEMY_TRACK_MODIFICATIONS = False
class users(db.Model):
	__tablename__ = 'user'
	name = db.Column(db.String(255), primary_key = True)
	holding = db.Column(db.Integer(), default = 0, nullable = False)
	stage = db.Column(db.Integer(), default = 0 )

	# 0 Before Start 
	# 1 Given 'bid' command 
	# 2 Selected Type 
	# 3 Selected Slot 
	# 4 Amount Given 
	# -> leave 
	def __str__(self):
		return str(self.name)
	def __repr__(self):
		return str(self.name)

class bidInfo(db.Model):
	__tablename__ = 'infoBid'
	id = db.Column(db.Integer(), primary_key = True)
	name = db.Column(db.Integer(), nullable = False)
	slot_id = db.Column(db.Integer(), nullable = False)

class slots(db.Model):
	__tablename__ = 'slotsInfo'
	slot_id = db.Column(db.Integer(), primary_key = True)
	start_time = db.Column(db.DateTime)
	slot_type = db.Column(db.String(255))
	duration = db.Column(db.Integer(), default = 20)
	highestBid = db.Column(db.Integer(), default =0)
	highestBidder = db.Column(db.String(255))
