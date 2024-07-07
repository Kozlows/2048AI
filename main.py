import game as g2048
import ai

ai2048 = ai.NeuralNetwork(4, 4)
game = g2048.Game2048(ai2048)
game.startGame()
print(ai2048.boardInput(game.board))