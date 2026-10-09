# LogiRota — Entrega da Semana 1

## Requisitos
- Python 3 instalado (a biblioteca `sqlite3` ja vem com Python).
- Nenhuma dependencia externa.

## Como executar
Abra o terminal nesta pasta e execute:

```powershell
python main.py
```

Na primeira execucao, o programa cria `logirota.db` e cadastra os pontos e vias iniciais uma unica vez. Nas execucoes seguintes, pontos e vias sao carregados do banco. Use a opcao 2 para cadastrar pedidos e a opcao 3 para conferir os pedidos pendentes. Os pedidos continuam salvos depois de fechar o programa.

## Modulos
- `logirota/banco.py`: esquema SQLite e funcoes de persistencia.
- `main.py`: inicializacao, carga dos dados do banco e menu de demonstracao.
- Os TADs de dominio (`ponto.py`, `grafo.py`, fila, pilha e busca) foram reaproveitados sem alteracoes.
