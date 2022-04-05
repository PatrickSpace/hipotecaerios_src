const viewData = async (selector) => {

    const nameSele = document.querySelector('#name-click-' +  selector);
    
    nameSele.addEventListener('click', (event) => {

    nameSele.style.color = "#de4c8a";
  

    const xhttp = new XMLHttpRequest();
  
    xhttp.open('GET', 'comparecientes.json', true);
  
    xhttp.send();
  
    xhttp.onreadystatechange = function() {
      if(this.readyState == 4 && this.status == 200){
        let comparecientes = JSON.parse(this.responseText)
  
        document.getElementById('compa-nombre').value = comparecientes[0]['comparecientes_'+ selector].nombre ;
        document.getElementById('compa-nacionalidad').value = comparecientes[0]['comparecientes_'+ selector].nacionalidad ;
        document.getElementById('compa-estadocivil').value = comparecientes[0]['comparecientes_'+ selector].estadocivil ;
        document.getElementById('compa-profesion').value = comparecientes[0]['comparecientes_'+ selector].profesion ;
        document.getElementById('compa-domicilio').value = comparecientes[0]['comparecientes_'+ selector].domicilio ;
        document.getElementById('compa-dni').value = comparecientes[0]['comparecientes_'+ selector].dni ;
      
      }      
    }
  })

}

const dataCompareciente1 = viewData('1')
const dataCompareciente2 = viewData('2')
const dataCompareciente3 = viewData('3')
const dataCompareciente4 = viewData('4')
const dataCompareciente5 = viewData('5')

const createJSON = async () => {

    const processSelector = document.getElementById('process-btn');

    let jsonCompa = {};
    let count = 0;
    let jsonTemp = {};
    
    await processSelector.addEventListener('click', (event) => {

        count += 1 ;
        jsonTemp['nombre'] = document.getElementById('compa-nombre').value;
        jsonTemp['nacionalidad'] = document.getElementById('compa-nacionalidad').value;
        jsonTemp['estadocivil'] = document.getElementById('compa-estadocivil').value;
        jsonTemp['profesion'] = document.getElementById('compa-profesion').value;
        jsonTemp['domicilio'] = document.getElementById('compa-domicilio').value;
        jsonTemp['dni'] = document.getElementById('compa-dni').value;
        jsonCompa['comparecientes' + count.toString()] = jsonTemp;
        console.log(jsonTemp)
        console.log(jsonCompa);
    })

    return jsonCompa 
}

const jsonCompa = createJSON()

const createJSON2 = async () => {

    const processSelector = document.getElementById('process-btn-banco');

    let jsonBanInm = {};
    let jsonTemp = {};
    
    await processSelector.addEventListener('click', (event) => {

        for (let item of ['banco', 'inmobiliaria']){
            console.log('process-' + item  + '-nombre');
            jsonTemp['nombre'] = document.getElementById('process-' + item  + '-nombre').innerText;
            jsonTemp['ruc'] = document.getElementById('process-' + item + '-ruc').innerText;
            jsonTemp['domicilio'] = document.getElementById('process-' + item + '-domicilio').innerText;
            jsonBanInm[item] = jsonTemp;
            console.log(jsonTemp)
            console.log(jsonBanInm);
            }
        });

    return jsonBanInm
}


const jsonBanInm = createJSON2()

