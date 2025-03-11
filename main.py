from flask import Flask, render_template_string, request, jsonify
from datetime import datetime

app = Flask(__name__)
LOG_FILE = r"/var/log/tetris_logs/tetoris_log.txt"
  # 記録するファイル

@app.route("/")
def home():
    html = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>テトリス</title>
        <style>
            body { text-align: center; font-family: Arial, sans-serif; }
            canvas { background: black; display: block; margin: auto; }
            #score { font-size: 20px; margin: 10px; }
        </style>
    </head>
    <body>
        <h1>テトリス</h1>
        <p id="score">スコア: 0</p>
        <button onclick="recordScore()">記録</button>
        <canvas id="gameCanvas" width="300" height="600"></canvas>
        
        <script>
            const canvas = document.getElementById("gameCanvas");
            const ctx = canvas.getContext("2d");
            const ROWS = 20, COLS = 10, SIZE = 30;
            const board = Array.from({ length: ROWS }, () => Array(COLS).fill(0));
            let block = { r: 0, c: Math.floor(COLS / 2) };
            let score = 0;
            let interval;

            function drawBoard() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                for (let r = 0; r < ROWS; r++) {
                    for (let c = 0; c < COLS; c++) {
                        if (board[r][c]) {
                            ctx.fillStyle = "cyan";
                            ctx.fillRect(c * SIZE, r * SIZE, SIZE, SIZE);
                            ctx.strokeRect(c * SIZE, r * SIZE, SIZE, SIZE);
                        }
                    }
                }
                ctx.fillStyle = "cyan";
                ctx.fillRect(block.c * SIZE, block.r * SIZE, SIZE, SIZE);
                ctx.strokeRect(block.c * SIZE, block.r * SIZE, SIZE, SIZE);
            }

            function moveBlock(dx, dy) {
                if (isValidMove(block.r + dy, block.c + dx)) {
                    block.c += dx;
                    block.r += dy;
                    drawBoard();
                }
            }

            function isValidMove(r, c) {
                return r >= 0 && r < ROWS && c >= 0 && c < COLS && board[r][c] === 0;
            }

            function dropBlock() {
                if (isValidMove(block.r + 1, block.c)) {
                    block.r++;
                } else {
                    board[block.r][block.c] = 1;
                    clearFullRows();
                    block = { r: 0, c: Math.floor(COLS / 2) };
                    if (!isValidMove(block.r, block.c)) {
                        alert("Game Over!");
                        resetGame();
                    }
                }
                drawBoard();
            }

            function hardDrop() {
                while (isValidMove(block.r + 1, block.c)) {
                    block.r++;
                }
                board[block.r][block.c] = 1;
                clearFullRows();
                block = { r: 0, c: Math.floor(COLS / 2) };
                if (!isValidMove(block.r, block.c)) {
                    alert("Game Over!");
                    resetGame();
                }
                drawBoard();
            }

            function clearFullRows() {
                let linesCleared = 0;
                for (let r = ROWS - 1; r >= 0; r--) {
                    if (board[r].every(cell => cell === 1)) {
                        board.splice(r, 1);
                        board.unshift(Array(COLS).fill(0));
                        linesCleared++;
                    }
                }
                if (linesCleared > 0) {
                    score += linesCleared * 10;
                    document.getElementById("score").innerText = "スコア: " + score;
                }
            }

            function resetGame() {
                for (let r = 0; r < ROWS; r++) {
                    board[r].fill(0);
                }
                block = { r: 0, c: Math.floor(COLS / 2) };
                score = 0;
                document.getElementById("score").innerText = "スコア: " + score;
            }

            function startGame() {
                interval = setInterval(dropBlock, 500);
            }

            function recordScore() {
                let currentTime = new Date().toISOString();
                fetch("/record", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ score: score, timestamp: currentTime })
                })
                .then(response => response.json())
                .then(data => alert("スコア記録: " + data.message));
            }

            document.addEventListener("keydown", (event) => {
                if (event.key === "ArrowLeft") moveBlock(-1, 0);
                if (event.key === "ArrowRight") moveBlock(1, 0);
                if (event.key === "ArrowDown") moveBlock(0, 1);
                if (event.key === "ArrowUp") hardDrop();
            });

            startGame();
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route("/record", methods=["POST"])
def record():
    """スコアを txt ファイルに記録"""
    data = request.get_json()
    score = data.get("score", 0)
    timestamp = data.get("timestamp", datetime.now().isoformat())

    # txt ファイルにスコアを追記
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp}, {score}\n")

    return jsonify({"message": f"スコア {score} を {timestamp} に記録しました。"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)
