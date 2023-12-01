import chess

def verifyPlayerMove(move, board):
    try:
        board.push_san(move)
    except chess.MoveError:
        print("Jogada inválida, faça outra jogada")
pawnTable = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
knightsTable = [-10, 5, 15, 30, 30, 30, 30, 30, 5, -10]
bishopsTable = [-20, 10, 25, 40, 40, 40, 40, 40, 10, -20]
rooksTable = [-40, 30, 50, 60, 60, 60, 60, 60, 30, -40]
queensTable = [-60, 40, 60, 80, 80, 80, 80, 80, 40, -60]
kingsTable = [-100, -50, -25, 0, 0, 0, 0, -25, -50, -100]

def sicilianaGame(board, count):
    # Implementation of sicilianaGame function
    if count == 0:
        move = chess.Move("e2", "e4")
    else:
        move = get_stockfish_move(board)

    return move

def gameOver(board):
    # Implementation of gameOver function
    if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.can_claim_threefold_repetition():
        return True
    return False

def get_stockfish_move(board, depth=4, time_limit=1.0, path="D:\Dowloads\stockfish-windows-x86-64-modern\stockfish\stockfish-windows-x86-64-modern.exe"):
    # Implementation of get_stockfish_move function
       with chess.engine.SimpleEngine.popen_uci(path) as engine:
        result = engine.play(board, chess.engine.Limit(time=time_limit), root_moves=chess.engine.ALL_LEGAL)
        best_move = result.best_move

        # Verifique se a jogada ataca ou come uma peça
        for square in board.attacked_squares(board.turn):
            if best_move.to == square:
                return best_move

        # Se nenhuma jogada atacar ou comer uma peça, retorne a jogada original
        return best_move