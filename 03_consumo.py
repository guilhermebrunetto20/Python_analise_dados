from flask import Flask, request, render_template_string

import pandas as pd

import sqlite3

import plotly.express as px 

import plotly.io as pio

import random as rd 

import os

pio.renderers.default = "browser"

# carregar o arquivo drinks

caminho = "C:/Users/sabado/Desktop/Python - AD Guilherme/Analise_dados/"
tabela01 = ["drinks.csv","avengers.csv"]

codHtml = '''
        <h1> Dashboards - Consumo de Alcool </h1>
        <h2> Parte 01 </h2>
            <ul>
                <li><a href="/grafico1"> Top 10 países em consumo de alcool </a></li>
                <li><a href="/grafico2"> Media de consumo por Tipo </a></li>
                <li><a href="/grafico3"> Consumo total por Região </a></li>
                <li><a href="/grafico4"> Comparativo entre tipos de bebidas </a></li>
                <li><a href="pais"> Insights por pais </a></li>
            </ul>
        <h2> Parte 02 </h2>
            <ul>
                <li><a href="/comparar"> Comparar </a></li>
                <li><a href="/upload"> Upload CSV  Vingadores </a></li>
                <li><a href="/apagar"> Apagar Tabela </a></li>
                <li><a href="/ver"> Ver Tabela </a></li>
                <li><a href="/vaa"> V.A.A (Vingadores Alcolicos Anonimos) </a></li>
            </ul>    

'''

#dfDrinks = pd.read_csv(r"C:\Users\sabado\Desktop\Python - AD Guilherme\Analise_dados\drinks.csv")

def carregarCsv():


    # #Carregar o arquivo drinks
    # caminho = "C:/Users/sabado/Desktop/Python - AD Guilherme/Analise_dados/"
    # tabela01 = ["drinks.csv","avengers.csv"]


    # dfDrinks = pd.read_csv(os.path.join(caminho,tabela01[0]))
    # dfAvengers = pd.read_csv(os.path.join(caminho,tabela01[1]),encoding='latin1')

    try:
        dfDrinks = pd.read_csv(os.path.join(caminho,tabela01[0]))
        dfAvengers = pd.read_csv(os.path.join(caminho,tabela01[1]),encoding='latin1')
        return dfDrinks, dfAvengers

    except Exception as error:
        print(f"Erro ao carregar arquivos CSV: {error}")
        return None, None
    
def criarBancoDados():
    conn = sqlite3.connect(f"{caminho}banco01.bd")

    dfDrinks, dfAvengers = carregarCsv()
    if dfDrinks is None or dfAvengers is None:
        print("Falha ao carregar os dados!")
        return

    #inserir as tabelas no banco de dados

    dfDrinks.to_sql("bebidas", conn, if_exists="replace", index=False)
    dfAvengers.to_sql("vingadores", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(codHtml)


@app.route('/grafico1')

def grafico1():
    with sqlite3.connect(f'{caminho}banco01.bd') as conn:
        df = pd.read_sql_query("""
             SELECT  country, total_litres_of_pure_alcohol FROM bebidas ORDER BY total_litres_of_pure_alcohol LIMIT 10               
        """, conn)

    figuraGrafico01 = px.bar(
        df,
        x = "country",
        y = "total_litres_of_pure_alcohol",
        title = " Top 10 paises com consumo de alcool"

    )
    return figuraGrafico01.to_html()

@app.route('/grafico2')
def grafico2():
    with sqlite3.connect(f'{caminho}banco01.bd') as conn:
        df = pd.read_sql_query(""" 
            SELECT AVG(beer_servings) AS cerveja,AVG(spirit_servings) AS destilados, AVG(wine_servings) AS vinhos FROM bebidas         

         """, conn)
        
    df_melted = df.melt(var_name ='Bebidas',value_name='Média de porções')
    figuraGrafico02 = px.bar(
        df_melted,
        x = "Bebidas",
        y = "Média de porções",
        title = "Media de consumo global por tipo"
    )
    return figuraGrafico02.to_html()

@app.route("/grafico3")
def grafico3():
    regioes = {
        "Europa":['France','Germany','Spain','Italy','Portugal'],
        "Asia": ['China','Japan','India','Thailand'],
        "Africa": ['Angola','Nigeria','Egypt','Algeria'],
        "Americas": ['USA', 'Canada','Brazil','Argentina','Mexico']

    }
    dados = []
    with sqlite3.connect(f'{caminho}banco01.bd') as conn:
        # Itera sobre o dicionario, de regioes onde cada chave(regiao tem uma lista de paises)
        for regiao, paises in regioes.items():
            placeholders = ",".join([f" '{pais} '" for pais in paises])
            query = f"""
                SELECT SUM(total_litres_of_pure_alcohol) AS total
                FROM bebidas
                WHERE country IN ({placeholders})
             
            """
            total = pd.read_sql_query(query, conn).iloc[0,0]
            dados.append({
                "Região": regiao,
                "Consumo Total": total
            })
    dfRegioes = pd.DataFrame(dados)
    figuraGrafico3 = px.pie(
        dfRegioes,
        names = "Região",
        values = "Consumo Total",
        title = "Consumo Total por Região!"
    )

    return figuraGrafico3.to_html()


 


if __name__ == '__main__':
    criarBancoDados()
    app.run(debug=True)
