from config.supabase_client import supabase

class PlanCuentasService:

    def _parse_codigo(self, codigo: str):
        """Convierte '1.2.10' en [1,2,10] para orden natural."""
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
                     .select("*") \
                     .order("codigo") \
                     .execute().data
        if not res:
            return []
        # Orden personalizado por segmentos numéricos
        return sorted(res, key=lambda x: self._parse_codigo(x["codigo"]))

    def insertar(self, codigo: str, nombre: str, tipo: str):
        # Calcular naturaleza según tipo contable
        if tipo in ('ACTIVO', 'COSTO', 'GASTO'):
            naturaleza = 'DEUDORA'
        else:
            naturaleza = 'ACREEDORA'

        nivel = codigo.count('.')

        return supabase.table("plan_cuentas").insert({
            "codigo": codigo,
            "nombre": nombre,
            "tipo": tipo,
            "naturaleza": naturaleza,
            "nivel": nivel,
            "id_padre": None  # Podés calcularlo si querés relaciones jerárquicas
        }).execute().data

    def eliminar(self, codigo: str):
        return supabase.table("plan_cuentas") \
                      .delete() \
                      .eq("codigo", codigo) \
                      .execute().data