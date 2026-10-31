"""Leitura e gravação do histórico, sem classes ou dependências externas."""

import json
from typing import Optional, Union
from datetime import datetime
from pathlib import Path

ARQUIVO_HISTORICO = Path(__file__).resolve().parent / "dados" / "historico.json"


def agora() -> str:
    """Data/hora local e fuso do sistema que executa o programa."""
    return datetime.now().astimezone().isoformat(timespec="seconds")


def novo_historico() -> dict:
    """Cria e retorna o dicionario que armazena o historico das sessoes."""
    return {"versao": 1, "sessoes": []}


def validar_historico(dados: object) -> bool:
    """Verifica a estrutura dos dados antes de carregar o historico."""
    if not isinstance(dados, dict) or dados.get("versao") != 1:
        return False
    sessoes = dados.get("sessoes")
    if not isinstance(sessoes, list):
        return False
    ids = set()
    for sessao in sessoes:
        if not isinstance(sessao, dict):
            return False
        if not all(isinstance(sessao.get(c), str) for c in ("id", "inicio", "tipo", "status")):
            return False
        if sessao["id"] in ids:
            return False
        ids.add(sessao["id"])
        mensagens = sessao.get("mensagens")
        if not isinstance(mensagens, list):
            return False
        for mensagem in mensagens:
            if not isinstance(mensagem, dict) or not all(
                isinstance(mensagem.get(c), str) for c in ("horario", "papel", "texto")
            ):
                return False
    return True


def carregar_historico(
    caminho: Union[str, Path] = ARQUIVO_HISTORICO,
) -> tuple[Optional[dict], Optional[str]]:
    """Retorna (dados, erro). Arquivo inválido nunca é substituído."""
    try:
        dados = json.loads(Path(caminho).read_text(encoding="utf-8"))
        if not validar_historico(dados):
            raise ValueError("estrutura de histórico incompatível")
        # Uma interrupção abrupta pode deixar uma sessão sem finalização.
        for sessao in dados["sessoes"]:
            if sessao["status"] == "em andamento":
                sessao["status"] = "interrompida"
        return dados, None
    except FileNotFoundError:
        return novo_historico(), None
    except (OSError, ValueError) as erro:
        return None, f"Não foi possível ler o histórico: {erro}"


def salvar_historico(dados: dict, caminho: Union[str, Path] = ARQUIVO_HISTORICO) -> Optional[str]:
    """Grava em temporario e substitui somente apos a escrita completa.

    Args:
        dados: Dicionario com as sessoes e mensagens do historico.
        caminho: Local do arquivo JSON que sera criado ou atualizado.

    Returns:
        None quando a gravacao termina, ou uma mensagem descrevendo o erro.
    """
    caminho = Path(caminho)
    temporario = caminho.with_suffix(".tmp")
    try:
        caminho.parent.mkdir(parents=True, exist_ok=True)
        temporario.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
        # A substituicao evita deixar o JSON definitivo parcialmente escrito.
        temporario.replace(caminho)
        return None
    except OSError as erro:
        return f"Não foi possível salvar o histórico: {erro}. Dados mantidos em memória."


def criar_sessao(dados: dict, tipo: str) -> dict:
    """Cria uma sessao, adiciona ao historico e retorna seu dicionario."""
    # Microssegundos evitam colisões entre sessões iniciadas no mesmo segundo.
    identificador = datetime.now().astimezone().isoformat(timespec="microseconds")
    sessao = {
        "id": identificador,
        "inicio": agora(),
        "tipo": tipo,
        "status": "em andamento",
        "mensagens": [],
        "resultado": None,
    }
    dados["sessoes"].append(sessao)
    return sessao


def registrar(sessao: dict, papel: str, texto: str) -> None:
    """Adiciona uma mensagem com horario e papel ao registro da sessao."""
    sessao["mensagens"].append({"horario": agora(), "papel": papel, "texto": str(texto)})


def excluir_sessoes(dados: dict, identificador: Optional[str] = None) -> dict:
    """Retorna uma cópia sem a sessão escolhida, ou sem todas as sessões."""
    return {
        "versao": dados["versao"],
        "sessoes": [
            s for s in dados["sessoes"] if identificador is not None and s["id"] != identificador
        ],
    }
