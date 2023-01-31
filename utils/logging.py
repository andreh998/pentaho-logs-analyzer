import logging
import os

def write_log(message):
    """
        Função responsável por gravar o log de execução
        desse script

        Parâmetros:
        type (str): recebe uma string 'info', 'warning', 'error' ou 'debug'
        message (str): a mensagem que deverá ser salva no log
    """
    filename = os.getcwd()
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S', filename=f'{filename}/main.log', level=logging.INFO)
    logging.info(message)
    