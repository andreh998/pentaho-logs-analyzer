# Analizador de logs do pentaho

- No diretório do projeto:
    ```python
	docker build . -t logs_analyzer --no-cache
	docker run -d --name logs_analyzer logs_analyzer 
	```
