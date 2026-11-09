import unittest
from unittest.mock import patch
from datetime import date, time, timedelta
from sistema_marcacao_online.services.marcacao_servico import atualizar_estado_marcacao, listar_marcacoes, listar_horarios_disponiveis, criar_marcacao

class TestMarcacaoServico(unittest.TestCase):

    @patch(
        "sistema_marcacao_online.services.marcacao_servico."
        "atualizar_estado_marcacao_repo"
    )
    def test_atualiza_estado_valido(self, atualizar_repo):
        atualizar_repo.return_value = 3

        resultado = atualizar_estado_marcacao(3, " realizada ")

        self.assertEqual(resultado, 3)
        atualizar_repo.assert_called_once_with(3, "realizada")

    @patch(
        "sistema_marcacao_online.services.marcacao_servico."
        "atualizar_estado_marcacao_repo"
    )
    def test_recusa_estado_invalido(self, atualizar_repo):
        with self.assertRaises(ValueError):
            atualizar_estado_marcacao(3, "pendente")

        atualizar_repo.assert_not_called()

    @patch(
        "sistema_marcacao_online.services.marcacao_servico."
        "atualizar_estado_marcacao_repo"
    )
    def test_avisa_quando_marcacao_nao_existe(self, atualizar_repo):
        atualizar_repo.return_value = None

        with self.assertRaises(ValueError):
            atualizar_estado_marcacao(999, "falta")

    @patch(
        "sistema_marcacao_online.services.marcacao_servico."
        "listar_marcacoes_repo"
    )
    def test_lista_marcacoes(self, listar_repo):
        marcacoes_ficticias = [(3, "2026-11-20", "15:30", "confirmada")]
        listar_repo.return_value = marcacoes_ficticias

        resultado = listar_marcacoes()

        self.assertEqual(resultado, marcacoes_ficticias)

    @patch(
        "sistema_marcacao_online.services.marcacao_servico."
        "listar_horarios_ocupados_repo"
    )
        
    def test_lista_somente_horarios_livres(self, listar_ocupados):
        data = date.today() + timedelta(days=1)
        while data.weekday() >= 5:
            data += timedelta(days=1)

        listar_ocupados.return_value = [time(10), time(14)]

        horarios = listar_horarios_disponiveis(data)

        self.assertEqual(
            horarios,
            [time(8), time(12), time(16), time(18)],
        )

    def test_recusa_marcacao_no_fim_de_semana(self):
        data = date.today()
        while data.weekday() != 5:
            data += timedelta(days=1)

        with self.assertRaises(ValueError):
            listar_horarios_disponiveis(data)

    def test_recusa_hora_fora_dos_turnos(self):
        data = date.today() + timedelta(days=1)
        while data.weekday() >= 5:
            data += timedelta(days=1)

        with self.assertRaises(ValueError):
            criar_marcacao(1, data, "09:00", "1")

if __name__ == "__main__":
    unittest.main()