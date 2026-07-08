from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from services.plan_cuentas import PlanCuentasService
from services.balance_inicial import BalanceInicialService
from services.libro_diario import LibroDiarioService
from services.libro_mayor import LibroMayorService
from services.balance_comprobacion import BalanceComprobacionService
from services.auth import (
    autenticar_usuario,
    listar_usuarios,
    crear_usuario,
    eliminar_usuario,
)

app = FastAPI()

# Servicios
plan_service = PlanCuentasService()
balance_service = BalanceInicialService()
diario_service = LibroDiarioService()
mayor_service = LibroMayorService()
comp_service = BalanceComprobacionService()

# Esquema OAuth2 (no se usa para proteger endpoints, pero se define por si más adelante se requiere)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# CORS
origins = [
    "https://sistema-contable-flax.vercel.app",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===================== AUTENTICACIÓN =====================
@app.post("/login")
def login(data: dict):
    """
    Inicio de sesión.
    Espera un JSON con: { "nombre": "usuario", "password": "contraseña" }
    Retorna: { "token": "...", "rol": "admin|contador", "nombre": "usuario" }
    """
    return autenticar_usuario(data["nombre"], data["password"])

# ===================== GESTIÓN DE USUARIOS (solo ADMIN) =====================
@app.get("/usuarios")
def obtener_usuarios():
    """Lista todos los usuarios (nombre y rol)."""
    return listar_usuarios()

@app.post("/usuarios")
def registrar_usuario(data: dict):
    """
    Crea un nuevo usuario.
    Espera: { "nombre": "...", "password": "...", "rol": "admin|contador" }
    """
    return crear_usuario(data["nombre"], data["password"], data["rol"])

@app.delete("/usuarios/{user_id}")
def borrar_usuario(user_id: int):
    """Elimina un usuario por su ID."""
    return eliminar_usuario(user_id)

# ===================== PLAN DE CUENTAS =====================
@app.get("/cuentas")
def listar_cuentas():
    return plan_service.listar()

@app.post("/cuentas")
def crear_cuenta(data: dict):
    try:
        return plan_service.insertar(data["codigo"], data["nombre"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/cuentas/{codigo}")
def eliminar_cuenta(codigo: str):
    return plan_service.eliminar(codigo)

# ===================== BALANCE INICIAL =====================
@app.post("/balance-inicial")
def agregar_saldo(data: dict):
    return balance_service.agregar_o_actualizar(
        data["codigo"], float(data["saldo"]), data["debe_haber"]
    )

@app.get("/balance-inicial")
def listar_saldos():
    return balance_service.listar()

@app.put("/balance-inicial/{codigo}")
def editar_saldo(codigo: str, data: dict):
    return balance_service.editar(codigo, float(data["saldo"]))

@app.delete("/balance-inicial/{codigo}")
def eliminar_saldo(codigo: str):
    return balance_service.eliminar(codigo)

# ===================== LIBRO DIARIO =====================
@app.post("/asientos")
def crear_asiento(data: dict):
    return diario_service.registrar_asiento(
        data["fecha"], data["glosa"], data["lineas"]
    )

@app.get("/asientos")
def listar_asientos():
    return diario_service.listar_asientos()

@app.delete("/asientos/{id_asiento}")
def eliminar_asiento(id_asiento: int):
    return diario_service.eliminar_asiento(id_asiento)

@app.put("/asientos/{id_asiento}")
def editar_asiento(id_asiento: int, data: dict):
    return diario_service.editar_asiento(
        id_asiento, data["fecha"], data["glosa"], data["lineas"]
    )

# ===================== LIBRO MAYOR =====================
@app.get("/libro-mayor/cuentas")
def listar_cuentas_movimientos():
    """Devuelve las cuentas que tienen movimientos en el diario."""
    return mayor_service.listar_cuentas_con_movimientos()

@app.get("/libro-mayor/{codigo}")
def libro_mayor_por_cuenta(codigo: str):
    """Obtiene el libro mayor para una cuenta específica."""
    return mayor_service.obtener_mayor_por_cuenta(codigo)

# ===================== BALANCE DE COMPROBACIÓN =====================
@app.get("/balance-comprobacion")
def balance_comprobacion():
    """Genera el balance de comprobación con todos los movimientos y saldos iniciales."""
    return comp_service.generar()