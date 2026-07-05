const API = "https://sistema-contable-backend-xglb.onrender.com";

// --- Líneas dinámicas (nuevo asiento) ---
function agregarLinea() {
  const container = document.getElementById("lineasContainer");
  const div = document.createElement("div");
  div.className = "linea flex gap-2 mb-2";
  div.innerHTML = `
    <input placeholder="Código cuenta" class="codigo w-1/3 rounded-2xl border border-slate-700 bg-slate-900 px-3 py-2">
    <select class="debeHaber w-1/4 rounded-2xl border border-slate-700 bg-slate-900 px-2 py-2">
      <option value="DEBE">DEBE</option>
      <option value="HABER">HABER</option>
    </select>
    <input type="number" step="0.01" placeholder="Monto" class="monto w-1/3 rounded-2xl border border-slate-700 bg-slate-900 px-3 py-2">
    <button onclick="eliminarLinea(this)" class="text-rose-400 px-2">✕</button>
  `;
  container.appendChild(div);
}

function eliminarLinea(boton) {
  boton.parentElement.remove();
}

async function registrarAsiento() {
  const fecha = document.getElementById("fecha").value;
  const glosa = document.getElementById("glosa").value.trim();
  if (!fecha || !glosa) return alert("Fecha y glosa obligatorias");
  const lineasElements = document.querySelectorAll(".linea");
  const lineas = [];
  lineasElements.forEach((el) => {
    const codigo = el.querySelector(".codigo").value.trim();
    const debeHaber = el.querySelector(".debeHaber").value;
    const monto = parseFloat(el.querySelector(".monto").value);
    if (codigo && !isNaN(monto)) {
      lineas.push({ codigo, debe_haber: debeHaber, monto });
    }
  });
  if (lineas.length < 2) return alert("Agregá al menos dos líneas");
  try {
    await fetch(`${API}/asientos`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ fecha, glosa, lineas }),
    });
    document.getElementById("fecha").value = "";
    document.getElementById("glosa").value = "";
    document.getElementById("lineasContainer").innerHTML = `
      <div class="linea flex gap-2 mb-2">
        <input placeholder="Código cuenta" class="codigo w-1/3 rounded-2xl border border-slate-700 bg-slate-900 px-3 py-2">
        <select class="debeHaber w-1/4 rounded-2xl border border-slate-700 bg-slate-900 px-2 py-2">
          <option value="DEBE">DEBE</option>
          <option value="HABER">HABER</option>
        </select>
        <input type="number" step="0.01" placeholder="Monto" class="monto w-1/3 rounded-2xl border border-slate-700 bg-slate-900 px-3 py-2">
        <button onclick="eliminarLinea(this)" class="text-rose-400 px-2">✕</button>
      </div>`;
    listarAsientos();
  } catch (e) {
    alert(e.message);
  }
}

// --- Listar asientos ---
async function listarAsientos() {
  const cont = document.getElementById("listaAsientos");
  cont.innerHTML = "";
  try {
    const res = await fetch(`${API}/asientos`);
    const asientos = await res.json();
    asientos.forEach((a) => {
      let html = `<div class="bg-slate-900/90 rounded-3xl p-4 border border-slate-700">
        <div class="flex justify-between">
          <h3 class="font-bold text-white">Asiento #${a.id_asiento} - ${a.fecha}</h3>
          <span class="text-slate-400">${a.glosa}</span>
        </div>
        <ul class="mt-2 space-y-1">`;
      a.lineas.forEach((l) => {
        html += `<li class="flex justify-between text-sm"><span>${l.codigo} ${l.nombre}</span> <span class="font-mono">${l.debe_haber} $${l.monto}</span></li>`;
      });
      html += `</ul></div>`;
      cont.innerHTML += html;
    });
  } catch (e) {
    cont.innerHTML = `<p class="text-rose-400">${e.message}</p>`;
  }
}

// --- Editar / Eliminar ---
async function cargarAsientoParaEditar() {
  const id = document.getElementById("idEditar").value;
  if (!id) return alert("Ingresá ID");
  try {
    const res = await fetch(`${API}/asientos`);
    const asientos = await res.json();
    const asiento = asientos.find((a) => a.id_asiento == id);
    if (!asiento) return alert("Asiento no encontrado");
    document.getElementById("editFecha").value = asiento.fecha;
    document.getElementById("editGlosa").value = asiento.glosa;
    const lineasCont = document.getElementById("editLineasContainer");
    lineasCont.innerHTML = "";
    asiento.lineas.forEach((l) => {
      lineasCont.innerHTML += `
        <div class="linea-edit flex gap-2 mb-2">
          <input class="codigoEdit w-1/3 rounded-2xl border border-slate-700 bg-slate-900 px-3 py-2" value="${l.codigo}">
          <select class="debeHaberEdit w-1/4 rounded-2xl border border-slate-700 bg-slate-900 px-2 py-2">
            <option value="DEBE" ${l.debe_haber === "DEBE" ? "selected" : ""}>DEBE</option>
            <option value="HABER" ${l.debe_haber === "HABER" ? "selected" : ""}>HABER</option>
          </select>
          <input type="number" step="0.01" class="montoEdit w-1/3 rounded-2xl border border-slate-700 bg-slate-900 px-3 py-2" value="${l.monto}">
          <button onclick="this.parentElement.remove()" class="text-rose-400 px-2">✕</button>
        </div>`;
    });
    document.getElementById("editorAsiento").classList.remove("hidden");
  } catch (e) {
    alert(e.message);
  }
}

function agregarLineaEdicion() {
  const cont = document.getElementById("editLineasContainer");
  const div = document.createElement("div");
  div.className = "linea-edit flex gap-2 mb-2";
  div.innerHTML = `
    <input placeholder="Código" class="codigoEdit w-1/3 rounded-2xl border border-slate-700 bg-slate-900 px-3 py-2">
    <select class="debeHaberEdit w-1/4 rounded-2xl border border-slate-700 bg-slate-900 px-2 py-2">
      <option value="DEBE">DEBE</option>
      <option value="HABER">HABER</option>
    </select>
    <input type="number" step="0.01" placeholder="Monto" class="montoEdit w-1/3 rounded-2xl border border-slate-700 bg-slate-900 px-3 py-2">
    <button onclick="this.parentElement.remove()" class="text-rose-400 px-2">✕</button>
  `;
  cont.appendChild(div);
}

async function guardarEdicion() {
  const id = document.getElementById("idEditar").value;
  const fecha = document.getElementById("editFecha").value;
  const glosa = document.getElementById("editGlosa").value.trim();
  if (!fecha || !glosa) return alert("Completá fecha y glosa");
  const lineas = [];
  document.querySelectorAll(".linea-edit").forEach((el) => {
    const codigo = el.querySelector(".codigoEdit").value.trim();
    const debeHaber = el.querySelector(".debeHaberEdit").value;
    const monto = parseFloat(el.querySelector(".montoEdit").value);
    if (codigo && !isNaN(monto))
      lineas.push({ codigo, debe_haber: debeHaber, monto });
  });
  try {
    await fetch(`${API}/asientos/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ fecha, glosa, lineas }),
    });
    document.getElementById("editorAsiento").classList.add("hidden");
    listarAsientos();
  } catch (e) {
    alert(e.message);
  }
}

async function eliminarAsiento() {
  const id = document.getElementById("idEditar").value;
  if (!id) return alert("Ingresá ID");
  if (!confirm("¿Eliminar asiento?")) return;
  try {
    await fetch(`${API}/asientos/${id}`, { method: "DELETE" });
    document.getElementById("idEditar").value = "";
    listarAsientos();
  } catch (e) {
    alert(e.message);
  }
}

// Inicial
listarAsientos();
