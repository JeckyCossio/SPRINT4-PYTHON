"""Dados, validacoes e funcionalidades do Agente de IA para Camera.

As funcoes deste modulo recebem os dados de que precisam por parametro e,
quando apropriado, retornam resultados. A Sprint 4 acrescenta preparacao
simulada, consulta meteorologica e historico persistente.
"""

from pathlib import Path
from typing import Optional, Union
from persistencia import agora, registrar, salvar_historico, excluir_sessoes
from regras import CATEGORIAS, PERFIS, decidir_configuracao
from clima import consultar_clima, formatar_clima


# Coordenadas das cinco cidades paulistas disponiveis para consulta.
CIDADES_SP = {
    "1": {"name": "São Paulo", "latitude": -23.5505, "longitude": -46.6333},
    "2": {"name": "Campinas", "latitude": -22.9056, "longitude": -47.0608},
    "3": {"name": "Santos", "latitude": -23.9608, "longitude": -46.3336},
    "4": {"name": "Sorocaba", "latitude": -23.5015, "longitude": -47.4526},
    "5": {"name": "Ribeirão Preto", "latitude": -21.1704, "longitude": -47.8103},
}


def input_seguro(prompt: str = "") -> str:
    """Le uma entrada e remove espacos nas extremidades.

    O cancelamento e tratado por quem recebe a resposta, para que a sessao
    tambem registre o atalho '/' antes de retornar ao menu principal.
    """
    return input(prompt).strip()


def gravar(dados: dict, caminho: Union[str, Path]) -> bool:
    """Salva o historico e retorna se a gravacao foi concluida."""
    erro = salvar_historico(dados, caminho)
    if erro:
        print(f"ATENÇÃO: {erro}")
    return erro is None


def dizer(dados: dict, sessao: dict, texto: str, caminho: Union[str, Path]) -> None:
    """Exibe uma mensagem e a registra no historico da sessao."""
    print("\n" + texto)
    registrar(sessao, "sistema", texto)
    gravar(dados, caminho)


def perguntar(dados: dict, sessao: dict, texto: str, caminho: Union[str, Path]) -> Optional[str]:
    """Solicita uma resposta e registra a entrada antes de verificar o atalho.

    Args:
        dados: Historico compartilhado entre as funcionalidades.
        sessao: Sessao que recebe a pergunta e a resposta do usuario.
        texto: Mensagem apresentada antes da leitura.
        caminho: Local do arquivo usado na persistencia do historico.

    Returns:
        O texto digitado sem espacos nas extremidades, ou None ao cancelar.
    """
    dizer(dados, sessao, texto + "\n(/ para cancelar e voltar ao menu)", caminho)
    resposta = input_seguro("> ")
    registrar(sessao, "usuario", resposta)
    gravar(dados, caminho)
    if resposta == "/":
        return None
    return resposta


def escolher(
    dados: dict, sessao: dict, pergunta: str, opcoes: dict, caminho: Union[str, Path]
) -> Optional[str]:
    """Solicita uma opcao ate que ela esteja entre as opcoes permitidas."""
    menu = pergunta + "\n" + "\n".join(f"{k} - {v}" for k, v in opcoes.items())
    while True:
        resposta = perguntar(dados, sessao, menu, caminho)
        if resposta is None or resposta in opcoes:
            return resposta
        dizer(dados, sessao, "Opção inválida. Escolha um dos números apresentados.", caminho)


def finalizar(dados: dict, sessao: dict, status: str, caminho: Union[str, Path]) -> None:
    """Registra o encerramento da sessao e informa o retorno ao menu."""
    sessao["status"] = status
    sessao["fim"] = agora()
    dizer(dados, sessao, f"Sessão {status}. Retornando ao menu principal.", caminho)


def fluxo_clima(dados: dict, sessao: dict, caminho: Union[str, Path]) -> tuple[Optional[dict], str]:
    """Consulta a cidade e retorna os dados do clima e o status da consulta."""
    opcoes = {numero: cidade["name"] for numero, cidade in CIDADES_SP.items()}
    escolha = escolher(dados, sessao, "Selecione a cidade (estado de São Paulo):", opcoes, caminho)
    if escolha is None:
        return None, "cancelada"
    cidade = dict(CIDADES_SP[escolha], admin1="São Paulo", country="Brasil")
    dizer(dados, sessao, "Consultando condições atuais e horários solares de hoje...", caminho)
    clima, erro = consultar_clima(cidade)
    if erro:
        dizer(dados, sessao, erro, caminho)
        return None, "falha na API"
    dizer(dados, sessao, formatar_clima(clima), caminho)
    return clima, "concluída"


def preparar_camera(dados: dict, sessao: dict, caminho: Union[str, Path]) -> None:
    """Prepara configuracoes simuladas e registra o resultado da sessao."""
    dizer(
        dados,
        sessao,
        "PREPARAÇÃO AUTOMÁTICA SIMULADA\n"
        "Não acessamos câmera, imagens, microfone ou IA. O disparo final é seu.",
        caminho,
    )
    autoriza = escolher(
        dados,
        sessao,
        "Autoriza iniciar esta simulação automática?",
        {"1": "Sim", "2": "Não"},
        caminho,
    )
    if autoriza != "1":
        finalizar(dados, sessao, "cancelada", caminho)
        return
    perguntas = [
        ("categoria", "O que você quer fotografar?", CATEGORIAS),
        ("ambiente", "Onde está a cena?", {"1": "Ambiente interno", "2": "Ambiente externo"}),
        (
            "luz",
            "Como está a iluminação real da cena?",
            {
                "1": "Baixa (pouca luz)",
                "2": "Suficiente e uniforme",
                "3": "Alto contraste (áreas muito claras e escuras)",
            },
        ),
        ("movimento", "O assunto principal está em movimento?", {"1": "Sim", "2": "Não"}),
        (
            "perfil",
            "Qual perfil de recursos deseja simular?",
            {k: v["nome"] for k, v in PERFIS.items()},
        ),
    ]
    respostas = {}
    for campo, pergunta, opcoes in perguntas:
        valor = escolher(dados, sessao, pergunta, opcoes, caminho)
        if valor is None:
            finalizar(dados, sessao, "cancelada", caminho)
            return
        respostas[campo] = valor
    cenario = {
        "categoria": respostas["categoria"],
        "ambiente": "externo" if respostas["ambiente"] == "2" else "interno",
        "luz": {"1": "baixa", "2": "uniforme", "3": "contraste"}[respostas["luz"]],
        "movimento": "sim" if respostas["movimento"] == "1" else "não",
    }
    clima = None
    if cenario["ambiente"] == "externo":
        consultar = escolher(
            dados,
            sessao,
            "Deseja consultar o clima antes de continuar?",
            {"1": "Sim", "2": "Não"},
            caminho,
        )
        if consultar is None:
            finalizar(dados, sessao, "cancelada", caminho)
            return
        if consultar == "1":
            clima, status = fluxo_clima(dados, sessao, caminho)
            if status == "cancelada":
                finalizar(dados, sessao, "cancelada", caminho)
                return
            if clima is None:
                dizer(
                    dados,
                    sessao,
                    "Continuando sem dados meteorológicos; "
                    "serão usadas somente as condições informadas por você.",
                    caminho,
                )
    resultado = decidir_configuracao(cenario, PERFIS[respostas["perfil"]])
    sessao["resultado"] = {"cenario": cenario, "configuracao": resultado, "clima": clima}
    texto = (
        f"RESULTADO SIMULADO — {CATEGORIAS[cenario['categoria']]}\n"
        f"Perfil: {resultado['perfil']}\nModo: {resultado['modo']}\n"
        f"HDR: {'ativado' if resultado['hdr'] else 'desativado'}\n"
        f"Foco: {resultado['foco']}\nExposição: {resultado['exposicao']}\n"
        "Flash: desativado\n"
    )
    texto += "\n".join(resultado["motivos"] + ["Limitação: " + a for a in resultado["avisos"]])
    texto += (
        "\nPreparação concluída apenas na simulação. Nenhuma configuração real foi alterada."
        "\nNa experiência proposta, você decide quando pressionar o botão de captura."
    )
    dizer(dados, sessao, texto, caminho)
    finalizar(dados, sessao, "concluída", caminho)


def consultar_condicoes(dados: dict, sessao: dict, caminho: Union[str, Path]) -> None:
    """Conduz a consulta meteorologica e registra seu encerramento."""
    resultado, status = fluxo_clima(dados, sessao, caminho)
    sessao["resultado"] = resultado
    finalizar(dados, sessao, status, caminho)


def listar_sessoes(dados: dict) -> None:
    """Apresenta as sessoes com numero, data, tipo e status."""
    for numero, sessao in enumerate(dados["sessoes"], 1):
        print(f"{numero} - {sessao['inicio']} | {sessao['tipo']} | {sessao['status']}")


def exibir_historico(dados: dict) -> None:
    """Exibe as mensagens de uma sessao escolhida, sem criar outra sessao."""
    if not dados["sessoes"]:
        print("\nNenhuma sessão registrada.")
        return
    listar_sessoes(dados)
    while True:
        escolha = input_seguro("Número da sessão para ler (/ para voltar): ")
        if escolha == "/":
            return
        if len(escolha) <= 9 and escolha.isdecimal() and 1 <= int(escolha) <= len(dados["sessoes"]):
            sessao = dados["sessoes"][int(escolha) - 1]
            print(f"\nSessão {sessao['id']} — {sessao['status']}")
            for mensagem in sessao["mensagens"]:
                print(f"[{mensagem['horario']}] {mensagem['papel']}: {mensagem['texto']}")
            return
        print("Número inválido. Escolha uma sessão da lista.")


def excluir_historico(dados: dict, caminho: Union[str, Path]) -> dict:
    """Confirma a exclusao e retorna o historico somente apos salva-lo."""
    if not dados["sessoes"]:
        print("\nNenhuma sessão para excluir.")
        return dados
    listar_sessoes(dados)
    while True:
        escolha = input_seguro("Número da sessão, T para todas ou / para voltar: ").lower()
        if escolha == "/":
            return dados
        if escolha == "t":
            identificador = None
            alvo = "TODAS as sessões"
            break
        if len(escolha) <= 9 and escolha.isdecimal() and 1 <= int(escolha) <= len(dados["sessoes"]):
            identificador = dados["sessoes"][int(escolha) - 1]["id"]
            alvo = f"a sessão {escolha}"
            break
        print("Opção inválida.")
    while True:
        confirma = input_seguro(f"Excluir {alvo}? Digite s ou n (/ cancela): ").lower()
        if confirma in ("n", "/"):
            print("Exclusão cancelada.")
            return dados
        if confirma == "s":
            novos = excluir_sessoes(dados, identificador)
            if gravar(novos, caminho):
                print("Exclusão concluída.")
                return novos
            print("Exclusão não concluída. Os dados anteriores foram mantidos.")
            return dados
        print("Digite s ou n.")
