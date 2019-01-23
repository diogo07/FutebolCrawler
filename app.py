from coleta.coleta import Coleta
from raspagem.raspagem import Raspagem
from dao.conexao import Conexao
from dao.partida_dao import PartidaDAO
from dao.cotacoes_dao import CotacoesDAO


coleta = Coleta("C:/Users/Diogo/Anaconda3/Scripts/chromedriver.exe", "chrome")

html_resultados = coleta.buscar_html_dinamico_por_data('https://www.resultados.com/', 30, '//div[@class="table-main"]', 0)


html_resultados = coleta.buscar_html_dinamico('https://www.resultados.com/', 30, '//div[@class="table-main"]')

raspagem = Raspagem()

links = raspagem.get_link_partidas(html_resultados)
conexao = Conexao('localhost', 'root', '', 'bets')
partidaDAO = PartidaDAO()
cotacoesDAO = CotacoesDAO()



for l in links:

   if l[0] == 'não iniciada':
      coleta = Coleta("C:/Users/Diogo/Anaconda3/Scripts/chromedriver.exe", "chrome")
      html_jogo = coleta.buscar_html_dinamico(l[1], 30, '//div[@class="odds-comparison-bookmark ifmenu-wrapper"]')
      partida = raspagem.get_dados_partida(html_jogo, l[0], l[2])
      print(partida.__repr__())
      partidaDAO.insert(partida, conexao.banco)
      cotacoesDAO.insert(partida.cotacoes, conexao.banco)

   if l[0] == 'encerrada':
      coleta = Coleta("C:/Users/Diogo/Anaconda3/Scripts/chromedriver.exe", "chrome")
      html_jogo = coleta.buscar_html_dinamico(l[1], 30, '//*[@id="flashscore"]/div[1]/div[2]')
      partida = raspagem.get_resultado(html_jogo, l[0], l[2])
      partidaDAO.insert(partida, conexao.banco)

