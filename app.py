from flask import Flask, jsonify, request, render_template, redirect, url_for
import json

app = Flask(__name__)

# Chosen Keyword
KEYWORD_OF_THE_DAY = 'i_love_python'


def read_counter():
    with open('counter.json') as f:
        data = json.load(f)
    return data


def update_counter(counter, request_number):
    with open('counter.json', 'w') as f:
        json.dump({'counter': counter, 
                   'request_number': request_number}, f)
    

def read_winners():
    with open('winners.json') as f:
        data = json.load(f)
    return data['winners']


def append_winner(name):
    winners = read_winners().copy()
    with open('winners.json', 'w') as f:
        winners.append(name)
        json.dump({'winners': winners}, f)


@app.route('/add_winner', methods=['POST'])
def add_winner():
    name = request.form['winner_name']
    append_winner(name)
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
def index(errors=None, msg=None):
    winners = read_winners()
    if request.method == 'GET':
        # The main page is rendered
        return render_template('index.html', winners=winners)

    elif request.method == 'POST':
        key_word = request.form['keyWord']
        number = int(request.form['number_3_digit'])
        if key_word == KEYWORD_OF_THE_DAY:
            # The total number of participants and the global counter are stored
            # in a .json file to ensure that the data can be recovered in case 
            # of system failure. 
            entries = read_counter()
            counter = entries['counter']
            request_number = entries['request_number'] + 1
            counter += number
            update_counter(counter, request_number)
        
            if counter % 11 == 0:
                old_counter = counter
                # Both the number of participants and the global counter are reset
                update_counter(0, 0)
                return render_template('congrats.html', counter=old_counter)
            else:
                return render_template('keyword_added.html', counter=counter, request_number=request_number)
        else:
            return render_template(
                'index.html', errors=True, msg="The keyword is not correct. Please try again.", winners=winners)


if __name__ == '__main__':  
    app.run(debug=True)