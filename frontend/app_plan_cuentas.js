const API = "https://sistema-contable-backend-xglb.onrender.com";

function parseCodigo(codigo) {
  return codigo
    .split(".")
    .map((s) => (/^\d+$/.test(s) ? parseInt(s, 10) : s.toLowerCase()));
}

function compararCodigo(a, b) {
  const la = parseCodigo(a.codigo);
  const lb = parseCodigo(b.codigo);
  for (let i = 0; i < Math.max(la.length, lb.length); i++) {
    if (la[i] === undefined) return -1;
    if (lb[i] === undefined) return 1;
    if (la[i] < lb[i]) return -1;
    if (la[i] > lb[i]) return 1;
  }
  return 0;
}

function nivel(codigo) {
  return codigo.split(".").length - 1;
}

function buildItem(cuenta) {
  const padding = nivel(cuenta.codigo) * 1.5;
  return `
    <li class="flex items-center justify-between bg-slate-900/90 p-4 rounded-3xl border border-slate-800" style="padding-left:${padding}rem;">
      <div>
        <p class="font-semibold text-white">${cuenta.codigo}</p>
        <p class="text-sm text-slate-400">${cuenta.nombre} <span class="text-sky-400">(${cuenta.tipo})</span></p>
      </div>
      <button onclick="eliminar('${cuenta.codigo}')" class="rounded-2xl bg-rose-500 px-4 py-2 text-sm font-semibold text-white hover:bg-rose-400">Eliminar</button>
    </li>`;
}

async function cargar() {
  const lista = document.getElementById("lista");
  lista.innerHTML = "";
  try {
    const res = await fetch(`${API}/cuentas`);
    const cuentas = await res.json();
    cuentas.sort(compararCodigo);
    if (!cuentas.length) {
      lista.innerHTML = `<li class="text-slate-400 text-center p-4">No hay cuentas registradas.</li>`;
      return;
    }
    cuentas.forEach((c) => (lista.innerHTML += buildItem(c)));
  } catch (e) {
    lista.innerHTML = `<li class="text-rose-400">${e.message}</li>`;
  }
}

async function guardar() {
  const codigo = document.getElementById("codigo").value.trim();
  const nombre = document.getElementById("nombre").value.trim();
  const tipo = document.getElementById("tipo").value;
  if (!codigo || !nombre) return alert("Completá los campos");
  try {
    const res = await fetch(`${API}/cuentas`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ codigo, nombre, tipo }),
    });
    if (!res.ok) throw new Error("Error al guardar");
    document.getElementById("codigo").value = "";
    document.getElementById("nombre").value = "";
    cargar();
  } catch (e) {
    alert(e.message);
  }
}

async function eliminar(codigo) {
  try {
    await fetch(`${API}/cuentas/${codigo}`, { method: "DELETE" });
    cargar();
  } catch (e) {
    alert(e.message);
  }
}

async function eliminarPorCodigo() {
  const cod = document.getElementById("codigoEliminar").value.trim();
  if (!cod) return alert("Ingresá el código");
  await eliminar(cod);
  document.getElementById("codigoEliminar").value = "";
}

cargar();
