//Created an object to keep track of values
const Calculator = {
    //will display 0 on calculator screen
    Display_Value: '0',
    //will hold first operand for any expressions, set to null for now
    First_Operand: null,
    //checks whether or not second operand has been inputted by user
    Wait_Second_Operand: false,
    //will hold operator, set to null for now
    operator: null,
};

//modifies values each time button is clicked on
function Input_Digit(digit) {
    const {Display_Value, Wait_Second_Operand} = Calculator;
    //checks if Wait_Second_Operand is true and sets Display_Value
    //to the key that was clicked on
    if (Wait_Second_Operand === true) {
        Calculator.Display_Value = digit;
        Calculator.Wait_Second_Operand = false;
    } else {
        //overwrites Display_Value if the current value is 0
        //otherwise it adds onto it
        Calculator.Display_Value = Display_Value === '0' ? digit : Display_Value + digit;
    }
}

//This section handles decimal points
function Input_Decimal(dot) {
    //ensures that accidental clicking of deciaml point doesn't cause
    //bugs in the operation
    if (Calculator.Wait_Second_Operand === true) return;
    if (!Calculator.Display_Value.includes(dot)) {
        //saying that if Display_Value doesn't contain a decimal point
        //want to add a decimal point
        Calculator.Display_Value += dot;
    }
}

//This section handles operators
function Handle_Operator(Next_Operator) {
    const {First_Operand, Display_Value, operator} = Calculator;
    //when operator key is pressed, convert correct number
    //displayed on the screen to a number and then store the result in
    //Calculator.First_Operand if it doesn't already exist
    const Value_of_Input = parseFloat(Display_Value);
    //checks if operator already exists and if Wait_Second_Operand is true,
    //then updates the operator and exits from function
    if (operator && Calculator.Wait_Second_Operand) {
        Calculator.operator = Next_Operator;
        return;
    }
    if (First_Operand == null) {
        Calculator.First_Operand = Value_of_Input;
    } else if (operator) { //Checks if an operator already exists
        const Value_Now = First_Operand || 0;
        //if operator exists, property lookup is performed for operator
        //in Perform_Calculation object and function that matched the
        //operator is executed
        let result = Perform_Calculation[operator](Value_Now, Value_of_Input);
        //add a fixed amount of numbers after the decimal
        result = Number(result).toFixed (9);
        //this will remove any trailing 0's
        result = (result* 1).toString();
        Calculator.Display_Value = parseFloat(result);
        Calculator.First_Operand = parseFloat(result);
    }
    Calculator.Wait_Second_Operand = true;
    Calculator.operator = Next_Operator;
}
const Perform_Calculation = {
    '/': (First_Operand, Second_Operand) => First_Operand / Second_Operand,
    '*': (First_Operand, Second_Operand) => First_Operand * Second_Operand,
    '+': (First_Operand, Second_Operand) => First_Operand + Second_Operand,
    '-': (First_Operand, Second_Operand) => First_Operand - Second_Operand,
    '=': (First_Operand, Second_Operand) => Second_Operand
};
function Calculator_Reset() {
    Calculator.Display_Value = '0';
    Calculator.First_Operand = null;
    Calculator.Wait_Second_Operand = false;
    Calculator.operator = null;
}
//This function updates calculator screen with contents of Display_Value
function Update_Display() {
    //makes use of calculator-screen class to target the
    //input tag in HTML document
    const display = document.querySelector('.calculator-screen');
    display.value = Calculator.Display_Value;
}

Update_Display();
//This section monitors button clicks
const keys = document.querySelector('.calculator-keys');
keys.addEventListener('click', (event) => {
    //target variable is an object that represents element that was clicked
    const { target } = event;
    //if the element that was clicked on is not a button, exit function
    if (!target.matches('button')) {
        return;
    }
    if (target.classList.contains('operator')) {
        Handle_Operator(target.value);
        Update_Display();
        return;
    }
    if (target.classList.contains('decimal')) {
        Input_Decimal(target.value);
        Update_Display();
        return;
    }
    //Ensures that AV clears all inputs from the Calculator screen
    if (target.classList.contains('all-clear')) {
        Calculator_Reset();
        Update_Display();
        return;
    }
    Input_Digit(target.value);
    Update_Display();
})