import flask
from service import database
import random


app = flask.Flask(__name__)


@app.route('/')
def my_form():
    return flask.render_template('search.html')

@app.route('/', methods=['POST'])
def my_form_post():

    phrase = flask.request.form['text']
    fragments = database.search(phrase, 'database.sqlite')

    for i in range(len(fragments)):
        etime = (fragments[i].startTime + fragments[i].duration) // 1000 + 10
        stime = fragments[i].startTime // 1000
        fragments[i] = str(fragments[i].url) + f'#t={stime},{etime}'
    if len(fragments) < 10:
        picked_fragments = fragments
    else:
        indices = []
        for i in range(10):
            ind = random.randint(0, len(fragments) - 1)
            if ind not in indices:
                indices.append(ind)
        picked_fragments = [fragments[index] for index in indices]
    return flask.render_template('video.html', context=picked_fragments)







