
const maxItems = 5; // Maximum number of items

// Function to add a new form dynamically
function addForm() {
    
    let formsContainer = document.getElementById('forms-container');

    // Check if maximum limit reached
    if (document.querySelectorAll('.item-form').length >= maxItems) {
        alert("Solo puedes añadir un maximo de 5 componentes.");
        return;
    }

    let formItem = document.createElement('div');
    formItem.classList.add('item-form');

    formItem.innerHTML = `
    <label for="marca_hw">Marca:</label>
        <input name="marca_hw" placeholder="Samsung" type="text" autocomplete="off">
        
        <label for="modelo_hw">Modelo:</label>
        <input name="modelo_hw" placeholder="SyncMaster" type="text" autocomplete="off">
                    
        <label for="n_serie_hw">N° Serie:</label>
        <input name="n_serie_hw" placeholder="12345657890" type="text" autocomplete="off">

        <label for="especificaciones_hw">Especificaciones:</label>
        <input name="especificaciones_hw" placeholder="HD 1280px 796px" type="text" autocomplete="off">

        <input name="capacidad_hw" value="" type="hidden">
        <input name="tipo_hw" value="" type="hidden">
        <input name="id_equipo_hw" value="{{ id_equipo }}" type="hidden">
    `;
    formsContainer.appendChild(formItem);
} 

// Event listener for the Add Item button. COMMENTED BCS BUTTON ONCLICK
// document.getElementById('addFormBtn').addEventListener('click', addForm);



// ----------- RAM -------------
function addRamForm() {

    const maxRam = 4;    
    let formsContainer = document.getElementById('rams-container');
    let n_rams = document.querySelectorAll('.ram-form').length

    // Check if maximum limit reached
    if (n_rams >= maxRam) {
        alert("Solo puedes añadir un maximo de 4 RAMs.");
        return;
    }

    let formItem = document.createElement('div');
    formItem.classList.add('ram-form');

    formItem.innerHTML = `
        <h5 class="my-2">Ram N° ${n_rams + 1}</h5> 
        <div class="row">
            <div class="col-md-6">
            <label for="marca_hw">Marca:</label>
            <input name="marca_hw" placeholder="Marca" type="text" autocomplete="off" class="form-control mb-2">
            </div>
            <div class="col-md-6">
            <label for="modelo_hw">Modelo:</label>
            <input name="modelo_hw" placeholder="Modelo" type="text" autocomplete="off" class="form-control mb-2">
            </div>
        </div>
        <div class="row">
            <div class="col-md-6">
            <label for="capacidad_hw">Capacidad:</label>
            <input name="capacidad_hw" placeholder="Capacidad" type="text" autocomplete="off" class="form-control mb-2">
            </div>
            <div class="col-md-6">
            <label for="especificaciones_hw">Especificaciones:</label>
            <input name="especificaciones_hw" placeholder="Especificaciones" type="text" autocomplete="off" class="form-control mb-2">
            </div>  
            <!-- <div class="col-md-6">
            <label for="n_serie_hw">N° Serie:</label> -->
            <input name="n_serie_hw" placeholder="N° Serie" type="hidden" autocomplete="off" class="form-control mb-2">
            <!-- </div> -->
        </div>
        <div class="row">
            <div class="col-md-6">
            <input name="tipo_hw" value="ram" type="hidden">
            <input name="id_equipo_hw" value="{{ id_equipo }}" type="hidden">
            </div>
        </div>
        `;
    formsContainer.appendChild(formItem);
} 

// Event listener for the Add Item button. COMMENTED BCS BUTTON ONCLICK
// document.getElementById('addFormBtn').addEventListener('click', addForm);



// ------- ALMACENAMIENTO --------
function addAlmForm() {

    const maxAlm = 4;    
    let formsContainer = document.getElementById('alms-container');
    let n_alm = document.querySelectorAll('.alm-form').length

    // Check if maximum limit reached
    if (n_alm >= maxAlm) {
        alert("Solo puedes añadir un maximo de 4 unidades de almacenamiento.");
        return;
    }

    let formItem = document.createElement('div');
    formItem.classList.add('alm-form');

    formItem.innerHTML = `
        <h5 class="my-2">Unidad de almacenamiento N° ${n_alm + 1}</h5>
        <div class="row">
            <div class="col-md-6">
            <label for="marca_hw">Marca:</label>
            <input name="marca_hw" placeholder="Marca" type="text" autocomplete="off" class="form-control mb-2">
            </div>
            <div class="col-md-6">
            <label for="modelo_hw">Modelo:</label>
            <input name="modelo_hw" placeholder="Modelo" type="text" autocomplete="off" class="form-control mb-2">
            </div>
        </div>
        <div class="row">
            <div class="col-md-6">
            <label for="capacidad_hw">Capacidad:</label>
            <input name="capacidad_hw" placeholder="Capacidad" type="text" autocomplete="off" class="form-control mb-2">
            </div>
            <div class="col-md-6">
            <label for="n_serie_hw">N° Serie:</label>
            <input name="n_serie_hw" placeholder="N° Serie" type="text" autocomplete="off" class="form-control mb-2">
            </div>
        </div>
        <div class="row">
            <div class="col-md-6">
            <label for="especificaciones_hw">Especificaciones:</label>
            <input name="especificaciones_hw" placeholder="Especificaciones" type="text" autocomplete="off" class="form-control mb-2">
            </div>
            <div class="col-md-6">
            <input name="tipo_hw" value="almacenamiento" type="hidden">
            <input name="id_equipo_hw" value="{{ id_equipo }}" type="hidden">
            </div>
        </div>
    `;
    formsContainer.appendChild(formItem);
} 

// Event listener for the Add Item button. COMMENTED BCS BUTTON ONCLICK
// document.getElementById('addFormBtn').addEventListener('click', addForm);


// ------- MONITOR --------
function addMonForm() {

    const maxMon = 3;    
    let formsContainer = document.getElementById('mon-container');
    let n_mon = document.querySelectorAll('.mon-form').length

    // Check if maximum limit reached
    if (n_mon >= maxMon) {
        alert("Solo puedes añadir un maximo de 3 monitores.");
        return;
    }

    let formItem = document.createElement('div');
    formItem.classList.add('mon-form');

    formItem.innerHTML = `
        <h5 class="my-2">Monitor N° ${n_mon + 1}</h5>
        <div class="row">
            <div class="col-md-6">
            <label for="marca_hw">Marca:</label>
            <input name="marca_hw" placeholder="Marca" type="text" autocomplete="off" class="form-control mb-2">
            </div>
            <div class="col-md-6">
            <label for="modelo_hw">Modelo:</label>
            <input name="modelo_hw" placeholder="Modelo" type="text" autocomplete="off" class="form-control mb-2">
            </div>
        </div>
        <div class="row">
            <div class="col-md-6">
            <label for="n_serie_hw">N° Serie:</label>
            <input name="n_serie_hw" placeholder="12345657890" type="text" autocomplete="off" class="form-control mb-2">
            </div>
            <div class="col-md-6">
            <label for="especificaciones_hw">Especificaciones:</label>
            <input name="especificaciones_hw" placeholder="Especificaciones" type="text" autocomplete="off" class="form-control mb-2">
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
            <input name="capacidad_hw" value="" type="hidden">
            <input name="tipo_hw" value="monitor" type="hidden">
            <input name="id_equipo_hw" value="{{ id_equipo }}" type="hidden">
            </div>
        </div>
    `;
    formsContainer.appendChild(formItem);
} 

// Event listener for the Add Item button. COMMENTED BCS BUTTON ONCLICK
// document.getElementById('addFormBtn').addEventListener('click', addForm);


// ------- OTROS --------
function addOtroForm() {

    const maxOtro = 7;    
    let formsContainer = document.getElementById('otro-container');
    let n_otro = document.querySelectorAll('.otro-form').length

    // Check if maximum limit reached
    if (n_otro >= maxOtro) {
        alert("Haz alcanzado el limite de hardware añadido.");
        return;
    }

    let formItem = document.createElement('div');
    formItem.classList.add('otro-form');

    formItem.innerHTML = `
        <h5 class="my-2">Hardware añadido N° ${n_otro + 1}</h5>
        <div class="row">
            <div class="col-md-6">
            <label for="tipo_hw">Tipo:</label>
            <select name="tipo_hw" class="form-control mb-2">
                <option value="red">Tarjeta de red</option>
                <option value="bluetooth">Adaptador de bluetooth</option>
                <option value="webcam">Cámara web</option>
                <option value="escaner">Escaner</option>
                <option value="altavoces">Altavoces</option>
                <option value="audifonos">Audifonos</option>
                <option value="otro">Otro</option>
                <option value="">Ninguno</option>

            </select>
            </div>
            <div class="col-md-6">
            <label for="marca_hw">Marca:</label>
            <input name="marca_hw" placeholder="Marca" type="text" autocomplete="off" class="form-control mb-2">
            </div>
        </div>
        <div class="row">
            <div class="col-md-6">
            <label for="modelo_hw">Modelo:</label>
            <input name="modelo_hw" placeholder="Modelo" type="text" autocomplete="off" class="form-control mb-2">
            </div>
            <div class="col-md-6">
            <label for="n_serie_hw">N° Serie:</label>
            <input name="n_serie_hw" placeholder="N° Serie" type="text" autocomplete="off" class="form-control mb-2">
            </div>
        </div>
        <div class="row">
            <div class="col-md-6">
            <label for="especificaciones_hw">Especificaciones:</label>
            <input name="especificaciones_hw" placeholder="Especificaciones" type="text" autocomplete="off" class="form-control mb-2">
            </div>
            <div class="col-md-6">
            <input name="capacidad_hw" value="" type="hidden">
            <input name="id_equipo_hw" value="{{ id_equipo }}" type="hidden">
            </div>
        </div>
    `;
    formsContainer.appendChild(formItem);
} 

// Event listener for the Add Item button. COMMENTED BCS BUTTON ONCLICK
// document.getElementById('addFormBtn').addEventListener('click', addForm);


// ------- Items de Hardware por separado --------
function addHwItemForm() {

    const maxHwItem = 3;    
    let formsContainer = document.getElementById('hwitem-container');
    let n_hwitem = document.querySelectorAll('.hwitem-form').length

    // Check if maximum limit reached
    if (n_hwitem >= maxHwItem) {
        alert(`Solo puedes añadir un máximo de ${maxHwItem} elementos.`);
        return;
    }

    let formItem = document.createElement('div');
    formItem.classList.add('hwitem-form');
    formItem.classList.add('mb-3');


    formItem.innerHTML = `
        <h5 class="my-2">Item N° ${n_hwitem + 1}</h5>
                <div class="row">
                    <div class="col-md-6">
                        <label for="tipo_hw">Tipo:</label>
                        <select name="tipo_hw" class="form-control mb-2">
                            <option value="case">Case</option>
                            <option value="placa">Placa base</option>
                            <option value="cpu">Procesador</option>
                            <option value="ram">Tarjeta RAM</option>
                            <option value="almacenamiento">Almacenamiento</option>
                            <option value="fuente">Fuente de poder</option>

                            <option value="monitor">Monitor</option>
                            <option value="teclado">Teclado</option>
                            <option value="mouse">Mouse</option>
                            <option value="impresora">Impresora</option>


                            <option value="red">Tarjeta de red</option>
                            <option value="bluetooth">Adaptador de bluetooth</option>
                            <option value="webcam">Cámara web</option>
                            <option value="escaner">Escaner</option>
                            <option value="altavoces">Altavoces</option>
                            <option value="audifonos">Audifonos</option>
                            <option value="otro">Otro</option>
                        </select>
                    </div>
                    <div class="col-md-6">
                        <label for="marca_hw">Marca:</label>
                        <input name="marca_hw" placeholder="Marca" type="text" autocomplete="off" class="form-control mb-2">
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        <label for="modelo_hw">Modelo:</label>
                        <input name="modelo_hw" placeholder="Modelo" type="text" autocomplete="off" class="form-control mb-2">
                    </div>
                    <div class="col-md-6">
                        <label for="n_serie_hw">N° Serie:</label>
                        <input name="n_serie_hw" placeholder="N° Serie" type="text" autocomplete="off" class="form-control mb-2">
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        <label for="especificaciones_hw">Especificaciones:</label>
                        <input name="especificaciones_hw" placeholder="Especificaciones" type="text" autocomplete="off" class="form-control mb-2">
                    </div>
                    <div class="col-md-6">
                        <label for="capacidad_hw">Capacidad:</label>
                        <input name="capacidad_hw" placeholder="Capacidad" type="text" autocomplete="off" class="form-control mb-2">
                        <input name="id_equipo_hw" value="{{ id_equipo }}" type="hidden">
                    </div>
                </div>
    `;
    formsContainer.appendChild(formItem);
} 

// Event listener for the Add Item button. COMMENTED BCS BUTTON ONCLICK
// document.getElementById('addFormBtn').addEventListener('click', addForm);



// ------- SISTEMA OPERATIVO --------
function addSoForm() {

    const maxSo = 2;    
    let formsContainer = document.getElementById('so-container');
    let n_so = document.querySelectorAll('.so-form').length
    // Check if maximum limit reached
    if (n_so >= maxSo) {
        alert("Solo puedes añadir 2 sistemas operativos.");
        return;
    }

    let formItem = document.createElement('div');
    formItem.classList.add('so-form');

    formItem.innerHTML = `
        <h5 class="my-2">Sistema operativo N° ${n_so + 1}</h5>
        <div class="row">
            <div class="col-md-6">
            <label for="nombre_so">Nombre:</label>
            <select name="nombre_so" class="form-control mb-2">
                <option value="windows">Windows</option>
                <option value="linux">Linux</option>
                <option value="macos">MacOS</option>
                <option value="otro">Otro</option>
            </select>
            </div>
            <div class="col-md-6">
            <label for="edicion_so">Edición:</label>
            <input name="edicion_so" placeholder="Windows 7 Professional" type="text" autocomplete="off" class="form-control mb-2">
            </div>
        </div>
        <div class="row">
            <div class="col-md-6">
            <label for="arq_so">Arquitectura:</label>
            <select name="arq_so" class="form-control mb-2">
                <option value="32 bits">32 bits</option>
                <option value="64 bits">64 bits</option>
            </select>
            </div>
            <div class="col-md-6">
            <label for="desarrollador_so">Desarrollador:</label>
            <input name="desarrollador_so" placeholder="Microsoft" type="text" autocomplete="off" class="form-control mb-2">
            </div>
        </div>
        <div class="row">
            <div class="col-md-6">
            <label for="licencia_so">Licencia:</label>
            <input name="licencia_so" placeholder="Microsoft" type="text" autocomplete="off" class="form-control mb-2">
            </div>
            <div class="col-md-6">
            <input name="id_equipo_so" value="{{ id_equipo }}" type="hidden">
            </div>
        </div>
    `;
    formsContainer.appendChild(formItem);
} 

// Event listener for the Add Item button. COMMENTED BCS BUTTON ONCLICK
// document.getElementById('addFormBtn').addEventListener('click', addForm);



// ------- NAVEGADOR --------
function addNavForm() {

    const maxNav = 4;    
    let formsContainer = document.getElementById('nav-container');
    let n_nav = document.querySelectorAll('.nav-form').length
    // Check if maximum limit reached
    if (n_nav >= maxNav) {
        alert("Solo puedes añadir 6 navegadores.");
        return;
    }

    let formItem = document.createElement('div');
    formItem.classList.add('nav-form');

    formItem.innerHTML = `
        <h5 class="my-2">Navegador N° ${n_nav + 1}</h5>
        <div class="row">
            <div class="col-md-6">
            <label for="nombre_sw">Nombre:</label>
            <input name="nombre_sw" placeholder="Nombre del Navegador" type="text" autocomplete="off" class="form-control mb-2">
            </div>
            <div class="col-md-6">
            <label for="version_sw">Versión:</label>
            <input name="version_sw" placeholder="Versión" type="text" autocomplete="off" class="form-control mb-2">
            </div>
        </div>
        <div class="row">
            <div class="col-md-6">
            <label for="desarrollador_sw">Desarrollador:</label>
            <input name="desarrollador_sw" placeholder="Desarrollador" type="text" autocomplete="off" class="form-control mb-2">
            </div>
            <div class="col-md-6">
            <input name="licencia_sw" value="" type="hidden">
            <input name="categoria_sw" value="navegador" type="hidden">
            <input name="id_equipo_hw" value="{{ id_equipo }}" type="hidden">
            </div>
        </div>
    `;
    formsContainer.appendChild(formItem);
} 

// Event listener for the Add Item button. COMMENTED BCS BUTTON ONCLICK
// document.getElementById('addFormBtn').addEventListener('click', addForm);


// ------- OFIMATICA --------
function addOfiForm() {

    const maxOfi = 8;    
    let formsContainer = document.getElementById('ofi-container');
    let n_ofi = document.querySelectorAll('.ofi-form').length
    // Check if maximum limit reached
    if (n_ofi >= maxOfi) {
        alert("Solo puedes añadir 6 navegadores.");
        return;
    }

    let formItem = document.createElement('div');
    formItem.classList.add('ofi-form');

    formItem.innerHTML = `
        <h5 class="my-2">Programa de ofimática N° ${n_ofi + 1}</h5>
        <div class="row">
            <div class="col-md-6">
            <label for="nombre_sw">Nombre:</label>
            <input name="nombre_sw" placeholder="Nombre del Software" type="text" autocomplete="off" class="form-control mb-2">
            </div>
            <div class="col-md-6">
            <label for="version_sw">Versión:</label>
            <input name="version_sw" placeholder="Versión" type="text" autocomplete="off" class="form-control mb-2">
            </div>
        </div>
        <div class="row">
            <div class="col-md-6">
            <label for="desarrollador_sw">Desarrollador:</label>
            <input name="desarrollador_sw" placeholder="Desarrollador" type="text" autocomplete="off" class="form-control mb-2">
            </div>
            <div class="col-md-6">
            <label for="licencia_sw">Licencia:</label>
            <input name="licencia_sw" placeholder="Licencia" type="text" autocomplete="off" class="form-control mb-2">
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
            <input name="categoria_sw" value="ofimatica" type="hidden">
            <input name="id_equipo_hw" value="{{ id_equipo }}" type="hidden">
            </div>
        </div>
    `;
    formsContainer.appendChild(formItem);
} 

// Event listener for the Add Item button. COMMENTED BCS BUTTON ONCLICK
// document.getElementById('addFormBtn').addEventListener('click', addForm);



// ------- SEGURIDAD --------
function addSegForm() {

    const maxSeg = 4;    
    let formsContainer = document.getElementById('seg-container');
    let n_seg = document.querySelectorAll('.seg-form').length
    // Check if maximum limit reached
    if (n_seg >= maxSeg) {
        alert("Alcanzaste el limite de programas de seguridad.");
        return;
    }

    let formItem = document.createElement('div');
    formItem.classList.add('seg-form');

    formItem.innerHTML = `
        <h5 class="my-2">Programa de ofimática N° ${n_seg + 1}</h5>
        <div class="row">
            <div class="col-md-6">
            <label for="nombre_sw">Nombre:</label>
            <input name="nombre_sw" placeholder="Nombre del Software" type="text" autocomplete="off" class="form-control mb-2">
            </div>
            <div class="col-md-6">
            <label for="version_sw">Versión:</label>
            <input name="version_sw" placeholder="Versión" type="text" autocomplete="off" class="form-control mb-2">
            </div>
        </div>
        <div class="row">
            <div class="col-md-6">
            <label for="desarrollador_sw">Desarrollador:</label>
            <input name="desarrollador_sw" placeholder="Desarrollador" type="text" autocomplete="off" class="form-control mb-2">
            </div>
            <div class="col-md-6">
            <label for="licencia_sw">Licencia:</label>
            <input name="licencia_sw" placeholder="Licencia" type="text" autocomplete="off" class="form-control mb-2">
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
            <input name="categoria_sw" value="seguridad" type="hidden">
            <input name="id_equipo_hw" value="{{ id_equipo }}" type="hidden">
            </div>
        </div>
    `;
    formsContainer.appendChild(formItem);
} 

// Event listener for the Add Item button. COMMENTED BCS BUTTON ONCLICK
// document.getElementById('addFormBtn').addEventListener('click', addForm);


// ------- DEMAS --------
function addOtroSwForm() {

    const maxOtroSw = 20;    
    let formsContainer = document.getElementById('otrosw-container');
    let n_otro_sw = document.querySelectorAll('.otrosw-form').length

    // Check if maximum limit reached
    if (n_otro_sw >= maxOtroSw) {
        alert("Alcanzaste el limite de programas añadidos.");
        return;
    }

    let formItem = document.createElement('div');
    formItem.classList.add('otrosw-form');

    formItem.innerHTML = `
        <h5 class="my-2">Software añadido N° ${n_otro_sw + 1}
        <div class="row">
            <div class="col-md-6">
            <label for="categoria_sw">Categoría:</label>
            <select name="categoria_sw" class="form-control mb-2">
                <option selected value="">Ninguno</option>
                <option value="multimedia">Multimedia</option>
                <option value="diseño grafico">Diseño grafico</option>
                <option value="diseño audiovisual">Diseño Audiovisual</option>
                <option value="sistema">Sistema</option>
                <option value="administrativo">Administrativo</option>
                <option value="comunicacion">Comunicación</option>
                <option value="desarrollo">Desarrollo</option>
                <option value="videojuego">Juegos</option>
                <option value="otro">Otro</option>
            </select>
            </div>
            <div class="col-md-6">
            <label for="nombre_sw">Nombre:</label>
            <input name="nombre_sw" placeholder="Nombre del Software" type="text" autocomplete="off" class="form-control mb-2">
            </div>
        </div>
        <div class="row">
            <div class="col-md-6">
            <label for="version_sw">Versión:</label>
            <input name="version_sw" placeholder="Versión" type="text" autocomplete="off" class="form-control mb-2">
            </div>
            <div class="col-md-6">
            <label for="desarrollador_sw">Desarrollador:</label>
            <input name="desarrollador_sw" placeholder="Desarrollador" type="text" autocomplete="off" class="form-control mb-2">
            </div>
        </div>
        <div class="row">
            <div class="col-md-6">
            <label for="licencia_sw">Licencia:</label>
            <input name="licencia_sw" placeholder="Licencia" type="text" autocomplete="off" class="form-control mb-2">
            </div>
            <div class="col-md-6">
            <input name="id_equipo_hw" value="{{ id_equipo }}" type="hidden">
            </div>
        </div>
    `;
    formsContainer.appendChild(formItem);
} 

// Event listener for the Add Item button. COMMENTED BCS BUTTON ONCLICK
// document.getElementById('addFormBtn').addEventListener('click', addForm);
