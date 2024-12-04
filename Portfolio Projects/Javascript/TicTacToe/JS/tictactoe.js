//Keeps track of whose turn it is
let activePlayer = 'X';
//Stores an array of moves, used to determine win conditions
let selectedSquares = [];

//function for placing an x or o in a square
function placeXOrO(squareNumber) {
    //Condition ensures a square hasn't been selected already
    //.some() method used to check each element of selectSquare array
    //to see if it containes the square number clicked on
    if (!selectedSquares.some(element => element.includes(squareNumber))) {
        //This variable retrieves the HTML element id that was clocked
        let select = document.getElementById(squareNumber);
        //This condition checks who's turn it is
        if (activePlayer === 'X') {
            //If activePlayer is equal to 'X', the x.png is placed in HTML
            select.style.backgroundImage = 'url("images/x2.png")';
            //Active player may only 'X' or 'O' so, if not 'X' it much 'O'
        } else {
            //If activePlayer is equal to 'O', the o.png is placed in HTML
            select.style.backgroundImage = 'url("Images/o2.png")';
        }
        //squareNumber and activePlayer are concatenated together and added to array.
        selectedSquares.push(squareNumber + activePlayer);
        //This calls a function to check for any win conditions.
        checkWinConditions();
        //This condition is for changing the active player
        if (activePlayer === 'X') {
            //if active player is 'X' change it to 'O'
            activePlayer = 'O';
        } else {
            //Change activePlayer to 'X'
            activePlayer = 'X';
        }
        //This function plays placement sound
        audio('./media/place2.mp3');
        //This condition checks to see if it is the computer's turn
        if (activePlayer === 'O') {
            //This function disables clicking for computer's turn
            disableClick();
            //This function waits 1 second before the computer places an image and enable click
            setTimeout(function() { computersTurn();}, 1000);
        }
        //Returning true is needed for computersTurn() function
        return true;
    }
    //This function results in a radom square being selected by the computer
    function computersTurn() {
        //This boolean is needed for while loop
        let success = false;
        //This variable stores a random number 0-9
        let pickASquare;
        //This condition allows while loop to keep trying if square is selected already
        while (!success) {
            //A random number between 0 and 8 is selected
            pickASquare = String(Math.floor(Math.random() * 9));
            //If random number return true, square hasn't been selected yet
            if (placeXOrO(pickASquare)) {
                //This line calls the function
                placeXOrO(pickASquare);
                //This changed boolean and end loop
                success = true;
            };
        }
    }
}

//This function parses the selectedSquares array to search for win conditions
//drawLine() function is called to draw a line on the screen if the condition is met
function checkWinConditions() {
    if (arrayIncludes('0X', '1X', '2X')) {drawWinLine(50, 100, 558, 100)}
    else if (arrayIncludes('3X', '4X', '5X')) {drawWinLine(50, 304, 558, 304)}
    else if (arrayIncludes('6X', '7X', '8X')) {drawWinLine(50, 508, 558, 508)}
    else if (arrayIncludes('0X', '3X', '6X')) {drawWinLine(100, 50, 100, 558)}
    else if (arrayIncludes('1X', '4X', '7X')) {drawWinLine(304, 50, 304, 558)}
    else if (arrayIncludes('2X', '5X', '8X')) {drawWinLine(508, 50, 508, 558)}
    else if (arrayIncludes('6X', '4X', '2X')) {drawWinLine(100, 508, 510, 90)}
    else if (arrayIncludes('0X', '4X', '8X')) {drawWinLine(100, 100, 520, 520)}
    else if (arrayIncludes('0O', '1O', '2O')) {drawWinLine(50, 100, 558, 100)}
    else if (arrayIncludes('3O', '4O', '5O')) {drawWinLine(50, 304, 558, 304)}
    else if (arrayIncludes('6O', '7O', '8O')) {drawWinLine(50, 508, 558, 508)}
    else if (arrayIncludes('0O', '3O', '6O')) {drawWinLine(100, 50, 100, 558)}
    else if (arrayIncludes('1O', '4O', '7O')) {drawWinLine(304, 50, 304, 558)}
    else if (arrayIncludes('2O', '5O', '8O')) {drawWinLine(508, 50, 508, 558)}
    else if (arrayIncludes('6O', '4O', '2O')) {drawWinLine(100, 508, 510, 90)}
    else if (arrayIncludes('0O', '4O', '8O')) {drawWinLine(100, 100, 520, 520)}
    //This condition checks for a tie. If non of the above conditions are met and
    //9 squares are selected the code executes
    else if (selectedSquares.length >= 9) {
        //This function plays the tie game sounds
        audio('./media/tie2.mp3');
        //This function sets a .3 second timer before the resetGame is called
        setTimeout(function () { resetGame(); }, 500);
    }
    //This function checks if an array includes 3 strings
    //Used to check for each wine condition
    function arrayIncludes(squareA, squareB, squareC) {
        //These 3 variables will be used to check for 3 in a row
        const a = selectedSquares.includes(squareA);
        const b = selectedSquares.includes(squareB);
        const c = selectedSquares.includes(squareC);
        //If the 3 variables we pass are all included in our array then
        //true is returned and our else if condition executes the drawLine() function
        if (a === true && b === true && c === true) { return true; }
    }
}

//This function makes our body element temporarily unclickable
function disableClick() {
    //This makes our body unclickable
    body.style.pointerEvents = 'none';
    //This makes our body clickable again after 1 second
    setTimeout(function () { body.style.pointerEvents = 'auto'; }, 1000);
}

//This function takes a string parameter of the path set earlier for
//placement sound('./media/place.mp3')
function audio(audioURL) {
    //Create new audio object and pass the path as a parameter
    let audio = new Audio(audioURL);
    //Play method plays audio sound
    audio.play();
}

//This function utilizes HTML canvas to draw win lines
function drawWinLine(coordX1, coordY1, coordX2, coordY2) {
    //This line accesses our HTML canvas element
    const canvas = document.getElementById('win-lines');
    //This line give access to methods and properties to use on canvas
    const c = canvas.getContext('2d');
    //This line indicates where the start of a line's x axis is
    let x1 = coordX1,
        //This line indicates where start of line's y axis is
        y1 = coordY1;
        //This line indicates where end of line's x axis is
        x2 = coordX2;
        //This line indicated where end of line's y axis is
        y2 = coordY2;
        //This variable store temporary x axis data we update in our animation loop
        x = x1;
        //This variable stores temporary y axis data we update in our animation loop
        y = y1;
    //This function interacts with the canvas
    function animateLineDrawing() {
        //This variable creates a loop
        const animationLoop = requestAnimationFrame(animateLineDrawing);
        //This method clears content from the last loop iteration
        c.clearRect(0, 0, 608, 608);
        //This method starts a new path
        c.beginPath();
        //This method moves to a startig point in line
        c.moveTo(x1, y1);
        //This method indicated the end point in our line
        c.lineTo(x, y);
        //This method sets the width of our line
        c.lineWidth = 10;
        //This method sets the color of our line
        c.strokeStyle = 'rgba(70, 255, 33, .8)';
        //This method draws everything we laid out above
        c.stroke();
        //This condition checks if we've reached the endpoints
        if (x1 <= x2 && y1 <= y2) {
            //This condition adds 10 to the previous end x endpoint
            if (x < x2) { x += 10; }
            //This condition adds 10 to the previous end y endpoint
            if (y < y2) { y += 10; }
            //This condition is similar to the one above
            //This is necessary for the 6, 4, 2 win condition
            if (x >= x2 && y >= y2) { cancelAnimationFrame(animationLoop); }
        }
        //this condition is similar to the one above
        //this is necessary for the 6, 4, 2 win condition
        if (x1 <= x2 && y1 >= y2) {
            if (x < x2) { x += 10; }
            if (y > y2) { y -= 10; }
            if (x >= x2 && y <= y2) { cancelAnimationFrame(animationLoop); }
        }
    }
    //This function clears canvas after win line is drawn
    function clear() {
        //This line starts animation loop
        const animationLoop = requestAnimationFrame(clear);
        //This line clears canvas
        c.clearRect(0, 0, 608, 608);
        //This line stops our animation loop
        cancelAnimationFrame(animationLoop);
    }
    //This line disallows clicking while the win sound is playing
    disableClick();
    //this line plays win sound
    audio('./media/winGame2.mp3');
    //this line calls main animation loop
    animateLineDrawing();
    //this line waits 1 second, then clears canvas, resets game and allows clicking again
    setTimeout(function () { clear(); resetGame(); }, 1000);
}
//This function resets the game in the event of a tie or win
function resetGame() {
    //This for loop iterated through each HTML square element
    for (let i = 0; i < 9; i++) {
        //This variable gets the HTML element i
        let square = document.getElementById(String(i));
        //This removes our elements backgroundImage
        square.style.backgroundImage = "";
    }
    //This resets array so it's empty and can start over
    selectedSquares = [];
}

window.addEventListener('DOMContentLoaded', () => {
    document.body.classList.remove('fade-out');
});