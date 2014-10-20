from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class Result(Base):
        __tablename__ = 'results'
		
        data = Column(String(150), primary_key=True)
        source = Column(String(150), primary_key=True)
        type = Column(String(100), ForeignKey("result_types.id"), primary_key=True)
		
        def __init__(self, data, source, type):	
			self.data = data
			self.source = source
			self.type = type

class ResultType(Base):
	__tablename__ = 'result_types'
	id = Column(Integer, primary_key=True)
	rtype = Column(String(15))
	
	def __init__(self, id, rtype):
		self.id = id
		self.rtype = rtype
		

def save_result(session, data, source, type):
	db_type = session.query(ResultType).filter_by(rtype=type).first()
	result = Result(data, source, db_type.id)
	try:
		session.add(result)
		session.commit()
	except IntegrityError:
		session.rollback()