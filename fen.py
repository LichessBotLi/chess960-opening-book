import chess.pgn

INPUT_FILE = "chess960_book_3moves.pgn"
OUTPUT_FILE = "chess960_book_fen_only.pgn"

def strip_moves_and_keep_fen(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        
        count = 0
        while True:
            game = chess.pgn.read_game(infile)
            if game is None:
                break
            
            if "FEN" not in game.headers:
                continue  # Skip non-960 games

            new_game = chess.pgn.Game()
            new_game.headers.update(game.headers)
            # Don't add any moves

            print(new_game, file=outfile)
            print("", file=outfile)  # Ensure newline between games
            count += 1

        print(f"✅ Stripped moves from {count} Chess960 games.")

if __name__ == "__main__":
    strip_moves_and_keep_fen(INPUT_FILE, OUTPUT_FILE)
