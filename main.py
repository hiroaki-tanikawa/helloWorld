from flask import Flask, render_template_string
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>テトリス</title>
        <style>
            body {{ text-align: center; font-family: Arial, sans-serif; }}
            canvas {{ background: red; display: block; margin: auto; }}
        </style>
    </head>
    <body>
        <h1>テトリス</h1>

        <canvas id="gameCanvas" width="300" height="600"></canvas>
        <script>
            const canvas = document.getElementById("gameCanvas");
            const ctx = canvas.getContext("2d");
            const ROWS = 20, COLS = 10, SIZE = 30;
            const board = Array.from({{ length: ROWS }}, () => Array(COLS).fill(0));

            let block = {{ r: 0, c: Math.floor(COLS / 2) }};
            let interval;

            function drawBoard() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                for (let r = 0; r < ROWS; r++) {{
                    for (let c = 0; c < COLS; c++) {{
                        if (board[r][c]) {{
                            ctx.fillStyle = "cyan";
                            ctx.fillRect(c * SIZE, r * SIZE, SIZE, SIZE);
                            ctx.strokeRect(c * SIZE, r * SIZE, SIZE, SIZE);
                        }}
                    }}
                }}
                ctx.fillStyle = "cyan";
                ctx.fillRect(block.c * SIZE, block.r * SIZE, SIZE, SIZE);
                ctx.strokeRect(block.c * SIZE, block.r * SIZE, SIZE, SIZE);
            }}

            function moveBlock(dx, dy) {{
                if (isValidMove(block.r + dy, block.c + dx)) {{
                    block.c += dx;
                    block.r += dy;
                    drawBoard();
                }}
            }}

            function isValidMove(r, c) {{
                return r >= 0 && r < ROWS && c >= 0 && c < COLS && board[r][c] === 0;
            }}

            function dropBlock() {{
                if (isValidMove(block.r + 1, block.c)) {{
                    block.r++;
                }} else {{
                    board[block.r][block.c] = 1;
                    clearFullRows();
                    block = {{ r: 0, c: Math.floor(COLS / 2) }};
                    if (!isValidMove(block.r, block.c)) {{
                        alert("Game Over!");
                        resetGame();
                    }}
                }}
                drawBoard();
            }}

            function hardDrop() {{
                while (isValidMove(block.r + 1, block.c)) {{
                    block.r++;
                }}
                board[block.r][block.c] = 1;
                clearFullRows();
                block = {{ r: 0, c: Math.floor(COLS / 2) }};
                if (!isValidMove(block.r, block.c)) {{
                    alert("Game Over!");
                    resetGame();
                }}
                drawBoard();
            }}

            function clearFullRows() {{
                for (let r = ROWS - 1; r >= 0; r--) {{
                    if (board[r].every(cell => cell === 1)) {{
                        board.splice(r, 1);
                        board.unshift(Array(COLS).fill(0));
                    }}
                }}
            }}

            function resetGame() {{
                for (let r = 0; r < ROWS; r++) {{
                    board[r].fill(0);
                }}
                block = {{ r: 0, c: Math.floor(COLS / 2) }};
            }}

            function startGame() {{
                interval = setInterval(dropBlock, 500);
            }}

            document.addEventListener("keydown", (event) => {{
                if (event.key === "ArrowLeft") moveBlock(-1, 0); // 左
                if (event.key === "ArrowRight") moveBlock(1, 0);  // 右
                if (event.key === "ArrowDown") moveBlock(0, 1);   // 下
                if (event.key === "ArrowUp") hardDrop();          // 上で即落下
            }});

            startGame();
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)
