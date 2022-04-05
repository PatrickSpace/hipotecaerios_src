const genDoc = async () => {
    const generateButtom = document.getElementById("btn-generate");
    generateButtom.addEventListener('click', async(event) => {
        console.log("Nueva funcion: generando doc")
        const kardex = await documentContentInfo({
            "kardex": document.getElementById('kardex-input').value
        }, 'generar');
        if (kardex.mensaje != "Documento generado") {
            alert("El proyecto no está abierto. Diríjase a Documentación")
        } else {
            alert("Documento Generado!")
        }
    })
};

genDoc();