let servidorapi = "http://localhost:5000";
let servidorweb = "http://localhost:8000";

let nomePai = sessionStorage.getItem('nome').split(" ")[0];
let idPai = sessionStorage.getItem('id');
document.getElementById('pai').innerHTML = nomePai;

document.getElementById('formulario').addEventListener('submit', function(event) {
    event.preventDefault();
    let nome = document.getElementById('inome').value;
    nome = capitalizeWords(nome);
    let datanas = document.getElementById('idata').value;
    let tel = document.getElementById('itel').value;
    let mem = document.getElementById('imem').value;
    if(document.getElementById('imem').checked == true) {   
        mem = true
        } else {  
        mem = false      
        };
    let dependente = {"idPai": `${idPai}`, "nome": `${nome}`, "datanas": `${datanas}`, "telefone": `${tel}`, "membro": `${mem}`};
    fetch(`${servidorapi}/dependente`, {
        method: 'post',
        headers: {
            'content-type': 'application/json'
        },
        body: JSON.stringify(dependente)
    }).then(res => res.json()).then(data => {
        let param = data
        sessionStorage.setItem('dep', param);
        window.location.href = `/inscrito.html`;
});
});

function capitalizeWords(str) {
    return str.split(' ') 
              .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()) 
              .join(' '); 
}

$('#idata').mask('00/00/0000');
$('#itel').mask('(00) 00000-0000');