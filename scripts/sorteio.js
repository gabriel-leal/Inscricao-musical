let servidorapi = "http://localhost:5000";
let servidorweb = "http://localhost:8000";

const btn = document.getElementById("btn");
var load = document.getElementById("carregando");
var resposta = document.getElementById("res");
var secao = document.getElementsByTagName("section")[0];
const jsConfetti = new JSConfetti();

let datatmp = JSON.parse(localStorage.getItem("lista"))
let data = []
datatmp.forEach(e => {
    if (e.presenca == 1) {
        batata = {"id": `${e.id}`, "nome": `${e.nome}`}
        data.push(batata)
    }
});

btn.addEventListener("click", async () => {
    resposta.style.display = "none"; 
    load.style.display = "block";  
    secao.style.backgroundColor = "white";
    secao.style.boxShadow = "0px 0px 10px rgba(0, 0, 0, 0.468)";
    await sleep(2000);        
    const sorteado = sortearPessoa();
    resposta.innerHTML = `ID: ${sorteado.id} <br>Nome: ${sorteado.nome}`;     
    load.style.display = "none";
    resposta.style.display = "block"; 
    jsConfetti.addConfetti();
});

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
};

function sortearPessoa() {
    const indice = Math.floor(Math.random() * data.length);
    return data[indice];
};