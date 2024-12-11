
function validar() {
    var resp= validaNombre();
    if (resp==false) {
        return false;
    }
    return true;
}

function validaNombre() {
    var nombre = document.getElementById("txtNombre").value;
    if (nombre.trim().length==0) {
        alert("nombre esta en blanco");
        return false;
    }
    return true;
}