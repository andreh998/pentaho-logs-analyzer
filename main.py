from utils.ssh import SSH
from logs.log import Log
from utils.email import Email
from utils.managing_text import getFilesModifiedYesterday, getFileNameOnly, getFilteredLogs, getTaskName
import os
from dotenv import load_dotenv
from utils.logging import write_log

load_dotenv()

def prepareEmail(file_name, log):

    SMTP_PORT = os.getenv("SMTP_PORT")
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    EMAIL_LOGIN = os.getenv("EMAIL_LOGIN")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    TO_EMAIL = os.getenv("TO_EMAIL")

    # Retorna o nome da tarefa
    task_name = getTaskName(file_name)

    # Crio o objeto com as configurações de email
    email = Email(SMTP_PORT, SMTP_SERVER, EMAIL_LOGIN, EMAIL_PASSWORD)
    # Assunto 
    subject = f'Pentaho - Tarefa {task_name} com erros'
    # Mensagem
    message = f"""\
        <!DOCTYPE html>
        <html>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inconsolata&display=swap');
            </style>
            <body>
                <div>
                    <div style="font-size:14px">
                        <p>Olá!</p>
                        <p>Ocorreram alguns erros na execução da tarefa {task_name}.</p>
                        <p>Segue log completo:</p>
                    </div>
                </div>
                <div style="width:100%;white-space:break-spaces;background-color:#eee;padding: 0 10px 0 10px;">
                    <div style="font-family:'Inconsolata',monospace;font-size:13px">
                        {log}
                    </div>
                </div>
            </body>
        </html>
    """
    # Registra no log que está enviando email
    write_log(f"Enviando email devido a erros na tarefa {task_name}")

    # Chama o método responsável por enviar o email
    email.sendEmail(TO_EMAIL, EMAIL_LOGIN, subject, message)

def capturaLogs():

    SERVER = os.getenv("SERVER")
    SERVER_LOGIN = os.getenv("SERVER_LOGIN")
    SERVER_PASSWORD = os.getenv("SERVER_PASSWORD")
    LOGS_PATH = os.getenv("LOGS_PATH")

    # Crio um objeto ssh
    ssh = SSH(SERVER, SERVER_LOGIN, SERVER_PASSWORD)
    # abro a conexão com o host
    ssh_client = ssh.connect()
    # Pego todos os arquivos de log que estão no caminho informado
    # e as demais informações que o comando "ls -la" do linux retorna
    files = ssh.getFiles(LOGS_PATH, ssh_client)

    # As tarefas do Pentaho rodam entre as 18h e 23H
    # Esse script roda após as 00h
    # Então, filtro apenas pelos arquivos modificados no dia anterior
    filesModified = getFilesModifiedYesterday(files);

    # Limpo os dados que o comando ls -la traz para pegar
    # apenas o nome do arquivo
    file_names = getFileNameOnly(filesModified)
    
    # verifico se existem arquivos
    if len(file_names) != 0:
        # crio um dicionário onde ficarão os logs de cada arquivo
        dict_logs = {}
        
        # Percorro a lista com o nome dos arquivos
        for file_name in file_names:
            # Para cada nome de arquivo, chamo a função responsável por capturar
            # as últimas 100 linhas de log presentes nesse arquivo.
            log_lines = ssh.getLogFromFile(LOGS_PATH, file_name, ssh_client)

            # Filtro os logs para pegar apenas a data de ontem
            logs = getFilteredLogs(file_name, log_lines)
            
            # adiciono os logs no dicionário no formato:
            # {"nome_arquivo": "logs"}
            dict_logs[file_name] = logs        

        # Percorro o dicionário com os logs
        for key, value in dict_logs.items():
            # Crio um objeto log
            log = Log(file_name = key, log = value)
            # Chamo o método que verifica se existe erro
            error = log.findError()
            # Se existe erro prepara o envio de um email
            if error == True:
                # registra no log que encontrou erro
                write_log(f"Erros encontrados no arquivo {key}")
                # chama a função para enviar e-mail
                prepareEmail(file_name=key, log=value)
            
    # fecho a conexão com o host remoto
    ssh.close(ssh_client)

def main():
    # Salva um log de execução
    write_log("Iniciando execução")
    # Inicio a captura dos logs no servidor
    capturaLogs()

    write_log("Fim da execução")

if __name__ == "__main__":
    main()

