from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        '''runs before each test'''
        self.client = app.test_client()
        app.config['TESTING'] = True


    def test_display_home_page(self):
        '''docstring'''
        with self.client:
            res = self.client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<p>Let's play the ultimate word search game!</p>", html)
            self.assertIn('games_played', session)
            self.assertEqual(session.get('high_score'), 0)


    def test_initialize_game(self):
        '''docstring'''
        with self.client:
            res = self.client.get('/init')

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, 'http://localhost/game')

            resp = self.client.get('/init', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            self.assertIn('game_board', session)
            self.assertEqual(session.get('current_score'), 0)
            self.assertEqual(session.get('guesses'), [])


    def test_init_sessions(self):
        '''docstring'''
        with self.client as client:
            with client.session_transaction() as sess:
                sess['guesses'] = ['cat', 'bat', 'ball']
            res = self.client.get('/init')
            self.assertEqual(res.status_code, 302)
            self.assertIn('cat', session['guesses'])


    def test_display_game_board(self):    
        '''docstring'''  
        with self.client as client:
            with client.session_transaction() as sess:
                sess['game_board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
            res = self.client.get('/game')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<p class='guess'>GUESS A WORD:</p>", html) 


    def test_post_display_game_board(self):
        '''docstring'''
        with self.client as client:
            with client.session_transaction() as sess:
                sess['game_board'] = [['N', 'V', 'E', 'O', 'W'],
                    ['S', 'S', 'X', 'P', 'B'],
                    ['I', 'X', 'N', 'Q', 'O'],
                    ['L', 'Q', 'F', 'X', 'V'],
                    ['O', 'U', 'A', 'W', 'F']]
            post_res = self.client.post('/game')

            self.assertEqual(post_res.status_code, 200)


# def test_submit_guess(self, word): 


    def test_game_over(self):
        '''docstring'''
        with self.client as client:
            with client.session_transaction() as sess:
                sess['current_score'] = 25
                sess['high_score'] = 0
                sess['games_played'] = 1
            res = self.client.get('/endgame')

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, 'http://localhost/init')
            self.assertEqual(session['current_score'], 25)
            self.assertIn('games_played', session)


            resp = client.get('/endgame', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)


