import paramiko
from utils.logging import write_log

class SSH:
    def __init__(self, hostname, username, password):
        """ 
            Representa uma conexão ssh
            atributos:
                hostname (str): nome ou ip do computador ou servidor
                username (str): usuário de acesso
                password (str): senha de acesso
        """
        self.hostname = hostname
        self.username = username
        self.password = password

    def connect(self):
        """
            Abre a conexão com o host

            Retorno:
            obj: objeto cliente
        """
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname = self.hostname,
            username = self.username,
            password = self.password
        )
        return client

    def close(self, ssh_client):
        """
            Encerra a conexão com o host remoto

            Parâmetros:
            ssh_client (obj): objeto cliente de conexão
        """
        ssh_client.close()

    def getFiles(self, path, ssh_client):
        """
            Esse método retorna os arquivos encontrados no
            diretório informado.
            
            Parametros: 
            path (str): caminho da pasta com os arquivos
            ssh_client (obj): objeto para conexão

            Retorno:
            list: uma lista com o nome de todos os arquivos
        """

        # Utilizo o comando "ls -la --full-time", pois além do nome do arquivo 
        # também é necessário a informação da data de modificação. Isso acaba
        # retornando muita sujeira além do necessário, o que deverá ser limpo depois.
        stdin, stdout, stderr = ssh_client.exec_command(f"cd {path}; ls -la --full-time")
        files = (stdout.read().decode()).split("\n")
        # registra no arquivo de log os arquivos encontrados
        write_log("Arquivos encontrados:")
        write_log(files)
        return files
               
    def getLogFromFile(self, path, file, ssh_client):
        """
            Método que captura o texto de dentro do arquivo
            e retorna uma lista com cada linha do texto.
            
            Parametros:
            path (str): caminho para chegar ao arquivo
            file (str): nome do arquivo
            ssh_client (obj): objeto para conexão

            Retorno:
            list: uma lista com cada linha de log presente no arquivo
        """
        # Capturo as últimas 100 linhas do arquivo de logs
        # As tarefas geram no máximo 50 ou 60 linhas de log
        stdin, stdout, stderr = ssh_client.exec_command(f"tail -100 {path}{file}")
        # Lê o retorno do comando e quebra as linhas
        # cada item da lista é uma linha do log
        log = (stdout.read().decode()).split("\n")
        return log
        
