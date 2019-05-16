from model.vo.cotacoes import Cotacoes


class Partida:
    def __init__(self, codigo, campeonato, data, horario, time_casa, time_fora, status, placar_casa, placar_fora):
        self.codigo = codigo
        self.campeonato = campeonato
        self.data = data
        self.horario = horario
        self.time_casa = time_casa
        self.time_fora = time_fora
        self.status = status
        self.placar_casa = placar_casa
        self.placar_fora = placar_fora
        self.cotacoes = Cotacoes(codigo)

    def __repr__(self):
        return str(self.__dict__)
