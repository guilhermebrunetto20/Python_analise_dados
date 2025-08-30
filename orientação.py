class Carro:
    def __init__(self, modelo, cor):
        #Atributos do carro
        self.modelo = modelo
        self.cor = cor
        self.velocidade = 0 # o carro começa parado

    def acelerar(self, incremento):
        self.velocidade += incremento
        print(f'O {self.modelo} acelerou para {self.velocidade} km/h')

    def freiar(self, reduction):
        self.velocidade -= reduction
        print(f'O {self.modelo} desacelerou para {self.velocidade} km/h')

    def stop(self):
        self.velocidade = 0
        print(f'O {self.modelo} parou')

    def reduzir_velocidade(self,reducao):
        while self.velocidade > 0:
            self.velocidade -= reducao
            print(f'O {self.modelo} reduziu pra {self.velocidade} km/h')
        print(f'O {self.modelo} esta parado')

#criar o objeto do carro

meu_carro = Carro('Fusca','Amarelo')
outro_carro = Carro('BMW','Azul')

meu_carro.acelerar(20)
meu_carro.acelerar(30)

outro_carro.acelerar(60)
outro_carro.acelerar(80)
outro_carro.reduzir_velocidade(10)
#outro_carro.stop()
#outro_carro.freiar(120)