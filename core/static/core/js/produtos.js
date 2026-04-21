function abrirModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.style.display = 'flex';
    }
}

function fecharModal(id) {
    const modal = document.getElementById(id);
    if (modal) {
        modal.style.display = 'none';
    }
}

function trocarImagem(produtoId, miniatura) {// rece qual prouto está no modal e qualç miniatura clicada
    const imagemPrincipal = document.getElementById(`imagem-principal-${produtoId}`); 
    // encontra a imagem grande correspondente aquele produto
    if (imagemPrincipal) {
        imagemPrincipal.src = miniatura.src;
        //troca a imagem grande pela miniatura clicada
    }

    const galeria = miniatura.parentElement;
    const miniaturas = galeria.querySelectorAll('.galeria-img');

    miniaturas.forEach(function(img) {
        img.classList.remove('ativa');
    });

    miniatura.classList.add('ativa');
    //tira o destaque das outras miniaturas e deixa somente a clicada com destaque
}

window.addEventListener('click', function(event) {
    const modais = document.querySelectorAll('.modal');

    modais.forEach(function(modal) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});