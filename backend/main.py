from fastapi import FastAPI
from services.plan_cuentas import PlanCuentasService

app = FastAPI()
service = PlanCuentasService()

@app.get("/cuentas")
def listar():
    return service.listar()

@app.post("/cuentas")
def insertar(data: dict):
    return service.insertar(data["codigo"], data["nombre"])

@app.delete("/cuentas/{codigo}")
def eliminar(codigo: str):
    return service.eliminar(codigo)