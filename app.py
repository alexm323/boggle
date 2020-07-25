

from boggle import Boggle
from flask import Flask, request, render_template, redirect, session, jsonify, url_for


app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"

# set a 'SECRET_KEY' to enable the Flask session cookies

# creates an instance of the Boggle Class called boggle_game


boggle_game = Boggle()


# **************************************************************


@app.route('/')
def start_boggle_game():
    session['game_board'] = boggle_game.make_board()
    board = session['game_board']
    hi_score = session.get('hi_score', 0)
    times_played = session.get('times_played', 0)
    return render_template('boggle.html', board=board, hi_score=hi_score, times_played=times_played)


@app.route("/check_word")
def check_word():
    """Check if word is in dictionary."""
    word = request.args["word"]
    # reverse_word = word[::-1]
    board = session["game_board"]
    response = boggle_game.check_valid_word(board, word)
    # print(word)

    # return jsonify({'word': word, 'testing': reverse_word, 'wordFound': response})
    return jsonify({'result': response, 'word': word})


@app.route('/post_score', methods=['POST'])
def post_score():
    score = request.json['score']
    score = int(score)
    hi_score = session.get('hi_score', 0)
    hi_score = int(hi_score)
    times_played = session.get('times_played', 0)
    times_played = int(times_played)

    session['times_played'] = times_played + 1
    session['hi_score'] = max((score), (hi_score))

    return jsonify(new_record=hi_score > score)
