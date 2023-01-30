from datetime import datetime, timedelta
import re

DAYS_TO_SUBTRACT = 1

def getFilesModifiedYesterday(files):
    """
        Função que encontra em uma lista de arquivos
        quais tiveram alterações no dia anterior.

        Parametros: 
        files (list): lista de arquivos para verificação

        Retorno:
        list: lista com os arquivos
    """
    yesterday = datetime.now() - timedelta(days=DAYS_TO_SUBTRACT)
    date = yesterday.strftime("%Y-%m-%d")
    
    modified = []

    for file in files:
        if date in file:
            modified.append(file)
    
    return modified

def getFileNameOnly(files):
    """
        Essa função fará uma limpeza nos nomes dos arquivos, 
        Pegando apenas o nome no formato 'nome_arquivo.txt'

        Parametros:
        files (list): lista com os nomes dos arquivos

        Retorno:
        lista com os nomes corretos dos arquivos
    """
    file_names = []

    for item in files:
        try:
            print(item)
            name = re.search("\D*[.]txt$", item)
            file_names.append(name[0].strip())
        except Exception:
            print(f"Erro no item: {item}")
            pass

    return file_names

def getFilteredLogs(file_name, log_lines):
    """
        Assim como pego apenas os aquivos de log que foram alterados ontem,
        preciso limpar o arquivo de log para filtrar apenas os logs
        que foram gerados na data de ontem.

        Parâmetro:
        file_name (str): nome do arquivo
        log_lines (list): lista com os logs

        Retorno:
        string com os logs filtrados
    """
    yesterday = datetime.now() - timedelta(days=DAYS_TO_SUBTRACT)
    print(yesterday)
    date = yesterday.strftime("%Y/%m/%d")

    yesterday_logs = ''

    for line in log_lines:
        if date in line:
            yesterday_logs += line + '\n'

    return yesterday_logs

def getTaskName(file_name):
    """
        Retorna o nome da tarefa com base no nome do arquivo.

        Parametros:
        file_name (str): nome do arquivo de log

        Retorno:
        str: remove o .txt e retorna.
    """
    return file_name[0:file_name.find(".")]
