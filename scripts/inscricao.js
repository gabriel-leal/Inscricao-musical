let servidorapi = "http://localhost:5000";
let servidorweb = "http://localhost:8000";

addEventListener('load', () => {

    fetch(`${servidorapi}/totalinscritos`)
        .then(T => T.json())
        .then((data) => {
            let totalins = data['totalinscritos']
            if(totalins > 210) {
                window.location.href = `/espera.html`;
            }
        });

})

document.getElementById('formulario').addEventListener('submit', async function(event) {
    event.preventDefault();
    // cont ++;
    let nome = document.getElementById('inome').value;
    nome = capitalizeWords(nome);
    let datanas = document.getElementById('idata').value;
    let anodata = datanas.split('/')[2]
    let tel = document.getElementById('itel').value;
    let mem = document.getElementById('imem').value;
    if(document.getElementById('imem').checked == true) {   
        mem = true
    } else {  
        mem = false      
    };
    let inscricao = {"nome": `${nome}`, "datanas": `${datanas}`, "telefone": `${tel}`, "membro": `${mem}`}; 

    try {
        var flgrava = 0;
        if (anodata >= 2020) {
            const errocrianca = await fetch(`${servidorapi}/totalcriancas`, {
                    method: 'get'
                });
            const datacrianca = await errocrianca.json();
            var criancas = JSON.parse(datacrianca)
            if (criancas['erro'] == 3) {
                flgrava = 1;
                document.getElementById('erro').innerHTML = "Limite de Crianças foi atingido! Sentimos muito"
                showmodalE();
            }
        }
        if (flgrava == 0) {
            const response = await fetch(`${servidorapi}/inscricao`, {
                method: 'post',
                mode: "cors",
                headers: { 
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': '*',
                    'Access-Control-Allow-Headers': '*',
                    'content-type': 'application/json' 
                },
                body: JSON.stringify(inscricao)
            });
            const data = await response.json();
            if(!response.ok) { throw "Erro na chamada da API"};
            let param = JSON.parse(data);
            if (param['erro'] == 1) {
                let nomePai = param['nome'].split(" ")[0];
                document.getElementById('erro').innerHTML = `Você já é dependente do(a) <strong>${nomePai}</strong>.`
                showmodalE();
            };
            if (param['nome'] != nome && param['erro'] === 2) {
                document.getElementById('erro').innerHTML = "Esse número de telefone já foi cadastrado por alguém!!"
                showmodalE();
            };
            if (param['erro'] == 0) {
                sessionStorage.setItem('id', param['id']);
                sessionStorage.setItem('nome', param['nome']);
                buscaDependente(param['id']);
                window.location.href = `/inscrito.html`;
            };
        }
    
    }catch (error) {
        console.error(error);
    };

});

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

function buscaDependente(idPai){
    let dependente = {"idPai": `${idPai}`}
    fetch(`${servidorapi}/procuradep`, {
        method: 'post',
        headers: {
            'content-type': 'application/json'
        },
        body: JSON.stringify(dependente)
    }).then(res => res.json()).then(data => {
        let param = data
        sessionStorage.setItem('dep', param);
    });
};

function capitalizeWords(str) {
    return str.split(' ') 
              .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()) 
              .join(' '); 
}

$('#idata').mask('00/00/0000');
$('#itel').mask('(00) 00000-0000');