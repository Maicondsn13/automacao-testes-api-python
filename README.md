# Automação de Testes de API com Python

Projeto desenvolvido durante o curso **Fundamentos de Lógica de Programação para QA**, com foco na criação de uma suíte de testes automatizados para uma API REST.

## Tecnologias

* Python
* Pytest
* Requests
* API REST

## Testes realizados

A suíte contempla testes para:

* Consulta de marcas
* Criação de marcas
* Consulta de uma marca criada
* Alteração de marcas
* Exclusão de marcas
* Confirmação da ausência após exclusão
* Testes de autenticação
* Validação de dados inválidos

## Boas práticas utilizadas

* Testes automatizados com Pytest
* Requisições HTTP utilizando Requests
* Validação de códigos de status HTTP
* Validação do conteúdo das respostas
* Dados dinâmicos para evitar conflitos
* Timeout nas requisições
* Testes independentes

## Como executar

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute os testes:

```bash
pytest test_marcas.py -v
```

## Objetivo

Praticar conceitos de QA e automação de testes de API utilizando Python, desenvolvendo uma suíte capaz de validar diferentes cenários de uma API REST.

## Resultado dos testes

10 testes executados — 10 aprovados.
