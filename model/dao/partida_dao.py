
class PartidaDAO:

    def insert(self, partida, banco):
        if self.select(banco, partida.codigo):
            self.update(partida, banco)
        else:
            mycursor = banco.cursor()
            sql = "INSERT INTO partidas (codigo, campeonato, data_jogo, horario, time_casa, time_fora, status_jogo, placar_casa, placar_fora) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            vals = (partida.codigo, partida.campeonato, partida.data, partida.horario, partida.time_casa, partida.time_fora, partida.status, partida.placar_casa, partida.placar_fora)
            mycursor.execute(sql, vals)
            banco.commit()

    def select(self, banco, codigo):
        mycursor = banco.cursor()
        mycursor.execute("SELECT * FROM partidas WHERE codigo = '"+codigo+"'")
        myresult = mycursor.fetchall()
        if myresult.__len__() > 0:
            return True
        else:
            return False

    def update(self, partida, banco):
        mycursor = banco.cursor()
        sql = "UPDATE partidas SET status_jogo = %s, placar_casa = %s, placar_fora = %s WHERE codigo = %s"
        vals = (partida.status, partida.placar_casa, partida.placar_fora, partida.codigo)
        mycursor.execute(sql, vals)
        banco.commit()