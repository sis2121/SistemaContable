const API = "https://sistema-contable-backend-xglb.onrender.com";

function parseCodigo(codigo) {
  return codigo
    .split(".")
    .map((s) => (/^\d+$/.test(s) ? parseInt(s, 10) : s.toLowerCase()));
}

async function cargarSaldos() {
  const lista = document.getElementById("listaSaldos");
  lista.innerHTML = "";
  try {
    const res = await fetch(`${API}/balance-inicial`);
    const saldos = await res.json();
    if (!saldos.length) {
      lista.innerHTML = `<li class="text-slate-400 text-center p-4">No hay saldos iniciales (distintos de 0).</li>`;
      return;
    }
    saldos.forEach((s) => {
      lista.innerHTML += `
        <li class="flex justify-between bg-slate-900/90 p-4 rounded-3xl border border-slate-800">
          <div>
            <p class="font-semibold text-white">${s.codigo} - ${s.nombre}</p>
            <p class="text-sm text-slate-400">${s.debe_haber}: $${s.saldo}</p>
          </div>
        </li>`;
    });
  } catch (e) {
    lista.innerHTML = `<li class="text-rose-400">${e.message}</li>`;
  }
}

async function agregarSaldo() {
  const codigo = document.getElementById("codigoSaldo").value.trim();
  const saldo = document.getElementById("saldo").value;
  const debeHaber = document.getElementById("debeHaber").value;
  if (!codigo || !saldo) return alert("Completá todos los campos");
  try {
    const res = await fetch(`${API}/balance-inicial`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        codigo,
        saldo: parseFloat(saldo),
        debe_haber: debeHaber,
      }),
    });
    if (!res.ok) throw new Error("Error al guardar");
    document.getElementById("codigoSaldo").value = "";
    document.getElementById("saldo").value = "";
    cargarSaldos();
  } catch (e) {
    alert(e.message);
  }
}

async function editarSaldo() {
  const codigo = document.getElementById("codigoEditar").value.trim();
  const saldo = document.getElementById("nuevoSaldo").value;
  if (!codigo || !saldo) return alert("Ingresá código y nuevo saldo");
  try {
    await fetch(`${API}/balance-inicial/${codigo}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ saldo: parseFloat(saldo) }),
    });
    document.getElementById("codigoEditar").value = "";
    document.getElementById("nuevoSaldo").value = "";
    cargarSaldos();
  } catch (e) {
    alert(e.message);
  }
}

async function eliminarSaldo() {
  const codigo = document.getElementById("codigoEditar").value.trim();
  if (!codigo) return alert("Ingresá el código");
  try {
    await fetch(`${API}/balance-inicial/${codigo}`, { method: "DELETE" });
    document.getElementById("codigoEditar").value = "";
    cargarSaldos();
  } catch (e) {
    alert(e.message);
  }
}

cargarSaldos();
