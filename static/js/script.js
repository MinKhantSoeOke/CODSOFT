document.addEventListener('DOMContentLoaded', function () {
    const display = document.getElementById('display');
    const buttons = document.querySelectorAll('.button');
    let currentInput = '';
    let previousInput = '';
    let operator = null;

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const action = button.getAttribute('data-action');
            handleInput(action);
        });
    });

    function handleInput(action) {
        if (isNumber(action)) {
            handleNumber(action);
        } else if (action === 'decimal') {
            handleDecimal();
        } else if (action === 'clear') {
            handleClear();
        } else if (action === 'sign') {
            handleSign();
        } else if (action === 'percent') {
            handlePercent();
        } else if (isOperator(action)) {
            handleOperator(action);
        } else if (action === 'equals') {
            handleEquals();
        }
        updateDisplay();
    }

    function isNumber(value) {
        return !isNaN(value);
    }

    function handleNumber(number) {
        if (operator === null) {
            currentInput = currentInput === '' ? number : currentInput + number;
        } else {
            if (previousInput === '') {
                previousInput = currentInput;
                currentInput = number;
            } else {
                currentInput = currentInput === '' ? number : currentInput + number;
            }
        }
    }

    function handleDecimal() {
        if (!currentInput.includes('.')) {
            currentInput += '.';
        }
    }

    function handleClear() {
        currentInput = '';
        previousInput = '';
        operator = null;
    }

    function handleSign() {
        currentInput = currentInput.charAt(0) === '-' ? currentInput.substring(1) : '-' + currentInput;
    }

    function handlePercent() {
        currentInput = String(parseFloat(currentInput) / 100);
    }

    function isOperator(value) {
        return ['add', 'subtract', 'multiply', 'divide'].includes(value);
    }

    function handleOperator(op) {
        if (operator !== null && previousInput !== '' && currentInput !== '') {
            handleEquals();
        }
        operator = op;
    }

    function handleEquals() {
        if (operator && previousInput !== '' && currentInput !== '') {
            sendCalculationRequest(previousInput, currentInput, operator);
            operator = null;
            previousInput = '';
        }
    }

    function sendCalculationRequest(operand1, operand2, operator) {
        fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                operand1: operand1,
                operand2: operand2,
                operator: operator
            })
        })
        .then(response => response.json())
        .then(data => {
            currentInput = String(data.result);
            updateDisplay();
        })
        .catch(error => console.error('Error:', error));
    }

    function updateDisplay() {
        display.textContent = currentInput || '0';
    }
});
