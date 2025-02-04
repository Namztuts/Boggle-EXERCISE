from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""
        print('***homepage***')
        
        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'seconds remaining', response.data)

    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session"""
        print('***valid_word***')
        
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["W", "O", "R", "D", "S"], 
                                 ["W", "O", "R", "D", "S"], 
                                 ["W", "O", "R", "D", "S"], 
                                 ["W", "O", "R", "D", "S"], 
                                 ["W", "O", "R", "D", "S"]]
        response = self.client.get('/check-word?word=wow')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is in the dictionary"""
        print('***invalid_word***')
        
        self.client.get('/')
        response = self.client.get('/check-word?word=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_non_english_word(self):
        """Test if word is on the board"""
        print('***non_english_word***')
        
        self.client.get('/')
        response = self.client.get(
            '/check-word?word=supercalifragilisticexpialadocious')
        self.assertEqual(response.json['result'], 'not-word')