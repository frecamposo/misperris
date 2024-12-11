function mensaje() {
    alert('hola mundo');
}
function validaNombre(){
    var nombre= document.getElementById("txtNombreCompleto").value;
    if (nombre.trim().length==0) {
        //alert("el nombre no puede estar en blanco");
        Swal.fire({
            icon: 'error',
            title: 'Nombre Completo',
            text: 'el nombre no puede estar en blanco'
        });
        return false;
    }
    return true;
}
function validarFormulario() {
    var resp = validaRut();
    if ( resp == false ) {
        return false;
    }
    resp = validaFecha();
    if (resp==false) {
        return false;
    }
    resp = validaNombre();
    if (resp==false) {
        return false;
    }
    return true;
}
function validaFecha() {
    var fechaUsuario = document.getElementById('txtFechaNaci').value;
    var fechaSistema = new Date();
    console.log('Fecha Usuario:'+fechaUsuario);
    console.log('Fecha Sistema:'+fechaSistema);

    var ano = fechaUsuario.slice(0,4);
    var mes = fechaUsuario.slice(5,7);
    var dia = fechaUsuario.slice(8,10);
    console.log('Año:'+ano);
    console.log('Mes:'+mes);
    console.log('Dia:'+dia);

    var fechaNuevaUsuario = new Date(ano,(mes-1),dia);
    console.log('Nueva Fecha:'+fechaNuevaUsuario);
    /// fecha ingresada menor a la actual 
    if ( fechaNuevaUsuario > fechaSistema ) {
        //alert('fecha incorrecta');
        Swal.fire({
            icon: 'error',
            title: 'Fecha Nacimiento',
            text: 'fecha incorrecta'
          });
        return false;
    }
    // minimo 18 años
    var unDia = 24 * 60 * 60 *1000; // 1 dia en milisegundos
    var diferencia =Math.trunc((fechaSistema.getTime() - fechaNuevaUsuario.getTime()) / unDia);
    console.log('Dias:'+diferencia);
    var anos = Math.trunc( diferencia / 365 );
    console.log('Edad:'+anos);
    if ( anos < 18) {
        //alert('es menor de edad, usted tiene '+anos+' años de edad');
        Swal.fire({
            icon: 'error',
            title: 'Fecha Nacimiento',
            text: 'es menor de edad, usted tiene '+anos+' años de edad'
          });
        return false;
    }
    return true;
}

function validaRut() {
    var rut = document.getElementById('txtRut').value;
    //alert(rut);
    console.log(rut);
    var num = 3;
    var suma = 0;
    for (let index = 0; index < 8; index++) {
        var caracter = rut.slice(index,index+1);
        console.log(caracter+ ' x '+num);
        suma = suma + ( caracter * num );
        num = num - 1;
        if (num == 1) {
            num = 7;
        }
    }
    console.log('suma:'+suma);
    var resto = suma % 11;
    var dv = 11 - resto;
    if ( dv > 9) {
        if ( dv == 10 ) {
            dv = 'K';
        }else{
            dv = 0;
        }
    }
    console.log(dv);
    var dv_usuario = rut.slice(-1).toUpperCase();
    if ( dv != dv_usuario ) {
        //alert('rut es incorrecto');
        //Swal.fire('rut es incorrecto');
        Swal.fire({
            icon: 'error',
            title: 'Rut',
            text: 'el rut es incorrecto, verifiquelo'
          });
        return false;
    }
    return true;
}