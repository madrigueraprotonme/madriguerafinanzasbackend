from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal,engine,Base,Usuario,Cartera,Profile
from pydantic import BaseModel
from datetime import date
from dotenv import load_dotenv
import stripe
import os

app = FastAPI()

Base.metadata.create_all(bind=engine)


    
#creacion de una instancia a las tablas
class ProfileCreate(BaseModel):
    usuario_profile:str
    edad:int
    riesgo_global_profile:int
    riesgo_operacion_profile:int
    capital_inicial_profile:int 

class UsuarioCreate(BaseModel):
    nombre:str
    edad:int
    
class CarteraCreate(BaseModel):
    nombre_accion:str
    fecha_compra:date
    capital:int
    riesgo_operacion:int
    precio_compra:float
    precio_venta:float
    acciones_comprar:float
    inversion:float 
    liquidacion:float
    usuario_id:str

#creamos backend para stripe
load_dotenv()
STRIPE_SECRET_KEY=os.getenv("STRIPE_SECRET_KEY")
stripe.api_key=STRIPE_SECRET_KEY

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/crear-pago")
async def crear_pago():
    sesssion=stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": "Kid Finanzas",
                        "images": ["https://i.imgur.com/5e8y4lI.png"],
                    },
                    "unit_amount":33900,
                
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
    )
    return {'url': sesssion.url}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
 
#actualizamos el perfil del usuario
@app.put("/profile/{usuario_profile}")
def actualizar_profile(profile:ProfileCreate,db:Session=Depends(get_db)):
    profile_success=db.query(Profile).filter(Profile.usuario_profile==profile.usuario_profile).first()
    if not profile_success:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    #actualizamos campos
    profile_success.usuario_profile=profile.usuario_profile
    profile_success.edad=profile.edad
    profile_success.riesgo_global_profile=profile.riesgo_global_profile   
    profile_success.riesgo_operacion_profile=profile.riesgo_operacion_profile            
    profile_success.capital_inicial_profile=profile.capital_inicial_profile
    #confrimaos cambios bd
    db.commit()
    db.refresh(profile_success)
    return {"mensaje":"actualizado"}


        
#sacamos el perfil del usuuario
@app.get("/profile/{usuario_profile}")
def obtener_profile(usuario_profile:str,db:Session=Depends(get_db)):
    profile=db.query(Profile).filter(Profile.usuario_profile==usuario_profile).all()
    return profile


#creamos un nuevo perfil    
@app.post("/profile/")
def crear_profile(profile:ProfileCreate,db:Session=Depends(get_db)):
    nuevo_profile=Profile(
        usuario_profile=profile.usuario_profile,
        edad=profile.edad,
        riesgo_global_profile=profile.riesgo_global_profile,
        riesgo_operacion_profile=profile.riesgo_operacion_profile,
        capital_inicial_profile=profile.capital_inicial_profile
    )
    db.add(nuevo_profile)
    db.commit()

#borramos una accin en base a la seleccion id
@app.delete("/usuarios/cartera/{id}")
def eliminar_cartera(id:int,db:Session=Depends(get_db)):
    db.query(Cartera).filter(Cartera.id==id).delete()
    db.commit()
    db.refresh(Cartera)
    return Cartera


#obtenenemo las acciones creadas por un usuario
@app.get("/usuarios/{usuario_id}/cartera/")
def obtener_carteras_por_usuario(usuario_id: str, db: Session = Depends(get_db)):
    carteras = db.query(Cartera).filter(Cartera.usuario_id == usuario_id).all()
    return carteras


#obtenenmos todas las acciones creadas
@app.get("/usuarios/cartera/")
def listar_cartera(db:Session=Depends(get_db)):
    return db.query(Cartera).all()


#creamos una nueva accion
@app.post("/usuarios/cartera/")
def crear_cartera(cartera:CarteraCreate,db:Session=Depends(get_db)):
    nueva_cartera=Cartera(
        nombre_accion=cartera.nombre_accion,
        fecha_compra=cartera.fecha_compra,
        capital=cartera.capital,
        riesgo_operacion=cartera.riesgo_operacion,
        precio_compra=cartera.precio_compra,
        precio_venta=cartera.precio_venta,
       
        acciones_comprar=cartera.acciones_comprar,
        inversion=cartera.inversion,
        liquidacion=cartera.liquidacion,
        usuario_id=cartera.usuario_id
    )
    db.add(nueva_cartera)
    db.commit()
    db.refresh(nueva_cartera)
    return nueva_cartera

    
    
#creamos un nuevo usuaurio    
@app.post("/usuarios/")
def crear_usuario(usuario:UsuarioCreate,db:Session=Depends(get_db)):
    nuevo_usuario=Usuario(nombre=usuario.nombre,edad=usuario.edad)#instancia de la tabla Usuario
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario
#sacamos la tabla de usuaruios
@app.get("/usuarios/")
def listar_usuarios(db:Session=Depends(get_db)):
    return db.query(Usuario).all()

