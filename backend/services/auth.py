from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from config.supabase_client import supabase
from fastapi import HTTPException, status

SECRET_KEY = "libreria-el-estudiante-secret-key-2025"  # Cambiar en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 horas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_password(password_plano: str, password_hash: str) -> bool:
    return pwd_context.verify(password_plano, password_hash)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def crear_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def autenticar_usuario(nombre: str, password: str):
    user = supabase.table("usuarios") \
                 .select("*") \
                 .eq("nombre", nombre) \
                 .single().execute().data
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    if not verificar_password(password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    token = crear_token({"sub": user["nombre"], "rol": user["rol"]})
    return {"token": token, "rol": user["rol"], "nombre": user["nombre"]}

def listar_usuarios():
    users = supabase.table("usuarios") \
                   .select("id, nombre, rol") \
                   .order("id") \
                   .execute().data
    return users

def crear_usuario(nombre: str, password: str, rol: str):
    # Verificar si ya existe
    existe = supabase.table("usuarios") \
                    .select("id") \
                    .eq("nombre", nombre) \
                    .execute().data
    if existe:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
    password_hash = get_password_hash(password)
    data = {"nombre": nombre, "password_hash": password_hash, "rol": rol}
    supabase.table("usuarios").insert(data).execute()
    return {"mensaje": "Usuario creado exitosamente"}

def eliminar_usuario(user_id: int):
    supabase.table("usuarios") \
           .delete() \
           .eq("id", user_id) \
           .execute()
    return {"mensaje": "Usuario eliminado"}