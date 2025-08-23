import meu_modulo as mm

print(mm.soma(2,6))
print(mm.saudacao(' Guilherme', 32))

valor_a = int(input('Insira o primeiro valor: '))
valor_b = int(input('Insira o segundo valor: '))

print(mm.soma(valor_a,valor_b))


from datetime import datetime

ano_atual = datetime.now().year
ano_nascimento = int(input('\nDigite o ano do seu nascimento: '))

idade = mm.calcular_idade(ano_atual,ano_nascimento)
print(f'Você tem {idade} Anos')
