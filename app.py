from flask import Flask, request, render_template, redirect, flash, session, make_response, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'

boggle_game = Boggle()
BOGGLE_KEY = 'board'


@app.route('/')
def landing():
    
    board = boggle_game.make_board()
    session[BOGGLE_KEY] = board             #session {'board': [['w','o','r','d','s'],['w','o','r','d','s'],['w','o','r','d','s'],['w','o','r','d','s'],['w','o','r','d','s']]}
    highscore = session.get("highscore", 0) #get highscore | if no highscore, set as 0
    nplays = session.get("nplays", 0)       #get num of plays | if no num of plays, set as 0
    
    return render_template('landing.html', board=board, highscore=highscore, nplays=nplays)


@app.route("/check-word")
def check_word():
    """Check if word is in dictionary."""

    word = request.args["word"] #js-file | retrieving word from the axios request
    board = session[BOGGLE_KEY]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)
    print((score,highscore))
    print('json',jsonify(score,highscore))
    return jsonify(brokeRecord=score > highscore)


#failed attempt ******************
# @app.route('/guess')
# def guess():
#     user_guess = request.form['guess']
#     current_guesses = session[BOGGLE_GUESSES]
#     current_guesses.append(user_guess)
#     session[BOGGLE_GUESSES] = current_guesses
    
#     game_state = session[BOGGLE_KEY]