const API = "https://sistema-contable-backend-xglb.onrender.com";

// LISTAR
async function cargar() {
  const res = await fetch(`${API}/cuentas`);
  const data = await res.json();

  const lista = document.getElementById("lista");
  lista.innerHTML = "";

  data.forEach((item) => {
    lista.innerHTML += `
      <li class="flex justify-between items-center bg-white p-3 rounded shadow-sm border">

        <div>
          <p class="font-semibold text-gray-700">${item.codigo}</p>
          <p class="text-sm text-gray-500">${item.nombre}</p>
        </div>

        <button 
          onclick="eliminar('${item.codigo}')"
          class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm"
        >
          Eliminar
        </button>

      </li>
    `;
  });
}

// GUARDAR
async function guardar() {
  const codigo = document.getElementById("codigo").value;
  const nombre = document.getElementById("nombre").value;

  if (!codigo || !nombre) {
    alert("Completa los campos");
    return;
  }

  await fetch(`${API}/cuentas`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ codigo, nombre }),
  });

  document.getElementById("codigo").value = "";
  document.getElementById("nombre").value = "";

  cargar();
}

// ELIMINAR
async function eliminar(codigo) {
  await fetch(`${API}/cuentas/${codigo}`, {
    method: "DELETE",
  });

  cargar();
}

cargar();
