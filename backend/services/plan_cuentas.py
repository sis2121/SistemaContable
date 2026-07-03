from config.supabase_client import supabase

class PlanCuentasService:

    def listar(self):
        return supabase.table("plan_cuentas").select("*").execute().data

    def insertar(self, codigo, nombre):
        return supabase.table("plan_cuentas").insert({
            "codigo": codigo,
            "nombre": nombre
        }).execute().data

    # 🔥 NUEVO: eliminar por código
    def eliminar(self, codigo):
        return supabase.table("plan_cuentas") \
            .delete() \
            .eq("codigo", codigo) \
            .execute().data