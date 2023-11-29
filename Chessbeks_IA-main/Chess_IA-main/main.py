from funcoes import *
import random
import chess
import chess.engine


def get_stockfish_move(board, depth=4, path= (r"D:\Dowloads\stockfish-windows-x86-64\stockfish")):
    with chess.engine.SimpleEngine.popen_uci(path) as engine:
        result = engine.play(board, chess.engine.Limit(time=1.0), root_moves=chess.engine.ALL_LEGAL)
        return result.move


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
                print("Jogada da IA (beks):")
                move = minimaxRoot(4, board, True)
                move = chess.Move.from_uci(str(move))
                board.push(move)
            
            clearConsole()
            print(board)
    
    print("Xeque mate, parabéns você ganhou!!!!!")

if __name__ == "__main__":
    main()
