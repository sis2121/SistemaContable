const API = "https://sistema-contable-backend-xglb.onrender.com";

function parseCodigo(codigo) {
  return codigo
    .trim()
    .split(".")
    .map((segment) => {
      const num = Number(segment);
      return Number.isNaN(num) ? segment.toLowerCase() : num;
    });
}

function compararCodigo(a, b) {
  const left = parseCodigo(a.codigo || a);
  const right = parseCodigo(b.codigo || b);

  const maxLength = Math.max(left.length, right.length);
  for (let i = 0; i < maxLength; i += 1) {
    if (left[i] === undefined) return -1;
    if (right[i] === undefined) return 1;

    if (left[i] < right[i]) return -1;
    if (left[i] > right[i]) return 1;
  }

  return 0;
}

function obtenerNivel(codigo) {
  return Math.max(0, codigo.split(".").length - 1);
}

function buildCuentaItem(item) {
  const nivel = obtenerNivel(item.codigo);
  return `
    <li class="flex items-center justify-between bg-slate-900/90 p-4 rounded-3xl border border-slate-800 shadow-sm"
        style="padding-left: ${nivel * 1.5}rem;">
      <div>
        <p class="font-semibold text-white">${item.codigo}</p>
        <p class="text-sm text-slate-400">${item.nombre}</p>
      </div>
      <button
        onclick="eliminar('${item.codigo}')"
        class="rounded-2xl bg-rose-500 px-4 py-2 text-sm font-semibold text-white transition hover:bg-rose-400"
      >
        Eliminar
      </button>
    </li>
  `;
}

async function cargar() {
  const lista = document.getElementById("lista");
  lista.innerHTML = "";

  try {
    const res = await fetch(`${API}/cuentas`);
    if (!res.ok) throw new Error("Error al cargar las cuentas");

    const data = await res.json();
    const cuentas = Array.isArray(data) ? data.sort(compararCodigo) : [];

    if (!cuentas.length) {
      lista.innerHTML = `
        <li class="rounded-3xl border border-dashed border-slate-700 bg-slate-900/60 p-8 text-center text-slate-400">
          No hay cuentas registradas todavía.
        </li>
      `;
      return;
    }

    cuentas.forEach((item) => {
      lista.innerHTML += buildCuentaItem(item);
    });
  } catch (error) {
    lista.innerHTML = `
      <li class="rounded-3xl border border-rose-500 bg-rose-950/10 p-6 text-center text-rose-200">
        ${error.message}
      </li>
    `;
    console.error(error);
  }
}

async function guardar() {
  const codigoInput = document.getElementById("codigo");
  const nombreInput = document.getElementById("nombre");
  const codigo = codigoInput.value.trim();
  const nombre = nombreInput.value.trim();

  if (!codigo || !nombre) {
    alert("Completa los campos");
    return;
  }

  try {
    const res = await fetch(`${API}/cuentas`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ codigo, nombre }),
    });

    if (!res.ok) throw new Error("No se pudo guardar la cuenta");
    codigoInput.value = "";
    nombreInput.value = "";
    cargar();
  } catch (error) {
    alert(error.message);
    console.error(error);
  }
}

async function eliminar(codigo) {
  if (!codigo) return;

  try {
    const res = await fetch(`${API}/cuentas/${codigo}`, {
      method: "DELETE",
    });

    if (!res.ok) throw new Error("No se pudo eliminar la cuenta");
    cargar();
  } catch (error) {
    alert(error.message);
    console.error(error);
  }
}

async function eliminarPorCodigo() {
  const codigoEliminar = document.getElementById("codigoEliminar").value.trim();
  if (!codigoEliminar) {
    alert("Introduce el código de la cuenta a eliminar");
    return;
  }

  await eliminar(codigoEliminar);
  document.getElementById("codigoEliminar").value = "";
}

cargar();
