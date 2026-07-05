from config.supabase_client import supabase

class LibroDiarioService:

    def registrar_asiento(self, fecha: str, glosa: str, lineas: list):
        """
        lineas: [ { "codigo": "1.1.1", "debe_haber": "DEBE", "monto": 1000.00 }, ... ]
        """
        # Insertar cabecera
        asiento = supabase.table("asientos").insert({
            "fecha": fecha,
            "glosa": glosa
        }).execute().data[0]

        id_asiento = asiento["id_asiento"]

        # Obtener id_cuenta por código
        codigos = [l["codigo"] for l in lineas]
        cuentas_db = supabase.table("plan_cuentas") \
                            .select("codigo, id_cuenta") \
                            .in_("codigo", codigos) \
                            .execute().data
        mapa = {c["codigo"]: c["id_cuenta"] for c in cuentas_db}

        detalles = []
        for linea in lineas:
            id_cuenta = mapa.get(linea["codigo"])
            if not id_cuenta:
                raise Exception(f"Cuenta no encontrada: {linea['codigo']}")
            detalles.append({
                "id_asiento": id_asiento,
                "id_cuenta": id_cuenta,
                "debe_haber": linea["debe_haber"],
                "monto": linea["monto"]
            })

        supabase.table("detalle_asientos").insert(detalles).execute()
        return asiento

    def listar_asientos(self):
        # Obtener cabeceras ordenadas por fecha ascendente
        asientos = supabase.table("asientos") \
                          .select("*") \
                          .order("fecha") \
                          .execute().data

        for a in asientos:
            detalles = supabase.table("detalle_asientos") \
                              .select("id_detalle, debe_haber, monto, plan_cuentas!inner(codigo, nombre)") \
                              .eq("id_asiento", a["id_asiento"]) \
                              .execute().data
            lineas = []
            for d in detalles:
                c = d["plan_cuentas"]
                lineas.append({
                    "codigo": c["codigo"],
                    "nombre": c["nombre"],
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
        # Actualizar cabecera
        supabase.table("asientos").update({
            "fecha": fecha,
            "glosa": glosa
        }).eq("id_asiento", id_asiento).execute()

        # Borrar detalles anteriores
        supabase.table("detalle_asientos") \
               .delete() \
               .eq("id_asiento", id_asiento) \
               .execute()

        # Insertar nuevos
        codigos = [l["codigo"] for l in lineas]
        cuentas_db = supabase.table("plan_cuentas") \
                            .select("codigo, id_cuenta") \
                            .in_("codigo", codigos) \
                            .execute().data
        mapa = {c["codigo"]: c["id_cuenta"] for c in cuentas_db}

        nuevos = []
        for l in lineas:
            id_cuenta = mapa.get(l["codigo"])
            if not id_cuenta:
                raise Exception(f"Cuenta no encontrada: {l['codigo']}")
            nuevos.append({
                "id_asiento": id_asiento,
                "id_cuenta": id_cuenta,
                "debe_haber": l["debe_haber"],
                "monto": l["monto"]
            })
        supabase.table("detalle_asientos").insert(nuevos).execute()
        return supabase.table("asientos").select("*").eq("id_asiento", id_asiento).single().execute().data