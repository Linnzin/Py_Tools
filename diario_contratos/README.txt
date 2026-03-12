[ Gera planilha e/ou texto com as contratações presentes no diário. ]

[ Como usar ]

    - Passo 1: Texto dos contratos. 

        Copie todos os contratos do diário em um arquivo de texto ('.txt'). 
        Copie a partir do "RESUMO DO CONTRATO" até o final do último contrato.
    
        >> ATENÇÃO: NÃO COPIE o cabeçalho da página do diário <<

    - Passo 2: Execute o programa.

        Execute o programa 'py_tools_terminal.py'.
        Selecione o número referente à este programa ('diario_contratos.py').

    - Passo 3: Cole o caminho, escreva a data e escolha o modelo.

        Este programa possui três campos de entrada.

        Primeiro campo: Cole o caminho do arquivo de texto criado no "Passo 1".
        Segundo campo: Digite a data de publicação do diário.
        Terceiro campo: Escolha a estrutura da saída (mais detalhes abaixo).

[ Resultado esperado ]

    Todos os arquivos gerados serão salvos na área de trabalho.

    Estrutura 1: 'contratos_dirfesp.xlsx'

        As informações dos contratos serão organizados de acordo com a formatação da planilha 'contratos_dirfesp.xlsx'.

    Estrutura 2: 'resumo_contratos.xlsx' & 'resumo_contratos.txt'

        Serão gerados dois arquivos na área de trabalho:

        'resumo_contratos.txt': Todos os contratos serão organizados em forma de mensagem. Seguindo o seguinte modelo:

            "CONTRATO Nº XXX/2026, [Cláusula primeira].
            
            [Cláusula segunda]"

        'resumo_contratos.xlsx': Todos os contratos serão organizados em uma planilha com as seguintes colunas:

            • "n_contrato": Número do contrato;
            • "n_pr": Número do processo;
            • "atracao": Nome da atração (se houver);
            • "valor": Valor da contratação (se houver);
            • "data_evento": Data do evento (se houver);
            • "data_afm": Data do evento na formatação afm (se houver);
            • "carnaval": Marcação se a contratação é ou não referente ao carnaval;
            • "data_diario": Data de publicação do diário (fornecida no "Passo 1");

[ Erros conhecidos ]

    - Não reconhece erros de digitação.
    - Não reconhece CNPJ que não segue o padrão "XX.XXX.XXX/XXXX-XX".
    - Qualquer mudança de ordem das cláusulas não será reconhecida.
      (situação ex.: valor do contrato apareça na terceira cláusula ao invés da segunda, como de costume) 
    - Por via de regra, qualquer alteração na estrutura do texto do resumo do contrato tem grande potencial de não ser reconhecido.
      (O programa é preciso e rigoroso)

[ Observação ]

    Antes de organizar as informações, o programa separa os contratos do texto.
    É possível conferir se o programa separou os contratos de maneira correta.
    Para isso, basta escrever "debug" no primeiro campo, se no campo seguinte colar o caminho do texto do "Passo 1".
    Será gerado na área de trabalho um arquivo de texto com os contratos separados ('contratos_debug.txt'), após isso o programa se encerrará.
    Esse texto pode ser útil para resolver erros nos arquivos gerados pelo programa (fica mais fácil de ver onde o programa está errando).
    É possível usar esse texto no "Passo 1".