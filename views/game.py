from flask import Blueprint, render_template, request, flash, redirect
from flask_login import login_required, current_user
import random

bp_game = Blueprint('bp_name', __name__)


@bp_game.route('/game', methods=['GET'])
@login_required
def game():
    return render_template('/game/index.html', current_user=current_user, logged_in=True)


@bp_game.route('/play/<string:choice>', methods=['GET'])
@login_required
def play(choice):
    if request.method == 'GET':
        game = ['rock', 'paper', 'scissors']
        if choice in game:
            user_choice = choice
            computer_choice = random.choice(game)
            result = {
                'user_choice': user_choice,
                'computer_choice': computer_choice,
            }

            if user_choice == computer_choice:
                result['result'] = 'it\'s a tie!'
            elif (user_choice == 'rock' and computer_choice == 'scissors') or \
                    (user_choice == 'paper' and computer_choice == 'rock') or \
                    (user_choice == 'scissors' and computer_choice == 'paper'):
                result['result'] = 'you win!'
            else:
                result['result'] = 'you lose!'
            return render_template('/game/index.html', result=result, current_user=current_user, logged_in=True)

        else:
            flash('Please choose a valid move!', 'danger')
            return redirect('/game')