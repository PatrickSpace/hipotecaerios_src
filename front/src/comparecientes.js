class Comparecientes {
    constructor() {
        //this.indx;
    }

    async seleccion(event) {
        console.log("click");
        let ids = [];
        var compList = document.getElementById('item-child')
        if (!compList) {
            ids = [];
        } else {
            var everyChild = document.querySelectorAll("#item-child")//("#comparecientes-list")
            console.log("cantidad: ", everyChild.length)
            for (let index = 0; index < everyChild.length; index++) {
                //console.log(everyChild[index].children["name-click-"+index])
                ids.push("name-click-"+index)
            }
        }



        const click = event.srcElement.id
        this.indx=ids.indexOf(click)
        console.log(this.indx, click)
        if (ids.includes(click)) {
            console.log("existe")
            document.querySelector("#"+click).style.color = "#de4c8a"
            const indice = ids.indexOf(click)
            console.log(documentacion.data.comparecientes[indice])
            const keysComparecientes = Object.keys(documentacion.data.comparecientes[indice])
            keysComparecientes.forEach(element => {
                document.getElementById("compa-"+element).value = documentacion.data.comparecientes[indice][element]
            });
        }
    };
    
    async seleccion2(event) {
        let lsdata = JSON.parse( localStorage.getItem('data'))
        console.log("data", lsdata)
        const click = event.srcElement.id
        let numberOfClick = parseInt(click.split("-")[click.split("-").length - 1])
        console.log(click, numberOfClick)
        localStorage.setItem('numberOfClick',JSON.stringify(numberOfClick))
        //this.numberOfClick = numberOfClick
        this.indx = numberOfClick
        console.log(this.indx, ".....", this.numberOfClick)
        document.querySelector("#" + click).style.color = "#de4c8a"
        console.log(lsdata.comparecientes[numberOfClick])
        const keysComparecientes = Object.keys(lsdata.comparecientes[numberOfClick])
            keysComparecientes.forEach(element => {
                document.getElementById("compa-"+element).value = lsdata.comparecientes[numberOfClick][element]
            });
    }

    async cantidades() {
        let ids = [];
        var compList = document.getElementById('item-child')
        if (!compList) {
            ids = [];
        } else {
            var everyChild = document.querySelectorAll("#item-child")//("#comparecientes-list")
            console.log("cantidad: ", everyChild.length)
            for (let index = 0; index < everyChild.length; index++) {
                //console.log(everyChild[index].children["name-click-"+index])
                ids.push("name-click-"+index)
            }
        }
        return ids
    };

    async actualizar() {
        
        const buttonAgregar = document.getElementById("process-btn-comparecientes");
        await buttonAgregar.addEventListener('click', async(event) => {
            console.log("actualizar")
            const kardexNumber = document.getElementById("kardex-input")
            const lsdata = JSON.parse( localStorage.getItem('data'))
            const kardex = await documentContentInfo({
                "data": lsdata,
                "kardex": kardexNumber
            }, 'crear-compareciente')
        });
    };

    async añadir(){ 
        const d = document;
        var lsdata = JSON.parse( localStorage.getItem('data'))
    
        const nombre= d.getElementById('compa-nombre').value
        const nacionalidad= d.getElementById('compa-nacionalidad').value
        const estadoCv= d.getElementById('compa-estado civil').value
        const profesion= d.getElementById('compa-profesion').value
        const domicilio= d.getElementById('compa-domicilio').value
        const dni= d.getElementById('compa-dni').value
        const representante= d.getElementById('compa-representante').value
        const genero= d.getElementById('compa-genero').value
        
        
    
    
        let data= {
            nombre,
            nacionalidad,
            "estado civil": estadoCv,
            profesion,
            domicilio,
            dni,
            representante,
            genero
        };
        lsdata.comparecientes.push(data)
        console.log(lsdata)
        localStorage.setItem('data',JSON.stringify(lsdata))
    
        documentacion.displayData(lsdata)
        documentacion.guardar(lsdata)
    
    
    }
    
    async eliminar(){
        //console.log(e.target)
        let lsDataE = JSON.parse(localStorage.getItem('data'));
        const lsNumberClick = JSON.parse(localStorage.getItem('numberOfClick'))
        lsDataE.comparecientes.splice(lsNumberClick, 1)
        console.log(lsDataE)
    
        localStorage.setItem('data',JSON.stringify(lsDataE))
        documentacion.displayData(lsDataE)
        
        documentacion.guardar(lsDataE)
    
    }
      
    procesar(){
        let data = localStorage.getItem('data').comparecientes,
    
        //EndPoint
        url="http://localhost:5544/api/bothip/crear-compareciente"; // COLOCAR LA RUTA
       // console.log(ls.getItem('data'))
       // console.log(JSON.parse(ls.getItem('data')))
       
        fetch(url,{
            method:'POST',
            headers:{
                'Content-Type':'application/json;charset=utf-8'
            },
            body:JSON.stringify(data)
        }).then(res=>{
            if(res.ok){
              res.json()
              form.reset()
            }else{
                Promise.reject(res)
            }
        }).then(text=>{
            console.log(text)
        })
        .catch(err=>{
            console.log(err  )
        })
    }
}

comparecientes = new Comparecientes()

document.getElementById('process-btn-comparecientes-añadir').onclick =comparecientes.añadir
document.getElementById('process-btn-comparecientes-eliminar').onclick =comparecientes.eliminar
//document.getElementById('process-btn-comparecientes').onclick =comparecientes.procesar
document.getElementById('comparecientes-list').onclick = comparecientes.seleccion2
comparecientes.actualizar();