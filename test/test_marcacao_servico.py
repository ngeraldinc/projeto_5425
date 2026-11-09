import unittest
from unittest.mock import patch

from sistema_marcacao_online.services.marcacao_servico import (
    atualizar_estado_marcacao,
    listar_marcacoes,
)

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

if __name__ == "__main__":
    unittest.main()