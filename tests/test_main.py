import unittest
from unittest.mock import MagicMock, patch
from discord.ext import commands
from main import create_embed, SessionLocal, Trivia, Question

class TestMain(unittest.TestCase):
    def test_create_embed(self):
        embed = create_embed("Test Title", "This is a description.", 0x123456)
        self.assertEqual(embed.title, "Test Title")
        self.assertEqual(embed.description, "This is a description.")
        self.assertEqual(embed.color.value, 0x123456)

    @patch('main.SessionLocal')
    def test_crearTrivia(self, mock_session):
        # Mock the session
        mock_instance = mock_session.return_value
        mock_instance.add = MagicMock()
        mock_instance.commit = MagicMock()

        # Create a command context mock
        ctx = MagicMock()
        nombre = "Test Trivia"
        embed = create_embed(f"Creado Trivia '{nombre}'", "Ahora puedes añadir preguntas a esta trivia.", 0x00ff00)

        # Call the function
        crearTrivia(ctx, nombre)

        # Assertions
        mock_instance.add.assert_called_once_with(Trivia(title=nombre, description="Trivia creada por el usuario"))
        mock_instance.commit.assert_called_once()
        ctx.respond.assert_called_once_with(embed=embed)

    @patch('main.SessionLocal')
    def test_jugarTrivia_no_trivias(self, mock_session):
        # Mock the session
        mock_instance = mock_session.return_value
        mock_instance.query = MagicMock(return_value=[])

        # Create a command context mock
        ctx = MagicMock()

        # Call the function
        jugarTrivia(ctx)

        # Assertions
        ctx.respond.assert_called_once_with(embed=create_embed("No hay trivias disponibles", "Por favor, crea una trivia primero.", 0xff0000))

if __name__ == '__main__':
    unittest.main()