# ···········································································
# :MM'"""""`MM          oo dP dP                                            :
# :M' .mmm. `M             88 88                                            :
# :M  MMMMMMMM dP    dP dP 88 88d888b. .d8888b. 88d888b. 88d8b.d8b. .d8888b.:
# :M  MMM   `M 88    88 88 88 88'  `88 88ooood8 88'  `88 88'`88'`88 88ooood8:
# :M. `MMM' .M 88.  .88 88 88 88    88 88.  ... 88       88  88  88 88.  ...:
# :MM.     .MM `88888P' dP dP dP    dP `88888P' dP       dP  dP  dP `88888P':
# :MMMMMMMMMMM                                                              :
# :                                                                         :
# :M#"""""""'M                                        dP     dP             :
# :##  mmmm. `M                                       88     88             :
# :#'        .M 88d888b. dP    dP 88d888b. .d8888b. d8888P d8888P .d8888b.  :
# :M#  MMMb.'YM 88'  `88 88    88 88'  `88 88ooood8   88     88   88'  `88  :
# :M#  MMMM'  M 88       88.  .88 88    88 88.  ...   88     88   88.  .88  :
# :M#       .;M dP       `88888P' dP    dP `88888P'   dP     dP   `88888P'  :
# :M#########M                                                              :
# ···········································································

#Autor: Guilherme Brunetto
#Data: 20/09/2025
#Version: 1.0.0


from flask import Flask, request, jsonify,render_template_string
import pandas as pd
import sqlite3
import os
import plotly.graph_objects as go
from dash import Dash, dcc, html
import numpy as np
import config  #nosso config.py
from sklearn.cluster import KMeans  
from sklearn.preprocessing import StandardScaler

caminhoBd = config.DB_PATH
pasta = config.FOLDER
app = Flask(__name__)
rotas = config.ROTAS
vazio = 0

def init_db():
    with sqlite3.connect(f'{pasta}{caminhoBd}') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inadimplencia (
                       mes TEXT PRIMARY KEY,
                       inadimplencia REAL)          
    
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS selic (
                       mes TEXT PRIMARY KEY,
                       selic_diaria REAL)          
    
        ''')
        conn.commit()

@app.route(rotas[0])
def index():
    return render_template_string(f'''
    <h1>Upload de dados Economicos</h1>
    <form action = "{rotas[1]}" method = "POST" enctype = "multipart/form-data">
        <label for ="campo_inadimplencia"> Arquivo de Inadimplência:</label>
        <input name ="campo_inadimplencia" type="file" required> </br>
                                  

        <label for ="campo_selic"> Arquivo de Taxa Selic (CSV):</label>
        <input name ="campo_selic" type="file" required> </br>
                                  
        
        <input type="submit" value="Fazer Upload">
    
    </form>
    <br><br>
    <a href="{rotas[2]}"> Consultar dados Armazenados </a><br>
    <a href="{rotas[3]}"> Visualizar Graficos </a><br>
    <a href="{rotas[4]}"> Editar Inadimplencia </a><br>
    <a href="{rotas[5]}"> Analisar Correlação </a><br>
    ''')

@app.route(rotas[1], methods=['POST','GET'])
def upload():
    inad_file = request.files.get('campo_inadimplencia')
    selic_file = request.files.get('campo_selic')

    if not inad_file or not selic_file:
        return jsonify({"Erro": "Ambos arquivos devem ser enviados"}),406
    
    inad_df = pd.read_csv(inad_file, sep=';', names =['data','inadimplencia'], header=0)

       
    selic_df = pd.read_csv(selic_file, sep=';', names =['data','selic_diaria'], header=0)

    inad_df['data'] = pd.to_datetime(inad_df['data'], format='%d/%m/%Y')

    selic_df['data'] = pd.to_datetime(selic_df['data'], format='%d/%m/%Y')

    inad_df['mes'] = inad_df['data'].dt.to_period('M').astype(str).drop_duplicates()

    selic_df['mes'] = selic_df['data'].dt.to_period('M').astype(str)


    #inad_df['mes'] = inad_df[['mes', 'inadimplencia']].drop_duplicates()
    selic_mensal = selic_df.groupby('mes')['selic_diaria'].mean().reset_index()

    with sqlite3.connect(f'{pasta}{caminhoBd}') as conn:
        inad_df.to_sql('inadimplencia', conn, if_exists='replace', index=False)
        selic_df.to_sql('selic', conn, if_exists='replace', index=False)
    
    return jsonify({"Mensagem": "Upload e processamento concluídos com sucesso!"}),200


@app.route(rotas[2], methods=['POST','GET'])
def consultar():

    if request.method == 'POST':
        tabela = request.form.get('Campo_tabela')
        if tabela not in ['inadimplencia', 'selic']:
            return jsonify({"Erro": "Tabela é inválida"}),400
        
        with sqlite3.connect(f'{pasta}{caminhoBd}') as conn:
            df = pd.read_sql_query(f'SELECT * FROM {tabela}', conn)
        
        return df.to_html(index=False)


    return render_template_string(f'''
        <h1> Consulta de Tabelas </h1>
        <form method = "POST">
            <label for = "Campo_tabela"> Escolha a Tabela: </label>
            <select name = "Campo_tabela">
                <option value="inadimplencia"> Inadimplência </option>
                <option value="selic"> Selic </option>
                <option value="usuarios"> Usuarios </option>
            </select>
            <input type="submit" value="Consultar">
        </form>
        <br>
        <a href="{rotas[0]}"> Voltar </a>
    ''')


@app.route(rotas[4], methods=['POST','GET'])
def editar_inadimplencia():
    if request.method =="POST":
        mes = request.form.get('campo_mes')
        novo_valor = request.form.get('campo_valor')
        try:
            novo_valor = float(novo_valor)
        
        except:
            return jsonify({"Erro": "Valor inválido"}),418
        
        with sqlite3.connect(f'{pasta}{caminhoBd}') as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE inadimplencia SET inadimplencia = ? WHERE mes = ?', (novo_valor, mes))
            conn.commit()
            return jsonify({"Mensagem":f"Valor atualizado para o mês {mes}"}),200



    return render_template_string(f'''
        <h1> Editar Inadimplencia </h1>
            <form method = "POST">
                <label for = "campo_mes"> </label>
                <input type="text" name="campo_mes"> </br>
                                  

                <label for = "campo_valor"> Novo valor </label>
                <input type="text" name="campo_valor"> </br>
                
                <input type="submit" value="Salvar"> </br>

            </form>
            <br>
            <a href="{rotas[0]}"> Voltar </a>
        ''')



@app.route(rotas[5])
def correlacao():
    with sqlite3.connect(f'{pasta}{caminhoBd}') as conn:
        inad_df = pd.read_sql_query('SELECT * FROM inadimplencia', conn)
        selic_df = pd.read_sql_query('SELECT * FROM selic', conn)


        # realiza uma junção (merge) entre os dois DataFrames com base na coluna 'mes'
        merged = pd.merge(inad_df, selic_df, on='mes', how='inner')


        #calcula o coeficiente de correlação de Pearson entre as duas variáveis.

        correl = merged['inadimplencia'].corr(merged['selic_diaria'])
       
        # registra as variáveis para a regressão linear inde X é variável independente e Y é a dependente

        X = merged['selic_diaria']
        Y = merged['inadimplencia']

        #calcula os coeficientes da regressão linear onde M é a inclinação e B é a interseção

        m, b = np.polyfit(X,Y,1)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x= X,
            y= Y,
            mode = 'markers', 
            name = 'Inadimplência vs Selic',
            marker = dict(
                size = 12,
                color = 'rgba(0,123,255,0.8)',
                line = dict(
                    width = 2,
                    color = 'white'),
                symbol = 'circle'
               ),
            hovertemplate = 'Selic: %{x:.2f}% <br>Inadimplência: %{y:.2f}%<extra></extra>' 


        ))

        fig.add_trace(go.Scatter(
            x = x,
            y = m * x + b,
            mode = 'lines',
            line = dict(
                color = 'rgba(255,53,69,1)',
                width = 4,
                dash = 'dot'
            )
        ))

    fig.update_layout(
        title = {
            'text': f'<b>Correlação entre Inadimplência e Selic</b></br><span style="font-size:16px;"> Coeficiente de Correlação: {correl:.2f}</span>',
            'y':0.95,
            'x': 0.5,
            'xanchor':'center',
            'yanchor':'top'
        },
        xaxis_title = dict(
            text = 'SELIC Média mensal (%)',
            font = dict(
                family = 'Arial',
                size = 18,
                color = 'gray'
            )),
        yaxis_title = dict(
            text = 'Inadimplência (%)',
            font = dict(
                family = 'Arial',
                size = 18,
                color = 'gray'
            )
            ),
        xaxis = dict(tickfont = dict(size=14,family='Arial',color='black'), gridcolor = 'lightgray'),
                
        yaxis = dict(tickfont = dict(size=14,family='Arial', color='black'), gridcolor = 'lightgray'),
        
        font = dict(tickfont = dict(size=14,family='Arial', color='black'), gridcolor = 'lightgray'),
        
        legend = dict(
            orientation = 'h',
            yanchor = 'bottom',
            y = 1.05,
            xanchor = 'center',
            x = 0.5,
            bgcolor = 'rgba(0,0,0,0)',
            borderwidth = 0
        ),
    
        margin = dict(l = 60, r = 60, t = 120 , b = 60),
        plot_bgcolor = 'white',
        paper_bgcolor = 'white',
    
    )

    graph_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
    return render_template_string(f'''
        <html>
            <head>
                <title>Correlação Inadimplência e Selic</title>
            </head>
            <body>
                <h1> Correlação entre Inadimplência e Selic </h1>
                <div>{{ graph|safe }}</div>
                <br>
                <a href="{rotas[0]}"> Voltar </a>   
            </body>
        </html>
        
    ''', grafico = graph_html, voltar = rotas[0])

     
if __name__ == '__main__':
     
    init_db()
    app.run(debug=config.FLASK_DEBUG, host=config.FLASK_HOST, port=config.FLASK_PORT)
