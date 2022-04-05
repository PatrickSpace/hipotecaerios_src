class Documentacion {
    constructor() {
        this.jsonName = {}
        this.formData = {}
        this.data = {}
    }

    async procesar(idProcess, formData) {
        const buttonProcess = await document.getElementById(idProcess)
       
        const allButton = document.querySelectorAll(".btnAll");
         
        await buttonProcess.addEventListener('click', async(event) => {
            console.log("se pulsó el botón y se instancio clase")
            this.data = {}
            const entidades = {
                banco: "banco",
                inmobiliaria: "inmobiliaria"
            }

            for(let i=0, len = allButton.length;i<len;i++){
                allButton[i].disabled=true
                allButton[i].classList.add('opacity-50')
                allButton[i].classList.remove('hover:bg-gray-800','hover:bg-white','hover:text-red-700')
                
                
               
            }

            const fileMinuta = await document.getElementById("file-selector-minuta").value
            const fileClausula = await document.getElementById("file-selector-clausula").value
            const fileContrato = await document.getElementById("file-selector-contrato").value

            if (!fileMinuta && !fileClausula && !fileContrato) {
                alert("Debe ingresar un documento")
            } else {
                
                var carga = await this.statusBar()
                const data = await documentContentDocument(formData,"documentacion");
                
                localStorage.setItem('data',JSON.stringify(data))
                const getData=JSON.parse(localStorage.getItem('data'))
                this.data = data;
                console.log(data)
                
                await this.displayData(getData) //
                if (data) {
                    
                    carga.style.width = "100%";
                    carga.textContent = "100";
                    await alert('Documento Generado!')
                    for(let i=0, len = allButton.length;i<len;i++){
                        allButton[i].disabled=false
                        allButton[i].classList.remove('opacity-50')
                        allButton[i].classList.add('hover:bg-gray-800','hover:bg-white','hover:text-red-700')
                        
                        
                       
                    }
          

                }
            }
        })
    }

    async promiseStatus() {
        return new Promise( (resolve, reject) => {
            setTimeout(() => {
                let fine = true;
                if (fine) {
                    resolve("bien")
                } else {
                    reject("mal")
                }
            }, 2000)
        })

    }

    async statusBar() {
        let width = 0,
        id = setInterval(await frame, 100),
        carga = document.querySelector(".progress");
        carga.style.width = "0%";
        carga.textContent = "0";
        async function frame() {
            const varWidth = Math.floor(Math.random()*(80-70+1)+70)
            if (width >= varWidth) {
                clearInterval(id);
            } else {
                width++;
                carga.style.width = `${width}%`;
                carga.textContent = width;
            }
        }

        return carga
    }

    async statusBarG() {
        let width = 0,
        id = setInterval(await frame, 100),
        carga = document.querySelector(".progressG");
        carga.style.width = "0%";
        carga.textContent = "0";
        async function frame() {
            const varWidth = Math.floor(Math.random()*(80-60+1)+60)
            if (width >= varWidth) {
                clearInterval(id);
            } else {
                width++;
                carga.style.width = `${width}%`;
                carga.textContent = width;
            }
        }

        return carga
    }


    async uploadFile(selector) {
        const fileSelector = document.getElementById('file-selector-' + selector);
        const nameSelector = document.getElementById('name-selector-' + selector);
        await fileSelector.addEventListener('change', async(event) => {
            console.log("el documento cambió")
            let fileList = event.target.files;
            console.log(fileList)
            let output = [];
            for (let i = 0, f; f = fileList[i]; i++) {
                formData.append('file-' + selector + '-'+ i ,fileList[i])
                output.push(f.name)
            }
            nameSelector.value = output;
            this.jsonName[selector] = output;
            console.log(this.jsonName)
            //console.log("form -- ", formData)
        })
    };

    async displayData(data) {
        const keysComparecientesM = ["nombre", "nacionalidad", "estado civil", "profesion", "domicilio", "dni", "representante", "genero"];
        if (data.banco !== undefined) {
            let keysDatosBanco = Object.keys(data.banco)
            keysDatosBanco.forEach(nameKeys => document.getElementById('process-banco-' + nameKeys).textContent = data.banco[nameKeys]);
        }

        if (data.inmobiliaria !== undefined) {
            let keysDatosInmo = Object.keys(data.inmobiliaria)
            keysDatosInmo.forEach(nameKeys => document.getElementById('process-inmobiliaria-' + nameKeys).textContent = data.inmobiliaria[nameKeys]);
        }
        
        document.getElementById('kardex-input').value = data.kardex ? data.kardex : null

        if (data.comparecientes !== undefined) {
            const HTMLResponse = document.querySelector('#comparecientes-list');
            while (HTMLResponse.firstChild) {
                HTMLResponse.removeChild(HTMLResponse.firstChild)
            }
            //console.log(document.querySelector('#comparecientes-list'))
    
            let count = 0;
            let idArray = [];
    
            for(let item of data.comparecientes) {
                //console.log("item ", item)
                HTMLResponse.insertAdjacentHTML("beforeend",`<div id = "item-child-${count}" class=" flex justify-start cursor-pointer text-gray-700 hover:text-white hover:bg-gray-800 rounded-md px-2 py-2 my-2">
                <span class="bg-gray-800 h-2 w-2 m-2 rounded-full"></span>
                <div id="name-click-${count}"  class="hijo flex-grow font-medium px-2">${item.nombre}</div>
                <div class="text-sm font-normal text-gray-500 hover:text-white tracking-wide uppercase">${item.representante}</div>
                </div>`);
                idArray.push('name-click-' + count);
                count += 1;
            }
        }
        
        //console.log(document.querySelector('#comparecientes-list'))
        
    };

    async generar() {
        const buttonGenerate = document.getElementById("btn-generate");
        //let kardex = ""
        await buttonGenerate.addEventListener('click', async(event) => {
            var carga = await this.statusBarG()
            const kardex = await documentContentInfo({
                "kardex": document.getElementById("kardex-input").value
            }, 'generar')

            if (typeof(kardex) !== "undefined") {
                console.log("kardex: ", kardex)
                if (kardex.mensaje != "Documento generado") {
                    alert("El proyecto no está abierto. Diríjase a Documentación")
                } else {
                    alert("Documento Generado!")
                    carga.style.width = "100%";
                    carga.textContent = "100";
                }
            }
        });
        //console.log(typeof(kardex), typeof(kardex) === "undefined")
    }

    async guardar(datals){
        console.log("guardar")
        //this.data = JSON.parse(datals)
    }

};


const documentacion = new Documentacion();
const $formSelector = document.querySelector('#form-minuta');
const formData = new FormData($formSelector)

documentacion.uploadFile('minuta', formData);
documentacion.uploadFile('clausula', formData);
documentacion.uploadFile('contrato', formData);
documentacion.procesar('click-selector-procesar', formData);

documentacion.generar();