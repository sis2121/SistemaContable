from config.supabase_client import supabase
from fastapi import HTTPException

class LibroDiarioService:

    def registrar_asiento(self, fecha: str, glosa: str, lineas: list):
        # Insertar cabecera
        asiento = supabase.table("asientos").insert({
            "fecha": fecha,
            "glosa": glosa
        }).execute().data[0]

        id_asiento = asiento["id_asiento"]

        # Validar que todas las cuentas existan
        codigos = [l["codigo"] for l in lineas]
        cuentas_db = supabase.table("plan_cuentas") \
                            .select("codigo") \
                            .in_("codigo", codigos) \
                            .execute().data
        existentes = {c["codigo"] for c in cuentas_db}
        for c in codigos:
            if c not in existentes:
                raise HTTPException(status_code=400, detail=f"Cuenta no encontrada: {c}")

        detalles = []
        for linea in lineas:
            detalles.append({
                "id_asiento": id_asiento,
                "codigo": linea["codigo"],
                "debe_haber": linea["debe_haber"],
                "monto": linea["monto"]
            })
        supabase.table("detalle_asientos").insert(detalles).execute()
        return asiento

    def listar_asientos(self):
        asientos = supabase.table("asientos") \
                          .select("*") \
                          .order("fecha") \
                          .execute().data
        for a in asientos:
            detalles = supabase.table("detalle_asientos") \
                              .select("codigo, debe_haber, monto") \
                              .eq("id_asiento", a["id_asiento"]) \
                              .execute().data
            lineas = []
            for d in detalles:
                cuenta_info = supabase.table("plan_cuentas") \
                                    .select("nombre") \
                                    .eq("codigo", d["codigo"]) \
                                    .single().execute().data
                lineas.append({
                    "codigo": d["codigo"],
                    "nombre": cuenta_info["nombre"] if cuenta_info else "",
                    "debe_haber": d["debe_haber"],
                    "monto": d["monto"]
                })
            a["lineas"] = lineas
        return asientos

    def eliminar_asiento(self, id_asiento: int):
        return supabase.table("asientos") \
                      .delete() \
                      .eq("id_asiento", id_asiento) \
                      .execute().data

    def editar_asiento(self, id_asiento: int, fecha: str, glosa: str, lineas: list):
        supabase.table("asientos").update({
            "fecha": fecha,
            "glosa": glosa
        }).eq("id_asiento", id_asiento).execute()

        supabase.table("detalle_asientos") \
               .delete() \
               .eq("id_asiento", id_asiento) \
               .execute()

        codigos = [l["codigo"] for l in lineas]
        cuentas_db = supabase.table("plan_cuentas") \
                            .select("codigo") \
                            .in_("codigo", codigos) \
                            .execute().data
        existentes = {c["codigo"] for c in cuentas_db}
        for c in codigos:
            if c not in existentes:
                raise HTTPException(status_code=400, detail=f"Cuenta no encontrada: {c}")

        nuevos = []
        for l in lineas:
            nuevos.append({
                "id_asiento": id_asiento,
                "codigo": l["codigo"],
                "debe_haber": l["debe_haber"],
                "monto": l["monto"]
            })
        supabase.table("detalle_asientos").insert(nuevos).execute()
        return supabase.table("asientos").select("*").eq("id_asiento", id_asiento).single().execute().data