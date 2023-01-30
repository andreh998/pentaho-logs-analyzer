
class Log:
    def __init__(self, file_name, log):
        self.file_name = file_name
        self.log = log

    def findError(self):
        """
            Esse método procura dentro do log se existem
            informações de erro.

            Retorno:
            Bolean: se erro retorna True, senão retorna False.
        """
        if "Error" in self.log or "Fail" in self.log:
            return True
        else:
            return False