[ Centraliza as relações de evento do ano. ]

[ Como usar ]

    - PASSO 1: Copie os caminhos necessários.

        a. Caminho da pasta que contém as relações semanais.

            >> X - MÊS << (copie o caminho desta pasta)
                ↳ 1 - XX.XX a XX.XX.XXXX
                ↳ 2 - XX.XX a XX.XX.XXXX
                ↳ 3 - XX.XX a XX.XX.XXXX
                ↳ 4 - XX.XX a XX.XX.XXXX
                    ↳ FINAL DE SEMANA
                    ↳ XX - RELAÇÃO EVENTOS - XX.XX a XX.XX.XXXX - CREDOR.xlsx
            
        (O programa não considerará os arquivos contidos nas pastas referentes aos finais de semana.)
        
        b. Caminho da planilha que receberá as relações semanais.

        >> ATENÇÃO - COLUNAS DAS PLANILHAS <<

            Planilha Central:   

            D       E       F       G       H       I       J           K       L               M       N 
            Nº CI   PRN°    DATA    EVENTO  LOCAL   VALOR   SERVIÇO     OBS.    SITUAÇÃO REAL   STATUS  OBS

            Planilhas das relações semanais:  

            A       B       C       D       E       F       G           H       I               J
            Nº CI   PRNº    DATA    EVENTO  LOCAL   VALOR   SERVIÇO     OBS.    SITUAÇÃO REAL   NOTA DE EMPENHO


    - PASSO 2: Execute o programa.

        Execute o programa 'py_tools_terminal.py'.
        Selecione o número referente à este programa ('add_infra.py').


    - PASSO 3: Cole os caminhos, confirme a pasta e escolha a guia da planilha central.

        Com o programa aberto, faça o seguinte:

        a. Cole o caminho da pasta que contém as relações semanais (copiada no Passo 1);
        b. Serão exibidas as planilhas encontradas nessa pasta, neste campo você deverá confirmar ('s' ou 'n') se as planilhas encontradas estão corretas;
        c. Cole o caminho da planilha que receberá as relações semanais (copiada no Passo 1);
        d. Será exibido todas as guias da planilha, escolha a guia que será atualizada;

[ Resultado esperado ]

    - Backup da planilha (antes de ser atualizada) editada na pasta de backup.
    - Planilha central fornecida receberá as relações semanais. 

[ Erros conhecidos ]

    - O programa não atualizará a planilha se ela estiver aberta.
    - O programa não identifica duplicatas; apenas adiciona linhas à planilha central. Se executado duas vezes, os dados serão duplicados.
    - Qualquer alteração na posição das colunas fará o programa quebrar.
