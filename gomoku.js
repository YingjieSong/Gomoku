const CANVAS_ID = 'canvas',
    WINDOW_COLOR = 'Wheat',
    LINE_COLOR = 'Black',
    LINE_WIDTH = 1,
    BORDER_LINE_WIDTH = 2,
    BORDER_PADDING = 5,
    BORDER_COLOR = 'Black',
    P1_COLOR = 'Black',
    P2_COLOR = 'White';

var intersectNum = 15;            // number of intersections, default 15x15 board
var gridNum = intersectNum - 1;   // number of grids
var board = [];                   // underlying array
for (i=0; i<intersectNum; i++) {
    board.push('0'.repeat(intersectNum));
}

var p1Cur = true,      // current player is p1 (holds black stones)
    gameEnd = false,   // game ends
    hist = [];         // history of moves

var minWH, gridSize, dotRadius, stoneRadius, windowSize, borderLenth;

var canvas = document.getElementById(CANVAS_ID),
    context = canvas.getContext('2d');

changeSizes();
drawCanvas(CANVAS_ID);

window.addEventListener("load", function() {
    changeBackground(WINDOW_COLOR);
});

window.addEventListener('resize', function(){
    changeSizes();
    drawCanvas(CANVAS_ID);
}, true);

function changeBackground(color) {
    document.body.style.background = color;
}

function changeSizes() {
    minWH = Math.min(window.innerWidth, window.innerHeight);  
    gridSize = minWH / (intersectNum + 1); // side length (in pixels) of a single grid
    dotRadius = gridSize / 8;
    stoneRadius = gridSize * 2 / 5;
    windowSize = minWH; //gridSize * (gridNum + 2);
    borderLenth = gridSize * gridNum + BORDER_PADDING * 2;
}

function drawCanvas(canvasID) {
    // set canvas size
    canvas.setAttribute('width', windowSize);
    canvas.setAttribute('height', windowSize);

    // erace canvas
    context.fillStyle = WINDOW_COLOR;
    context.fillRect(0,0,canvas.width,canvas.height);

    // draw border
    context.beginPath();
    context.lineWidth = BORDER_LINE_WIDTH;
    context.strokeStyle = BORDER_COLOR;
    context.rect(gridSize - BORDER_PADDING, gridSize - BORDER_PADDING, borderLenth, borderLenth);
    context.stroke();

    // draw grids
    context.lineWidth = LINE_WIDTH;
    context.strokeStyle = LINE_COLOR;
    for (i=0; i<gridNum; i++) {
        for (j=0; j<gridNum; j++) {
            context.beginPath();
            context.rect(gridSize * (i + 1), gridSize * (j + 1), gridSize + 1, gridSize + 1);
            context.stroke();
            context.closePath();
            
            if (i == 3 && (j == 3 || j == gridNum - 3) ||
                    i == gridNum - 3 && (j == 3 || j == gridNum - 3) ||
                    i == gridNum / 2 && j == gridNum / 2) {
                context.beginPath();
                context.fillStyle = 'Black';
                context.arc(gridSize * (i + 1), gridSize * (j + 1), dotRadius, 0, 2 * Math.PI);
                context.fill();
                context.closePath();
            }
        }
    }

    for (i=0; i<hist.length; i++) {
        var color = i % 2 == 0 ? P1_COLOR : P2_COLOR;
        drawStone(color, hist[i][0], hist[i][1]);
    }
    if (gameEnd) {
        drawWinner();
    }
}

var handleMouseDown = function(event){
    console.log("mouse down");
    var deltaX, deltaY;
	deltaX = event.clientX - canvas.offsetLeft; 
    deltaY = event.clientY - canvas.offsetTop;

    event.stopPropagation();
    event.preventDefault();

    var x = Math.floor((deltaX - Math.floor(gridSize / 2)) / gridSize);
    var y = Math.floor((deltaY - Math.floor(gridSize / 2)) / gridSize);
    if (gameEnd == false) {
        console.log('x=' + x);
        console.log('y=' + y);
        if (y < 0 || y > intersectNum ||
                x < 0 || x > intersectNum ||
                board[y].charAt(x) != '0') {
            return;
        }
        draw(x, y);
    }
}

function drawStone(color, x, y) {
    context.beginPath();
    context.fillStyle = color;
    context.arc((x + 1) * gridSize, (y + 1) * gridSize, stoneRadius, 0, 2 * Math.PI);
    context.fill();
    context.closePath();
}

function draw(x, y) {
    var color = p1Cur ? P1_COLOR : P2_COLOR;
    drawStone(color, x, y);
    hist.push([x, y]);
    temp = board[y];
    temp = temp.substr(0, x) + (p1Cur ? '1' : '2') + temp.substr(x+1, intersectNum);
    board[y] = temp;
    check();
    if (!gameEnd) {
        p1Cur = !p1Cur;
    }
}

function check() {
    /*
    checking logic is learned from https://stackoverflow.com/a/4419699
    */
    var regex = /([^1]|^)1{5}([^1]|$)|([^2]|^)2{5}([^2]|$)/g;
    // row
    var text1 = board.join('0');
    var obj1 = text1.match(regex);
    // console.log(obj1 != null);
    
    // column
    var transBoard = board.map((string, i) => [...string].reduce( (acc, elem, j) => acc += board[j][i], '')); // transpose
    var text2 = transBoard.join('0');
    var obj2 = text2.match(regex);
    
    // upper-left to lower-right diagonal
    var board3 = [];
    for(i=0; i<intersectNum; i++) {
        board3.push('0'.repeat(i) + board[i] + '0'.repeat(intersectNum - 1 - i));
    }

    var transBoard3 = [];
    for(i=0; i<2*intersectNum-1; i++){
        var temp = '';
        for(j=0; j<intersectNum; j++){
            temp += board3[j].charAt(i);
        }
        transBoard3.push(temp);
    }

    var text3 = transBoard3.join('0');
    var obj3 = text3.match(regex);
    
    // lower-left to upper-right diagonal
    var board4 = [];
    for(i=0; i<intersectNum; i++) {
        board4.push('0'.repeat(intersectNum - 1 - i) + board[i] + '0'.repeat(i))
    }
    
    var transBoard4 = [];
    for(i=0; i<2*intersectNum-1; i++){
        var temp = '';
        for(j=0; j<intersectNum; j++){
            temp += board4[j].charAt(i);
        }
        transBoard4.push(temp);
    }

    var text4 = transBoard4.join('0');
    var obj4 = text4.match(regex);

    // end the game
    if (obj1 != null || obj2 != null || obj3 != null || obj4 != null) {
        gameEnd = true;
        drawWinner();
    }
}

function drawWinner() {
    context.font = `${(gridSize-BORDER_PADDING)/2}pt Arial`;
    context.fillStyle = 'red';
    var text = p1Cur ? "BLACK WIN!" : "WHITE WIN!";
    context.fillText(text, gridSize * ((intersectNum + 1) / 2 - 1.8), (gridSize-BORDER_PADDING) * 3 / 4);
}