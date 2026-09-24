# Rádio Cipó

Aplicação acadêmica em Django para pedidos musicais. O sistema utiliza SQLite e possui cadastro, consulta, edição e exclusão de músicas e pedidos pela própria interface, sem depender do Django Admin.

## Como executar

1. Instale o Python 3.
2. Abra um terminal na pasta do projeto.
3. Crie e ative um ambiente virtual.
4. Instale as dependências com `pip install -r requirements.txt`.
5. Prepare o banco com `python manage.py migrate`.
6. Inicie com `python manage.py runserver`.
7. Abra `http://127.0.0.1:8000/` no navegador.

No Windows, se a pasta `.venv` já estiver preparada, também é possível usar `iniciar.bat`.

## Verificações

- `python manage.py check`
- `python manage.py test`

As migrations criam a estrutura do banco. O pacote ZIP preparado para a entrega inclui um banco limpo com três músicas de demonstração e nenhum pedido. Se o projeto for obtido pelo GitHub sem o arquivo `db.sqlite3`, execute a migração, cadastre as músicas pela opção **Músicas** e use **Pedir música** para registrar pedidos.
