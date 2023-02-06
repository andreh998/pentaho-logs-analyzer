# Imagem do python
FROM python:3.9-alpine

# Defino um diretório de trabalho
WORKDIR /app

# Defino o timezone do container, para o mesmo que o host
# Isso garante que o cron rode no horário correto
ENV TZ="America/Sao_Paulo"

# Crio o diretório e o arquivo para os logs do python
RUN mkdir /app/log
RUN touch /app/log/main.log

# Copio tudo para o diretório de trabalho
COPY . .

# Mapeio o diretório onde ficará o log de execução do script
# O arquivo será mapeado na máquina em:
# /var/lib/docker/volumes/<volume_name>/_data/main.log
VOLUME /app/log

# Instalo os pacotes necessários
RUN pip3 install --no-cache-dir -r requirements.txt

# Instalo o cron
# RUN apk add --update --no-cache cron

# Adiciono uma job que executa o script a cada 10 minutos
# -u Força os fluxos stdout e stderr a serem sem buffer.
RUN echo "00 02 * * * python3 -u /app/main.py" >> /etc/crontabs/root

# Inicio o cron
CMD ["crond", "-f", "-l", "8"]