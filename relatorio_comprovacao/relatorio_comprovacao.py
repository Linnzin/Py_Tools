#!/usr/bin/env python3
"""
Programa para gerar o texto do relatório de comprovação.

Se for a primeira fez executando este código, execute isso no terminal: 
    pip install -r requirements.txt

Como usar:
    $ py relatorio_comprovacao.py
"""

from datetime import datetime
import os
from pathlib import Path
import re
from re import Match
import time

from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet


__version__: str = "1.2"
__author__: str = "Lincoln P. da Silva"
__license__: str = "Proprietário"

VERMELHO_N: str = '\033[1;31m'
MAGENTA_N: str = '\033[1;35m'
AZUL_N: str = '\033[1;34m'
CIANO_N: str = '\033[1;36m'
VERDE_N: str = '\033[1;32m'
AMARELO_N: str = '\033[1;33m'
RESET: str = '\033[0m'

ANO: int = 2026
AGORA: datetime = datetime.now().strftime("%d-%m-%y %H-%M-%S")

SAIDA = Path.home() / "Desktop"
if not SAIDA.exists():
    SAIDA = Path.home() / "OneDrive" / "Desktop"


def extrair_info(guia_planilha: Worksheet) -> list[dict[str, str] | None]:
    """
    Função para extrair as informações da planilha.

    :param guia_planilha: Guia da planilha.
    :type guia_planilha: Worksheet
    :return: Retorna uma lista de dicionários contendo as informações. Em caso de erro, a função retorna None.
    :rtype: list[dict[str, str]]
    """

    linha_fantasma: int = 0
    linha: int = 1
    lista_info: list[dict[str, str]] = []
    colunas = ["D", "F", "H", "K"]

    while not linha_fantasma > 20:
        if all(guia_planilha[f"{col}{linha}"].value is not None for col in colunas):
            if not (guia_planilha[f"D{linha}"].value == "QUANT. PR" or
                    guia_planilha[f"F{linha}"].value == "DATA DO EVENTO"):
                
                credor_completo: Match[str] | None = re.search(r"^\w+", str(guia_planilha[f"K{linha}"].value))
                credor: str = credor_completo.group() if credor_completo else "Desconhecido"
                data_evento = str(guia_planilha[f"F{linha}"].value)
                if isinstance(guia_planilha[f"F{linha}"].value, datetime):
                    data_evento = str(guia_planilha[f"F{linha}"].value.strftime("%d/%m/%Y"))

                info: dict[str, str] = {
                    "qunt_pr": f"{int(guia_planilha[f"D{linha}"].value):03}/{ANO}",
                    "data_evento": data_evento,
                    "evento": str(guia_planilha[f"G{linha}"].value),
                    "bairro": str(guia_planilha[f"H{linha}"].value),
                    "credor": credor
                }
                lista_info.append(info)
        else:
            linha_fantasma += 1
        linha += 1

    return lista_info


def escrever_texto(lista_info: list[dict[str, str]], direcao: bool) -> None:
    """
    Função para gerar o arquivo .txt contendo o texto para o relatório
    
    :param lista_info: Lista com os dicionários das informações.
    :type lista_info: list[dict[str, str]]
    :param direcao: Flag que indica qual tipo de relatório.
    :type direcao: bool
    """

    credores_repetidos: list = [evento["credor"] for evento in lista_info]
    credores: list = list(set(credores_repetidos))
    
    grupo: dict[str, list[dict[str,str]]] = {}
    for credor in credores:
        grupo[credor] = [evento for evento in lista_info if evento["credor"] == credor]

    with open(SAIDA / f"Relatório {AGORA}.txt", "w", encoding="utf-8") as relatorio:
        relatorio.write("EVENTOS SEM COMPROVAÇÃO:\n\n")
        for credor, evento in grupo.items():
            relatorio.write(f"*RELAÇÃO DE EVENTOS PENDENTES - SEMANA - {credor}*\n\n")
            for info in evento:
                if info["credor"] == credor:
                    if direcao:
                        relatorio.write(f"{info["evento"].strip()} - {info["bairro"].strip()}\n")
                    else:
                        relatorio.write(f"{info["qunt_pr"].strip()} - {info["data_evento"].strip()} - {info["evento"].strip()} - {info["bairro"].strip()}\n")
            relatorio.write("\n")


def main () -> None:
    """
    Coordena o fluxo do programa. 
    """

    def verificar_sair(input_user: str) -> bool:
        """
        Função auxiliar para verificar se o usuário quer sair do programa.
        
        :param input_user: Str que o usuário forneceu.
        :type input_user: str
        :return: Flag que indica se o usuário quer ou não finalizar o programa.
        :rtype: bool
        """

        if input_user.lower() == "sair":
            os.system('cls' if os.name == 'nt' else 'clear')
            return True
        return False


    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{AMARELO_N}   === [ {Path(__file__).name} ] ==={RESET}")
        print(f"{AMARELO_N}         [ 'sair' para finalizar ]    {RESET}\n")

        print(f"{CIANO_N}\n -> Cole o {AZUL_N}caminho da planilha{CIANO_N} com os eventos sem comprovação:{RESET}")
        print(f"{AMARELO_N}\n    OBS.: As colunas devem estar desta maneira:{RESET}")
        print(f"{AMARELO_N}    D           E       F                   G           H           I           J           K{RESET}")
        print(f"{AMARELO_N}    QUANT. PR   PR°     DATA DO EVENTO      EVENTO      Bairros     VALOR       ASSUNTO     CREDOR{RESET}")
        resposta: str = input("\n >> ").strip('"').strip("'")
        if verificar_sair(resposta):
            break

        caminho_planilha: Path = Path(resposta)
        if caminho_planilha.is_dir() or not caminho_planilha.suffix.lower() == ".xlsx":
            print(f"{VERMELHO_N}\n -> Caminho inválido! {MAGENTA_N}('.xlsx' não encontrado no caminho.)")
            time.sleep(5)
            continue

        try:
            planilha: Workbook = load_workbook(caminho_planilha, data_only=False)

            nomes_guias: list[str] = planilha.sheetnames
            for i, guia in enumerate(nomes_guias):
                print(f"\n{AZUL_N}    {i+1}{CIANO_N} • {guia}{RESET}")

            print(f"{CIANO_N}\n -> Escolha a {AZUL_N}Guia{CIANO_N} a ser atualizada:{RESET}")
            resposta: str = input(f"\n >> ").strip('"').strip("'")
            if verificar_sair(resposta):
                break
            if not resposta.isdigit():
                print(f"{VERMELHO_N}\n -> Escolha inválida! {MAGENTA_N}(Digite o número correspondente.){RESET}")
                time.sleep(3)
                continue

            guia_planilha_texto: str = nomes_guias[int(resposta)-1]
            guia_planilha: Worksheet = planilha[guia_planilha_texto]

            lista = extrair_info(guia_planilha)
            if lista is None:
                continue

            print(f"{CIANO_N}\n -> É um relatório para {AZUL_N}direção? {AMARELO_N}[ S | N ]{RESET}")
            direcao: str = input("\n >> ").upper().strip('"').strip("'")
            if verificar_sair(direcao):
                break

            if direcao == "S":
                direcao = True
            elif direcao == "N":
                direcao = False
            else: 
                print(f"{VERMELHO_N}\n -> Resposta inválida! {MAGENTA_N}('S' ou 'N')")
                time.sleep(3)
                continue

            escrever_texto(lista, direcao)

            print(f"{VERDE_N}\n -> Relatório gerado na Área de Trabalho.{RESET}")
            time.sleep(3)
            os.system('cls' if os.name == 'nt' else 'clear')
            break

        except PermissionError:
            print(f"{VERMELHO_N}\n -> Falha ao salvar. {MAGENTA_N}Feche a planilha e tente novamente.{RESET}")
        except InvalidFileException:
            print(f"{VERMELHO_N}\n -> Formato de planilha incompatível. {MAGENTA_N}Use uma planilha '.xlsx'.{RESET}")


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')  # Garante que as cores funcionem no terminal.
    main()
