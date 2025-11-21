from sqlalchemy import create_engine, Column, Integer, String,Date,ForeignKey,Text,Boolean,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
# creamos conexion y tabla

SQLALCHEMY_DATABASE_URL = "sqlite:///database.db"

engine=create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()

class Usuario(Base):#convierte la clase en un tabla
    #nombre de la tabla
    __tablename__="usuarios"
    
    id=Column(Integer,primary_key=True,index=True) #columna de tipo entero
    nombre=Column(String(50),index=True)
    edad=Column(Integer)
    
    #relacion con cartera
    cartera=relationship("Cartera",back_populates="usuario",uselist=False)
class Cartera(Base):
    __tablename__="carteras"
    id=Column(Integer,primary_key=True, index=True)
    nombre_accion=Column(String(50))
    fecha_compra=Column(Date)
    capital=Column(Integer)
    riesgo_operacion=Column(Integer)
    precio_compra=Column(Float)
    precio_venta=Column(Float)
    acciones_comprar=Column(Float)
    inversion=Column(Float)
    liquidacion=Column(Float)   
    
    #relacion con usuario
    usuario_id=Column(Integer,ForeignKey("usuarios.id"), unique=False)
    
    usuario=relationship("Usuario",back_populates="cartera")


class Profile(Base):
    __tablename__="profiles"
    id=Column(Integer,primary_key=True,index=True)
    usuario_profile=Column(String(50))
    edad=Column(Integer)
    riesgo_global_profile=Column(Integer)
    riesgo_operacion_profile=Column(Integer)
    capital_inicial_profile=Column(Integer)
    #relacion con usuario