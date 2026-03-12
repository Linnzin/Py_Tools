#!/usr/bin/env python3
"""
Programa para gerar planilha e/ou texto com as contratações presentes no diário.
É possivel gerar um resumo simples das contratações do diário (planilha + texto), ou 
formartar as informações no padrão da planilha 'Controle Contratos DIRFESP' (restando 
apenas colar as informações na planilha citada). 

Se for a primeira fez executando este código, execute isso no terminal: 
    pip install -r requirements.txt 

Como usar:
    $ py diario_contratos.py
"""

import os
from pathlib import Path
import re
from re import Match
import time
from typing import Any

import pandas as pd
from pandas import DataFrame


__version__: str = "1.5"
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


def organizar_info(texto_caminho: Path, data_diario: str, debug: bool) -> list[dict[str, str | float]] | None:
    """
    Função para extrair e organizar as informações do arquivo de texto informado.
    
    :param texto: Caminho do arquivo de texto.
    :type texto: Path
    :param data_diario: Data de publicação do diário.
    :type data_diario: str
    :param debug: Flag para gerar um arquivo de texto com os contratos que o programa identificou.
    :type debug: bool
    :return: Lista com as informações separadas (dicionário). Retorna 'None' somente em caso de debug.
    :rtype: list[dict[str, str | float]]
    """

    def extrair_info(padrao: str, contrato: str) -> str | None:
        """
        Função auxiliar para extrair uma informação específica de um resumo de contrato.
        A informação extraída é definida pelo "group(1)" do padrão re fornecido.
        
        :param padrao: Padrão re.
        :type padrao: str
        :param contrato: Texto contendo o resumo do contrato
        :type contrato: str
        :return: "group(1)" do padrão (se houver)
        :rtype: str | None
        """

        texto_match: Match | None = re.search(padrao, contrato, re.IGNORECASE | re.DOTALL)
        return str(texto_match.group(1)) if texto_match else None

    with open(texto_caminho, 'r', encoding="utf-8") as arquivo:
        texto_bruto: str = arquivo.read()
    texto: str = re.sub(r'-\n', '', texto_bruto)
    texto: str = " ".join(texto.split())

    contratos: list[str] = []
    partes_texto: list[str | Any] = re.split(r"(?=CONTRATO\s+[Nn]?[ºo0O°\.]?\s*(?:[a-zA-Z0-9-]+\/\d{4}).?)", texto)
    for parte in partes_texto:
        if re.match(r"CONTRATO\s+[Nn]?[ºo0O°\.]?\s*(?:[a-zA-Z0-9-]+\/\d{4}).?", parte):
            contratos.append(parte)

    if debug:
        with open(SAIDA / "contratos_debug.txt", "w", encoding="utf-8") as arquivo:
            for contrato in contratos:
                arquivo.write(f"{contrato}\n\n---------\n\n")
        return None

    infos: list[dict[str, str | float | None]] = []

    for contrato in contratos:
        valor: str | None = extrair_info(r"CLÁUSULA\s*SEGUNDA\s*(?:.*?)(?:R\$\s*)(\d+(?:\.\d{3})*(?:,\d{2})?)(?:.*?)\s*CLÁUSULA\s*TERCEIRA", contrato)
        if valor is not None:
            valor: float = float(valor.replace('.','').replace(',','.'))

        infos.append({
            "n_contrato": extrair_info(r"CONTRATO(?:\s*[Nn][ºo0°O\.]?\s*|\s*)([a-zA-Z0-9-]+\/\d{4}).?", contrato),
            "n_pr": extrair_info(r"PROCESSO(?:.*?)(?:\s*n[ºo0O\.]?\s*|\s*)(\S+\/\d{4})", contrato),
            "credor": extrair_info(r"Contratada:\s*(.*?)\s*CNPJ", contrato),
            "cnpj": extrair_info(r"CNPJ(?:\s*[Nn][ºo0O\.]?\s*|\s*)?\s*:?\s*(\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2})", contrato),
            "objeto": extrair_info(r"CLÁUSULA\s*PRIMEIRA\s*[-–]\s*DO\s*OBJETO\s*[-–]\s*(.*?)\s*CLÁUSULA\s*SEGUNDA", contrato),
            "atracao": extrair_info(r"CLÁUSULA\s*PRIMEIRA\s*(?:.*?)(?:atração\s*artística|representação\s*de)\s*[“”\"](.*?)[“”\"]\s*,?(?:.*?)\s*CLÁUSULA\s*SEGUNDA", contrato),
            "valor": valor,
            "fonte": extrair_info(r"CLÁUSULA\s*TERCEIRA\s*(?:.*?)\sFonte\s*:\s*(\d{1}\.\d{3}\.\d{1})", contrato),
            "proj_ativ": extrair_info(r"CLÁUSULA\s*TERCEIRA\s*(?:.*?)\s*Ação\s*:\s*\d*(\d{4})", contrato),
            "el_despesa": extrair_info(r"CLÁUSULA\s*TERCEIRA\s*(?:.*?)\s*Elemento\s*de\s*Despesa\s*:\s*(\d{2}\.\d{2}\.\d{2})", contrato),
            "clausula_segunda": extrair_info(r"CLÁUSULA\s*SEGUNDA\s*[-–]\s*DO\s*VALOR\s*[-–]\s*(.*?)\s*CLÁUSULA\s*TERCEIRA", contrato),
            "data_evento": extrair_info(r"CLÁUSULA\s*PRIMEIRA\s*(?:.*?)?\s*nos?\s*dias?\s*(.*?(?:2026))(?:.*?)\s*CLÁUSULA\s*SEGUNDA", contrato),
            "carnaval": extrair_info(r"CLÁUSULA\s*PRIMEIRA\s*(?:.*?)(Carnaval )(?:.*?)\s*CLÁUSULA\s*SEGUNDA", contrato),
            "data_diario": data_diario
        })
            
    return infos


def gerar_planilha(infos: list[dict[str, str | float | None]], resumo: bool) -> None:
    """
    Função para gerar a planilha com as informações dos contratos.
    
    :param info: Lista com as informações dos contratos. 
    :type info: list[dict[str, str | float | None]]
    :param resumo: Flag que define a estrutura da planilha.
    :type resumo: bool
    """

    def formatar_datas(datas: list[str | None]) -> list[str | None]:
        """
        Função auxiliar para formatar datas completas.
        Exemplo:
        'dia de mes de ano' -> 'dd/mm/aaaa'
        'dia e dia de mes de ano' -> 'dd, dd/mm/aaaa'
        
        :param datas: Lista de datas para formatar.
        :type datas: list[str | None]
        :return: Lista de datas formatadas
        :rtype: list[str | None]
        """

        datas_formatadas: list[str] = []
        dict_meses: dict[str, str] = {
            'janeiro': '01', 'fevereiro': '02', 'março': '03',
            'abril': '04', 'maio': '05', 'junho': '06',
            'julho': '07', 'agosto': '08', 'setembro': '09',
            'outubro': '10', 'novembro': '11', 'dezembro': '12'
        }
        padrao_data_completa: str = r"(\d{1,2})\s+de\s+([a-zç]+)\s+de\s+(\d{4})"

        for data_ in datas:

            if data_ is None:
                datas_formatadas.append(data_)
                continue

            partes: list[str] = [p.strip() for p in re.split(r',|\se\s', data_) if p.strip()]
            ultima_parte: str = partes[-1]

            ultima_data_final = None
            if data_match := re.match(padrao_data_completa, ultima_parte):
                dia, mes_nome, ano = data_match.groups()
                mes_numero = dict_meses.get(mes_nome)

                ultima_data_final: str = f"{dia.zfill(2)}/{mes_numero}/{ano}"

            extras_data_final: list[str] = []
            for parte in partes[:-1]:
                dia_extra = re.sub(r'\D', '', parte)
                extras_data_final.append(dia_extra)

            if extras_data_final and ultima_data_final:
                data_final: str = ", ".join(extras_data_final)
                data_final += f", {ultima_data_final}"

            elif ultima_data_final:
                data_final: str = ultima_data_final

            else:
                data_final: str = data_
            
            if data_final == "None":
                data_final = None
            datas_formatadas.append(data_final)

        return datas_formatadas


    def formatar_datas_afm(datas: list[str | None]) -> list[str| None]:
        """
        Função auxiliar para formatar as datas no padrão encontrado na 'afm'.
        Exemplo:
        'dia de mes de ano' -> 'dd/mm/aaaa'
        'dia e dia de mes de ano' -> 'dd/mm e dd/mm/aaaa'
        
        :param datas: Description
        :type datas: list[str | None]
        :return: Description
        :rtype: list[str | None]
        """

        datas_afm: list[str | None] = []
        for data_ in datas:

            if data_ == None:
                datas_afm.append(None)
                continue 

            partes: list[str] = [p.strip() for p in re.split(r',', data_) if p.strip()]

            ultima_parte: str = partes.pop()
            ultima_parte_cortada: Match | None = re.match(r"(\d{1,2})\/(\d{1,2})\/(\d{4})", ultima_parte)
            if ultima_parte_cortada is None:
                datas_afm.append(None)
                continue

            mes: str = ultima_parte_cortada.group(2)
            for i, parte in enumerate(partes):
                partes[i] = f"{parte}/{mes}"
            dias_extras: str = ", ".join(partes)
            if dias_extras:
                datas_afm.append(f"{dias_extras} e {ultima_parte}")
                continue

            datas_afm.append(ultima_parte)

        return datas_afm


    df: DataFrame = pd.DataFrame(infos)
    if not resumo:
        df = df.drop(columns=["atracao", "clausula_segunda", "data_evento", "carnaval"])
        df.to_excel(SAIDA / "contratos_dirfesp.xlsx", header=False, index=False)

    else:
        datas_formatadas: list[str | None] = formatar_datas([info["data_evento"] for info in infos])
        datas_afm_formatadas: list[str | None] = formatar_datas_afm(datas_formatadas)

        df = df.filter(items=["n_contrato", "n_pr", "atracao", "valor", "data_evento", "carnaval", "data_diario"])
        df["data_evento"] = datas_formatadas
        pos = df.columns.get_loc("data_evento")
        df.insert(pos + 1, "data_afm", datas_afm_formatadas)

        df.to_excel(SAIDA / "resumo_contratos.xlsx", header=True, index=False)


def gerar_texto(infos: list[dict[str, str | float | None]]) -> None:
    """
    Função para gerar o resumo das contratações artísticas.
    
    :param infos: Informações extraídas do diário.
    :type infos: list[dict[str, str | float | None]]
    """

    with open(SAIDA / "resumo_contratos.txt", "w", encoding="utf-8") as resumo:
        for info in infos:
            resumo.write(f"CONTRATO Nº {info["n_contrato"]}, {info["objeto"]}\n\n{info["clausula_segunda"]}\n\n")


def main() -> None:
    """
    Coordena o fluxo do programa. 
    """

    while True:
        debug = False
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n{AMARELO_N}   === [ {Path(__file__).name} ] ==={RESET}")
        print(f"{AMARELO_N}      [ 'sair' para finalizar ]    {RESET}\n")

        print(f"\n{CIANO_N} -> Cole o {AZUL_N}caminho do texto ('.txt') {CIANO_N}com os {AZUL_N}Contratos da SALTUR:{RESET}")
        resposta: str = input("\n >> ").strip('"').strip("'")

        if resposta.lower() == "debug":
            debug = True
            resposta: str = input("\n >> ").strip('"').strip("'")
        if resposta.lower() == "sair":
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        texto_caminho: Path = Path(resposta)
        if texto_caminho.is_dir():
            print(f"{VERMELHO_N}\n -> Caminho inválido! {MAGENTA_N}(O caminho indicado é uma pasta e não um arquivo de texto!){RESET}")
            time.sleep(5)
            continue
        if not texto_caminho.suffix == ".txt":
            print(f"{VERMELHO_N}\n -> Caminho inválido! {MAGENTA_N}('.txt' não encontrado no caminho.){RESET}")
            time.sleep(5)
            continue
        if not texto_caminho.exists():
            print(f"{VERMELHO_N}\n -> Caminho inválido! {MAGENTA_N}(Este arquivo não existe!){RESET}")
            time.sleep(5)
            continue

        print(f"\n{CIANO_N} -> Escreva a {AZUL_N}data de publicação {CIANO_N}do diário: {AMARELO_N}[ dd/mm/aaaa ]{RESET}")
        data: str = input("\n >> ").strip('"').strip("'")

        if data.lower() == "sair":
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        data_match = re.search(r"\d{2}\/\d{2}\/\d{4}", data)
        if data_match is None:
            print(f"{VERMELHO_N}\n -> Data inválida! {MAGENTA_N}(Não está no formato 'dd/mm/aaaa'!){RESET}")
            time.sleep(5)
            continue
            
        infos: list[dict[str, str | float | None]] = organizar_info(texto_caminho, data, debug)

        if debug:
            os.system('cls' if os.name == 'nt' else 'clear')
            break

        print(f"\n{CIANO_N} -> Deseja {AZUL_N}organizar{CIANO_N} as informações de qual maneira?{RESET}")
        print(f"\n{AMARELO_N}    1 • Padrão 'Controle Contratos DIRFESP.xlsb'{RESET}")
        print(f"\n{AMARELO_N}    2 • Resumo dos Contratos{RESET}")
        resposta: str = input("\n >> ").strip('"').strip("'")

        if resposta.lower() == "sair":
            os.system('cls' if os.name == 'nt' else 'clear')
            break

        elif resposta.lower() == "1":
            gerar_planilha(infos, False)

            print(f"{VERDE_N}\n -> Planilha gerada na Área de Trabalho.{RESET}")
            time.sleep(5)
            os.system('cls' if os.name == 'nt' else 'clear')
            break

        elif resposta.lower() == "2":
            gerar_planilha(infos, True)
            gerar_texto(infos)

            print(f"{VERDE_N}\n -> Planilha e texto gerados na Área de Trabalho.{RESET}")
            time.sleep(5)
            os.system('cls' if os.name == 'nt' else 'clear')
            break

        else:
            print(f"{VERMELHO_N}\n -> Resposta inválida! {MAGENTA_N}(Escolha um número! [ 1 | 2 ]){RESET}")
            time.sleep(5)
            continue    


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')  # Garante que as cores funcionem no terminal.
    main()
