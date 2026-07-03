const API = "https://sistema-contable-backend-xglb.onrender.com";

async function cargar() {
  const res = await fetch(`${API}/cuentas`);
  const data = await res.json();

  const lista = document.getElementById("lista");
  lista.innerHTML = "";

  data.data.forEach((item) => {
    lista.innerHTML += `
      <li class="border p-2 rounded">
        ${item.codigo} - ${item.nombre}
      </li>
    `;
  });
}

async function guardar() {
  const codigo = document.getElementById("codigo").value;
  const nombre = document.getElementById("nombre").value;

  await fetch(`${API}/cuentas`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ codigo, nombre }),
  });

  cargar();
}

cargar();
