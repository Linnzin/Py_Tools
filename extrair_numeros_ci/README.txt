[ Extrai CI das pastas de contratação. ]

[ Como usar ]

    - Passo 1: Copie o caminho da pasta com as comprovações separadas por mês.

        >> pasta_a_ser_copiada <<
            ↳ mês
                ↳ pasta_de_contratação (xxxx - xx - xxxx - credor - evento)

        O programa também funcionará caso a pasta copiada seja a de um mês específico, mas o resultado só será referente a este mês. 

    - Passo 2: Execute o programa.

        Execute o programa 'py_tools_terminal.py'.
        Selecione o número referente à este programa ('extrair_numeros.py').

    - Passo 3: Cole o caminho no programa.

        Este programa só possui um campo de entrada.
        Neste campo, o usuário deverá colar o caminho da pasta copiada no "Passo 1".
        Também, neste campo, o usuário poderá escrever 'sair' para voltar para o menu de seleção de ferramentas.

[ Resultado esperado ]

    Será gerada na área de trabalho uma planilha "numeros_ci.xlsx". 
    Nesta planilha haverá apenas uma coluna "CI's", esta coluna haverá os números iniciais de cada pasta de contratação.

[ Erros conhecidos ]

    - O programa só considera 3 ou 4 números iniciais do nome da pasta. Qualquer coisa diferente disso será IGNORADA.
    - Se o nome da pasta não começar com o número do ci, a pasta será IGNORADA.
    - Se houver uma pasta que inicie com 3 ou 4 números e que não seja uma pasta de contratação, o programa incluirá na planilha.