let servidorapi = "http://localhost:5000";
let servidorweb = "http://localhost:8000";


const cardContainer = document.querySelector(".card-container");
const searchInput = document.querySelector("#searchInput");

document.querySelector("#lupa").addEventListener("click", function(){
    var box = document.getElementById("searchInput")
    if(box.style.display == "none"){
        box.style.display = "block"
    } else {
        box.style.display = "none"
    }

});

var data = '';

async function getData() {
    const url = `${servidorapi}/buscaPessoas`;
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
  
      const json = await response.json();
    } catch (error) {
      console.error(error.message);
    }
}

if(localStorage.getItem("lista") === null) {

    fetch(`${servidorapi}/buscaPessoas`)
        .then(T => T.json())
        .then((data) => {
            localStorage.setItem("lista", JSON.stringify(data));
            displayData(data);
        });
} else {
    localStorage.removeItem("lista");

    fetch(`${servidorapi}/buscaPessoas`)
    .then(T => T.json())
    .then((data) => {
        localStorage.setItem("lista", JSON.stringify(data));
        displayData(data);
    });    
};

function displayData (data) {
    cardContainer.innerHTML = "";
    let total = 0
    let criancas = 0
    data.forEach(e => {
        if (e.presenca == 1 && e.nome != 'Total') {
            if (e.idpai > 0) {
                cardContainer.innerHTML += 
                `<tr>
                    <td class="presente cetralizacoluna" onclick="marcarPresenca(this, ${e.id})">${e.id}</td>
                    <td class="presente dependente" onclick="marcarPresenca(this, ${e.id})">${e.nome}</td>
                    <td class="presente cetralizacoluna" onclick="marcarPresenca(this, ${e.id})"><i class="bi bi-check2"></i></td>
                </tr>`
            }
            if (e.idpai == 0) {
                cardContainer.innerHTML += 
                `<tr>
                    <td class="presente cetralizacoluna" onclick="marcarPresenca(this, ${e.id})">${e.id}</td>
                    <td class="presente linhapai" onclick="marcarPresenca(this, ${e.id})">${e.nome}</td>
                    <td class="presente cetralizacoluna" onclick="marcarPresenca(this, ${e.id})"><i class="bi bi-check2"></i></td>
                </tr>`
            }
        } 
        if (e.presenca == 0 && e.nome != 'Total') {
            if (e.idpai > 0) {
                cardContainer.innerHTML += 
                `<tr>
                    <td class="cetralizacoluna" onclick="marcarPresenca(this, ${e.id})">${e.id}</td>
                    <td class="dependente" onclick="marcarPresenca(this, ${e.id})">${e.nome}</td>
                    <td onclick="marcarPresenca(this, ${e.id})"></td>
                </tr>`
            }
            if (e.idpai == 0) {
                cardContainer.innerHTML += 
                `<tr>
                    <td class="cetralizacoluna" onclick="marcarPresenca(this, ${e.id})">${e.id}</td>
                    <td class="linhapai" onclick="marcarPresenca(this, ${e.id})">${e.nome}</td>
                    <td onclick="marcarPresenca(this, ${e.id})"></td>
                </tr>`
            }
        }
        if (e.nome == 'Total') {
            total = e.idpai
            criancas = e.pai
        }
    });
    cardContainer.innerHTML += `
        <tr>
            <td class="totallista cetralizacoluna" >Total</td>
            <td class="totallista cetralizacoluna" >Inscrições : ${total} e Crianças : ${criancas}</td>
            <td class="totallista" ></td>
        </tr>
        `    
}

searchInput.addEventListener("keyup", (e) => {
    data = JSON.parse(localStorage.getItem("lista"))
    if(parseInt(searchInput.value)) {
        const search = data.filter(i => i.id.toString().includes(e.target.value));
        displayData(search);
    } 
    if(!parseInt(searchInput.value)) {
        const search = data.filter(i => i.nome.toLocaleLowerCase().includes(e.target.value.toLocaleLowerCase()));
        displayData(search);
    }
});

function marcarPresenca(element, idPai) {
    let linha = element.parentElement;

    data = JSON.parse(localStorage.getItem("lista"))
    data.forEach(e => {
        if (e.id == idPai && e.presenca == 0) {
            e.presenca = 1
            
        } else if (e.id == idPai && e.presenca == 1) {           
            e.presenca = 0
        }
    });
    localStorage.setItem("lista", JSON.stringify(data));

    $.post(`${servidorapi}/recepcao`, JSON.stringify(data),
    function(status){
        console.log("Status: " + status);
    });

    displayData(data);
    searchInput.value = "";
}

window.addEventListener("load", showModal)
const modal = document.querySelector("dialog")

function showModal() {
    setTimeout(() => {
        modal.showModal()
        modal.classList.add('show');
        modal.classList.remove('hide');
    }, 1500);
}

function hideModal() {
    modal.classList.remove('show');
    modal.classList.add('hide')
    setTimeout(() => {
        modal.close();
    }, 300);
}