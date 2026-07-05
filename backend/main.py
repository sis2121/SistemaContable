from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.plan_cuentas import PlanCuentasService
from services.balance_inicial import BalanceInicialService
from services.libro_diario import LibroDiarioService

app = FastAPI()
plan_service = PlanCuentasService()
balance_service = BalanceInicialService()
diario_service = LibroDiarioService()

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

# Plan de cuentas
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

# Balance inicial
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

# Libro diario
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