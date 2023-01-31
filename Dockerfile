# imagem base com ubuntu
FROM ubuntu:latest

# diretório padrão
WORKDIR /app/log_analyzer

# instala o python3, pip3 e cron
RUN apt-get update
RUN apt-get -y install python3 python3-pip
RUN apt-get -y install cron

# copia o arquivo com todas as libs necessárias
COPY requirements.txt requirements.txt

# executa o comando para instalar as libs
RUN pip3 install -r requirements.txt

# copia todos os demais arquivos do diretório atual 
# para dentro da imagem
COPY . .

# o comando abaixo vai dizer para o crontab 
# todos os dias da semana, às 2h da madrugada.
RUN crontab -l | { cat; echo "00 2 * * * python3 /app/log_analyzer/main.py"; } | crontab -

# comando executado quando o container iniciar
# ficará ouvindo os logs de execução do script
CMD cron && tail -f /app/log_analyzer/main.log

# para criar a imagem rodo o comando abaixo no terminal mesmo diretório do Dockerfile
# . indica que o dockerfile está nesse mesmo diretório
# -t Nome da imagem
# docker build . -t <nome_da_imagem>

# para iniciar o container use o comando abaixo:
# docker run -d --name <nome_do_container> <nome_da_imagem> 