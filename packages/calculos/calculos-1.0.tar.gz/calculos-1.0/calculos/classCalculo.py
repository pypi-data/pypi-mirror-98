"""
Pacote contendo uma Classe chamada Calculo com métodos de aplicação.
"""


class Calculos:
    # Iniciando a Classe e instanciando parâmetros:
    def __init__(self, num1, operador, num2):
        self.num1 = num1
        self.operador = operador
        self.num2 = num2

    # Métodos()
    def somar(self):
        return self.num1 + self.num2

    def subtrair(self):
        return self.num1 - self.num2

    def multiplicar(self):
        return self.num1 * self.num2

    def dividir(self):
        return self.num1 / self.num2

    def quociente(self):
        return self.num1 // self.num2

    def resto(self):
        return self.num1 % self.num2

    def potenciacao(self):
        return self.num1 ** self.num2
