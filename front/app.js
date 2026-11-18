// LOCALIZANDO OS ELEMENTOS DO HTML

const formulario = document.getElementById("formLivro");
const campoTitulo = document.getElementById("titulo");
const campoAutor = document.getElementById("autor");
const campoAno = document.getElementById("ano");
const listaLivros = document.getElementById("listaLivros");
const mensagem = document.getElementById("mensagem");

// ENDEREÇO DA NOSSA API PYTHON

const API_URL = "http://127.0.0.1:5000/api/livros";

// FUNÇÃO PARA LISTAR OS LIVROS DO BANCO

async function carregarLivros() {
    try {
        const resposta = await fetch(API_URL);

        if (!resposta.ok) {
            throw new Error("Erro ao buscar livros.");
        }

        const livros = await resposta.json();

        mostrarLivros(livros);

    } catch (erro) {
        mensagem.textContent = "Não foi possível carregar os livros.";
        console.error(erro);
    }
}

// FUNÇÃO PARA EXIBIR OS LIVROS NA TELA

function mostrarLivros(livros) {

    listaLivros.innerHTML = "";

    if (livros.length === 0) {
        listaLivros.innerHTML =
            '<p class="lista-vazia">Nenhum livro cadastrado ainda.</p>';
        return;
    }

    livros.forEach(function(livro) {

        const item = document.createElement("article");
        item.className = "livro";

        const titulo = document.createElement("h3");
        titulo.textContent = livro.titulo;

        const autor = document.createElement("p");
        autor.textContent = "Autor: " + livro.autor;

        const ano = document.createElement("p");
        ano.textContent = "Ano: " + livro.ano;

        // CRIANDO O BOTÃO DE EXCLUIR
        const botaoExcluir = document.createElement("button");
        botaoExcluir.textContent = "Excluir";
        botaoExcluir.className = "botao-excluir";

        // Adicionando o evento de clique para deletar o livro
        botaoExcluir.addEventListener("click", async function() {
            try {
                const resposta = await fetch(`${API_URL}/${livro.id}`, {
                    method: "DELETE"
                });

                const resultado = await resposta.json();

                if (!resposta.ok) {
                    throw new Error(resultado.erro || "Erro ao excluir livro.");
                }

                mensagem.textContent = resultado.mensagem;

                // Recarrega a lista após excluir
                await carregarLivros();

            } catch (erro) {
                mensagem.textContent = erro.message;
                console.error(erro);
            }
        });

        // Adiciona os textos e o botão dentro do artigo do livro
        item.append(titulo, autor, ano, botaoExcluir);

        listaLivros.appendChild(item);
    });
}

// CADASTRANDO UM LIVRO NO BANCO DE DADOS

formulario.addEventListener("submit", async function(event) {

    event.preventDefault();

    const dadosLivro = {
        titulo: campoTitulo.value.trim(),
        autor: campoAutor.value.trim(),
        ano: Number(campoAno.value)
    };

    if (!dadosLivro.titulo || !dadosLivro.autor || !dadosLivro.ano) {
        mensagem.textContent = "Preencha todos os campos.";
        return;
    }

    try {

        const resposta = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(dadosLivro)
        });

        const resultado = await resposta.json();

        if (!resposta.ok) {
            throw new Error(resultado.erro || "Erro ao cadastrar livro.");
        }

        mensagem.textContent = resultado.mensagem;

        formulario.reset();

        // Atualiza a lista buscando os dados diretamente do banco.
        await carregarLivros();

    } catch (erro) {

        mensagem.textContent = erro.message;
        console.error(erro);

    }

});

// CARREGA OS LIVROS QUANDO A PÁGINA ABRIR

carregarLivros();