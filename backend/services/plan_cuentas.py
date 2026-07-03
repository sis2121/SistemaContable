from config.supabase_client import supabase

class PlanCuentasService:

    def insertar(self, codigo, nombre):
        return supabase.table("plan_cuentas").insert({
            "codigo": codigo,
            "nombre": nombre
        }).execute()

    def listar(self):
        return supabase.table("plan_cuentas").select("*").order("codigo").execute()

    def eliminar(self, codigo):
        return supabase.table("plan_cuentas").delete().eq("codigo", codigo).execute()