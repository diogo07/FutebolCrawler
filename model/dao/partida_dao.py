
class PartidaDAO:

    def insert(self, partida, banco):
        if self.select(banco, partida.id):
            self.update(partida, banco)
        else:
            mycursor = banco.cursor()
            sql = "INSERT INTO partida (id, campeonato, data_jogo, horario, time_casa, time_fora, status_jogo, placar_casa, placar_fora) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            vals = (partida.id, partida.campeonato, partida.data, partida.horario, partida.time_casa, partida.time_fora, partida.status, partida.placar_casa, partida.placar_fora)
            mycursor.execute(sql, vals)
            banco.commit()

    def select(self, banco, id):
        mycursor = banco.cursor()
        mycursor.execute("SELECT * FROM partida WHERE id = '"+id+"'")
        myresult = mycursor.fetchall()
        if myresult.__len__() > 0:
            return True
        else:
            return False

    def update(self, partida, banco):
        mycursor = banco.cursor()
        sql = "UPDATE partida SET status_jogo = %s, placar_casa = %s, placar_fora = %s WHERE id = %s"
        vals = (partida.status, partida.placar_casa, partida.placar_fora, partida.id)
        mycursor.execute(sql, vals)
        banco.commit()