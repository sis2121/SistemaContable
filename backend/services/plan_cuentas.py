from config.supabase_client import supabase

class PlanCuentasService:

    def listar(self):
        cuentas = supabase.table("plan_cuentas").select("*").execute().data
        if not cuentas:
            return []

        def parse_codigo(codigo):
            parts = codigo.split('.')
            parsed = []
            for part in parts:
                if part.isdigit():
                    parsed.append(int(part))
                else:
                    parsed.append(part.lower())
            return parsed

        return sorted(cuentas, key=lambda item: parse_codigo(item["codigo"]))

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