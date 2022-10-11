


class bicicleta:
    def __init__(self, cor, modelo, ano, valor) -> None:
        self.cor = cor 
        self.modelo = modelo
        self.ano = ano
        self.valor = valor 
    def buzinar (self): #metodo para identificar, similar as funcoes/ e preciso declara um metodo sempre 
        print("plim plim")
    def parar(self):
        print("bicileta parada")
    def correr(self):
        print("vrum")
    def get_cor(self):
        return self.cor
    def __str__(self):
        return f"{self.__class__.__name__}: {','.join([f'{chave} = {valor}' for chave, valor in self.__dict__.items()])}"
b1 = bicicleta("vermelho", "caloi", 2022, 600)
b1.buzinar()
b1.correr()
b1.parar()

b2= bicicleta( "verde", "monark", 2000, 360)
b2.buzinar() # sáo iguais bicicleta.buzinar(b2)  # a classe pode ser usada em mais de um objeto
print(b2.get_cor())
print(b2)