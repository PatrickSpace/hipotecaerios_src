const main = async () => {
  const keysComparecientesM = ["nombre", "nacionalidad", "estado civil", "profesion", "domicilio", "dni", "representante", "genero"];
  const keysDatosM = ["nombre", "ruc", "domicilio"];
  const getData = async (data) => {

      let keysDatos = Object.keys(data.banco);
      let keysComparecientes = Object.keys(data.comparecientes[0]);

      keysDatos.forEach(nameKeys => document.getElementById('process-banco-' + nameKeys).textContent = data.banco[nameKeys]);

      keysDatos.forEach(nameKeys => document.getElementById('process-inmobiliaria-' + nameKeys).textContent = data.inmobiliaria[nameKeys]);

      const HTMLResponse = document.querySelector('#comparecientes-list');

      let count = 0;
      let idArray = [];

      while (HTMLResponse.firstChild) {
        HTMLResponse.removeChild(HTMLResponse.firstChild);
      }

    
      for(let item of data.comparecientes) {
        //console.log("item ", item)
        HTMLResponse.insertAdjacentHTML("beforeend",`<div id = "item-child" class=" flex justify-start cursor-pointer text-gray-700 hover:text-white hover:bg-gray-800 rounded-md px-2 py-2 my-2">
        <span class="bg-gray-800 h-2 w-2 m-2 rounded-full"></span>
        <div id="name-click-${count}"  class="hijo flex-grow font-medium px-2">${item.nombre}</div>
        <div class="text-sm font-normal text-gray-500 hover:text-white tracking-wide">${item.representante}</div>
        </div>`);
        idArray.push('name-click-' + count);
        count += 1;
      }
      
    let selector;
      
      const captureClick = async (e) => {
          
          click = e.srcElement.id
          if(idArray.includes(click)){
              selector = idArray.indexOf(click);
              await getComparecientes(selector);
          }

        
      }
      
      const getComparecientes = async (selector) => {
      
          const nameSele = document.querySelector('#name-click-' +  selector);
          console.log('#name-click-' +  selector)   
          
          await nameSele.addEventListener('click', (event) => {

              nameSele.style.color = "#de4c8a";
              
              keysComparecientes.forEach(namekeys => document.getElementById('compa-' + namekeys).value = data.comparecientes[selector][namekeys]);
            });  
      }

      const updateJsonDatos = async (entidad) => {

          const processDatos = document.getElementById('process-btn-datos');
          
          await processDatos.addEventListener('click', async (event) => { 
                  
              keysDatos.forEach(nameKeys => data[entidad][nameKeys] = document.getElementById('process-' + entidad + '-' + nameKeys).textContent);
              data = await documentContentInfo(data, "documentacion");
              getData(data)
                  
          })
        
      }

      const updateJsonComparecientes = async () =>{


          const processComparecientes = document.getElementById('process-btn-comparecientes');

          await processComparecientes.addEventListener('click', async (event) => { 
            console.log("selector ", selector)
            if(selector != undefined){
              keysComparecientes.forEach(nameKeys => data.comparecientes[selector][nameKeys] = document.getElementById('compa-' + nameKeys).value);
              data = await documentContentInfo(data, "comparecientes");
              console.log("data: ", data)
              getData(data)
            }
          })
        
      }

      //1
      

      

      
      updateJsonDatos('banco');
      updateJsonDatos('inmobiliaria');
      generateDocument(); 
      //updateJsonComparecientes();
      document.getElementById('comparecientes-list').onclick =  await captureClick;
    
  }

  const uploadFile = async (selector,jsonName, formData) => {

      const fileSelector = document.getElementById('file-selector-' + selector);
      const nameSelector = document.getElementById('name-selector-' + selector);
      
      await fileSelector.addEventListener('change', (event) => {

        //const isEmpty = Object.values(formData).every(x => (x === null || x === ''));
          //if (isEmpty === false) {
          if(Object.keys(jsonName).length === 0){
    
          const termInteraction = ['minuta', 'clausula', 'contrato'];
    
          for (const prop of termInteraction) {
            document.getElementById('line-color-alert-' + prop).style.borderColor = "rgb(229, 231, 235)";
            document.getElementById('name-selector-' + prop).value = "";
          }
        }
        
        let fileList = event.target.files;
        let output = [];
        for (let i = 0, f; f = fileList[i]; i++) {
          formData.append('file-' + selector + '-'+ i ,fileList[i])
        output.push(f.name)}
        nameSelector.value = output;
        jsonName[selector] = output;
      })     
  }      
            
  const process = async (idProcess, jsonName, formData) => {
    
    const buttonProcess = document.getElementById(idProcess);
      
    await buttonProcess.addEventListener('click', async (event) => {

      
      //const isEmpty = Object.values(formData).every(x => (x === null || x === ''));
    
      //if (isEmpty === false) {
      //if( Object.keys(jsonName).length != 3 || !document.getElementById('select-inmobiliaria').value || !document.getElementById('select-banco').value  ){
      if( Object.keys(jsonName).length === 0 || !document.getElementById('select-inmobiliaria').value || !document.getElementById('select-banco').value ){
        //or () or ()
        const termInteraction = ['minuta', 'clausula', 'contrato'];
          
        termInteraction.forEach(prop => document.getElementById('line-color-alert-' + prop).style.borderColor = "#c53030");

        termInteraction.forEach(prop => document.getElementById('name-selector-' + prop).value = "No ha seleccionado un archivo");

        if ( !document.getElementById('select-inmobiliaria').value && !document.getElementById('select-banco').value && (Object.keys(jsonName).length != 0)) {
          alert("Requiere ingresar datos del banco, inmobiliaria y archivos.")
        } else if (Object.keys(jsonName).length === 0) {
          alert("Falta seleccionar al menos un archivo.")
        } else if (!document.getElementById('select-inmobiliaria').value || !document.getElementById('select-banco').value ) {
          alert("Requiere ingresar datos del banco e inmobiliaria.")
        }

      } else {

        const bankData = {
          "banco": document.getElementById('select-banco').value,
          "inmobiliaria": document.getElementById('select-inmobiliaria').value
        }

        data = await documentContentDocument(formData,"documentacion", bankData);
        document.getElementById('kardex-input').value = data.kardex
        getData(data)
        if (data) {
          alert("Documento Generado!")
        }
      }
    })
  }

  const closeIt = () => {
    
    const termInteraction = ['minuta', 'clausula', 'contrato'];
    const keysComparecientes = ["nombre","nacionalidad","estado civil","profesion","domicilio","dni","representante", "genero"];
    
    termInteraction.forEach(prop => document.getElementById('line-color-alert-' + prop).style.borderColor = "rgb(229, 231, 235)");

    termInteraction.forEach(prop => document.getElementById('name-selector-' + prop).value = "");
    
    keysComparecientes.forEach(nameKeys => document.getElementById('compa-' + nameKeys).value = "");

    return "Any string value here forces a dialog box to \n" + 
    "appear before closing the window.";
  }

  /*const generateDocument = () => {

    const generateButtom = document.getElementById("btn-generate");
    console.log("Generate Final Document")
    generateButtom.addEventListener('click', async (event) => { 
      const kardex = await documentContentInfo({
        "kardex": document.getElementById('kardex-input').value
      }, 'generar');
      console.log("kardex ", kardex)
      if (kardex.mensaje != "Documento generado") {
        alert("El proyecto no está abierto. Dirijase a documentación")
      } else {
        alert("Documento generado")
      }

    })
  }*/
  
  const testing = async () => {
    const updateData = document.getElementById('process-btn-comparecientes')
    await updateData.addEventListener('click', async (event) => {
      let data = {};
      keysComparecientesM.forEach(nameKey => {
        //console.log(document.getElementById('compa-'+nameKey).value)
        data[nameKey] = document.getElementById('compa-'+nameKey).value
      });
      const body = {
        compareciente: data,
        kardex: document.getElementById('kardex-input').value
      }
      //console.log("body ", body)
      dataOut = await documentContentInfo(body, "comparecientes");
      //console.log("data: ", dataOut)
      getData(dataOut)
    })
  }

  const $formSelector = document.querySelector('#form-minuta');
  const formData = new FormData($formSelector)
  const jsonName = new Object();

  //generateDocument();
  testing();

  uploadFile('minuta', jsonName,formData)
  uploadFile('clausula', jsonName,formData)
  uploadFile('contrato', jsonName,formData)
  await process('click-selector-procesar',jsonName, formData)
  window.onbeforeunload = closeIt;

}

main()