import pandas as pd

#carregar dados da planilha

caminho = r'C:\Users\sabado\Desktop\Python - AD Guilherme\Analise_dados\01_base_vendas.xlsx'


df1 =pd.read_excel(caminho, sheet_name='Relatório de Vendas')

df2 = pd.read_excel(caminho, sheet_name='Relatório de Vendas1')

#exibir as primeiras linhas das tabelas

print('------Primeiro Relatório--------')
print(df1.head())


print('------Segundo Relatório--------')
print(df2.head())



#verificar se há duplicatas nas tabelas

print('Duplicatas no relatório 01')
print(df1.duplicated().sum())

print('Duplicatas no relatório 02')
print(df2.duplicated().sum())

#Consolidação das duas tabelas

print('Dados consolidados')

dfConsolidado = pd.concat([df1,df2],ignore_index=True)

print(dfConsolidado.head())


#Exibir o numero de clientes por cidade

ClientesPorCidade = dfConsolidado.groupby('Cidade')['Cliente'].nunique().sort_values(ascending=False) #Nesse caso, vou agrupar a cidade primeiro e depois trazer a quantidade de clientes e classificando do menor para o maior

print(ClientesPorCidade)

# Numero de vendas por planta

vendasPorPlano = dfConsolidado['Plano Vendido'].value_counts()
print(vendasPorPlano)

#exibir as 3 cidades com mais clientes:

top3Cidades = ClientesPorCidade.head(3)
print('Top 3 Cidades')
print(top3Cidades)

# Adicionar uma nova coluna de status (Exemplo ficticio analise)
# vamos Classificar os planos como premium se for entreprise, os demais serão padrão.


dfConsolidado['Status'] = dfConsolidado['Plano Vendido'].apply(lambda x: 'Premium' if x == 'Entreprise' else 'Padrão')

#Função Lambda gera o X e nos possibilita fazer o if

#Exibir a distribuição dos status

statusDist = dfConsolidado['Status'].value_counts()

print('Distribuição dos status: ')
print(statusDist)

#salvar a tabela em excel

dfConsolidado.to_excel('Dados_consolidados.xlsx',index=False)
print('Dados salvos na planilha do excel')

#salvar a tabela em csv

dfConsolidado.to_csv('Dados_consolidados.csv', index=False)
print('Dados salvos em CSV')

#Mensagem final

Print('---Programa Finalizado"----')