from config.supabase_client import supabase
from fastapi import HTTPException

class LibroMayorService:

    def obtener_mayor_por_cuenta(self, codigo: str):
        # Verificar que la cuenta existe
        cuenta = supabase.table("plan_cuentas").select("*").eq("codigo", codigo).single().execute().data
        if not cuenta:
            raise HTTPException(status_code=404, detail="Cuenta no encontrada")

        # Obtener balance inicial
        balance = supabase.table("balance_inicial") \
            .select("saldo, debe_haber") \
            .eq("codigo", codigo) \
            .maybe_single().execute().data

        saldo_inicial = 0.0
        signo = 1
        if balance:
            saldo_inicial = float(balance["saldo"])
            if balance["debe_haber"] == "HABER":
                signo = -1

        saldo_inicial_valor = saldo_inicial * signo

        # Obtener movimientos del diario para esa cuenta
        movimientos = supabase.table("detalle_asientos") \
            .select("id_asiento, codigo, debe_haber, monto, folio, asientos(fecha, glosa)") \
            .eq("codigo", codigo) \
            .order("id_asiento") \
            .execute().data

        # Construir lista ordenada por fecha
        items = []
        for mov in movimientos:
            asiento = mov["asientos"]
            items.append({
                "fecha": asiento["fecha"],
                "glosa": asiento["glosa"],
                "folio": mov.get("folio", ""),
                "debe": float(mov["monto"]) if mov["debe_haber"] == "DEBE" else 0,
                "haber": float(mov["monto"]) if mov["debe_haber"] == "HABER" else 0
            })

        # Ordenar por fecha (y por id_asiento si es necesario, aunque ya ordenamos)
        items.sort(key=lambda x: x["fecha"])

        # Calcular saldos corrientes
        saldo_acumulado = saldo_inicial_valor
        for item in items:
            saldo_acumulado += item["debe"] - item["haber"]
            item["saldo"] = saldo_acumulado

        return {
            "codigo": codigo,
            "nombre": cuenta["nombre"],
            "saldo_inicial": saldo_inicial_valor,
            "movimientos": items,
            "saldo_final": saldo_acumulado
        }

    def listar_cuentas_con_movimientos(self):
        # Devuelve códigos de cuentas que aparecen en detalle_asientos
        res = supabase.table("detalle_asientos") \
            .select("codigo") \
            .execute().data
        codigos = list({d["codigo"] for d in res})
        # Obtener nombre de esas cuentas
        cuentas = supabase.table("plan_cuentas") \
            .select("codigo, nombre") \
            .in_("codigo", codigos) \
            .execute().data
        cuentas.sort(key=lambda c: c["codigo"])
        return cuentas