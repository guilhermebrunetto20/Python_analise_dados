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

# Configurações comuns do sistema:

FOLDER = "C:/Users/sabado/Desktop/Python - AD Guilherme/Analise_dados/AIS/"
DB_PATH = "bancoDeDadosAIS.db"
FLASK_DEBUG = True
FLASK_PORT = 5000
FLASK_HOST = "127.0.0.1"


# Rotas comuns do sistema

ROTAS =[
    '/',                            # rota 00
    '/upload',                      # rota 01
    '/consultar',                   # rota 02   
    '/graficos',                    # rota 03
    '/editar_inadimplencia',         # rota 04
    '/correlacao'                  # rota 05
    
]



