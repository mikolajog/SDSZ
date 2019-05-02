from gameoflife import GameOfLife

"""
Code responsible for running the game. 
We check whether file is included or run. 
"""

if __name__ == "__main__":
    game = GameOfLife(80, 40)
    game.run()