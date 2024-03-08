from flask import Flask, request, render_template, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "the_s3cr3t_k3y"

boggle_game = Boggle()

@app.route('/')
def home_page():
    the_board = boggle_game.make_board()
    session['board'] = the_board
    highscore = session.get("highscore",0)
    nplays = session.get("nplays",0)

    return render_template("index.html", board = the_board , highscore = highscore, nplays=nplays)

@app.route('/word-check')
def check_submitted_word():
    word = request.args['word']
    board = session['board']

    res = boggle_game.check_valid_word(board,word)

    return jsonify({'result' : res})

@app.route("/post-score", methods=["POST"])
def post_score():
    score = request.json["score"]
    highscore = session.get("highscore",0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)