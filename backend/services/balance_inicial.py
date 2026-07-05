from config.supabase_client import supabase
from fastapi import HTTPException

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
        # Verificar que la cuenta exista
        cuenta = supabase.table("plan_cuentas") \
                        .select("codigo") \
                        .eq("codigo", codigo) \
                        .single().execute().data
        if not cuenta:
            raise HTTPException(status_code=404, detail="Cuenta no encontrada")

        existente = supabase.table("balance_inicial") \
                           .select("id_balance") \
                           .eq("codigo", codigo) \
                           .execute().data
        if existente:
            return supabase.table("balance_inicial") \
                          .update({"saldo": saldo, "debe_haber": debe_haber}) \
                          .eq("codigo", codigo) \
                          .execute().data
        else:
            return supabase.table("balance_inicial") \
                          .insert({
                              "codigo": codigo,
                              "saldo": saldo,
                              "debe_haber": debe_haber
                          }).execute().data

    def listar(self):
        res = supabase.table("balance_inicial") \
                     .select("codigo, saldo, debe_haber") \
                     .execute().data
        cuentas = []
        for r in res:
            # Obtener nombre de la cuenta
            cuenta_info = supabase.table("plan_cuentas") \
                                .select("nombre") \
                                .eq("codigo", r["codigo"]) \
                                .single().execute().data
            cuentas.append({
                "codigo": r["codigo"],
                "nombre": cuenta_info["nombre"] if cuenta_info else "",
                "saldo": r["saldo"],
                "debe_haber": r["debe_haber"]
            })
        # Filtrar saldo != 0 y ordenar
        cuentas = [c for c in cuentas if c["saldo"] != 0]
        return sorted(cuentas, key=lambda x: self._parse_codigo(x["codigo"]))

    def editar(self, codigo: str, saldo: float):
        existente = supabase.table("balance_inicial") \
                           .select("id_balance") \
                           .eq("codigo", codigo) \
                           .execute().data
        if not existente:
            raise HTTPException(status_code=404, detail="No existe saldo para esa cuenta")
        return supabase.table("balance_inicial") \
                      .update({"saldo": saldo}) \
                      .eq("codigo", codigo) \
                      .execute().data

    def eliminar(self, codigo: str):
        return supabase.table("balance_inicial") \
                      .delete() \
                      .eq("codigo", codigo) \
                      .execute().data