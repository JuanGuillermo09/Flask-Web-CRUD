
// Validación del login (frontend)
function validateLogin() {
  // Tomar los valores de usuario y contraseña
  const u = document.getElementById("username").value.trim();
  const p = document.getElementById("password").value;

  // Si alguno está vacío, mostrar alerta y bloquear envío
  if (!u || !p) {
    alert("Usuario y contraseña son obligatorios.");
    return false;
  }

  return true; // todo está bien
}

// Validación del formulario principal (frontend)
function validateMainForm() {
  const nombre = document.getElementById("nombre").value.trim();
  const email = document.getElementById("email").value.trim();
  const telefono = document.getElementById("telefono").value.trim();
  const comentarios = document.getElementById("comentarios").value.trim();

  // Campos obligatorios: nombre y email
  if (!nombre || !email) {
    alert("Nombre y correo son obligatorios.");
    return false;
  }

  // Validación básica de email con regex
  const re = /\S+@\S+\.\S+/;
  if (!re.test(email)) {
    alert("Ingrese un correo válido.");
    return false;
  }

  // Validar comentarios: máximo 200 caracteres
  if (comentarios.length > 200) {
    alert("Los comentarios no pueden superar los 200 caracteres.");
    return false;
  }

  // Teléfono debe ser solo números si hay valor
  if (telefono && !/^\d+$/.test(telefono)) {
    alert("El teléfono debe contener solo números.");
    return false;
  }

  return true; // todo correcto
}

// Limpiar formulario (UX)
function clearForm() {
  if (confirm("¿Limpiar el formulario?")) {
    document.getElementById("mainForm").reset(); // reinicia los campos
  }
}


// Función para escapar HTML y evitar XSS en el cliente
function escapeHtml(unsafe) {
  if (!unsafe) return "";
  return unsafe.replace(/[&<>"']/g, function (m) {
    return {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#039;",
    }[m];
  });
}

// Eventos DOM cargado para eliminar registros
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".deleteBtn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.dataset.id;

      if (!confirm("¿Seguro que deseas eliminar este registro?")) return;

      fetch("/delete", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `id=${encodeURIComponent(id)}`,
      })
        .then((resp) => {
          if (resp.ok) {
            btn.closest("tr").remove(); // elimina la fila del DOM
            alert("Registro eliminado correctamente");
          } else {
            alert("Error al eliminar el registro");
          }
        })
        .catch((err) => alert("Error: " + err.message));
    });
  });
});

// Eventos DOM cargado para editar registros
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".editBtn").forEach((btn) => {
    btn.addEventListener("click", () => {
      // Obtener datos del registro desde los atributos data-*
      const id = btn.dataset.id;
      const nombre = btn.dataset.nombre;
      const email = btn.dataset.email;
      const telefono = btn.dataset.telefono;
      const comentarios = btn.dataset.comentarios;

      // Llenar el formulario principal con los datos
      document.getElementById("nombre").value = nombre;
      document.getElementById("email").value = email;
      document.getElementById("telefono").value = telefono;
      document.getElementById("comentarios").value = comentarios;

      // Guardar el id en un input oculto para saber que es edición
      let inputId = document.getElementById("registroId");
      if (!inputId) {
        inputId = document.createElement("input");
        inputId.type = "hidden";
        inputId.id = "registroId";
        inputId.name = "id";
        document.getElementById("mainForm").appendChild(inputId);
      }
      inputId.value = id;

      // Hacer scroll hacia el formulario principal suavemente
      document.getElementById("mainForm").scrollIntoView({ behavior: "smooth" });

      // Subir al top de la página suavemente
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  });
});

// Botón scroll arriba
const scrollTopBtn = document.getElementById("scrollTopBtn");

// Mostrar el botón cuando se baja 100px
window.onscroll = function () {
  if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
    scrollTopBtn.style.display = "block";
  } else {
    scrollTopBtn.style.display = "none";
  }
};

// Al hacer clic, subir suavemente al top
scrollTopBtn.addEventListener("click", () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
});
