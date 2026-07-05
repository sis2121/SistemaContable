from config.supabase_client import supabase
from fastapi import HTTPException

class PlanCuentasService:

    def _parse_codigo(self, codigo: str):
        parts = codigo.split('.')
        parsed = []
        for p in parts:
            if p.isdigit():
                parsed.append(int(p))
            else:
                parsed.append(p.lower())
        return parsed

    def listar(self):
        res = supabase.table("plan_cuentas") \
                     .select("codigo, nombre") \
                     .order("codigo") \
                     .execute().data
        if not res:
            return []
        return sorted(res, key=lambda x: self._parse_codigo(x["codigo"]))

    def insertar(self, codigo: str, nombre: str):
        try:
            return supabase.table("plan_cuentas").insert({
                "codigo": codigo,
                "nombre": nombre
            }).execute().data
        except Exception as e:
            error_str = str(e).lower()
            if "duplicate key" in error_str or "23505" in error_str:
                raise HTTPException(status_code=409, detail="El código de cuenta ya existe. Usá uno distinto.")
            raise HTTPException(status_code=400, detail=str(e))

    def eliminar(self, codigo: str):
        return supabase.table("plan_cuentas") \
                      .delete() \
                      .eq("codigo", codigo) \
                      .execute().data