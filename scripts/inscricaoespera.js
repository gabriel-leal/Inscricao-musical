let servidorapi = "http://localhost:5000";
let servidorweb = "http://localhost:8000";


document.getElementById('formulario').addEventListener('submit', async function (event) {
    event.preventDefault()
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

    let inscricao = {"nome": `${nome}`, "datanas": `${datanas}`, "telefone": `${tel}`, "membro": `${mem}`}; 

    // $.post(`${servidorapi}/filaespera`, JSON.stringify(inscricao),
    // function(status){
    //     console.log("Status: " + status);
    // });

    try {
        const response = await fetch(`${servidorapi}/filaespera`, {
            method: 'post',
            body: JSON.stringify(inscricao)
        });
        const data = await response.json();
        if(!response.ok) { throw "Erro na chamada da API"};
        let param = JSON.parse(data);

        if (param['erro'] == 2) {
            document.getElementById('erro').innerHTML = "Esse número de telefone já foi cadastrado por alguém!! Caso queira adicionar alguém sem telefone, pode deixar em branco"
            showmodalE();
        };
        if (param['erro'] == 0) {
            sessionStorage.setItem('id', param['id']);
            sessionStorage.setItem('nome', param['nome']);
            window.location.href = `/incritoespera.html`;
        };
    
    }catch (error) {
        console.error(error);
    };

})


const modalP = document.querySelector("dialog#politica");
const btnD = modalP.querySelector("button");

function showmodalP() {
    modalP.showModal();
    btnD.blur();
    modalP.scrollTop = 0;
    modalP.classList.add('show');
    modalP.classList.remove('hide');
    document.body.classList.add('no-scroll');
};

function hidemodalP() {
    modalP.classList.remove('show');
    document.body.classList.remove('no-scroll');
    modalP.classList.add('hide');
    setTimeout(() => {
        modalP.close();
    }, 300);
};

const modalE = document.querySelector("dialog#error");

function showmodalE() {
    modalE.showModal();
    btnD.blur();
    modalE.scrollTop = 0;
    modalE.classList.add('show');
    modalE.classList.remove('hide');
    document.body.classList.add('no-scroll');
};

function hidemodalE() {
    modalE.classList.remove('show');
    document.body.classList.remove('no-scroll');
    modalE.classList.add('hide');
    setTimeout(() => {
        modalE.close();
    }, 300);
};

function capitalizeWords(str) {
    return str.split(' ') 
              .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()) 
              .join(' '); 
}

$('#idata').mask('00/00/0000');
$('#itel').mask('(00) 00000-0000');