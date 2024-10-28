let id = sessionStorage.getItem('id');
let nome = sessionStorage.getItem('nome').split(" ")[0];
let tabela = document.getElementById('tabela');

tabela.innerHTML += `
            <tr>
                <td>${id}</td>
                <td>${nome}</td>
            </tr>
                `;
