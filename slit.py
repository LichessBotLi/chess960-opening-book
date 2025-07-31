import chess.pgn
import os
import math

INPUT_FILE = "chess960.pgn"
OUTPUT_DIR = "split_pgns"
GAMES_PER_FILE = 1001
TOTAL_GAMES = 128137

def split_pgn():
    total_files = math.ceil(TOTAL_GAMES / GAMES_PER_FILE)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for file_number in range(1, total_files + 1):
            output_path = os.path.join(OUTPUT_DIR, f"chess960_{file_number:03}.pgn")
            with open(output_path, "w", encoding="utf-8") as out_file:
                for _ in range(GAMES_PER_FILE):
                    game = chess.pgn.read_game(f)
                    if game is None:
                        return  # Done reading all games
                    print(game, file=out_file, end="\n\n")

    print(f"✅ Split {TOTAL_GAMES} games into {total_files} files in {OUTPUT_DIR}/")

if __name__ == "__main__":
    split_pgn()
