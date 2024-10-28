let id = sessionStorage.getItem('id');
let nome = sessionStorage.getItem('nome').split(" ")[0];
let tabela = document.getElementById('tabela');
let dep = JSON.parse(sessionStorage.getItem('dep'));

tabela.innerHTML += `
            <tr>
                <td>${id}</td>
                <td>${nome}</td>
            </tr>
                `;

for (let index = 0; index < dep.length; index++) {
    const depen = dep[index];
    tabela.innerHTML += `
            <tr>
                <td>${depen.id}</td>
                <td>${depen.nome.split(" ")[0]}</td>
            </tr>
                `;
};