import chess.pgn
import chess.engine
from pathlib import Path
import sys

INPUT_FOLDER = Path("PNG")
OUTPUT_FOLDER = Path("extended_pgns")
STOCKFISH_PATH = "./stockfish/stockfish-ubuntu-x86-64-bmi2"
MAX_MOVES = 25

def extend_game(original_game, engine):
    board = original_game.board()
    moves = list(original_game.mainline_moves())

    new_game = chess.pgn.Game()
    node = new_game
    new_game.headers = original_game.headers.copy()

    for move in moves:
        board.push(move)
        node = node.add_main_variation(move)

    while board.fullmove_number <= MAX_MOVES and not board.is_game_over():
        result = engine.play(board, chess.engine.Limit(depth=12))
        board.push(result.move)
        node = node.add_main_variation(result.move)

    return new_game

def extend_pgn(input_path, output_path, engine):
    with open(input_path) as infile, open(output_path, "w") as outfile:
        while True:
            game = chess.pgn.read_game(infile)
            if game is None:
                break
            extended = extend_game(game, engine)
            print(extended, file=outfile, end="\n\n")

def main():
    if len(sys.argv) != 3:
        print("Usage: python extend_batch.py <batch_start> <batch_size>")
        sys.exit(1)

    batch_start = int(sys.argv[1])  # 1-indexed
    batch_size = int(sys.argv[2])
    OUTPUT_FOLDER.mkdir(exist_ok=True)

    pgn_files = sorted(INPUT_FOLDER.glob("*.pgn"))
    batch = pgn_files[batch_start - 1 : batch_start - 1 + batch_size]

    print(f"Processing PGNs {batch_start} to {batch_start + len(batch) - 1}")

    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        for pgn_file in batch:
            out_file = OUTPUT_FOLDER / pgn_file.name
            print(f"Extending {pgn_file} -> {out_file}")
            extend_pgn(pgn_file, out_file, engine)

if __name__ == "__main__":
    main()
