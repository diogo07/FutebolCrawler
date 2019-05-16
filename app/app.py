from coleta.coleta import Coleta
from coleta.raspagem import Raspagem
from model.dao.conexao import Conexao
from model.dao.partida_dao import PartidaDAO
from model.dao.cotacoes_dao import CotacoesDAO

#baixar o drive do navegador no link abaixo
#https://sites.google.com/a/chromium.org/chromedriver/downloads
#colocar na pasta /Scripts/ onde está instalado o Python
#Trocar o nome Diogo pelo nome de usuario do seu PC no caminho abaixo
webdriver = "C:/Python/virtualenv/virtual_futebol_crawler/Scripts/chromedriver.exe"

coleta = Coleta(webdriver, "chrome")


#Nesse método é retornado o html dos jogos da data atual somada com a quantidade de dias fornecida no ultimo parâmetro da função
html_resultados = coleta.buscar_html_dinamico_por_data('https://www.resultados.com/', 30, '//*[@id="live-table"]/div[3]', 0)

#Nesse método é retornado o html dos jogos da data atual
#html_resultados = coleta.buscar_html_dinamico('https://www.resultados.com/', 30, '//div[@class="table-main"]')

raspagem = Raspagem()

links = raspagem.get_link_partidas(html_resultados)
#conexao = Conexao('localhost', 'root', '', 'futebol')
partidaDAO = PartidaDAO()
cotacoesDAO = CotacoesDAO()



for l in links:

   if l[0] == 'encerrada':
      # Trocar o nome Diogo pelo nome de usuario do seu PC no caminho abaixo
      coleta = Coleta(webdriver, "chrome")
      html_jogo = coleta.buscar_html_dinamico(l[1], 30, '//div[@class="odds-comparison-bookmark ifmenu-wrapper"]')
      partida = raspagem.get_dados_partida(html_jogo, l[0], l[2])
      print(partida.__repr__())
      #partidaDAO.insert(partida, conexao.banco)
      #cotacoesDAO.insert(partida.cotacoes, conexao.banco)
   '''
   if l[0] == 'encerrada':
      # Trocar o nome Diogo pelo nome de usuario do seu PC no caminho abaixo
      coleta = Coleta(webdriver, "chrome")
      html_jogo = coleta.buscar_html_dinamico(l[1], 30, '//*[@id="flashscore"]/div[1]/div[2]')
      partida = raspagem.get_resultado(html_jogo, l[0], l[2])
      #partidaDAO.insert(partida, conexao.banco)
      print(partida.__repr__())
   '''