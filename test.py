from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        '''Test the homepage. The homepage loads up the game, the timer, sets up the UL we are appending too , and GETs the last high score for this session and number of times played. Lots to test here'''

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session"""

        with self.client as client:
            with client.session_transaction() as session:
                session['game_board'] = [["H", "E", "L", "L", "O"],
                                         ["E", "E", "X", "X", "X"],
                                         ["L", "X", "L", "X", "T"],
                                         ["L", "X", "X", "L", "X"],
                                         ["O", "X", "X", "X", "O"]]
        response = self.client.get('/check_word?word=hello')
        # print(response.json['result'], 'ok')

        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is in the dictionary"""

        self.client.get('/')
        response = self.client.get('/check_word?word=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_existent_word(self):
        """Test if word is on the board"""

        self.client.get('/')
        response = self.client.get('/check_word?word=DOESNOTCOMPUTE')
        self.assertEqual(response.json['result'], 'not-word')
