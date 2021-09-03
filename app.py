from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_strng54321'
#app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


boggle_game = Boggle()

@app.route('/')
def display_home_page():
	'''display initial information about the game and button to start the game'''

	return render_template('home.html')