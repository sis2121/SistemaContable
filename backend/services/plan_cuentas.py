from fastapi import HTTPException
from config.supabase_client import supabase
import re

class PlanCuentasService:
    # ... (los demás métodos se mantienen)

    def insertar(self, codigo: str, nombre: str, tipo: str):
        if tipo in ('ACTIVO', 'COSTO', 'GASTO'):
            naturaleza = 'DEUDORA'
        else:
            naturaleza = 'ACREEDORA'
        nivel = codigo.count('.')

        try:
            return supabase.table("plan_cuentas").insert({
                "codigo": codigo,
                "nombre": nombre,
                "tipo": tipo,
                "naturaleza": naturaleza,
                "nivel": nivel,
                "id_padre": None
            }).execute().data
        except Exception as e:
            error_str = str(e).lower()
            if "duplicate key" in error_str or "23505" in error_str:
                raise HTTPException(status_code=409, detail="El código de cuenta ya existe. Usá uno distinto.")
            raise HTTPException(status_code=400, detail=str(e))