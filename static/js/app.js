document.querySelectorAll('.confirmar-exclusao').forEach(form => {
    form.addEventListener('submit', event => {
        const item = form.dataset.item || 'este registro';
        if (!window.confirm(`Deseja realmente excluir ${item}?`)) event.preventDefault();
    });
});

const tiposContato = document.querySelectorAll('input[name="tipo_contato"]');
const campoContato = document.querySelector('#id_contato');
const labelContato = document.querySelector('#label-contato');

function atualizarContato() {
    if (!campoContato || !labelContato) return;
    const selecionado = document.querySelector('input[name="tipo_contato"]:checked');
    const email = selecionado && selecionado.value === 'email';
    labelContato.textContent = email ? 'E-mail' : 'Telefone';
    campoContato.placeholder = email ? 'nome@exemplo.com' : '(91) 99999-9999';
}

tiposContato.forEach(campo => campo.addEventListener('change', atualizarContato));
atualizarContato();
