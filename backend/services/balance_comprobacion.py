from config.supabase_client import supabase

class BalanceComprobacionService:

    def generar(self):
        # Todas las cuentas (o al menos las que tienen movimientos o saldo inicial)
        cuentas = supabase.table("plan_cuentas").select("codigo, nombre").execute().data
        balances = supabase.table("balance_inicial").select("codigo, saldo, debe_haber").execute().data
        bal_dict = {b["codigo"]: b for b in balances}

        # Movimientos agrupados por cuenta
        movs = supabase.table("detalle_asientos") \
            .select("codigo, debe_haber, monto") \
            .execute().data

        from collections import defaultdict
        sumas_debe = defaultdict(float)
        sumas_haber = defaultdict(float)
        for m in movs:
            if m["debe_haber"] == "DEBE":
                sumas_debe[m["codigo"]] += float(m["monto"])
            else:
                sumas_haber[m["codigo"]] += float(m["monto"])

        resultado = []
        total_debe = total_haber = total_saldo_deudor = total_saldo_acreedor = 0.0

        for c in cuentas:
            cod = c["codigo"]
            nom = c["nombre"]
            sum_d = sumas_debe.get(cod, 0.0)
            sum_h = sumas_haber.get(cod, 0.0)

            # Saldo inicial
            si_debe = 0.0
            si_haber = 0.0
            if cod in bal_dict:
                b = bal_dict[cod]
                if b["debe_haber"] == "DEBE":
                    si_debe = float(b["saldo"])
                else:
                    si_haber = float(b["saldo"])

            total_debe_mov = si_debe + sum_d
            total_haber_mov = si_haber + sum_h

            saldo_deudor = max(0.0, total_debe_mov - total_haber_mov)
            saldo_acreedor = max(0.0, total_haber_mov - total_debe_mov)

            total_debe += total_debe_mov
            total_haber += total_haber_mov
            total_saldo_deudor += saldo_deudor
            total_saldo_acreedor += saldo_acreedor

            resultado.append({
                "codigo": cod,
                "nombre": nom,
                "debe": total_debe_mov,
                "haber": total_haber_mov,
                "saldo_deudor": saldo_deudor,
                "saldo_acreedor": saldo_acreedor
            })

        return {
            "cuentas": resultado,
            "totales": {
                "debe": total_debe,
                "haber": total_haber,
                "saldo_deudor": total_saldo_deudor,
                "saldo_acreedor": total_saldo_acreedor
            }
        }