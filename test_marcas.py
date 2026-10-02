import time

import pytest
import requests


# Endereço principal da API usada nos testes
BASE_URL = "https://api.practicesoftwaretesting.com"


def test_listar_marcas():
    # Faz a consulta da lista de marcas
    resposta = requests.get(
        f"{BASE_URL}/brands",
        timeout=10
    )

    # Primeiro verifico se a requisição deu certo
    assert resposta.status_code == 200, (
        f"status {resposta.status_code}, corpo: {resposta.text}"
    )

    dados = resposta.json()

    # A resposta esperada é uma lista
    assert isinstance(dados, list), (
        f"Esperado uma lista, recebido {type(dados).__name__}"
    )


def test_marcas_possuem_campos_e_tipos_corretos():
    resposta = requests.get(
        f"{BASE_URL}/brands",
        timeout=10
    )

    assert resposta.status_code == 200, (
        f"status {resposta.status_code}, corpo: {resposta.text}"
    )

    marcas = resposta.json()

    assert isinstance(marcas, list), (
        f"Esperado uma lista, recebido {type(marcas).__name__}"
    )

    # Verifica cada marca retornada pela API
    for indice, marca in enumerate(marcas):
        assert "id" in marca, (
            f"Item {indice} não possui o campo 'id': {marca}"
        )
        assert "name" in marca, (
            f"Item {indice} não possui o campo 'name': {marca}"
        )
        assert "slug" in marca, (
            f"Item {indice} não possui o campo 'slug': {marca}"
        )

        # Além de existir, os campos precisam ser strings
        assert isinstance(marca["id"], str), (
            f"Item {indice}: 'id' deveria ser string: {marca}"
        )
        assert isinstance(marca["name"], str), (
            f"Item {indice}: 'name' deveria ser string: {marca}"
        )
        assert isinstance(marca["slug"], str), (
            f"Item {indice}: 'slug' deveria ser string: {marca}"
        )


def test_criar_marca_e_consultar():
    # Uso um identificador diferente para evitar conflito entre execuções
    identificador = int(time.time())
    nome = f"Maicon Teste {identificador}"
    slug = f"maicon-teste-{identificador}"

    dados_marca = {
        "name": nome,
        "slug": slug
    }

    id_marca = None

    try:
        resposta_criacao = requests.post(
            f"{BASE_URL}/brands",
            json=dados_marca,
            timeout=10
        )

        assert resposta_criacao.status_code == 201, (
            f"status {resposta_criacao.status_code}, "
            f"corpo: {resposta_criacao.text}"
        )

        corpo_criacao = resposta_criacao.json()

        assert "id" in corpo_criacao, (
            f"Resposta de criação não possui 'id': {corpo_criacao}"
        )

        # Guardo o ID retornado para usar nas próximas operações
        id_marca = corpo_criacao["id"]

        resposta_consulta = requests.get(
            f"{BASE_URL}/brands/{id_marca}",
            timeout=10
        )

        assert resposta_consulta.status_code == 200, (
            f"status {resposta_consulta.status_code}, "
            f"corpo: {resposta_consulta.text}"
        )

        corpo_consulta = resposta_consulta.json()

        assert "id" in corpo_consulta, (
            f"Resposta da consulta não possui 'id': {corpo_consulta}"
        )
        assert "name" in corpo_consulta, (
            f"Resposta da consulta não possui 'name': {corpo_consulta}"
        )
        assert "slug" in corpo_consulta, (
            f"Resposta da consulta não possui 'slug': {corpo_consulta}"
        )

        assert corpo_consulta["id"] == id_marca, (
            f"ID diferente do criado: {corpo_consulta}"
        )
        assert corpo_consulta["name"] == nome, (
            f"Nome diferente do enviado: {corpo_consulta}"
        )
        assert corpo_consulta["slug"] == slug, (
            f"Slug diferente do enviado: {corpo_consulta}"
        )

    finally:
        # Se o teste criou uma marca, tento removê-la para não deixar lixo na API
        if id_marca is not None:
            # Faço login para obter o token necessário para operações administrativas
            resposta_login = requests.post(
                f"{BASE_URL}/users/login",
                json={
                    "email": "admin@practicesoftwaretesting.com",
                    "password": "welcome01"
                },
                timeout=10
            )

            assert resposta_login.status_code == 200, (
                f"status {resposta_login.status_code}, "
                f"corpo: {resposta_login.text}"
            )

            corpo_login = resposta_login.json()

            assert "access_token" in corpo_login, (
                f"Login não retornou 'access_token': {corpo_login}"
            )

            token = corpo_login["access_token"]

            resposta_exclusao = requests.delete(
                f"{BASE_URL}/brands/{id_marca}",
                headers={
                    "Authorization": f"Bearer {token}"
                },
                timeout=10
            )

            assert resposta_exclusao.status_code == 204, (
                f"status {resposta_exclusao.status_code}, "
                f"corpo: {resposta_exclusao.text}"
            )


def test_atualizar_marca_e_consultar():
    # Uso um identificador diferente para evitar conflito entre execuções
    identificador = int(time.time())
    nome_original = f"Maicon Teste {identificador}"
    slug_original = f"maicon-teste-{identificador}"

    nome_atualizado = f"Maicon Atualizado {identificador}"
    slug_atualizado = f"maicon-atualizado-{identificador}"

    id_marca = None

    try:
        resposta_criacao = requests.post(
            f"{BASE_URL}/brands",
            json={
                "name": nome_original,
                "slug": slug_original
            },
            timeout=10
        )

        assert resposta_criacao.status_code == 201, (
            f"status {resposta_criacao.status_code}, "
            f"corpo: {resposta_criacao.text}"
        )

        corpo_criacao = resposta_criacao.json()

        assert "id" in corpo_criacao, (
            f"Resposta de criação não possui 'id': {corpo_criacao}"
        )

        id_marca = corpo_criacao["id"]

        resposta_atualizacao = requests.put(
            f"{BASE_URL}/brands/{id_marca}",
            json={
                "name": nome_atualizado,
                "slug": slug_atualizado
            },
            timeout=10
        )

        assert resposta_atualizacao.status_code == 200, (
            f"status {resposta_atualizacao.status_code}, "
            f"corpo: {resposta_atualizacao.text}"
        )

        # Faço um novo GET para confirmar que a alteração realmente foi salva
        resposta_consulta = requests.get(
            f"{BASE_URL}/brands/{id_marca}",
            timeout=10
        )

        assert resposta_consulta.status_code == 200, (
            f"status {resposta_consulta.status_code}, "
            f"corpo: {resposta_consulta.text}"
        )

        corpo_consulta = resposta_consulta.json()

        assert "id" in corpo_consulta, (
            f"Resposta da consulta não possui 'id': {corpo_consulta}"
        )
        assert "name" in corpo_consulta, (
            f"Resposta da consulta não possui 'name': {corpo_consulta}"
        )
        assert "slug" in corpo_consulta, (
            f"Resposta da consulta não possui 'slug': {corpo_consulta}"
        )

        assert corpo_consulta["id"] == id_marca, (
            f"ID diferente do esperado: {corpo_consulta}"
        )
        assert corpo_consulta["name"] == nome_atualizado, (
            f"Nome não foi atualizado: {corpo_consulta}"
        )
        assert corpo_consulta["slug"] == slug_atualizado, (
            f"Slug não foi atualizado: {corpo_consulta}"
        )

    finally:
        # Se o teste criou uma marca, tento removê-la para não deixar lixo na API
        if id_marca is not None:
            resposta_login = requests.post(
                f"{BASE_URL}/users/login",
                json={
                    "email": "admin@practicesoftwaretesting.com",
                    "password": "welcome01"
                },
                timeout=10
            )

            assert resposta_login.status_code == 200, (
                f"status {resposta_login.status_code}, "
                f"corpo: {resposta_login.text}"
            )

            corpo_login = resposta_login.json()

            assert "access_token" in corpo_login, (
                f"Login não retornou 'access_token': {corpo_login}"
            )

            token = corpo_login["access_token"]

            resposta_exclusao = requests.delete(
                f"{BASE_URL}/brands/{id_marca}",
                headers={
                    "Authorization": f"Bearer {token}"
                },
                timeout=10
            )

            assert resposta_exclusao.status_code == 204, (
                f"status {resposta_exclusao.status_code}, "
                f"corpo: {resposta_exclusao.text}"
            )


def test_excluir_marca_e_confirmar_ausencia():
    # Uso um identificador diferente para evitar conflito entre execuções
    identificador = int(time.time())
    nome = f"Maicon Exclusao {identificador}"
    slug = f"maicon-exclusao-{identificador}"

    id_marca = None

    try:
        resposta_criacao = requests.post(
            f"{BASE_URL}/brands",
            json={
                "name": nome,
                "slug": slug
            },
            timeout=10
        )

        assert resposta_criacao.status_code == 201, (
            f"status {resposta_criacao.status_code}, "
            f"corpo: {resposta_criacao.text}"
        )

        corpo_criacao = resposta_criacao.json()

        assert "id" in corpo_criacao, (
            f"Resposta de criação não possui 'id': {corpo_criacao}"
        )

        id_marca = corpo_criacao["id"]

        # Faço login para obter o token necessário para operações administrativas
        resposta_login = requests.post(
            f"{BASE_URL}/users/login",
            json={
                "email": "admin@practicesoftwaretesting.com",
                "password": "welcome01"
            },
            timeout=10
        )

        assert resposta_login.status_code == 200, (
            f"status {resposta_login.status_code}, "
            f"corpo: {resposta_login.text}"
        )

        corpo_login = resposta_login.json()

        assert "access_token" in corpo_login, (
            f"Login não retornou 'access_token': {corpo_login}"
        )

        token = corpo_login["access_token"]

        resposta_exclusao = requests.delete(
            f"{BASE_URL}/brands/{id_marca}",
            headers={
                "Authorization": f"Bearer {token}"
            },
            timeout=10
        )

        assert resposta_exclusao.status_code == 204, (
            f"status {resposta_exclusao.status_code}, "
            f"corpo: {resposta_exclusao.text}"
        )

        resposta_consulta = requests.get(
            f"{BASE_URL}/brands/{id_marca}",
            timeout=10
        )

        assert resposta_consulta.status_code == 404, (
            f"status {resposta_consulta.status_code}, "
            f"corpo: {resposta_consulta.text}"
        )

        id_marca = None

    finally:
        # Se a exclusão principal falhar, tento limpar a marca criada
        if id_marca is not None:
            resposta_login = requests.post(
                f"{BASE_URL}/users/login",
                json={
                    "email": "admin@practicesoftwaretesting.com",
                    "password": "welcome01"
                },
                timeout=10
            )

            if resposta_login.status_code == 200:
                corpo_login = resposta_login.json()

                if "access_token" in corpo_login:
                    token = corpo_login["access_token"]

                    resposta_limpeza = requests.delete(
                        f"{BASE_URL}/brands/{id_marca}",
                        headers={
                            "Authorization": f"Bearer {token}"
                        },
                        timeout=10
                    )

                    assert resposta_limpeza.status_code == 204, (
                        f"status {resposta_limpeza.status_code}, "
                        f"corpo: {resposta_limpeza.text}"
                    )


def test_excluir_marca_sem_autenticacao():
    # Uso um identificador diferente para evitar conflito entre execuções
    identificador = int(time.time())
    nome = f"Maicon Sem Auth {identificador}"
    slug = f"maicon-sem-auth-{identificador}"

    id_marca = None

    try:
        resposta_criacao = requests.post(
            f"{BASE_URL}/brands",
            json={
                "name": nome,
                "slug": slug
            },
            timeout=10
        )

        assert resposta_criacao.status_code == 201, (
            f"status {resposta_criacao.status_code}, "
            f"corpo: {resposta_criacao.text}"
        )

        corpo_criacao = resposta_criacao.json()

        assert "id" in corpo_criacao, (
            f"Resposta de criação não possui 'id': {corpo_criacao}"
        )

        id_marca = corpo_criacao["id"]

        # Aqui a exclusão é feita sem token para verificar se a API bloqueia o acesso
        resposta_exclusao = requests.delete(
            f"{BASE_URL}/brands/{id_marca}",
            timeout=10
        )

        assert resposta_exclusao.status_code == 401, (
            f"status {resposta_exclusao.status_code}, "
            f"corpo: {resposta_exclusao.text}"
        )

        corpo_exclusao = resposta_exclusao.json()

        assert "message" in corpo_exclusao, (
            f"Campo 'message' não encontrado na resposta: {corpo_exclusao}"
        )

        assert corpo_exclusao["message"] == "Unauthorized", (
            f"Mensagem inesperada: {corpo_exclusao}"
        )

    finally:
        # Limpa a marca criada usando autenticação
        if id_marca is not None:
            resposta_login = requests.post(
                f"{BASE_URL}/users/login",
                json={
                    "email": "admin@practicesoftwaretesting.com",
                    "password": "welcome01"
                },
                timeout=10
            )

            if resposta_login.status_code == 200:
                corpo_login = resposta_login.json()

                if "access_token" in corpo_login:
                    token = corpo_login["access_token"]

                    resposta_limpeza = requests.delete(
                        f"{BASE_URL}/brands/{id_marca}",
                        headers={
                            "Authorization": f"Bearer {token}"
                        },
                        timeout=10
                    )

                    assert resposta_limpeza.status_code == 204, (
                        f"status {resposta_limpeza.status_code}, "
                        f"corpo: {resposta_limpeza.text}"
                    )


def test_login_com_senha_incorreta():
    resposta = requests.post(
        f"{BASE_URL}/users/login",
        json={
            "email": "admin@practicesoftwaretesting.com",
            "password": "senha-incorreta"
        },
        timeout=10
    )

    assert resposta.status_code == 401, (
        f"status {resposta.status_code}, corpo: {resposta.text}"
    )

    corpo_resposta = resposta.json()

    assert "error" in corpo_resposta, (
        f"Campo 'error' não encontrado na resposta: {corpo_resposta}"
    )

    assert corpo_resposta["error"] == "Unauthorized", (
        f"Erro inesperado na resposta: {corpo_resposta}"
    )


@pytest.mark.parametrize(
    "caso",
    [
        "sem_name",
        "sem_slug",
        "tipo_invalido"
    ],
    ids=[
        "sem_name",
        "sem_slug",
        "tipo_invalido"
    ]
)
def test_criar_marca_com_dados_invalidos(caso):
    # Gera um valor único para evitar conflito com dados já existentes
    identificador = time.time_ns()

    if caso == "sem_name":
        dados_marca = {
            "slug": f"maicon-sem-name-{identificador}"
        }
        campo_esperado = "name"
        mensagem_esperada = "The name field is required."

    elif caso == "sem_slug":
        dados_marca = {
            "name": f"Maicon Sem Slug {identificador}"
        }
        campo_esperado = "slug"
        mensagem_esperada = "The slug field is required."

    else:
        dados_marca = {
            "name": 12345,
            "slug": f"maicon-tipo-invalido-{identificador}"
        }
        campo_esperado = "name"
        mensagem_esperada = "The name field must be a string."

    resposta = requests.post(
        f"{BASE_URL}/brands",
        json=dados_marca,
        timeout=10
    )

    assert resposta.status_code == 422, (
        f"status {resposta.status_code}, corpo: {resposta.text}"
    )

    corpo_resposta = resposta.json()

    assert campo_esperado in corpo_resposta, (
        f"[{caso}] Campo '{campo_esperado}' não encontrado na resposta: "
        f"{corpo_resposta}"
    )

    assert mensagem_esperada in corpo_resposta[campo_esperado], (
        f"[{caso}] Mensagem esperada não encontrada: {corpo_resposta}"
    )