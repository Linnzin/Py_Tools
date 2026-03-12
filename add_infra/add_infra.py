#!/usr/bin/env python3
"""
Programa para centralizar as relações de evento do ano. 

Se for a primeira fez executando este código, execute isso no terminal: 
    pip install -r requirements.txt 

Como usar:
    $ py add_infra.py 
"""
 
from copy import copy
from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import time
from typing import Any

from openpyxl import load_workbook
from openpyxl.cell.cell import Cell
from openpyxl.utils import get_column_letter
from openpyxl.utils.exceptions import InvalidFileException
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet


__version__: str = "1.4"
__author__: str = "Lincoln P. da Silva"
__license__: str = "Proprietário"

VERMELHO_N: str = '\033[1;31m'
MAGENTA_N: str = '\033[1;35m'
AZUL_N: str = '\033[1;34m'
CIANO_N: str = '\033[1;36m'
VERDE_N: str = '\033[1;32m'
VERDE_ESCURO: str = '\033[38;5;22m'
AMARELO_N: str = '\033[1;33m'
RESET: str = '\033[0m'

PASTA_CODES: Path = Path(__file__).parent.parent.resolve()
CONFIG: Path = Path(os.path.realpath(Path(os.getenv('APPDATA')) / "py_tools_configs" / "config.json"))


def criar_backup(local_arquivo: Path, pasta_backup: Path) -> None:
    """
    Função para criar backup das pastas de trabalho (planilha). 
    
    :param local_arquivo: Local da pasta de trabalho (planilha).
    :type local_arquivo: str
    :param pasta_backup: Local da pasta em que a cópia será salva.
    :type pasta_backup: str
    """

    agora: datetime = datetime.now()
    local_backup: Path = pasta_backup / f"Cópia {agora.strftime('%d-%m-%Y---%H-%M-%S')} - {local_arquivo.name}"
    try:
        shutil.copy2(local_arquivo, local_backup)
        print(f"{VERDE_N}\n -> Cópia de {local_arquivo.name} feita em:\n    {VERDE_ESCURO}{local_backup}{RESET}")

    except FileNotFoundError:
        print(f"{VERMELHO_N}\n -> Backup Falhou. {MAGENTA_N}Planilha Central{VERMELHO_N} não encontrada.{RESET}")


def achar_novas_linhas(planilhas_parciais_lista: list[Path]) -> list[tuple[Any | Cell]]:
    """
    Função para extrair as linhas de contratação de cada planilha da lista fornecida.
    
    :param planilhas_parciais_lista: Description
    :type planilhas_parciais_lista: list[Path]
    :return: Description
    :rtype: list[tuple[Any | Cell]]
    """

    linhas_novas = []
    for planilha_caminho in planilhas_parciais_lista:
        planilha: Workbook = load_workbook(planilha_caminho, data_only=False)
        linhas_fantasmas: int = 0
        for linha in planilha.active.iter_rows(min_row=3, values_only=False):
            if not (linha[0].value == None or
                    linha[1].value == None or
                    linha[3].value == None or
                    str(linha[2].value).upper() == "DATA" or
                    str(linha[3].value).upper() == "EVENTO" or
                    str(linha[5].value).upper() == "VALOR" or
                    str(linha[4].value).upper() == "LOCAL"):
                linhas_novas.append(linha)
            else:
                linhas_fantasmas +=1
            if linhas_fantasmas > 20:
                break

    return linhas_novas


def atualizar_total(guia_planilha: Worksheet, linhas_novas: list[tuple[Any | Cell]]) -> None:
    """
    Atualiza a planilha principal com as informações fornecidas pela lista.
    :param guia_planilha: Guia da planilha central.
    :type guia_planilha: Worksheet
    :param linhas_novas: Linhas a serem adicionadas na guia da planilha central.
    :type linhas_novas: list[tuple[Any | Cell]]
    """


    def _achar_linha_vazia(linha_atual: int) -> int:
        """
        Função auxiliar para encontrar a próxima linha vazia dentro da planilha central
        
        :param linha_atual: Linha atual.
        :type linha_atual: int
        :return: Linha vazia.
        :rtype: int
        """

        while not (guia_planilha[f"D{linha_atual}"].value == None or
                   guia_planilha[f"E{linha_atual}"].value == None or
                   guia_planilha[f"G{linha_atual}"].value == None):
            linha_atual += 1
        return linha_atual

    linha: int = _achar_linha_vazia(6)
    for nova_linha in linhas_novas:

        if not (guia_planilha[f"D{linha}"].value == None or
                guia_planilha[f"E{linha}"].value == None or
                guia_planilha[f"G{linha}"].value == None):
            linha: int = _achar_linha_vazia(linha)

        # coluna D até a N. Tabela central é deslocada para a esquerda em relação as tabelas parciais.
        for x in range(4, 15):
            y = x - 4
            coluna: str = get_column_letter(x)
            guia_planilha[f"{coluna}{linha}"].value = nova_linha[y].value
            if nova_linha[y].has_style:
                guia_planilha[f"{coluna}{linha}"].fill = copy(nova_linha[y].fill)
                guia_planilha[f"{coluna}{linha}"].border = copy(nova_linha[y].border)
                guia_planilha[f"{coluna}{linha}"].alignment = copy(nova_linha[y].alignment)
                guia_planilha[f"{coluna}{linha}"].number_format = nova_linha[y].number_format

        linha += 1


def main() -> None:
    """ 
    Coordena o fluxo do programa.
    """
    with open(CONFIG, 'r', encoding='utf-8') as arquivo:
        config: dict[str, str | None] = json.load(arquivo)
        pasta_backup: Path = Path(config["backup"])

    if not pasta_backup.exists() or not pasta_backup.is_dir():
        pasta_backup = (PASTA_CODES / "backups").resolve()
        pasta_backup.mkdir(parents=True, exist_ok=True)
        config["backup"] = pasta_backup

        with open (CONFIG, 'w', encoding='utf-8') as arquivo:
            json.dump(config, arquivo, ensure_ascii=False, indent=4)
            
        with open(CONFIG, 'r', encoding='utf-8') as arquivo:
            config: dict[str, str | None] = json.load(arquivo)
            print(f"{CIANO_N} -> Pasta de backup {AZUL_N}INVÁLIDA{CIANO_N}! A pasta de backup foi redefinida para a pasta padrão: {RESET}")
            print(f"{RESET}    {config["backup"]}")


    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{AMARELO_N}   === [ {Path(__file__).name} ] ==={RESET}")
        print(f"{AMARELO_N}    [ 'sair' p/ finalizar ]    {RESET}\n")

        print(f"{CIANO_N}\n -> Cole o {AZUL_N}caminho da pasta {CIANO_N}contendo as {AZUL_N}relações do mês:{RESET}")
        texto: str = input(f"\n >> ").strip('"').strip("'")
        if texto.lower() == "sair":
            os.system('cls' if os.name == 'nt' else 'clear')
            break

        planilhas_parciais: Path = Path(texto)
        if ((not planilhas_parciais.is_dir) or (texto == '') or (not planilhas_parciais.exists())):
            print(f"{VERMELHO_N}\n -> Caminho inválido! {MAGENTA_N}(O caminho fornecido não é uma pasta válida.){RESET}")
            time.sleep(3)
            continue

        planilhas_parciais_lista: list[Path] = [planilha for planilha in planilhas_parciais.glob("*/*.xlsx")]
        print(f"\n{CIANO_N} -> Planilhas encontradas: {RESET}\n")
        for planilha in planilhas_parciais_lista:
            print(f"{AZUL_N}    • {planilha.name}")
        print(f"\n{AZUL_N} -> CONFIRMAÇÃO: {CIANO_N}Continuar com essas planilhas? [ S | N ]{RESET}")
        texto: str = input(f"\n >> ").strip('"').strip("'")
        if texto.lower() == "sair":
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        elif texto.lower() == "n":
            continue
        elif texto.lower() != "s":
            print(f"{VERMELHO_N}\n -> Resposta inválida! {MAGENTA_N}('S' ou 'N'){RESET}")
            time.sleep(3)
            continue

        print(f"{CIANO_N}\n -> Cole o {AZUL_N}caminho da planlha central {CIANO_N}que receberá as {AZUL_N}relações do mês:{RESET}")
        texto: str = input(f"\n >> ").strip('"').strip("'")
        if texto.lower() == "sair":
            os.system('cls' if os.name == 'nt' else 'clear')
            break

        local_planilha_central: Path = Path(texto)
        if (not local_planilha_central.exists() or local_planilha_central.suffix != ".xlsx"):
            print(f"{VERMELHO_N}\n -> Caminho inválido! {MAGENTA_N}(O arquivo não é uma planilha '.xlsx' ou não existe.){RESET}")
            time.sleep(3)
            continue

        try:
            planilha_central: Workbook = load_workbook(local_planilha_central, data_only=False)

            nomes_guias: list[str] = planilha_central.sheetnames
            for i, guia in enumerate(nomes_guias):
                print(f"\n{AZUL_N}    {i+1}{CIANO_N} • {guia}{RESET}")

            print(f"{CIANO_N}\n -> Escolha a {AZUL_N}Guia{CIANO_N} a ser atualizada:{RESET}")
            texto: str = input(f"\n >> ").strip('"').strip("'")
            if texto.lower() == "sair":
                os.system('cls' if os.name == 'nt' else 'clear')
                break
            if not texto.isdigit():
                print(f"{VERMELHO_N}\n -> Escolha inválida! {MAGENTA_N}(Digite o número correspondente.){RESET}")
                time.sleep(3)
                continue

            guia_planilha_central: str = nomes_guias[int(texto)-1]
            guia_planilha: Worksheet = planilha_central[guia_planilha_central]

            criar_backup(local_planilha_central, Path(pasta_backup))
            linhas_novas: list[tuple[Any | Cell]] = achar_novas_linhas(planilhas_parciais_lista)
            atualizar_total(guia_planilha, linhas_novas)
            planilha_central.save(local_planilha_central)

        except PermissionError:
            print(f"{VERMELHO_N}\n -> Falha ao salvar. {MAGENTA_N}Feche a planilha e tente novamente.{RESET}")
        except InvalidFileException:
            print(f"{VERMELHO_N}\n -> Formato de planilha incompatível. {MAGENTA_N}Use uma planilha '.xlsx'.{RESET}")

        print(f"{VERDE_N}\n -> Planilha atualizada!{RESET}")
        time.sleep(3)
        break
 

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')  # Garante que as cores funcionem no terminal.
    main()
