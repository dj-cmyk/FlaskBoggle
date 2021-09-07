from flask import Flask, render_template, redirect, request, url_for, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_strng54321'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


boggle_game = Boggle()


@app.route('/')
def display_home_page():
    '''display initial information about the game and button to start the game. Also initialize longer term session variables -> high score and number of games played'''

    session['games_played'] = 1
    session['high_score'] = 0

    return render_template('home.html')


@app.route('/init')
def initialize_game():
    '''initialize the current game variables -> game board, current score, and guesses'''
    game_board = boggle_game.make_board(5)
    session['game_board'] = game_board
    session['current_score'] = 0
    session['guesses'] = []

    return redirect('/game')


@app.route('/game', methods=['GET', 'POST'])
def display_game_board():
    '''start the game by showing the game board, guess form, and space to keep track of guessed words'''

    game_board = session['game_board']
    
    return render_template('game.html', game_board = game_board)


@app.route('/guess/<word>', methods=['GET', 'POST'])
def submit_guess(word):
    '''user submits a guess which is collected by JS file and sent here. The word is checked for validity as a word and on the board, and then return result of validity check'''
    
    game_board = session['game_board']
    check_guess = boggle_game.check_valid_word(game_board, word)
    scored_words = session['guesses']
    if request.method == 'POST':
        if check_guess == 'ok':
            scored_words.append(word)
            session['current_score'] += len(word)  
            print(session['guesses'], session['current_score'])
        return jsonify(check_guess)
    else:
        return jsonify(check_guess)


@app.route('/endgame', methods=['GET', 'POST'])
def game_over():
    '''when reset button is pressed, the round score is checked to see if it is a new high score, and the number of games played is incremented. Then we redirect to initialize another round'''

    if session['current_score'] > session['high_score']:
        session['high_score'] = session['current_score']
    session['games_played'] += 1
    
    return redirect('/init')