from config.supabase_client import supabase

class BalanceInicialService:

    def _parse_codigo(self, codigo):
        parts = codigo.split('.')
        parsed = []
        for p in parts:
            if p.isdigit():
                parsed.append(int(p))
            else:
                parsed.append(p.lower())
        return parsed

    def agregar_o_actualizar(self, codigo: str, saldo: float, debe_haber: str):
        # Buscar id_cuenta
        cuenta = supabase.table("plan_cuentas") \
                        .select("id_cuenta") \
                        .eq("codigo", codigo) \
                        .single().execute().data
        if not cuenta:
            raise Exception("Cuenta no encontrada")

        id_cuenta = cuenta["id_cuenta"]

        # Upsert manual: si existe, actualiza; si no, inserta
        existente = supabase.table("balance_inicial") \
                           .select("id_balance") \
                           .eq("id_cuenta", id_cuenta) \
                           .execute().data

        if existente:
            return supabase.table("balance_inicial") \
                          .update({"saldo": saldo, "debe_haber": debe_haber}) \
                          .eq("id_cuenta", id_cuenta) \
                          .execute().data
        else:
            return supabase.table("balance_inicial") \
                          .insert({
                              "id_cuenta": id_cuenta,
                              "saldo": saldo,
                              "debe_haber": debe_haber
                          }).execute().data

    def listar(self):
        # JOIN para traer código, nombre, saldo, debe_haber
        res = supabase.table("balance_inicial") \
                     .select("id_balance, saldo, debe_haber, plan_cuentas!inner(codigo, nombre)") \
                     .execute().data
        cuentas = []
        for r in res:
            cuenta = r["plan_cuentas"]
            cuentas.append({
                "codigo": cuenta["codigo"],
                "nombre": cuenta["nombre"],
                "saldo": r["saldo"],
                "debe_haber": r["debe_haber"]
            })

        # Filtrar saldo != 0 y ordenar
        cuentas = [c for c in cuentas if c["saldo"] != 0]
        return sorted(cuentas, key=lambda x: self._parse_codigo(x["codigo"]))

    def editar(self, codigo: str, saldo: float):
        cuenta = supabase.table("plan_cuentas") \
                        .select("id_cuenta") \
                        .eq("codigo", codigo) \
                        .single().execute().data
        if not cuenta:
            raise Exception("Cuenta no encontrada")

        return supabase.table("balance_inicial") \
                      .update({"saldo": saldo}) \
                      .eq("id_cuenta", cuenta["id_cuenta"]) \
                      .execute().data

    def eliminar(self, codigo: str):
        cuenta = supabase.table("plan_cuentas") \
                        .select("id_cuenta") \
                        .eq("codigo", codigo) \
                        .single().execute().data
        if not cuenta:
            raise Exception("Cuenta no encontrada")

        return supabase.table("balance_inicial") \
                      .delete() \
                      .eq("id_cuenta", cuenta["id_cuenta"]) \
                      .execute().data