"""Ponto de entrada do Agente de IA para Camera.

Este arquivo possui somente as responsabilidades principais do programa:
carregar o historico, apresentar o menu e chamar as funcionalidades
implementadas no modulo ``funcoes``.
"""

from datetime import datetime
from pathlib import Path
from typing import Union

from funcoes import (
    consultar_condicoes,
    excluir_historico,
    exibir_historico,
    finalizar,
    input_seguro,
    preparar_camera,
)
from persistencia import ARQUIVO_HISTORICO, carregar_historico, criar_sessao, registrar


def exibir_menu() -> None:
    """Apresenta as opcoes disponiveis no menu principal."""
    print("\n====================================================")
    print("JOVI AI — SPRINT 4 | Open Source Consulting")
    print("Horário do sistema: " + datetime.now().astimezone().strftime("%d/%m/%Y %H:%M:%S %z"))
    print("====================================================")
    print("  1 - Iniciar preparação automática simulada")
    print("  2 - Consultar condições para fotografar ao ar livre")
    print("  3 - Visualizar sessões anteriores")
    print("  4 - Excluir histórico")
    print("  0 - Sair")
    print("  / - Cancelar uma operação e voltar ao menu")
    print("====================================================")


def menu_principal(caminho: Union[str, Path] = ARQUIVO_HISTORICO) -> None:
    """Controla o menu principal ate que o usuario escolha sair.

    O mesmo dicionario de historico e passado por parametro para todas as
    funcionalidades. Na Sprint 4, os registros sao recuperados do arquivo
    JSON para que continuem disponiveis entre as execucoes.
    """
    dados, erro = carregar_historico(caminho)
    if erro:
        print(erro)
        print(f"Arquivo preservado: {caminho}")
        print("Faça uma cópia de segurança e corrija ou renomeie esse arquivo antes de reiniciar.")
        return

    while True:
        sessao = None
        try:
            exibir_menu()
            opcao = input_seguro("  Opção: ")

            # Somente preparacoes e consultas criam registros de conversa.
            if opcao in ("1", "2"):
                tipo = "preparação simulada" if opcao == "1" else "consulta meteorológica"
                sessao = criar_sessao(dados, tipo)
                registrar(sessao, "sistema", "Menu principal: 1 - Preparação; 2 - Clima.")
                registrar(sessao, "usuario", opcao)

            # if/elif mantem o programa compativel tambem com o Python 3.9.
            if opcao == "1":
                preparar_camera(dados, sessao, caminho)
            elif opcao == "2":
                consultar_condicoes(dados, sessao, caminho)
            elif opcao == "3":
                exibir_historico(dados)
            elif opcao == "4":
                dados = excluir_historico(dados, caminho)
            elif opcao == "0":
                print("Encerrando o JOVI AI. Até logo!")
                break
            elif opcao == "/":
                # Se '/' for digitado no proprio menu, apenas o mostramos de novo.
                continue
            else:
                print("Opção inválida. Escolha uma das opções do menu.")
        except (EOFError, KeyboardInterrupt):
            if sessao is not None:
                finalizar(dados, sessao, "interrompida", caminho)
            print("\nEntrada encerrada. Finalizando o programa com segurança.")
            return


if __name__ == "__main__":
    # Este bloco impede que o menu seja iniciado caso main.py seja importado.
    menu_principal()
