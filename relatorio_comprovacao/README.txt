[ Gera o texto do relatório de comprovação. ]

[ Como usar ]

    - PASSO 1: Copie o caminho da planilha.

        Copie o caminho da planilha que contém as comprovações.

        >> ATENÇÃO - COLUNAS DA PLANILHA <<

            D           E       F                   G           H           I           J           K
            QUANT. PR   PR°     DATA DO EVENTO      EVENTO      Bairros     VALOR       ASSUNTO     CREDOR


    - PASSO 2: Execute o programa.

        Execute o programa 'py_tools_terminal.py'.
        Selecione o número referente à este programa ('relatorio_comprovacao.py').


    - PASSO 3: Caminho, guia da planilha e estrutura do relatório.

        Com o programa aberto, faça o seguinte:

        a. Cole o caminho da planilha;
        b. Escolha a guia da planilha (escreva o número correspondente);
        c. Escolha a estrutura do relatório - o modelo de relatório destinado à direção é diferente (veja como é estrutura abaixo, em "[ Resultado esperado ]").


[ Resultado esperado ]

    Será gerado na Área de Trabalho um arquivo de texto ('.txt') com o relatório das comprovações da planilha fornecida.
    A estrutura do relatório depende da escolha do usuário no "PASSO 3".

    Estrutura 1 - Normal:

        "EVENTOS SEM COMPROVAÇÃO:

        *RELAÇÃO DE EVENTOS PENDENTES - SEMANA - [credor]*

        [contrato] - [data] - [evento] - [local]
        ..."

    Estrutura 2 - Para a direção:


        "EVENTOS SEM COMPROVAÇÃO:

        *RELAÇÃO DE EVENTOS PENDENTES - SEMANA - [credor]*

        [evento] - [local]
        ..."


[ Erros conhecidos ]

    O usuário terá que adicionar a SEMANA manualmente no texto. 
