#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
PostgreSQL database tables
"""

from sqlalchemy.orm import relationship, exc, column_property
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.query import Query as _Query
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, UniqueConstraint

Base = declarative_base()
Session = None


class Query(_Query):
    def values(self):
        try:
            return [i for (i,) in self]
        except ValueError as e:
            raise MultipleValuesFound(str(e))


class MultipleValuesFound(ValueError, exc.MultipleResultsFound):
    """
    raised when multiple values are found in a single result row
    """


class Employee(Base):
    __tablename__   = 'employee'	
    employee_id     = Column(Integer, primary_key=True)
    surname 		= Column(String, nullable=False)
    name 			= Column(String, nullable=False)
    patronymic 		= Column(String)
    fullname        = column_property(surname + ' ' + name + ' ' + patronymic)
    email 			= Column(String)
    unique_login 	= Column(String, unique=True, nullable=False)
    position_id 	= Column(Integer, ForeignKey('position.position_id'))
    shared_folder 	= Column(Boolean)
    network_printer = Column(Boolean)
    department_id 	= Column(Integer, ForeignKey('department.department_id'))
    room_id 		= Column(Integer, ForeignKey('room.room_id'))
    comments 		= Column(String)
    pc 			    = relationship('Pc', secondary='association', back_populates='employee')
    position 	    = relationship('Position', back_populates='employee')
    department      = relationship('Department', back_populates='employee')
    room 		    = relationship('Room', back_populates='employee')
    phone 		    = relationship('Phone', back_populates='employee', cascade='all, delete-orphan', passive_deletes=True)
    email           = relationship('Email', back_populates='employee', cascade='all, delete-orphan', passive_deletes=True)


class Position(Base):
	__tablename__   = 'position'	
	position_id     = Column(Integer, primary_key=True)
	name 		    = Column(String, unique=True, nullable=False)	
	employee        = relationship('Employee', back_populates='position')


class Department(Base):
	__tablename__   = 'department'	
	department_id 	= Column(Integer, primary_key=True)
	name 			= Column(String, unique=True, nullable=False)	
	employee        = relationship('Employee', back_populates='department')


class Phone(Base):
    __tablename__   = 'phone'
    phone_id        = Column(Integer, primary_key=True)
    employee_id     = Column(Integer, ForeignKey('employee.employee_id', ondelete = 'CASCADE'))
    number          = Column(String, unique=True, nullable=False)
    employee        = relationship('Employee', back_populates='phone')


class Email(Base):
    __tablename__   = 'email'
    email_id        = Column(Integer, primary_key=True)
    employee_id     = Column(Integer, ForeignKey('employee.employee_id', ondelete = 'CASCADE'))
    email           = Column(String, unique=True, nullable=False)
    employee        = relationship('Employee', back_populates='email')


class Room(Base):
    __tablename__   = 'room'
    __table_args__  = (UniqueConstraint('name', 'block_id', name='uix_name_block_id'),)
    room_id         = Column(Integer, primary_key=True)
    name	        = Column(String, nullable=False)
    block_id        = Column(Integer, ForeignKey('block.block_id', ondelete='CASCADE'))
    employee        = relationship('Employee', back_populates='room')
    block           = relationship('Block', back_populates='room')


class Block(Base):
    __tablename__   = 'block'
    __table_args__  = (UniqueConstraint('name', 'address_id', name='uix_name_address_id'),)
    block_id        = Column(Integer, primary_key=True)
    name 	        = Column(String, nullable=False)
    address_id      = Column(Integer, ForeignKey('address.address_id', ondelete='CASCADE'))
    room 	        = relationship('Room', back_populates='block', cascade='all, delete-orphan', passive_deletes=True)
    address         = relationship('Address', back_populates='block')


class Address(Base):
    __tablename__   = 'address'
    address_id 	    = Column(Integer, primary_key=True)
    name 		    = Column(String, unique=True, nullable=False)
    block           = relationship('Block', back_populates='address', cascade='all, delete-orphan', passive_deletes=True)

association_table = Table('association', Base.metadata,
	Column('employee_id', Integer, ForeignKey('employee.employee_id')),
	Column('pc_id', Integer, ForeignKey('pc.pc_id'))
    )


class Pc(Base):
    __tablename__   = 'pc'
    pc_id           = Column(Integer, ForeignKey("pcname.pc_id"), primary_key=True)
    mac_address     = Column(String, unique=True, nullable=False)
    power_socket_id = Column(Integer, ForeignKey('powersocket.power_socket_id'))
    con_type_id     = Column(Integer, ForeignKey('connectiontype.con_type_id'))
    app_server      = Column(String)
    windows_id      = Column(Integer, ForeignKey('windows.windows_id'))
    windows_os_key  = Column(String)
    office_id       = Column(Integer, ForeignKey('office.office_id'))
    ms_office_key   = Column(String)
    kes             = Column(Boolean)
    antivirus_id    = Column(Integer, ForeignKey('antivirus.antivirus_id'))
    consultant      = Column(Boolean)
    guarantee       = Column(Boolean)
    odin_s          = Column(Boolean)
    kdc             = Column(Boolean)
    mail_client     = Column(String)
    comments        = Column(String)
    employee        = relationship('Employee', secondary=association_table, back_populates='pc')
    connectiontype  = relationship('ConnectionType', back_populates='pc')
    pcname          = relationship('PcName', back_populates='pc')
    powersocket     = relationship('PowerSocket', back_populates='pc')
    windows         = relationship('Windows', back_populates='pc')
    office          = relationship('Office', back_populates='pc')
    antivirus       = relationship('Antivirus', back_populates='pc') 


class PcName(Base):
    __tablename__   = 'pcname'
    __table_args__  = (UniqueConstraint('name', 'domain_id', name='uix_name_domain_id'),)
    pc_id           = Column(Integer, primary_key=True)
    name            = Column(String, nullable=False)
    domain_id       = Column(Integer, ForeignKey('domain.domain_id'))
    pc              = relationship('Pc', back_populates='pcname')
    domain          = relationship('Domain', back_populates='pcname')


class Domain(Base):
    __tablename__   = 'domain'
    domain_id       = Column(Integer, primary_key=True)
    name            = Column(String, unique=True, nullable=False)
    pcname          = relationship('PcName', back_populates='domain')


class ConnectionType(Base):
    __tablename__   = 'connectiontype'
    con_type_id     = Column(Integer, primary_key=True)
    name            = Column(String, unique=True, nullable=False)
    pc              = relationship('Pc', back_populates='connectiontype')


class PowerSocket(Base):
    __tablename__   = 'powersocket'
    power_socket_id = Column(Integer, primary_key=True)
    name            = Column(String, unique=True, nullable=False)
    pc              = relationship('Pc', back_populates='powersocket')


class Windows(Base):
    __tablename__   = 'windows'
    windows_id      = Column(Integer, primary_key=True)
    name            = Column(String, unique=True, nullable=False)
    pc              = relationship('Pc', back_populates='windows')


class Office(Base):
    __tablename__   = 'office'
    office_id       = Column(Integer, primary_key=True)
    name            = Column(String, unique=True, nullable=False)
    pc              = relationship('Pc', back_populates='office')


class Antivirus(Base):
    __tablename__   = 'antivirus'
    antivirus_id    = Column(Integer, primary_key=True)
    name            = Column(String, unique=True, nullable=False)
    pc              = relationship('Pc', back_populates='antivirus')
