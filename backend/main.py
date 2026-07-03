from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.plan_cuentas import PlanCuentasService

app = FastAPI()
service = PlanCuentasService()

# ---------------- CORS ----------------
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

# ---------------- ENDPOINTS ----------------

@app.get("/cuentas")
def listar():
    return service.listar()

@app.post("/cuentas")
def insertar(data: dict):
    return service.insertar(data["codigo"], data["nombre"])

# 🔥 NUEVO: eliminar por código
@app.delete("/cuentas/{codigo}")
def eliminar(codigo: str):
    return service.eliminar(codigo)