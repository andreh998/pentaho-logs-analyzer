import smtplib, ssl
from email.message import EmailMessage

class Email:
    def __init__(self, port, smtp_server, email_login, password):
        """
            Representa uma conexão smtp
            atributos:
                port (str): porta de conexão
                smtp_server (str): servidor smtp
                email_login (str): endereço de e-mail para login no servidor
                password (str): senha do endereço usado para login
        """
        self.port = port
        self.smtp_server = smtp_server
        self.email_login = email_login
        self.password = password

    def sendEmail(self, to_email, from_email, subject, message):
        """
            Método responsável por enviar o e-mail com as informações
            encontradas no arquivo de log.

            Parametros:
            to_email (str): Endereço de email do destinatário
            from_email (str): Endereço de email do remetente
            subject (str): Título do email
            message (str): Conteudo do email
        """
        msg = EmailMessage()
        msg['To'] = [to_email]
        msg['From'] = from_email
        msg['Subject'] = subject

        msg.add_alternative(message, subtype='html')

        context = ssl.create_default_context()

        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls(context = context)
            server.login(self.email_login, self.password)
            server.send_message(msg)
        