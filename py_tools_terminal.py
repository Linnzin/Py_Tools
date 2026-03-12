#!/usr/bin/env python3
"""
Programa para centralizar a inicialização das ferramentas de automação.

Se for a primeira fez executando este código, execute isso no terminal (opcional, o código instalará automaticamente): 
    pip install -r requirements.txt

Como usar: 
    $ py py_tools_terminal.py
"""

import importlib
from importlib.metadata import distribution, PackageNotFoundError
import json
import os
from pathlib import Path
import shutil
import subprocess
import site
import sys
import threading
import time
from typing import Any


__version__: str = "1.4"
__author__: str = "Lincoln P. da Silva"
__license__: str = "Proprietário"

AMARELO_N: str = '\033[1;33m'
LARANJA_N: str = '\033[1;38;5;208m'
VERMELHO_N: str = '\033[1;31m'
MAGENTA_N: str = '\033[1;35m'
CIANO_N: str = '\033[1;36m'
AZUL_N: str = '\033[1;34m'
VERDE_N: str = '\033[1;32m'
RESET: str = '\033[0m'

PASTA_CODES: Path = Path(__file__).parent.resolve()
PASTA_CONFIG: Path = Path(os.path.realpath(Path(os.getenv('APPDATA')) / "py_tools_configs"))    # Lidando com o interpretador da Microsoft Store
SAIDA = Path.home() / "Desktop"
if not SAIDA.exists():
    SAIDA = Path.home() / "OneDrive" / "Desktop"


def garantir_lib(nome_pip: str) -> None:
    """
    Verifica se uma biblioteca está instalada.
    
    :param nome_pip: Nome do pacote no PyPI.
    :type nome_pip: str
    """
    try:
        distribution(nome_pip)

    except PackageNotFoundError:
        parar_spinner = threading.Event()

        def animar_spinner() -> None:
            """
            Função auxiliar para exibir no terminal uma roda de carregamento (spinner).
            """
            chars = ['|', '/', '-', '\\']
            idx = 0
            os.system('cls' if os.name == 'nt' else 'clear')
            while not parar_spinner.is_set():
                print(f"{AMARELO_N} -> Instalando {LARANJA_N}'{nome_pip}'{AMARELO_N} - {chars[idx]}{RESET}", end="\r")
                idx = (idx + 1) % len(chars)
                time.sleep(0.1)

        thread_spinner = threading.Thread(target=animar_spinner)
        thread_spinner.start()

        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", nome_pip],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            importlib.reload(site)

        except Exception as e:
            parar_spinner.set()
            thread_spinner.join()
            print(f"{VERMELHO_N}\n -> Erro ao instalar o pacote {MAGENTA_N}'{nome_pip}'{VERMELHO_N}. Verifique a conexão.{RESET}")
            print(f"{VERMELHO_N}\n -> Verifique sua conexão ou instale manualmente no Prompt de Comando via {MAGENTA_N}'pip install {nome_pip}'.{RESET}")
            time.sleep(3)
            sys.exit(1)

        parar_spinner.set()
        thread_spinner.join()
        print(f" -> {LARANJA_N}'{nome_pip}'{AMARELO_N} instalado com sucesso!{RESET}                        ")
        time.sleep(3)


def exibir_cabecalho() -> None:
    """
    Função para exibir o cabeçalho.  
    """

    os.system('cls' if os.name == 'nt' else 'clear')
    print(rf"""
       {AMARELO_N}___         {LARANJA_N}______          __  
      {AMARELO_N}/ _ \__ __  {LARANJA_N}/_  __/__  ___  / /__
     {AMARELO_N}/ ___/ // /   {LARANJA_N}/ / / _ \/ _ \/ (_-<
    {AMARELO_N}/_/   \_, /   {LARANJA_N}/_/  \___/\___/_/___/
         {AMARELO_N}/___/    {RESET}                        
    """)
    print(f"{AMARELO_N}       [ 'sair' para finalizar ]    {RESET}\n")
        

def exibir_menu() -> dict[str, Path]:
    """
    Função para exibir o menu do programa.
    O menu é construído dinamicamente, de acordo com os programas presentes na pasta. 
    
    :return: Dicionário com o índice e o caminho dos programas.
    :rtype: dict[str, Path]
    """

    print(f"\n{AMARELO_N} -> Selecione a {LARANJA_N}ferramenta desejada:{RESET}")

    dict_menu: dict[str, Path] = {}
    pastas = [p for p in PASTA_CODES.iterdir() if p.is_dir() and not p.name == "backups"]

    for i, pasta in enumerate(pastas, start=1):
        
        descricao: Path = PASTA_CODES / pasta.name / f"README.txt"
        caminho_arquivo: Path = PASTA_CODES / pasta.name / f"{pasta.name}.py"

        if not caminho_arquivo.exists():
            continue

        dict_menu[str(i)] = caminho_arquivo

        if descricao.exists():
            with open(descricao, "r", encoding="utf-8") as texto:
                descricao = texto.readline().strip()
        else:
            descricao = f"[ Descrição não encontrada. ]"

        nome_terminal: str = f"\n{AMARELO_N}    {i} • {caminho_arquivo.stem}{LARANJA_N}.py{RESET}"
        preenchimento: str = " " * (65 - len(nome_terminal))
        print(f"{nome_terminal}{preenchimento}{descricao}")

    return dict_menu


def criar_atalho() -> None:
    """
    Função para criar atalho na Área de Trabalho
    """
    try:
        garantir_lib("pywin32")
        from win32com.client import Dispatch, CDispatch

    except ImportError:
        print(f"{VERMELHO_N}\n -> Erro ao importar bibliotecas. {MAGENTA_N}As bibliotecas foram instaladas, mas o Windows impede a importação.{RESET}")
        time.sleep(3)
        sys.exit(1)

    path_atalho = SAIDA / f"Py_Tools.lnk"
    shutil.copy2(PASTA_CODES / "atalho_icone.ico", PASTA_CONFIG / "atalho_icone.ico")

    shell: CDispatch = Dispatch('WScript.Shell')

    atalho: Any = shell.CreateShortcut(str(path_atalho))
    atalho.TargetPath = sys.executable
    atalho.Arguments = f'"{__file__}"'
    atalho.WorkingDirectory = str(PASTA_CODES)
    atalho.Description = "Ferramentas de automação - Saltur."
    atalho.IconLocation = f"{(PASTA_CONFIG / "atalho_icone.ico").resolve()},0"
    atalho.save()

    print(f"{VERDE_N}\n -> Atalho criado!{RESET}")
    time.sleep(3)


def criar_config(caminho_backup: Path | None = None) -> None:
    """
    Função para criar o arquivo de configuração.
    
    :param caminho_backup: Caminho da pasta de backup.
    :type caminho_backup: Path | None
    """

    if not caminho_backup:
        caminho: Path = (PASTA_CODES / "backups").resolve()
        caminho.mkdir(parents=True, exist_ok=True)
    else:
        try:
            caminho_backup.resolve().mkdir(parents=True, exist_ok=True)
            caminho: Path = caminho_backup.resolve()
        except OSError as e:
            print(f"\n{AMARELO_N} -> Erro ao criar pasta personalizada. Mudando para a {LARANJA_N}pasta de backup padrão{AMARELO_N}.{RESET}")
            caminho: Path = (PASTA_CODES / "backups").resolve()
            caminho.mkdir(parents=True, exist_ok=True)


    configuracoes = {
        "backup": caminho
    }
    
    with open(PASTA_CONFIG / "config.json", "w", encoding="utf-8") as config:
        json.dump(configuracoes, config, ensure_ascii=False, indent=4, default=str)


def main() -> None:
    """
    Coordena o fluxo do programa.
    """
    while not (PASTA_CONFIG / "config.json").exists():
        PASTA_CONFIG.mkdir(parents=True, exist_ok=True)
        criar_config()
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{AMARELO_N}\n -> Deseja criar um {LARANJA_N}atalho na Área de Trabalho{AMARELO_N}? [ S | N ]{RESET}")
        resposta_atalho: str = input(f"\n >> ")
        if resposta_atalho.upper() == "S":
            criar_atalho()
        elif resposta_atalho.upper() == "N":
            pass
        else:
            print(f"{VERMELHO_N}\n -> Resposta inválida! {MAGENTA_N}('S' ou 'N')")
            time.sleep(3)
            continue

    while True:
        exibir_cabecalho()
        menu: dict[str, Path] = exibir_menu()
        escolha: str = input(f"\n >> ")

        if escolha.lower() == "sair":
            os.system('cls' if os.name == 'nt' else 'clear')
            break

        elif escolha.lower() == "atalho":
            criar_atalho()
            continue

        elif escolha.lower() == "pasta":
            os.startfile(PASTA_CODES)
            continue

        elif escolha.lower() == "config":
            os.startfile(PASTA_CONFIG)
            continue

        elif escolha.lower() == "backup":
            print(f"{AMARELO_N}\n -> Cole o caminho da nova pasta de {LARANJA_N}backup{AMARELO_N}: [ ENTER para cancelar ]{RESET}")
            caminho_backup: str = input(f"\n >> ")
            if caminho_backup == "":
                continue
            caminho_backup: Path = Path(caminho_backup)
            if not caminho_backup.is_dir():
                print(f"{VERMELHO_N}\n -> Caminho inválido! {MAGENTA_N}(O caminho fornecido não é uma pasta.)")
                time.sleep(3)
                continue
            criar_config(caminho_backup)
            print(f"{VERDE_N}\n -> Configuração atualizada!{RESET}")
            time.sleep(3)
            continue

        arquivo: Path | None = menu.get(escolha, None)
        if not arquivo:
            time.sleep(3)
            continue
        
        requirements_caminho: Path = arquivo.parent / "requirements.txt"
        with open (requirements_caminho, "r", encoding="utf-8") as requirements:
            bibliotecas: list[str] = requirements.readlines()
        for lib in bibliotecas:
            garantir_lib(lib.strip())

        subprocess.run(
            [sys.executable, arquivo.name],
            cwd=arquivo.parent
        )


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')  # Garante que as cores funcionem no terminal.
    main()
