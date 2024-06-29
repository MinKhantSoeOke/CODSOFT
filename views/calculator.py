from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

bp_calculator = Blueprint('bp_calculator', __name__)


@bp_calculator.route('/calculator', methods=['GET'])
@login_required
def calculator():
    return render_template('/calculator/index.html', current_user=current_user, logged_in=True)


@bp_calculator.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    operand1 = float(data['operand1'])
    operand2 = float(data['operand2'])
    operator = data['operator']

    try:
        if operator == 'add':
            result = operand1 + operand2
        elif operator == 'subtract':
            result = operand1 - operand2
        elif operator == 'multiply':
            result = operand1 * operand2
        elif operator == 'divide':
            result = operand1 / operand2 if operand1 != 0 else 'Error'
        else:
            result = 'Invalid operator'
        print(f'{operand1} {operator} {operand2} = {result}')
    except Exception as e:
        result = 'Error'

    return jsonify(result=result)