from config.supabase_client import supabase
from fastapi import HTTPException

def autenticar_usuario(nombre: str, password: str):
    user = supabase.table("usuarios") \
                 .select("*") \
                 .eq("nombre", nombre) \
                 .single().execute().data
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    if user["password"] != password:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    # Token falso (no se usa JWT realmente, solo para mantener compatibilidad con frontend)
    return {"token": "fake-token", "rol": user["rol"], "nombre": user["nombre"]}

def listar_usuarios():
    users = supabase.table("usuarios") \
                   .select("id, nombre, rol") \
                   .order("id") \
                   .execute().data
    return users

def crear_usuario(nombre: str, password: str, rol: str):
    existe = supabase.table("usuarios") \
                    .select("id") \
                    .eq("nombre", nombre) \
                    .execute().data
    if existe:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
    data = {"nombre": nombre, "password": password, "rol": rol}
    supabase.table("usuarios").insert(data).execute()
    return {"mensaje": "Usuario creado exitosamente"}

def eliminar_usuario(user_id: int):
    supabase.table("usuarios") \
           .delete() \
           .eq("id", user_id) \
           .execute()
    return {"mensaje": "Usuario eliminado"}