import chess
import chess.pgn
import chess.engine

INPUT_PGN = "chess960_book_3moves.pgn"
OUTPUT_PGN = "nor.pgn"
STOCKFISH_PATH = "./stockfish/stockfish-ubuntu-x86-64-bmi2"
MAX_MOVES = 40  # 30 full moves = 60 plies

def extend_game(original_game, engine):
    board = original_game.board()
    moves = list(original_game.mainline_moves())

    new_game = chess.pgn.Game()
    node = new_game

    # Copy headers (important for Chess960!)
    new_game.headers = original_game.headers.copy()

    for move in moves:
        board.push(move)
        node = node.add_main_variation(move)

    while board.fullmove_number <= MAX_MOVES and not board.is_game_over():
        result = engine.play(board, chess.engine.Limit(depth=20))
        board.push(result.move)
        node = node.add_main_variation(result.move)

    return new_game

def main():
    with open(INPUT_PGN) as infile:
        games = []
        while True:
            game = chess.pgn.read_game(infile)
            if game is None:
                break
            games.append(game)

    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        with open(OUTPUT_PGN, "w") as outfile:
            for game in games:
                extended_game = extend_game(game, engine)
                print(extended_game, file=outfile, end="\n\n")

if __name__ == "__main__":
    main()
