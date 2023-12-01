from main import get_stockfish_move
import chess
import chess.engine
import os
from main import verifyPlayerMove
from main import sicilianaGame
from main import gameOver

pawnTablew = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

pawnTableb = pawnTablew[::-1]

knightsTablew = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

knightsTableb = knightsTablew[::-1]

bishopsTablew = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

bishopsTableb = bishopsTablew[::-1]

rooksTablew = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]

rooksTableb = rooksTablew[::-1]

queensTablew = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

queensTableb = queensTablew[::-1]

kingsTablew = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]

kingsTableb = kingsTablew[::-1]

sicilianaGamew = ("e4","c5","nf3")
sicilianaGameb = ("e5", "Nc6", "Nf6")


def sicilianaGame(board, count):
    if count == 0:
        move = chess.Move("e2", "e4")
    else:
        move = get_stockfish_move(board)

    return move

def evaluateBoard(board):
    try:
        engine = chess.engine.SimpleEngine.popen_uci(
            r"D:\Dowloads\stockfish-windows-x86-64-modern\stockfish\stockfish-windows-x86-64-modern.exe"
        )
        evaluation = engine.evaluate(board)
        engine.close()

        return evaluation
    except Exception as e:
        # Analisar  possíveis erros
        print("Error evaluating board:", e)
        return 0


def minimaxRoot(depth, board, isMaximizing):
    # Chama o Stockfish para obter a avaliação da posição atual
    engine = chess.engine.SimpleEngine.popen_uci(r"D:\Dowloads\stockfish-windows-x86-64-modern\stockfish\stockfish-windows-x86-64-modern.exe")
    evaluation = engine.evaluate(board)
    engine.close()

    # Continua a execução do algoritmo minimax
    legalMoves = board.legal_moves
    bestMove = -9999
    finalMove = None
    for x in legalMoves:
        move = chess.Move.from_uci(str(x))
        board.push(move)
        value = max(bestMove, minimax(depth - 1, board, -10000, 10000, not isMaximizing))
        board.pop()
        if value > bestMove:
            bestMove = value
            finalMove = move
        return finalMove

def minimax(depth, board, maximizing, alpha, beta):
    if depth == 0 or board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material():
        return -evaluateBoard(board)

    legalMoves = list(board.legal_moves)

    if maximizing:
        bestMove = -9999
        for move in legalMoves:
            newBoard = board.copy()
            newBoard.push(move)
            bestMove = max(bestMove, minimax(depth - 1, newBoard, False, alpha, beta))
            alpha = max(alpha, bestMove)
            if beta <= alpha:
                return bestMove
        return bestMove
    else:
        bestMove = 9999
        for move in legalMoves:
            newBoard = board.copy()
            newBoard.push(move)
            bestMove = min(bestMove, minimax(depth - 1, newBoard, True, alpha, beta))
            beta = min(beta, bestMove)
            if beta <= alpha:
                return bestMove
        return bestMove

    
def verifyPlayerMove(move, board):
    try:
        board.push_san(move)
    except chess.MoveError:
        print("Jogada inválida, faça outra jogada")

def gameOver(board):
    return board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material()


pawnTable = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
knightsTable = [-10, 5, 15, 30, 30, 30, 30, 30, 5, -10]
bishopsTable = [-20, 10, 25, 40, 40, 40, 40, 40, 10, -20]
rooksTable = [-40, 30, 50, 60, 60, 60, 60, 60, 30, -40]
queensTable = [-60, 40, 60, 80, 80, 80, 80, 80, 40, -60]
kingsTable = [-100, -50, -25, 0, 0, 0, 0, -25, -50, -100]

def getPieceValue(piece, i):
    if piece is None:
        return 0
    value = 0
    if piece == "P" or piece == "p":
        value = 10 + pawnTable[i+1]
    if piece == "N" or piece == "n":
        value = 30 + knightsTable[i+1]
    if piece == "B" or piece == "b":
        value = 30 + bishopsTable[i+1]
    if piece == "R" or piece == "r":
        value = 50 + rooksTable[i+1]
    if piece == "Q" or piece == "q":
        value = 90 + queensTable[i+1]
    if piece == 'K' or piece == 'k':
        value = 900 + kingsTable[i+1]
    return value
def verifyPlayerMove(move, board):
    try:
        board.push_san(move)
    except chess.MoveError:
        print("Jogada inválida, faça outra jogada")

def gameOver(board):
    return board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material()

    return False