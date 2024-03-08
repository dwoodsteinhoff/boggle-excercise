from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True

class FlaskTests(TestCase):

    def test_home(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)
            self.assertIn('<p class = "message">',html)
            self.assertIn('<ul class = "accepted-words">',html)
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))

    def test_valid_word(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['board']=[["J", "U", "I", "C", "Y"], 
                                  ["F", "R", "O", "Z", "E"], 
                                  ["F", "U", "Z", "E", "S"], 
                                  ["B", "A", "N", "J", "O"], 
                                  ["B", "O", "X", "E", "S"]]
                
            res = client.get('/word-check?word=froze')
            self.assertEqual(res.json['result'], 'ok')

    def test_invalid_word(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['board']=[["J", "U", "I", "C", "Y"], 
                                ["F", "R", "O", "Z", "E"], 
                                ["F", "U", "Z", "E", "S"], 
                                ["B", "A", "N", "J", "O"], 
                                ["B", "O", "X", "E", "S"]]

            res = client.get('/word-check?word=frog')
            self.assertEqual(res.json['result'], 'not-on-board')

    def test_not_a_word(self):
        with app.test_client() as client:

            client.get('/')
            res = client.get('/word-check?word=dsfasf')
            self.assertEqual(res.json['result'], 'not-word')
