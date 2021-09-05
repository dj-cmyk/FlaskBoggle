from flask import Flask, render_template, redirect, request, url_for, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_strng54321'
#app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


boggle_game = Boggle()
game_board = boggle_game.make_board(5)



@app.route('/')
def display_home_page():
	'''display initial information about the game and button to start the game'''

	return render_template('home.html')


@app.route('/game', methods=['GET', 'POST'])
def display_game_board():
    '''start the game by showing the game board, guess form, and space to keep track of guessed words. Also initializes session variables'''

    session['game_board'] = game_board
    session['guesses'] = []
    session['current_score'] = 0
    return render_template('game.html', game_board = game_board)


@app.route('/guess/<word>', methods=['GET', 'POST'])
def submit_guess(word):
    '''user submits a guess and this is what happens'''
    # do not refresh the page!

    check_guess = boggle_game.check_valid_word(game_board, word)

    if check_guess == 'ok':
        scored_words = session['guesses']
        scored_words.append((word, len(word)))
        session['guesses'] = scored_words

        session['current_score'] += len(word)
        
        print(session['guesses'], session['current_score'])

    elif check_guess == 'not-on-board':
        flash(f"Can't find {word} on this board")
    else:
        flash('try again')

    return jsonify(check_guess)

    