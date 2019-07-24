from bs4 import BeautifulSoup
from model.vo.partida import Partida

class Raspagem:

    def get_link_partidas(self, html):
        link_partidas = []
        soup = BeautifulSoup(html, "html.parser")
        partidas_encerradas = soup.findAll('div', class_='event__match')
        partidas_em_andamento = soup.findAll('div', class_='event__match--live')
        partidas_nao_iniciadas = soup.findAll('div', class_='event__match--scheduled')

        print(partidas_encerradas.__len__())
        print(partidas_nao_iniciadas.__len__())
        print(partidas_em_andamento.__len__())


        for p_n_ini in partidas_nao_iniciadas:
            id_partida_nao_iniciada = str(p_n_ini.get('id')).replace('g_1_', '')
            dados = []
            dados.append('não iniciada')
            dados.append('https://www.resultados.com/jogo/' + id_partida_nao_iniciada + '/#comparacao-de-odds;1x2-odds;tempo-regulamentar')
            dados.append(id_partida_nao_iniciada)
            link_partidas.append(dados)

        for p_enc in partidas_encerradas:
            id_partida_encerrada = str(p_enc.get('id')).replace('g_1_', '')
            dados = []
            dados.append('encerrada')
            dados.append(
               'https://www.resultados.com/jogo/' + id_partida_encerrada + '/#comparacao-de-odds;1x2-odds;tempo-regulamentar')
            dados.append(id_partida_encerrada)
            link_partidas.append(dados)

        for p_and in partidas_em_andamento:
            id_partida_em_andamento = str(p_and.get('id')).replace('g_1_', '')
            dados = []
            dados.append('em andamento')
            dados.append(
               'https://www.resultados.com/jogo/' + id_partida_em_andamento + '/#comparacao-de-odds;1x2-odds;tempo-regulamentar')
            dados.append(id_partida_em_andamento)
            link_partidas.append(dados)



        return link_partidas

    def get_dados_partida(self, html, status, id):


        soup = BeautifulSoup(html, "html.parser")

        times = soup.findAll('a', class_="participant-imglink")
        time_casa = times[1].get_text()
        time_fora = times[3].get_text()

        info_horario = soup.findAll('div', class_='mstat-date')
        data = str(info_horario[0].get_text()).split(' ')[0].replace('.', '/')
        hora = str(info_horario[0].get_text()).split(' ')[1]

        info_campeonato = soup.find('div', class_='fleft')
        camp = info_campeonato.findAll('span')
        campeonato = camp[1].get_text()

        dados_vencedor_full_time = soup.find('div', id='block-1x2-ft')
        html_odds_vencedor_full_time = dados_vencedor_full_time.findAll('td', class_="kx")

        dados_vencedor_full_time = [odd.get_text() for odd in html_odds_vencedor_full_time]



        partida = Partida(id, campeonato, data, hora, time_casa, time_fora, status, 0 ,0)

        partida.cotacoes.odds_ganhador_casa_full_time = dados_vencedor_full_time[0]
        partida.cotacoes.odds_empate_full_time = dados_vencedor_full_time[1]
        partida.cotacoes.odds_ganhador_visitante_full_time = dados_vencedor_full_time[2]

        dados_vencedor_1_tempo = soup.find('div', id='block-1x2-1hf')

        if dados_vencedor_1_tempo != None:
            html_odds_vencedor_1_tempo = dados_vencedor_1_tempo.findAll('td', class_="kx")
            dados_vencedor_1_tempo = [odd.get_text() for odd in html_odds_vencedor_1_tempo]
            partida.cotacoes.odds_ganhador_casa_1_tempo = dados_vencedor_1_tempo[0]
            partida.cotacoes.odds_empate_1_tempo = dados_vencedor_1_tempo[1]
            partida.cotacoes.odds_ganhador_visitante_1_tempo = dados_vencedor_1_tempo[2]

        dados_vencedor_2_tempo = soup.find('div', id='block-1x2-2hf')
        if dados_vencedor_2_tempo != None:
            html_odds_vencedor_2_tempo = dados_vencedor_2_tempo.findAll('td', class_="kx")
            dados_vencedor_2_tempo = [odd.get_text() for odd in html_odds_vencedor_2_tempo]
            partida.cotacoes.odds_ganhador_casa_2_tempo = dados_vencedor_2_tempo[0]
            partida.cotacoes.odds_empate_2_tempo = dados_vencedor_2_tempo[1]
            partida.cotacoes.odds_ganhador_visitante_2_tempo = dados_vencedor_2_tempo[2]

        dados_soma_placar_casa_fora_full_time = soup.find('div', id='block-moneyline-ft')
        if dados_soma_placar_casa_fora_full_time != None:
            html_odds_soma_placar_casa_fora_full_time = dados_soma_placar_casa_fora_full_time.findAll('td', class_="kx")
            dados_soma_placar_casa_fora_full_time = [odd.get_text() for odd in
                                                     html_odds_soma_placar_casa_fora_full_time]
            partida.cotacoes.odds_soma_placar_casa_fora_full_time_par = dados_soma_placar_casa_fora_full_time[0]
            partida.cotacoes.odds_soma_placar_casa_fora_full_time_impar = dados_soma_placar_casa_fora_full_time[1]

        dados_quantidade_gols_full_time = soup.find('div', id='block-under-over-ft')
        if dados_quantidade_gols_full_time != None:

            qtd_gols_0_5_full_time = dados_quantidade_gols_full_time.find('table', id='odds_ou_0.5')
            if qtd_gols_0_5_full_time != None:
                html_odds_gols_0_5_full_time = qtd_gols_0_5_full_time.findAll('td', class_="kx")
                qtd_gols_0_5_full_time = [odd.get_text() for odd in html_odds_gols_0_5_full_time]

                partida.cotacoes.odds_mais_de_1_gol_full_time = qtd_gols_0_5_full_time[0]
                partida.cotacoes.odds_menos_de_1_gol_full_time = qtd_gols_0_5_full_time[1]

            qtd_gols_1_5_full_time = dados_quantidade_gols_full_time.find('table', id='odds_ou_1.5')
            if qtd_gols_1_5_full_time != None:
                html_odds_gols_1_5_full_time = qtd_gols_1_5_full_time.findAll('td', class_="kx")
                qtd_gols_1_5_full_time = [odd.get_text() for odd in html_odds_gols_1_5_full_time]

                partida.cotacoes.odds_mais_de_2_gols_full_time = qtd_gols_1_5_full_time[0]
                partida.cotacoes.odds_menos_de_2_gols_full_time = qtd_gols_1_5_full_time[1]

            qtd_gols_2_5_full_time = dados_quantidade_gols_full_time.find('table', id='odds_ou_2.5')
            if qtd_gols_2_5_full_time != None:
                html_odds_gols_2_5_full_time = qtd_gols_2_5_full_time.findAll('td', class_="kx")
                qtd_gols_2_5_full_time = [odd.get_text() for odd in html_odds_gols_2_5_full_time]

                partida.cotacoes.odds_mais_de_3_gols_full_time = qtd_gols_2_5_full_time[0]
                partida.cotacoes.odds_menos_de_3_gols_full_time = qtd_gols_2_5_full_time[1]

            qtd_gols_3_5_full_time = dados_quantidade_gols_full_time.find('table', id='odds_ou_3.5')
            if qtd_gols_3_5_full_time != None:
                html_odds_gols_3_5_full_time = qtd_gols_3_5_full_time.findAll('td', class_="kx")
                qtd_gols_3_5_full_time = [odd.get_text() for odd in html_odds_gols_3_5_full_time]

                partida.cotacoes.odds_mais_de_4_gols_full_time = qtd_gols_3_5_full_time[0]
                partida.cotacoes.odds_menos_de_4_gols_full_time = qtd_gols_3_5_full_time[1]

            qtd_gols_4_5_full_time = dados_quantidade_gols_full_time.find('table', id='odds_ou_4.5')
            if qtd_gols_4_5_full_time != None:
                html_odds_gols_4_5_full_time = qtd_gols_4_5_full_time.findAll('td', class_="kx")
                qtd_gols_4_5_full_time = [odd.get_text() for odd in html_odds_gols_4_5_full_time]

                partida.cotacoes.odds_mais_de_5_gols_full_time = qtd_gols_4_5_full_time[0]
                partida.cotacoes.odds_menos_de_5_gols_full_time = qtd_gols_4_5_full_time[1]

            qtd_gols_5_5_full_time = dados_quantidade_gols_full_time.find('table', id='odds_ou_5.5')
            if qtd_gols_5_5_full_time != None:
                html_odds_gols_5_5_full_time = qtd_gols_5_5_full_time.findAll('td', class_="kx")
                qtd_gols_5_5_full_time = [odd.get_text() for odd in html_odds_gols_5_5_full_time]

                partida.cotacoes.odds_mais_de_6_gols_full_time = qtd_gols_5_5_full_time[0]
                partida.cotacoes.odds_menos_de_6_gols_full_time = qtd_gols_5_5_full_time[1]

        dados_quantidade_gols_1_tempo = soup.find('div', id='block-under-over-1hf')

        if dados_quantidade_gols_1_tempo != None:

            qtd_gols_0_5_1_tempo = dados_quantidade_gols_1_tempo.find('table', id='odds_ou_0.5')
            if qtd_gols_0_5_1_tempo != None:
                html_odds_gols_0_5_1_tempo = qtd_gols_0_5_1_tempo.findAll('td', class_="kx")
                qtd_gols_0_5_1_tempo = [odd.get_text() for odd in html_odds_gols_0_5_1_tempo]

                partida.cotacoes.odds_mais_de_1_gol_1_tempo = qtd_gols_0_5_1_tempo[0]
                partida.cotacoes.odds_menos_de_1_gol_1_tempo = qtd_gols_0_5_1_tempo[1]

            qtd_gols_1_5_1_tempo = dados_quantidade_gols_1_tempo.find('table', id='odds_ou_1.5')
            if qtd_gols_1_5_1_tempo != None:
                html_odds_gols_1_5_1_tempo = qtd_gols_1_5_1_tempo.findAll('td', class_="kx")
                qtd_gols_1_5_1_tempo = [odd.get_text() for odd in html_odds_gols_1_5_1_tempo]

                partida.cotacoes.odds_mais_de_2_gols_1_tempo = qtd_gols_1_5_1_tempo[0]
                partida.cotacoes.odds_menos_de_2_gols_1_tempo = qtd_gols_1_5_1_tempo[1]

            qtd_gols_2_5_1_tempo = dados_quantidade_gols_1_tempo.find('table', id='odds_ou_2.5')
            if qtd_gols_2_5_1_tempo != None:
                html_odds_gols_2_5_1_tempo = qtd_gols_2_5_1_tempo.findAll('td', class_="kx")
                qtd_gols_2_5_1_tempo = [odd.get_text() for odd in html_odds_gols_2_5_1_tempo]

                partida.cotacoes.odds_mais_de_3_gols_1_tempo = qtd_gols_2_5_1_tempo[0]
                partida.cotacoes.odds_menos_de_3_gols_1_tempo = qtd_gols_2_5_1_tempo[1]

            qtd_gols_3_5_1_tempo = dados_quantidade_gols_1_tempo.find('table', id='odds_ou_3.5')
            if qtd_gols_3_5_1_tempo != None:
                html_odds_gols_3_5_1_tempo = qtd_gols_3_5_1_tempo.findAll('td', class_="kx")
                qtd_gols_3_5_1_tempo = [odd.get_text() for odd in html_odds_gols_3_5_1_tempo]

                partida.cotacoes.odds_mais_de_4_gols_1_tempo = qtd_gols_3_5_1_tempo[0]
                partida.cotacoes.odds_menos_de_4_gols_1_tempo = qtd_gols_3_5_1_tempo[1]

        dados_quantidade_gols_2_tempo = soup.find('div', id='block-under-over-2hf')

        if dados_quantidade_gols_2_tempo != None:

            qtd_gols_0_5_2_tempo = dados_quantidade_gols_2_tempo.find('table', id='odds_ou_0.5')
            if qtd_gols_0_5_2_tempo != None:
                html_odds_gols_0_5_2_tempo = qtd_gols_0_5_2_tempo.findAll('td', class_="kx")
                qtd_gols_0_5_2_tempo = [odd.get_text() for odd in html_odds_gols_0_5_2_tempo]

                partida.cotacoes.odds_mais_de_1_gol_2_tempo = qtd_gols_0_5_2_tempo[0]
                partida.cotacoes.odds_menos_de_1_gol_2_tempo = qtd_gols_0_5_2_tempo[1]

            qtd_gols_1_5_2_tempo = dados_quantidade_gols_2_tempo.find('table', id='odds_ou_1.5')
            if qtd_gols_1_5_2_tempo != None:
                html_odds_gols_1_5_2_tempo = qtd_gols_1_5_2_tempo.findAll('td', class_="kx")
                qtd_gols_1_5_2_tempo = [odd.get_text() for odd in html_odds_gols_1_5_2_tempo]

                partida.cotacoes.odds_mais_de_2_gols_2_tempo = qtd_gols_1_5_2_tempo[0]
                partida.cotacoes.odds_menos_de_2_gols_2_tempo = qtd_gols_1_5_2_tempo[1]

            qtd_gols_2_5_2_tempo = dados_quantidade_gols_2_tempo.find('table', id='odds_ou_2.5')
            if qtd_gols_2_5_2_tempo != None:
                html_odds_gols_2_5_2_tempo = qtd_gols_2_5_2_tempo.findAll('td', class_="kx")
                qtd_gols_2_5_2_tempo = [odd.get_text() for odd in html_odds_gols_2_5_2_tempo]

                partida.cotacoes.odds_mais_de_3_gols_2_tempo = qtd_gols_2_5_2_tempo[0]
                partida.cotacoes.odds_menos_de_3_gols_2_tempo = qtd_gols_2_5_2_tempo[1]

            qtd_gols_3_5_2_tempo = dados_quantidade_gols_2_tempo.find('table', id='odds_ou_3.5')
            if qtd_gols_3_5_2_tempo != None:
                html_odds_gols_3_5_2_tempo = qtd_gols_3_5_2_tempo.findAll('td', class_="kx")
                qtd_gols_3_5_2_tempo = [odd.get_text() for odd in html_odds_gols_3_5_2_tempo]

                partida.cotacoes.odds_mais_de_4_gols_2_tempo = qtd_gols_3_5_2_tempo[0]
                partida.cotacoes.odds_menos_de_4_gols_2_tempo = qtd_gols_3_5_2_tempo[1]

        dados_dupla_chance_full_time = soup.find('div', id="block-double-chance-ft")

        if dados_dupla_chance_full_time != None:
            html_dupla_chance_full_time = dados_dupla_chance_full_time.findAll('td', class_='kx')
            dupla_chance_full_time = [odd.get_text() for odd in html_dupla_chance_full_time]

            partida.cotacoes.odds_casa_ou_empate_full_time = dupla_chance_full_time[0]
            partida.cotacoes.odds_casa_ou_fora_full_time = dupla_chance_full_time[1]
            partida.cotacoes.odds_fora_empate_full_time = dupla_chance_full_time[2]

        dados_dupla_chance_1_tempo = soup.find('div', id="block-double-chance-1hf")

        if dados_dupla_chance_1_tempo != None:
            html_dupla_chance_1_tempo = dados_dupla_chance_1_tempo.findAll('td', class_='kx')
            dupla_chance_1_tempo = [odd.get_text() for odd in html_dupla_chance_1_tempo]

            partida.cotacoes.odds_casa_ou_empate_1_tempo = dupla_chance_1_tempo[0]
            partida.cotacoes.odds_casa_ou_fora_1_tempo = dupla_chance_1_tempo[1]
            partida.cotacoes.odds_fora_empate_1_tempo = dupla_chance_1_tempo[2]

        dados_dupla_chance_2_tempo = soup.find('div', id="block-double-chance-2hf")

        if dados_dupla_chance_2_tempo != None:
            html_dupla_chance_2_tempo = dados_dupla_chance_2_tempo.findAll('td', class_='kx')
            dupla_chance_2_tempo = [odd.get_text() for odd in html_dupla_chance_2_tempo]

            partida.cotacoes.odds_casa_ou_empate_2_tempo = dupla_chance_2_tempo[0]
            partida.cotacoes.odds_casa_ou_fora_2_tempo = dupla_chance_2_tempo[1]
            partida.cotacoes.odds_fora_empate_2_tempo = dupla_chance_2_tempo[2]

        dados_ganhador_intervalo_e_ganhador_final_da_partida = soup.find('div', id="block-ht-ft")

        if dados_ganhador_intervalo_e_ganhador_final_da_partida != None:
            dados_casa_casa = dados_ganhador_intervalo_e_ganhador_final_da_partida.find('table', id='odds_htft_27')
            html_casa_casa = dados_casa_casa.findAll('td', class_='kx')
            dados_casa_casa = [odd.get_text() for odd in html_casa_casa]

            partida.cotacoes.odds_casa_casa = dados_casa_casa[0]

            dados_casa_empate = dados_ganhador_intervalo_e_ganhador_final_da_partida.find('table', id='odds_htft_30')
            html_casa_empate = dados_casa_empate.findAll('td', class_='kx')
            dados_casa_empate = [odd.get_text() for odd in html_casa_empate]

            partida.cotacoes.odds_casa_empate = dados_casa_empate[0]

            dados_casa_fora = dados_ganhador_intervalo_e_ganhador_final_da_partida.find('table', id='odds_htft_33')
            html_casa_fora = dados_casa_fora.findAll('td', class_='kx')
            dados_casa_fora = [odd.get_text() for odd in html_casa_fora]

            partida.cotacoes.odds_casa_fora = dados_casa_fora[0]

            dados_empate_casa = dados_ganhador_intervalo_e_ganhador_final_da_partida.find('table', id='odds_htft_28')
            html_empate_casa = dados_empate_casa.findAll('td', class_='kx')
            dados_empate_casa = [odd.get_text() for odd in html_empate_casa]

            partida.cotacoes.odds_empate_casa = dados_empate_casa[0]

            dados_empate_empate = dados_ganhador_intervalo_e_ganhador_final_da_partida.find('table', id='odds_htft_31')
            html_empate_empate = dados_empate_empate.findAll('td', class_='kx')
            dados_empate_empate = [odd.get_text() for odd in html_empate_empate]

            partida.cotacoes.odds_empate_empate = dados_empate_empate[0]

            dados_empate_fora = dados_ganhador_intervalo_e_ganhador_final_da_partida.find('table', id='odds_htft_34')
            html_empate_fora = dados_empate_fora.findAll('td', class_='kx')
            dados_empate_fora = [odd.get_text() for odd in html_empate_fora]

            partida.cotacoes.odds_empate_fora = dados_empate_fora[0]

            dados_fora_casa = dados_ganhador_intervalo_e_ganhador_final_da_partida.find('table', id='odds_htft_29')
            html_fora_casa = dados_fora_casa.findAll('td', class_='kx')
            dados_fora_casa = [odd.get_text() for odd in html_fora_casa]

            partida.cotacoes.odds_fora_casa = dados_fora_casa[0]

            dados_fora_empate = dados_ganhador_intervalo_e_ganhador_final_da_partida.find('table', id='odds_htft_32')
            html_fora_empate = dados_fora_empate.findAll('td', class_='kx')
            dados_fora_empate = [odd.get_text() for odd in html_fora_empate]

            partida.cotacoes.odds_fora_empate = dados_fora_empate[0]

            dados_fora_fora = dados_ganhador_intervalo_e_ganhador_final_da_partida.find('table', id='odds_htft_35')
            html_fora_fora = dados_fora_fora.findAll('td', class_='kx')
            dados_fora_fora = [odd.get_text() for odd in html_fora_fora]

            partida.cotacoes.odds_fora_fora = dados_fora_fora[0]

        dados_placar_exato = soup.find('div', id="block-correct-score")

        if dados_placar_exato != None:

            dados_placar_exato_full_time = dados_placar_exato.find('div', id='block-correct-score-ft')

            if dados_placar_exato_full_time != None:
                dados_1_a_0_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_2')
                if dados_1_a_0_full_time != None:
                    html_1_a_0_full_time = dados_1_a_0_full_time.findAll('td', class_='kx')
                    dados_1_a_0_full_time = [odd.get_text() for odd in html_1_a_0_full_time]
                    partida.cotacoes.odds_1_a_0_full_time = dados_1_a_0_full_time[0]

                dados_2_a_0_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_5')
                if dados_2_a_0_full_time != None:
                    html_2_a_0_full_time = dados_2_a_0_full_time.findAll('td', class_='kx')
                    dados_2_a_0_full_time = [odd.get_text() for odd in html_2_a_0_full_time]
                    partida.cotacoes.odds_2_a_0_full_time = dados_2_a_0_full_time[0]

                dados_2_a_1_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_6')
                if dados_2_a_1_full_time != None:
                    html_2_a_1_full_time = dados_2_a_1_full_time.findAll('td', class_='kx')
                    dados_2_a_1_full_time = [odd.get_text() for odd in html_2_a_1_full_time]
                    partida.cotacoes.odds_2_a_1_full_time = dados_2_a_1_full_time[0]

                dados_3_a_0_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_10')
                if dados_3_a_0_full_time != None:
                    html_3_a_0_full_time = dados_3_a_0_full_time.findAll('td', class_='kx')
                    dados_3_a_0_full_time = [odd.get_text() for odd in html_3_a_0_full_time]
                    partida.cotacoes.odds_3_a_0_full_time = dados_3_a_0_full_time[0]

                dados_3_a_1_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_11')
                if dados_3_a_1_full_time != None:
                    html_3_a_1_full_time = dados_3_a_1_full_time.findAll('td', class_='kx')
                    dados_3_a_1_full_time = [odd.get_text() for odd in html_3_a_1_full_time]
                    partida.cotacoes.odds_3_a_1_full_time = dados_3_a_1_full_time[0]

                dados_3_a_2_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_12')
                if dados_3_a_2_full_time != None:
                    html_3_a_2_full_time = dados_3_a_2_full_time.findAll('td', class_='kx')
                    dados_3_a_2_full_time = [odd.get_text() for odd in html_3_a_2_full_time]
                    partida.cotacoes.odds_3_a_2_full_time = dados_3_a_2_full_time[0]

                dados_4_a_0_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_18')
                if dados_4_a_0_full_time != None:
                    html_4_a_0_full_time = dados_4_a_0_full_time.findAll('td', class_='kx')
                    dados_4_a_0_full_time = [odd.get_text() for odd in html_4_a_0_full_time]
                    partida.cotacoes.odds_4_a_0_full_time = dados_4_a_0_full_time[0]

                dados_4_a_1_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_19')
                if dados_4_a_1_full_time != None:
                    html_4_a_1_full_time = dados_4_a_1_full_time.findAll('td', class_='kx')
                    dados_4_a_1_full_time = [odd.get_text() for odd in html_4_a_1_full_time]
                    partida.cotacoes.odds_4_a_1_full_time = dados_4_a_1_full_time[0]

                dados_4_a_2_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_20')
                if dados_4_a_2_full_time != None:
                    html_4_a_2_full_time = dados_4_a_2_full_time.findAll('td', class_='kx')
                    dados_4_a_2_full_time = [odd.get_text() for odd in html_4_a_2_full_time]
                    partida.cotacoes.odds_4_a_2_full_time = dados_4_a_2_full_time[0]

                dados_4_a_3_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_21')
                if dados_4_a_3_full_time != None:
                    html_4_a_3_full_time = dados_4_a_3_full_time.findAll('td', class_='kx')
                    dados_4_a_3_full_time = [odd.get_text() for odd in html_4_a_3_full_time]
                    partida.cotacoes.odds_4_a_3_full_time = dados_4_a_3_full_time[0]

                dados_5_a_0_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_36')
                if dados_5_a_0_full_time != None:
                    html_5_a_0_full_time = dados_5_a_0_full_time.findAll('td', class_='kx')
                    dados_5_a_0_full_time = [odd.get_text() for odd in html_5_a_0_full_time]
                    partida.cotacoes.odds_5_a_0_full_time = dados_5_a_0_full_time[0]

                dados_5_a_1_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_37')
                if dados_5_a_1_full_time != None:
                    html_5_a_1_full_time = dados_5_a_1_full_time.findAll('td', class_='kx')
                    dados_5_a_1_full_time = [odd.get_text() for odd in html_5_a_1_full_time]
                    partida.cotacoes.odds_5_a_1_full_time = dados_5_a_1_full_time[0]

                dados_5_a_2_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_44')
                if dados_5_a_2_full_time != None:
                    html_5_a_2_full_time = dados_5_a_2_full_time.findAll('td', class_='kx')
                    dados_5_a_2_full_time = [odd.get_text() for odd in html_5_a_2_full_time]
                    partida.cotacoes.odds_5_a_2_full_time = dados_5_a_2_full_time[0]

                dados_6_a_0_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_38')
                if dados_6_a_0_full_time != None:
                    html_6_a_0_full_time = dados_6_a_0_full_time.findAll('td', class_='kx')
                    dados_6_a_0_full_time = [odd.get_text() for odd in html_6_a_0_full_time]
                    partida.cotacoes.odds_6_a_0_full_time = dados_6_a_0_full_time[0]

                dados_6_a_1_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_39')
                if dados_6_a_1_full_time != None:
                    html_6_a_1_full_time = dados_6_a_1_full_time.findAll('td', class_='kx')
                    dados_6_a_1_full_time = [odd.get_text() for odd in html_6_a_1_full_time]
                    partida.cotacoes.odds_6_a_1_full_time = dados_6_a_1_full_time[0]

                dados_0_a_0_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_1')
                if dados_0_a_0_full_time != None:
                    html_0_a_0_full_time = dados_0_a_0_full_time.findAll('td', class_='kx')
                    dados_0_a_0_full_time = [odd.get_text() for odd in html_0_a_0_full_time]
                    partida.cotacoes.odds_0_a_0_full_time = dados_0_a_0_full_time[0]

                dados_1_a_1_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_3')
                if dados_1_a_1_full_time != None:
                    html_1_a_1_full_time = dados_1_a_1_full_time.findAll('td', class_='kx')
                    dados_1_a_1_full_time = [odd.get_text() for odd in html_1_a_1_full_time]
                    partida.cotacoes.odds_1_a_1_full_time = dados_1_a_1_full_time[0]

                dados_2_a_2_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_7')
                if dados_2_a_2_full_time != None:
                    html_2_a_2_full_time = dados_2_a_2_full_time.findAll('td', class_='kx')
                    dados_2_a_2_full_time = [odd.get_text() for odd in html_2_a_2_full_time]
                    partida.cotacoes.odds_2_a_2_full_time = dados_2_a_2_full_time[0]

                dados_3_a_3_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_13')
                if dados_3_a_3_full_time != None:
                    html_3_a_3_full_time = dados_3_a_3_full_time.findAll('td', class_='kx')
                    dados_3_a_3_full_time = [odd.get_text() for odd in html_3_a_3_full_time]
                    partida.cotacoes.odds_3_a_3_full_time = dados_3_a_3_full_time[0]

                dados_4_a_4_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_17')
                if dados_4_a_4_full_time != None:
                    html_4_a_4_full_time = dados_4_a_4_full_time.findAll('td', class_='kx')
                    dados_4_a_4_full_time = [odd.get_text() for odd in html_4_a_4_full_time]
                    partida.cotacoes.odds_4_a_4_full_time = dados_4_a_4_full_time[0]

                dados_0_a_1_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_4')
                if dados_0_a_1_full_time != None:
                    html_0_a_1_full_time = dados_0_a_1_full_time.findAll('td', class_='kx')
                    dados_0_a_1_full_time = [odd.get_text() for odd in html_0_a_1_full_time]
                    partida.cotacoes.odds_0_a_1_full_time = dados_0_a_1_full_time[0]

                dados_0_a_2_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_9')
                if dados_0_a_2_full_time != None:
                    html_0_a_2_full_time = dados_0_a_2_full_time.findAll('td', class_='kx')
                    dados_0_a_2_full_time = [odd.get_text() for odd in html_0_a_2_full_time]
                    partida.cotacoes.odds_0_a_2_full_time = dados_0_a_2_full_time[0]

                dados_1_a_2_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_8')
                if dados_1_a_2_full_time != None:
                    html_1_a_2_full_time = dados_1_a_2_full_time.findAll('td', class_='kx')
                    dados_1_a_2_full_time = [odd.get_text() for odd in html_1_a_2_full_time]
                    partida.cotacoes.odds_1_a_2_full_time = dados_1_a_2_full_time[0]

                dados_0_a_3_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_16')
                if dados_0_a_3_full_time != None:
                    html_0_a_3_full_time = dados_0_a_3_full_time.findAll('td', class_='kx')
                    dados_0_a_3_full_time = [odd.get_text() for odd in html_0_a_3_full_time]
                    partida.cotacoes.odds_0_a_3_full_time = dados_0_a_3_full_time[0]

                dados_1_a_3_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_15')
                if dados_1_a_3_full_time != None:
                    html_1_a_3_full_time = dados_1_a_3_full_time.findAll('td', class_='kx')
                    dados_1_a_3_full_time = [odd.get_text() for odd in html_1_a_3_full_time]
                    partida.cotacoes.odds_1_a_3_full_time = dados_1_a_3_full_time[0]

                dados_2_a_3_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_14')
                if dados_2_a_3_full_time != None:
                    html_2_a_3_full_time = dados_2_a_3_full_time.findAll('td', class_='kx')
                    dados_2_a_3_full_time = [odd.get_text() for odd in html_2_a_3_full_time]
                    partida.cotacoes.odds_2_a_3_full_time = dados_2_a_3_full_time[0]

                dados_0_a_4_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_25')
                if dados_0_a_4_full_time != None:
                    html_0_a_4_full_time = dados_0_a_4_full_time.findAll('td', class_='kx')
                    dados_0_a_4_full_time = [odd.get_text() for odd in html_0_a_4_full_time]
                    partida.cotacoes.odds_0_a_4_full_time = dados_0_a_4_full_time[0]

                dados_1_a_4_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_24')
                if dados_1_a_4_full_time != None:
                    html_1_a_4_full_time = dados_1_a_4_full_time.findAll('td', class_='kx')
                    dados_1_a_4_full_time = [odd.get_text() for odd in html_1_a_4_full_time]
                    partida.cotacoes.odds_1_a_4_full_time = dados_1_a_4_full_time[0]

                dados_2_a_4_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_23')
                if dados_2_a_4_full_time != None:
                    html_2_a_4_full_time = dados_2_a_4_full_time.findAll('td', class_='kx')
                    dados_2_a_4_full_time = [odd.get_text() for odd in html_2_a_4_full_time]
                    partida.cotacoes.odds_2_a_4_full_time = dados_2_a_4_full_time[0]

                dados_3_a_4_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_22')
                if dados_3_a_4_full_time != None:
                    html_3_a_4_full_time = dados_3_a_4_full_time.findAll('td', class_='kx')
                    dados_3_a_4_full_time = [odd.get_text() for odd in html_3_a_4_full_time]
                    partida.cotacoes.odds_3_a_4_full_time = dados_3_a_4_full_time[0]

                dados_3_a_5_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_45')
                if dados_3_a_5_full_time != None:
                    html_3_a_5_full_time = dados_3_a_5_full_time.findAll('td', class_='kx')
                    dados_3_a_5_full_time = [odd.get_text() for odd in html_3_a_5_full_time]
                    partida.cotacoes.odds_3_a_5_full_time = dados_3_a_5_full_time[0]

                dados_4_a_5_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_46')
                if dados_4_a_5_full_time != None:
                    html_4_a_5_full_time = dados_4_a_5_full_time.findAll('td', class_='kx')
                    dados_4_a_5_full_time = [odd.get_text() for odd in html_4_a_5_full_time]
                    partida.cotacoes.odds_4_a_5_full_time = dados_4_a_5_full_time[0]

                dados_2_a_6_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_47')
                if dados_2_a_6_full_time != None:
                    html_2_a_6_full_time = dados_2_a_6_full_time.findAll('td', class_='kx')
                    dados_2_a_6_full_time = [odd.get_text() for odd in html_2_a_6_full_time]
                    partida.cotacoes.odds_2_a_6_full_time = dados_2_a_6_full_time[0]

                dados_3_a_6_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_48')
                if dados_3_a_6_full_time != None:
                    html_3_a_6_full_time = dados_3_a_6_full_time.findAll('td', class_='kx')
                    dados_3_a_6_full_time = [odd.get_text() for odd in html_3_a_6_full_time]
                    partida.cotacoes.odds_3_a_6_full_time = dados_3_a_6_full_time[0]

                dados_4_a_6_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_49')
                if dados_4_a_6_full_time != None:
                    html_4_a_6_full_time = dados_4_a_6_full_time.findAll('td', class_='kx')
                    dados_4_a_6_full_time = [odd.get_text() for odd in html_4_a_6_full_time]
                    partida.cotacoes.odds_4_a_6_full_time = dados_4_a_6_full_time[0]

                dados_5_a_6_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_63')
                if dados_5_a_6_full_time != None:
                    html_5_a_6_full_time = dados_5_a_6_full_time.findAll('td', class_='kx')
                    dados_5_a_6_full_time = [odd.get_text() for odd in html_5_a_6_full_time]
                    partida.cotacoes.odds_5_a_6_full_time = dados_5_a_6_full_time[0]

                dados_0_a_7_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_50')
                if dados_0_a_7_full_time != None:
                    html_0_a_7_full_time = dados_0_a_7_full_time.findAll('td', class_='kx')
                    dados_0_a_7_full_time = [odd.get_text() for odd in html_0_a_7_full_time]
                    partida.cotacoes.odds_0_a_7_full_time = dados_0_a_7_full_time[0]

                dados_1_a_7_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_51')
                if dados_1_a_7_full_time != None:
                    html_1_a_7_full_time = dados_1_a_7_full_time.findAll('td', class_='kx')
                    dados_1_a_7_full_time = [odd.get_text() for odd in html_1_a_7_full_time]
                    partida.cotacoes.odds_1_a_7_full_time = dados_1_a_7_full_time[0]

                dados_2_a_7_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_52')
                if dados_2_a_7_full_time != None:
                    html_2_a_7_full_time = dados_2_a_7_full_time.findAll('td', class_='kx')
                    dados_2_a_7_full_time = [odd.get_text() for odd in html_2_a_7_full_time]
                    partida.cotacoes.odds_2_a_7_full_time = dados_2_a_7_full_time[0]

                dados_3_a_7_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_84')
                if dados_3_a_7_full_time != None:
                    html_3_a_7_full_time = dados_3_a_7_full_time.findAll('td', class_='kx')
                    dados_3_a_7_full_time = [odd.get_text() for odd in html_3_a_7_full_time]
                    partida.cotacoes.odds_3_a_7_full_time = dados_3_a_7_full_time[0]

                dados_4_a_7_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_85')
                if dados_4_a_7_full_time != None:
                    html_4_a_7_full_time = dados_4_a_7_full_time.findAll('td', class_='kx')
                    dados_4_a_7_full_time = [odd.get_text() for odd in html_4_a_7_full_time]
                    partida.cotacoes.odds_4_a_7_full_time = dados_4_a_7_full_time[0]

                dados_0_a_5_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_40')
                if dados_0_a_5_full_time != None:
                    html_0_a_5_full_time = dados_0_a_5_full_time.findAll('td', class_='kx')
                    dados_0_a_5_full_time = [odd.get_text() for odd in html_0_a_5_full_time]
                    partida.cotacoes.odds_0_a_5_full_time = dados_0_a_5_full_time[0]

                dados_1_a_5_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_41')
                if dados_1_a_5_full_time != None:
                    html_1_a_5_full_time = dados_1_a_5_full_time.findAll('td', class_='kx')
                    dados_1_a_5_full_time = [odd.get_text() for odd in html_1_a_5_full_time]
                    partida.cotacoes.odds_1_a_5_full_time = dados_1_a_5_full_time[0]

                dados_2_a_5_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_54')
                if dados_2_a_5_full_time != None:
                    html_2_a_5_full_time = dados_2_a_5_full_time.findAll('td', class_='kx')
                    dados_2_a_5_full_time = [odd.get_text() for odd in html_2_a_5_full_time]
                    partida.cotacoes.odds_2_a_5_full_time = dados_2_a_5_full_time[0]

                dados_3_a_5_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_55')
                if dados_3_a_5_full_time != None:
                    html_3_a_5_full_time = dados_3_a_5_full_time.findAll('td', class_='kx')
                    dados_3_a_5_full_time = [odd.get_text() for odd in html_3_a_5_full_time]
                    partida.cotacoes.odds_3_a_5_full_time = dados_3_a_5_full_time[0]

                dados_4_a_5_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_56')
                if dados_4_a_5_full_time != None:
                    html_4_a_5_full_time = dados_4_a_5_full_time.findAll('td', class_='kx')
                    dados_4_a_5_full_time = [odd.get_text() for odd in html_4_a_5_full_time]
                    partida.cotacoes.odds_4_a_5_full_time = dados_4_a_5_full_time[0]

                dados_0_a_6_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_42')
                if dados_0_a_6_full_time != None:
                    html_0_a_6_full_time = dados_0_a_6_full_time.findAll('td', class_='kx')
                    dados_0_a_6_full_time = [odd.get_text() for odd in html_0_a_6_full_time]
                    partida.cotacoes.odds_0_a_6_full_time = dados_0_a_6_full_time[0]

                dados_1_a_6_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_43')
                if dados_1_a_6_full_time != None:
                    html_1_a_6_full_time = dados_1_a_6_full_time.findAll('td', class_='kx')
                    dados_1_a_6_full_time = [odd.get_text() for odd in html_1_a_6_full_time]
                    partida.cotacoes.odds_1_a_6_full_time = dados_1_a_6_full_time[0]

                dados_2_a_6_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_57')
                if dados_2_a_6_full_time != None:
                    html_2_a_6_full_time = dados_2_a_6_full_time.findAll('td', class_='kx')
                    dados_2_a_6_full_time = [odd.get_text() for odd in html_2_a_6_full_time]
                    partida.cotacoes.odds_2_a_6_full_time = dados_2_a_6_full_time[0]

                dados_3_a_6_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_58')
                if dados_3_a_6_full_time != None:
                    html_3_a_6_full_time = dados_3_a_6_full_time.findAll('td', class_='kx')
                    dados_3_a_6_full_time = [odd.get_text() for odd in html_3_a_6_full_time]
                    partida.cotacoes.odds_3_a_6_full_time = dados_3_a_6_full_time[0]

                dados_4_a_6_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_59')
                if dados_4_a_6_full_time != None:
                    html_4_a_6_full_time = dados_4_a_6_full_time.findAll('td', class_='kx')
                    dados_4_a_6_full_time = [odd.get_text() for odd in html_4_a_6_full_time]
                    partida.cotacoes.odds_4_a_6_full_time = dados_4_a_6_full_time[0]

                dados_5_a_6_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_64')
                if dados_5_a_6_full_time != None:
                    html_5_a_6_full_time = dados_5_a_6_full_time.findAll('td', class_='kx')
                    dados_5_a_6_full_time = [odd.get_text() for odd in html_5_a_6_full_time]
                    partida.cotacoes.odds_5_a_6_full_time = dados_5_a_6_full_time[0]

                dados_0_a_7_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_60')
                if dados_0_a_7_full_time != None:
                    html_0_a_7_full_time = dados_0_a_7_full_time.findAll('td', class_='kx')
                    dados_0_a_7_full_time = [odd.get_text() for odd in html_0_a_7_full_time]
                    partida.cotacoes.odds_0_a_7_full_time = dados_0_a_7_full_time[0]

                dados_1_a_7_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_61')
                if dados_1_a_7_full_time != None:
                    html_1_a_7_full_time = dados_1_a_7_full_time.findAll('td', class_='kx')
                    dados_1_a_7_full_time = [odd.get_text() for odd in html_1_a_7_full_time]
                    partida.cotacoes.odds_1_a_7_full_time = dados_1_a_7_full_time[0]

                dados_2_a_7_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_62')
                if dados_2_a_7_full_time != None:
                    html_2_a_7_full_time = dados_2_a_7_full_time.findAll('td', class_='kx')
                    dados_2_a_7_full_time = [odd.get_text() for odd in html_2_a_7_full_time]
                    partida.cotacoes.odds_2_a_7_full_time = dados_2_a_7_full_time[0]

                dados_3_a_7_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_88')
                if dados_3_a_7_full_time != None:
                    html_3_a_7_full_time = dados_3_a_7_full_time.findAll('td', class_='kx')
                    dados_3_a_7_full_time = [odd.get_text() for odd in html_3_a_7_full_time]
                    partida.cotacoes.odds_3_a_7_full_time = dados_3_a_7_full_time[0]

                dados_4_a_7_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_89')
                if dados_4_a_7_full_time != None:
                    html_4_a_7_full_time = dados_4_a_7_full_time.findAll('td', class_='kx')
                    dados_4_a_7_full_time = [odd.get_text() for odd in html_4_a_7_full_time]
                    partida.cotacoes.odds_4_a_7_full_time = dados_4_a_7_full_time[0]

                dados_0_a_8_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_66')
                if dados_0_a_8_full_time != None:
                    html_0_a_8_full_time = dados_0_a_8_full_time.findAll('td', class_='kx')
                    dados_0_a_8_full_time = [odd.get_text() for odd in html_0_a_8_full_time]
                    partida.cotacoes.odds_0_a_8_full_time = dados_0_a_8_full_time[0]

                dados_1_a_8_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_67')
                if dados_1_a_8_full_time != None:
                    html_1_a_8_full_time = dados_1_a_8_full_time.findAll('td', class_='kx')
                    dados_1_a_8_full_time = [odd.get_text() for odd in html_1_a_8_full_time]
                    partida.cotacoes.odds_1_a_8_full_time = dados_1_a_8_full_time[0]

                dados_2_a_8_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_73')
                if dados_2_a_8_full_time != None:
                    html_2_a_8_full_time = dados_2_a_8_full_time.findAll('td', class_='kx')
                    dados_2_a_8_full_time = [odd.get_text() for odd in html_2_a_8_full_time]
                    partida.cotacoes.odds_2_a_8_full_time = dados_2_a_8_full_time[0]

                dados_3_a_8_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_74')
                if dados_3_a_8_full_time != None:
                    html_3_a_8_full_time = dados_3_a_8_full_time.findAll('td', class_='kx')
                    dados_3_a_8_full_time = [odd.get_text() for odd in html_3_a_8_full_time]
                    partida.cotacoes.odds_3_a_8_full_time = dados_3_a_8_full_time[0]

                dados_0_a_9_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_68')
                if dados_0_a_9_full_time != None:
                    html_0_a_9_full_time = dados_0_a_9_full_time.findAll('td', class_='kx')
                    dados_0_a_9_full_time = [odd.get_text() for odd in html_0_a_9_full_time]
                    partida.cotacoes.odds_0_a_9_full_time = dados_0_a_9_full_time[0]

                dados_1_a_9_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_95')
                if dados_1_a_9_full_time != None:
                    html_1_a_9_full_time = dados_1_a_9_full_time.findAll('td', class_='kx')
                    dados_1_a_9_full_time = [odd.get_text() for odd in html_1_a_9_full_time]
                    partida.cotacoes.odds_1_a_9_full_time = dados_1_a_9_full_time[0]

                dados_2_a_9_full_time = dados_placar_exato_full_time.find('table', id='odds_correct_score_96')
                if dados_2_a_9_full_time != None:
                    html_2_a_9_full_time = dados_2_a_9_full_time.findAll('td', class_='kx')
                    dados_2_a_9_full_time = [odd.get_text() for odd in html_2_a_9_full_time]
                    partida.cotacoes.odds_2_a_9_full_time = dados_2_a_9_full_time[0]

            dados_placar_exato_1_tempo = dados_placar_exato.find('div', id='block-correct-score-1hf')

            if dados_placar_exato_1_tempo != None:
                dados_1_a_0_1_tempo = dados_placar_exato_1_tempo.find('table', id='odds_correct_score_2')
                if dados_1_a_0_1_tempo != None:
                    html_1_a_0_1_tempo = dados_1_a_0_1_tempo.findAll('td', class_='kx')
                    dados_1_a_0_1_tempo = [odd.get_text() for odd in html_1_a_0_1_tempo]
                    partida.cotacoes.odds_1_a_0_1_tempo = dados_1_a_0_1_tempo[0]

                dados_2_a_0_1_tempo = dados_placar_exato_1_tempo.find('table', id='odds_correct_score_5')
                if dados_2_a_0_1_tempo != None:
                    html_2_a_0_1_tempo = dados_2_a_0_1_tempo.findAll('td', class_='kx')
                    dados_2_a_0_1_tempo = [odd.get_text() for odd in html_2_a_0_1_tempo]
                    partida.cotacoes.odds_2_a_0_1_tempo = dados_2_a_0_1_tempo[0]

                dados_2_a_1_1_tempo = dados_placar_exato_1_tempo.find('table', id='odds_correct_score_6')
                if dados_2_a_1_1_tempo != None:
                    html_2_a_1_1_tempo = dados_2_a_1_1_tempo.findAll('td', class_='kx')
                    dados_2_a_1_1_tempo = [odd.get_text() for odd in html_2_a_1_1_tempo]
                    partida.cotacoes.odds_2_a_1_1_tempo = dados_2_a_1_1_tempo[0]

                dados_3_a_0_1_tempo = dados_placar_exato_1_tempo.find('table', id='odds_correct_score_10')
                if dados_3_a_0_1_tempo != None:
                    html_3_a_0_1_tempo = dados_3_a_0_1_tempo.findAll('td', class_='kx')
                    dados_3_a_0_1_tempo = [odd.get_text() for odd in html_3_a_0_1_tempo]
                    partida.cotacoes.odds_3_a_0_1_tempo = dados_3_a_0_1_tempo[0]

                dados_3_a_1_1_tempo = dados_placar_exato_1_tempo.find('table', id='odds_correct_score_11')
                if dados_3_a_1_1_tempo != None:
                    html_3_a_1_1_tempo = dados_3_a_1_1_tempo.findAll('td', class_='kx')
                    dados_3_a_1_1_tempo = [odd.get_text() for odd in html_3_a_1_1_tempo]
                    partida.cotacoes.odds_3_a_1_1_tempo = dados_3_a_1_1_tempo[0]

                dados_3_a_2_1_tempo = dados_placar_exato_1_tempo.find('table', id='odds_correct_score_12')
                if dados_3_a_2_1_tempo != None:
                    html_3_a_2_1_tempo = dados_3_a_2_1_tempo.findAll('td', class_='kx')
                    dados_3_a_2_1_tempo = [odd.get_text() for odd in html_3_a_2_1_tempo]
                    partida.cotacoes.odds_3_a_2_1_tempo = dados_3_a_2_1_tempo[0]

                dados_4_a_0_1_tempo = dados_placar_exato_1_tempo.find('table', id='odds_correct_score_18')
                if dados_4_a_0_1_tempo != None:
                    html_4_a_0_1_tempo = dados_4_a_0_1_tempo.findAll('td', class_='kx')
                    dados_4_a_0_1_tempo = [odd.get_text() for odd in html_4_a_0_1_tempo]
                    partida.cotacoes.odds_4_a_0_1_tempo = dados_4_a_0_1_tempo[0]

                dados_4_a_1_1_tempo = dados_placar_exato_1_tempo.find('table', id='odds_correct_score_19')
                if dados_4_a_1_1_tempo != None:
                    html_4_a_1_1_tempo = dados_4_a_1_1_tempo.findAll('td', class_='kx')
                    dados_4_a_1_1_tempo = [odd.get_text() for odd in html_4_a_1_1_tempo]
                    partida.cotacoes.odds_4_a_1_1_tempo = dados_4_a_1_1_tempo[0]

                dados_0_a_0_1_tempo = dados_placar_exato_1_tempo.find('table', id='odds_correct_score_1')
                if dados_0_a_0_1_tempo != None:
                    html_0_a_0_1_tempo = dados_0_a_0_1_tempo.findAll('td', class_='kx')
                    dados_0_a_0_1_tempo = [odd.get_text() for odd in html_0_a_0_1_tempo]
                    partida.cotacoes.odds_0_a_0_1_tempo = dados_0_a_0_1_tempo[0]

                dados_1_a_1_1_tempo = dados_placar_exato_1_tempo.find('table', id='odds_correct_score_3')
                if dados_1_a_1_1_tempo != None:
                    html_1_a_1_1_tempo = dados_1_a_1_1_tempo.findAll('td', class_='kx')
                    dados_1_a_1_1_tempo = [odd.get_text() for odd in html_1_a_1_1_tempo]
                    partida.cotacoes.odds_1_a_1_1_tempo = dados_1_a_1_1_tempo[0]

                dados_2_a_2_1_tempo = dados_placar_exato_1_tempo.find('table', id='odds_correct_score_7')
                if dados_2_a_2_1_tempo != None:
                    html_2_a_2_1_tempo = dados_2_a_2_1_tempo.findAll('td', class_='kx')
                    dados_2_a_2_1_tempo = [odd.get_text() for odd in html_2_a_2_1_tempo]
                    partida.cotacoes.odds_2_a_2_1_tempo = dados_2_a_2_1_tempo[0]

                dados_0_a_1_1_tempo = dados_placar_exato_1_tempo.find('table', id='odds_correct_score_4')
                if dados_0_a_1_1_tempo != None:
                    html_0_a_1_1_tempo = dados_0_a_1_1_tempo.findAll('td', class_='kx')
                    dados_0_a_1_1_tempo = [odd.get_text() for odd in html_0_a_1_1_tempo]
                    partida.cotacoes.odds_0_a_1_1_tempo = dados_0_a_1_1_tempo[0]

                dados_0_a_2_1_tempo = dados_placar_exato_1_tempo.find('table', id='odds_correct_score_9')
                if dados_0_a_2_1_tempo != None:
                    html_0_a_2_1_tempo = dados_0_a_2_1_tempo.findAll('td', class_='kx')
                    dados_0_a_2_1_tempo = [odd.get_text() for odd in html_0_a_2_1_tempo]
                    partida.cotacoes.odds_0_a_2_1_tempo = dados_0_a_2_1_tempo[0]

                dados_1_a_2_1_tempo = dados_placar_exato_1_tempo.find('table', id='odds_correct_score_8')
                if dados_1_a_2_1_tempo != None:
                    html_1_a_2_1_tempo = dados_1_a_2_1_tempo.findAll('td', class_='kx')
                    dados_1_a_2_1_tempo = [odd.get_text() for odd in html_1_a_2_1_tempo]

                    partida.cotacoes.odds_1_a_2_1_tempo = dados_1_a_2_1_tempo[0]

                dados_0_a_3_1_tempo = dados_placar_exato_1_tempo.find('table', id='odds_correct_score_16')
                if dados_0_a_3_1_tempo != None:
                    html_0_a_3_1_tempo = dados_0_a_3_1_tempo.findAll('td', class_='kx')
                    dados_0_a_3_1_tempo = [odd.get_text() for odd in html_0_a_3_1_tempo]

                    partida.cotacoes.odds_0_a_3_1_tempo = dados_0_a_3_1_tempo[0]

                dados_1_a_3_1_tempo = dados_placar_exato_1_tempo.find('table', id='odds_correct_score_15')
                if dados_1_a_3_1_tempo != None:
                    html_1_a_3_1_tempo = dados_1_a_3_1_tempo.findAll('td', class_='kx')
                    dados_1_a_3_1_tempo = [odd.get_text() for odd in html_1_a_3_1_tempo]

                    partida.cotacoes.odds_1_a_3_1_tempo = dados_1_a_3_1_tempo[0]

                dados_2_a_3_1_tempo = dados_placar_exato_1_tempo.find('table', id='odds_correct_score_14')
                if dados_2_a_3_1_tempo != None:
                    html_2_a_3_1_tempo = dados_2_a_3_1_tempo.findAll('td', class_='kx')
                    dados_2_a_3_1_tempo = [odd.get_text() for odd in html_2_a_3_1_tempo]

                    partida.cotacoes.odds_2_a_3_1_tempo = dados_2_a_3_1_tempo[0]

                dados_0_a_4_1_tempo = dados_placar_exato_1_tempo.find('table', id='odds_correct_score_25')
                if dados_0_a_4_1_tempo != None:
                    html_0_a_4_1_tempo = dados_0_a_4_1_tempo.findAll('td', class_='kx')
                    dados_0_a_4_1_tempo = [odd.get_text() for odd in html_0_a_4_1_tempo]

                    partida.cotacoes.odds_0_a_4_1_tempo = dados_0_a_4_1_tempo[0]

                dados_1_a_4_1_tempo = dados_placar_exato_1_tempo.find('table', id='odds_correct_score_24')
                if dados_1_a_4_1_tempo != None:
                    html_1_a_4_1_tempo = dados_1_a_4_1_tempo.findAll('td', class_='kx')
                    dados_1_a_4_1_tempo = [odd.get_text() for odd in html_1_a_4_1_tempo]

                    partida.cotacoes.odds_1_a_4_1_tempo = dados_1_a_4_1_tempo[0]

            dados_placar_exato_2_tempo = dados_placar_exato.find('div', id='block-correct-score-2hf')

            if dados_placar_exato_2_tempo != None:
                dados_1_a_0_2_tempo = dados_placar_exato_2_tempo.find('table', id='odds_correct_score_2')
                if dados_1_a_0_2_tempo != None:
                    html_1_a_0_2_tempo = dados_1_a_0_2_tempo.findAll('td', class_='kx')
                    dados_1_a_0_2_tempo = [odd.get_text() for odd in html_1_a_0_2_tempo]
                    partida.cotacoes.odds_1_a_0_2_tempo = dados_1_a_0_2_tempo[0]

                dados_2_a_0_2_tempo = dados_placar_exato_2_tempo.find('table', id='odds_correct_score_5')
                if dados_2_a_0_2_tempo != None:
                    html_2_a_0_2_tempo = dados_2_a_0_2_tempo.findAll('td', class_='kx')
                    dados_2_a_0_2_tempo = [odd.get_text() for odd in html_2_a_0_2_tempo]
                    partida.cotacoes.odds_2_a_0_2_tempo = dados_2_a_0_2_tempo[0]

                dados_2_a_1_2_tempo = dados_placar_exato_2_tempo.find('table', id='odds_correct_score_6')
                if dados_2_a_1_2_tempo != None:
                    html_2_a_1_2_tempo = dados_2_a_1_2_tempo.findAll('td', class_='kx')
                    dados_2_a_1_2_tempo = [odd.get_text() for odd in html_2_a_1_2_tempo]
                    partida.cotacoes.odds_2_a_1_2_tempo = dados_2_a_1_2_tempo[0]

                dados_3_a_0_2_tempo = dados_placar_exato_2_tempo.find('table', id='odds_correct_score_10')
                if dados_3_a_0_2_tempo != None:
                    html_3_a_0_2_tempo = dados_3_a_0_2_tempo.findAll('td', class_='kx')
                    dados_3_a_0_2_tempo = [odd.get_text() for odd in html_3_a_0_2_tempo]
                    partida.cotacoes.odds_3_a_0_2_tempo = dados_3_a_0_2_tempo[0]

                dados_3_a_1_2_tempo = dados_placar_exato_2_tempo.find('table', id='odds_correct_score_11')
                if dados_3_a_1_2_tempo != None:
                    html_3_a_1_2_tempo = dados_3_a_1_2_tempo.findAll('td', class_='kx')
                    dados_3_a_1_2_tempo = [odd.get_text() for odd in html_3_a_1_2_tempo]
                    partida.cotacoes.odds_3_a_1_2_tempo = dados_3_a_1_2_tempo[0]

                dados_3_a_2_2_tempo = dados_placar_exato_2_tempo.find('table', id='odds_correct_score_12')
                if dados_3_a_2_2_tempo != None:
                    html_3_a_2_2_tempo = dados_3_a_2_2_tempo.findAll('td', class_='kx')
                    dados_3_a_2_2_tempo = [odd.get_text() for odd in html_3_a_2_2_tempo]
                    partida.cotacoes.odds_3_a_2_2_tempo = dados_3_a_2_2_tempo[0]

                dados_4_a_0_2_tempo = dados_placar_exato_2_tempo.find('table', id='odds_correct_score_18')
                if dados_4_a_0_2_tempo != None:
                    html_4_a_0_2_tempo = dados_4_a_0_2_tempo.findAll('td', class_='kx')
                    dados_4_a_0_2_tempo = [odd.get_text() for odd in html_4_a_0_2_tempo]
                    partida.cotacoes.odds_4_a_0_2_tempo = dados_4_a_0_2_tempo[0]

                dados_4_a_1_2_tempo = dados_placar_exato_2_tempo.find('table', id='odds_correct_score_19')
                if dados_4_a_1_2_tempo != None:
                    html_4_a_1_2_tempo = dados_4_a_1_2_tempo.findAll('td', class_='kx')
                    dados_4_a_1_2_tempo = [odd.get_text() for odd in html_4_a_1_2_tempo]
                    partida.cotacoes.odds_4_a_1_2_tempo = dados_4_a_1_2_tempo[0]

                dados_0_a_0_2_tempo = dados_placar_exato_2_tempo.find('table', id='odds_correct_score_1')
                if dados_0_a_0_2_tempo != None:
                    html_0_a_0_2_tempo = dados_0_a_0_2_tempo.findAll('td', class_='kx')
                    dados_0_a_0_2_tempo = [odd.get_text() for odd in html_0_a_0_2_tempo]
                    partida.cotacoes.odds_0_a_0_2_tempo = dados_0_a_0_2_tempo[0]

                dados_1_a_1_2_tempo = dados_placar_exato_2_tempo.find('table', id='odds_correct_score_3')
                if dados_1_a_1_2_tempo != None:
                    html_1_a_1_2_tempo = dados_1_a_1_2_tempo.findAll('td', class_='kx')
                    dados_1_a_1_2_tempo = [odd.get_text() for odd in html_1_a_1_2_tempo]
                    partida.cotacoes.odds_1_a_1_2_tempo = dados_1_a_1_2_tempo[0]

                dados_2_a_2_2_tempo = dados_placar_exato_2_tempo.find('table', id='odds_correct_score_7')
                if dados_2_a_2_2_tempo != None:
                    html_2_a_2_2_tempo = dados_2_a_2_2_tempo.findAll('td', class_='kx')
                    dados_2_a_2_2_tempo = [odd.get_text() for odd in html_2_a_2_2_tempo]
                    partida.cotacoes.odds_2_a_2_2_tempo = dados_2_a_2_2_tempo[0]

                dados_0_a_1_2_tempo = dados_placar_exato_2_tempo.find('table', id='odds_correct_score_4')
                if dados_0_a_1_2_tempo != None:
                    html_0_a_1_2_tempo = dados_0_a_1_2_tempo.findAll('td', class_='kx')
                    dados_0_a_1_2_tempo = [odd.get_text() for odd in html_0_a_1_2_tempo]
                    partida.cotacoes.odds_0_a_1_2_tempo = dados_0_a_1_2_tempo[0]

                dados_0_a_2_2_tempo = dados_placar_exato_2_tempo.find('table', id='odds_correct_score_9')
                if dados_0_a_2_2_tempo != None:
                    html_0_a_2_2_tempo = dados_0_a_2_2_tempo.findAll('td', class_='kx')
                    dados_0_a_2_2_tempo = [odd.get_text() for odd in html_0_a_2_2_tempo]
                    partida.cotacoes.odds_0_a_2_2_tempo = dados_0_a_2_2_tempo[0]

                dados_1_a_2_2_tempo = dados_placar_exato_2_tempo.find('table', id='odds_correct_score_8')
                if dados_1_a_2_2_tempo != None:
                    html_1_a_2_2_tempo = dados_1_a_2_2_tempo.findAll('td', class_='kx')
                    dados_1_a_2_2_tempo = [odd.get_text() for odd in html_1_a_2_2_tempo]

                    partida.cotacoes.odds_1_a_2_2_tempo = dados_1_a_2_2_tempo[0]

                dados_0_a_3_2_tempo = dados_placar_exato_2_tempo.find('table', id='odds_correct_score_16')
                if dados_0_a_3_2_tempo != None:
                    html_0_a_3_2_tempo = dados_0_a_3_2_tempo.findAll('td', class_='kx')
                    dados_0_a_3_2_tempo = [odd.get_text() for odd in html_0_a_3_2_tempo]

                    partida.cotacoes.odds_0_a_3_2_tempo = dados_0_a_3_2_tempo[0]

                dados_1_a_3_2_tempo = dados_placar_exato_2_tempo.find('table', id='odds_correct_score_15')
                if dados_1_a_3_2_tempo != None:
                    html_1_a_3_2_tempo = dados_1_a_3_2_tempo.findAll('td', class_='kx')
                    dados_1_a_3_2_tempo = [odd.get_text() for odd in html_1_a_3_2_tempo]

                    partida.cotacoes.odds_1_a_3_2_tempo = dados_1_a_3_2_tempo[0]

                dados_2_a_3_2_tempo = dados_placar_exato_2_tempo.find('table', id='odds_correct_score_14')
                if dados_2_a_3_2_tempo != None:
                    html_2_a_3_2_tempo = dados_2_a_3_2_tempo.findAll('td', class_='kx')
                    dados_2_a_3_2_tempo = [odd.get_text() for odd in html_2_a_3_2_tempo]

                    partida.cotacoes.odds_2_a_3_2_tempo = dados_2_a_3_2_tempo[0]

                dados_0_a_4_2_tempo = dados_placar_exato_2_tempo.find('table', id='odds_correct_score_25')
                if dados_0_a_4_2_tempo != None:
                    html_0_a_4_2_tempo = dados_0_a_4_2_tempo.findAll('td', class_='kx')
                    dados_0_a_4_2_tempo = [odd.get_text() for odd in html_0_a_4_2_tempo]

                    partida.cotacoes.odds_0_a_4_2_tempo = dados_0_a_4_2_tempo[0]

                dados_1_a_4_2_tempo = dados_placar_exato_2_tempo.find('table', id='odds_correct_score_24')
                if dados_1_a_4_2_tempo != None:
                    html_1_a_4_2_tempo = dados_1_a_4_2_tempo.findAll('td', class_='kx')
                    dados_1_a_4_2_tempo = [odd.get_text() for odd in html_1_a_4_2_tempo]

                    partida.cotacoes.odds_1_a_4_2_tempo = dados_1_a_4_2_tempo[0]

        dados_qtd_gols_par_ou_impar = soup.find('div', id='block-oddeven')

        if dados_qtd_gols_par_ou_impar != None:

            dados_qtd_gols_par_ou_impar_full_time = dados_qtd_gols_par_ou_impar.find('div', 'block-oddeven-ft')

            if dados_qtd_gols_par_ou_impar_full_time != None:
                html_odds_qtd_par_ou_impar_full_time = dados_qtd_gols_par_ou_impar_full_time.findAll('td', class_="kx")

                dados_qtd_gols_par_ou_impar_full_time = [odd.get_text() for odd in html_odds_qtd_par_ou_impar_full_time]

                partida.cotacoes.odds_qtd_gols_impar_full_time = dados_qtd_gols_par_ou_impar_full_time[0]
                partida.cotacoes.odds_qtd_gols_par_full_time = dados_qtd_gols_par_ou_impar_full_time[1]

            dados_qtd_gols_par_ou_impar_1_tempo = dados_qtd_gols_par_ou_impar.find('div', 'block-oddeven-1hf')

            if dados_qtd_gols_par_ou_impar_1_tempo != None:
                html_odds_qtd_par_ou_impar_1_tempo = dados_qtd_gols_par_ou_impar_1_tempo.findAll('td', class_="kx")

                dados_qtd_gols_par_ou_impar_1_tempo = [odd.get_text() for odd in html_odds_qtd_par_ou_impar_1_tempo]

                partida.cotacoes.odds_qtd_gols_impar_1_tempo = dados_qtd_gols_par_ou_impar_1_tempo[0]
                partida.cotacoes.odds_qtd_gols_par_1_tempo = dados_qtd_gols_par_ou_impar_1_tempo[1]

        dados_ambas_sim = soup.find('div', id='block-both-teams-to-score')
        if dados_ambas_sim != None:
            dados_ambas_sim_full_time = dados_ambas_sim.find('div', id='block-both-teams-to-score-ft')
            if dados_ambas_sim_full_time != None:
                html_odds_ambas_sim_full_time = dados_ambas_sim_full_time.findAll('td', class_="kx")
                dados_ambas_sim_full_time = [odd.get_text() for odd in html_odds_ambas_sim_full_time]
                partida.cotacoes.odds_ambas_sim_full_time = dados_ambas_sim_full_time[0]
                partida.cotacoes.odds_ambas_nao_full_time = dados_ambas_sim_full_time[1]

            dados_ambas_sim_1_tempo = dados_ambas_sim.find('div', id='block-both-teams-to-score-1hf')
            if dados_ambas_sim_1_tempo != None:
                html_odds_ambas_sim_1_tempo = dados_ambas_sim_1_tempo.findAll('td', class_="kx")
                dados_ambas_sim_1_tempo = [odd.get_text() for odd in html_odds_ambas_sim_1_tempo]
                partida.cotacoes.odds_ambas_sim_1_tempo = dados_ambas_sim_1_tempo[0]
                partida.cotacoes.odds_ambas_nao_1_tempo = dados_ambas_sim_1_tempo[1]

            dados_ambas_sim_2_tempo = dados_ambas_sim.find('div', id='block-both-teams-to-score-1hf')
            if dados_ambas_sim_2_tempo != None:
                html_odds_ambas_sim_2_tempo = dados_ambas_sim_2_tempo.findAll('td', class_="kx")
                dados_ambas_sim_2_tempo = [odd.get_text() for odd in html_odds_ambas_sim_2_tempo]
                partida.cotacoes.odds_ambas_sim_2_tempo = dados_ambas_sim_2_tempo[0]
                partida.cotacoes.odds_ambas_nao_2_tempo = dados_ambas_sim_2_tempo[1]

        return partida

    def get_resultado(self, html, status, id):

        soup = BeautifulSoup(html)

        times = soup.findAll('a', class_="participant-imglink")
        time_casa = times[3].get_text()
        time_fora = times[1].get_text()

        info_horario = soup.findAll('div', class_='mstat-date')
        data = str(info_horario[0].get_text()).split(' ')[0].replace('.', '/')
        hora = str(info_horario[0].get_text()).split(' ')[1]

        info_campeonato = soup.find('div', class_='fleft')
        camp = info_campeonato.findAll('span')
        campeonato = camp[1].get_text()

        placar_time_casa = 0
        placar_time_fora = 0

        placar = soup.findAll('span', class_='scoreboard')
        if placar.__len__() != 0:
            placar_time_casa = placar[0].get_text()
            placar_time_fora = placar[1].get_text()

        partida = Partida(id, campeonato, data, hora, time_casa, time_fora, status, placar_time_casa, placar_time_fora)

        return partida
