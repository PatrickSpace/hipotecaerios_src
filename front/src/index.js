const direction = 'localhost';
const port = '5544';

//DOC_URL = 'res.json'

const documentContentInfo = async function (body, endpoint) {
    
    const myHeaders = new Headers();
    myHeaders.append('Content-Type', 'application/json');
    myHeaders.append('Accept', 'application/json');
    myHeaders.append('Access-Control-Allow-Origin', '*');
    
    const url = "http://" + direction + ":" + port + "/api/bothip/" + endpoint;
    
    const responsePromise = await fetch(url,{
        method: 'POST',
        mode: 'cors',
        headers: myHeaders,
        body: JSON.stringify(body)
    });

    const response = await responsePromise.json();

    return response   
}

const documentContentDocument = async function (body, endpoint, params={}) {
    
    const myHeaders = new Headers();
    myHeaders.append('Content-Type', 'multipart/form-data');
    myHeaders.append('Accept', 'application/json');
    myHeaders.append('Access-Control-Allow-Origin', '*');

    const url = new URL("http://" + direction + ":" + port + "/api/bothip/" + endpoint);

    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))

    const responsePromise = await fetch(url,{
        method: 'POST',
        mode: 'cors',
        //headers: myHeaders,
        body: body,
        
    });

    const response = await responsePromise.json();
    

    return response   
}

//multiparm form data 