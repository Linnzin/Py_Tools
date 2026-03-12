#!/usr/bin/env python3
"""
Programa para extrair CI das pastas de contratação. 
O programa entra na pasta de cada mês e armazena o número do ci de cada pasta de comprovação numa planilha.

Se for a primeira fez executando este código, execute isso no terminal: 
    pip install -r requirements.txt

Como usar:
    $ py extrair_numeros_ci.py 
"""

import os
import re
import time
from pathlib import Path

import pandas as pd
from pandas import DataFrame


__version__: str = "1.0"
__author__: str = "Lincoln P. da Silva"
__license__: str = "Proprietário"

VERMELHO_N: str = '\033[1;31m'
MAGENTA_N: str = '\033[1;35m'
AZUL_N: str = '\033[1;34m'
CIANO_N: str = '\033[1;36m'
VERDE_N: str = '\033[1;32m'
AMARELO_N: str = '\033[1;33m'
RESET: str = '\033[0m'

SAIDA = Path.home() / "Desktop"
if not SAIDA.exists():
    SAIDA = Path.home() / "OneDrive" / "Desktop"


def main() -> None:
    """
    Coordena o fluxo do programa.
    """

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{AMARELO_N}   === [ {Path(__file__).name} ] ==={RESET}")
        print(f"{AMARELO_N}       [ 'sair' para finalizar ]    {RESET}\n")

        print(f"\n{CIANO_N} -> Cole aqui o {AZUL_N}caminho da pasta geral{CIANO_N} da comprovações:{RESET}") 
        resposta: str = input("\n >> ").strip('"').strip("'")

        if resposta.lower() == "sair":
            os.system('cls' if os.name == 'nt' else 'clear')
            break

        caminho_pasta: Path = Path(resposta)
        if not caminho_pasta.is_dir():
            print(f"{VERMELHO_N}\n -> Caminho inválido! {MAGENTA_N}(O caminho fornecido não é uma pasta.){RESET}")
            time.sleep(5)
            continue
        
        pastas_lista: list[str] = [pasta_match.group(1) for pasta in caminho_pasta.rglob("*") if ((pasta.is_dir()) and (pasta_match := re.search(r"(\d{3,4})", pasta.name)))]
        df: DataFrame = pd.DataFrame({"CI's":pastas_lista})
        df.to_excel(SAIDA / "numeros_ci.xlsx", index=False)

        print(f"{VERDE_N}\n -> Planilha gerada na Área de Trabalho.{RESET}")
        time.sleep(5)
        os.system('cls' if os.name == 'nt' else 'clear')
        break


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')  # Garante que as cores funcionem no terminal.
    main()
