# Py_Tools

![Python Version](https://img.shields.io/badge/python-3.13+-blue?logo=python&logoColor=white) ![Platform](https://img.shields.io/badge/platform-Windows-0078D4?logo=windows&logoColor=white) [![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Este repositório contém um ecossistema de ferramentas desenvolvidas em **Python** para automação de fluxos administrativos, processamento de dados e integração com planilhas Excel. O projeto foi originalmente concebido e utilizado no setor de eventos da **SALTUR (Empresa Salvador Turismo)** para otimizar tarefas repetitivas e garantir a integridade dos dados.

Para usar qualquer ferramenta deste programa é preciso ter o interpretador **PYTHON 3.13+** instalado no computador.
**SO Compatível**: Windows 10/11 (Devido ao uso de bibliotecas de integração com a API Windows para criação de atalhos e automação de arquivos).

Este foi o meu **segundo projeto prático** utilizando Python. Desenvolvi este projeto com o objetivo de aprofundar meus conhecimentos na linguagem enquanto buscava uma solução real para otimizar os processos manuais no setor de eventos da SALTUR. 

## Funcionalidades Principais

O projeto é gerenciado por um **Hub Central** (`py_tools_terminal.py`) que oferece uma interface de terminal para acessar as seguintes ferramentas:

* **add_infra.py:** Sincronização automática entre planilhas de relações semanais e planilhas centrais de controle.
* **diario_contratos.py:** Processamento de textos de diários oficiais via **Regex**, extraindo dados estruturados para planilhas e resumos textuais.
* **extrair_numeros_ci.py:** Varredura em estruturas de diretórios para extração de identificadores de processos (CIs) baseada em padrões de nomenclatura.
* **relatorio_comprovacao.py:** Geração automatizada de relatórios de pendências para direção e gerência a partir de bases de dados Excel.

## Estrutura do Projeto

O projeto é modular. Cada ferramenta reside em sua própria subpasta com um `README.txt` específico e seu próprio arquivo de dependências. É possível adicionar outras ferramentas ao projeto: apenas tenha como base a estrutura das ferramentas já existentes.

## Como usar

* **Clone o repositório:**

```git clone https://github.com/Linnzin/Py_Tools.git```

* **Execute o arquivo:**

Caso seja a primeira vez executando o programa, o arquivo que deverá ser executado é o 'py_tools_terminal.py'.

```python py_tools_terminal.py```

Na primeira execução, o usuário é questionado se deseja criar um atalho na área de trabalho, nas execuções seguintes isso não será perguntado novamente.

* **Escolha a ferramenta:**

Este programa consiste em apenas uma tela de seleção de ferramenta.
Para selecionar a ferramenta, basta digitar o dígito correspondente à ferramenta desejada.
Após a escolha da ferramenta, o programa executará a ferramenta escolhida imediatamente.

## Outras Funcionalidades

Para utilizar qualquer uma das Funcionalidades abaixo, basta digitar a palavra entre aspas no menu de seleção de ferramentas.

* **"SAIR"**: Finaliza o programa. Dentro de outras ferramentas, para voltar para o HUB basta escrever "sair" em qualquer momento e em qualquer ferramenta.

* **"ATALHO"**: Gera um atalho na área de trabalho.

* **"PASTA"**: Abre a pasta do programa.

* **"CONFIG"**: Abre a pasta de configuração.

* **"BACKUP"**: Para mudar a pasta de backup. (Para resetar para a pasta padrão, apague o 'config.json' na pasta de configuração)
