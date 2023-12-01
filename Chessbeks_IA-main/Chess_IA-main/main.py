import random
from chess_functions import verifyPlayerMove, sicilianaGame, gameOver, get_stockfish_move
import chess
import chess.engine
import os

def clearConsole():
    if os.name == 'nt':
        os.system('cls')
    else:
        print('\n' * 100)
def get_stockfish_move(board, depth=4, time_limit=1.0, path=r"D:\Dowloads\stockfish-windows-x86-64-modern\stockfish\stockfish-windows-x86-64-modern.exe"):
    with chess.engine.SimpleEngine.popen_uci(path) as engine:
        result = engine.play(board, chess.engine.Limit(time=time_limit))
        best_move = result.move

        # Verifique se a jogada ataca ou come uma peça
        for move in board.legal_moves:
            if board.is_capture(move):
                return move

        # Se nenhuma jogada atacar ou comer uma peça, retorne a jogada original
        return best_move

def main():
    Heuristic = bool(random.getrandbits(1))
    count = 0
    board = chess.Board()

    # Solicitar a cor do jogador
    print("Bem-vindo ao Xadrez da tropa do 7, o nome da nossa IA é BEks, vamos começar!!!!")
    playerColor = bool(int(input("Escolha a cor: Branco(1) ou preto(0)? ")))
    
    print(board)
    
    while not gameOver(board):
        if board.turn == playerColor:
            print(board.legal_moves)
            move = input("Coloque sua jogada: ")
            verifyPlayerMove(move, board)
            print(board)
        else:
            if Heuristic:
                sicilianaGame(board, count)
                count += 1
                Heuristic = False if count > 2 else True
            else:
                print("Jogada da IA (BEks):")
                move = get_stockfish_move(board)  # função para obter a jogada do Stockfish
                board.push(move)

        clearConsole()
        print(board)

    print("Xeque mate, parabéns você ganhou!!!!!")

if __name__ == "__main__":
    main()
