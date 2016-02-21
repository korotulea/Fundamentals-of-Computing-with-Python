"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 10         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player

# Add your functions here.
def mc_trial(board, player):
    """
    This function takes a current board and the next player to move. 
    The function plays a game starting with the given player by making 
    random moves, alternating between players. 
    """
    while board.check_win() == None:
        # create a list of empty cells
        tmp_empty = board.get_empty_squares()
        # random move
        move = random.choice(tmp_empty)
        board.move(move[0], move[1], player)
        player = provided.switch_player(player)    

def mc_update_scores(scores, board, player): 
    """
    This function takes a grid of scores (a list of lists) with the same dimensions 
    as the Tic-Tac-Toe board, a board from a completed game, and which player 
    the machine player is. The function scores the completed board and update 
    the scores grid. 
    """
    # loop on scores
    if board.check_win() != provided.DRAW:
        for tmp_r in range(len(scores)):
            for tmp_c in range(len(scores[tmp_r])): 
                # base on player and game output updates the scores 
                if player == board.check_win():
                    if board.square(tmp_r, tmp_c) == player:
                        scores[tmp_r][tmp_c] += SCORE_CURRENT
                    elif board.square(tmp_r, tmp_c) != provided.EMPTY:
                        scores[tmp_r][tmp_c] -= SCORE_OTHER
                else:
                    if board.square(tmp_r, tmp_c) == player:
                        scores[tmp_r][tmp_c] -= SCORE_CURRENT
                    elif board.square(tmp_r, tmp_c) != provided.EMPTY:
                        scores[tmp_r][tmp_c] += SCORE_OTHER     

def get_best_move(board, scores):
    """
    This function takes a current board and a grid of scores. 
    The function finds all of the empty squares with the maximum score 
    and randomly return one of them as a (row, column) tuple.
    """
    # create a list of empty cells
    tmp_empty = board.get_empty_squares()
    tmp_score = [scores[score[0]][score[1]] for score in tmp_empty]
    max_score = max(tmp_score)
    # crate a list of cels with only max scores and random pick up one of them
    tmp_max_score = [score for score in tmp_empty 
                     if scores[score[0]][score[1]] == max_score]    
    best_move = random.choice(tmp_max_score)
    return best_move

def mc_move(board, player, trials):
    """
    This function takes a current board, which player the machine player is, 
    and the number of trials to run. The function uses the Monte Carlo simulation 
    to return a move for the machine player in the form of a (row, column) tuple.
    """
    b_dim = board.get_dim()
    scores = [[0 * tmp_r * tmp_c for tmp_c in range(b_dim)] for tmp_r in range(b_dim)]
    # paly game for a trial and update scores
    for tmp_trial in range(trials):
        tmp_trial = 1 * tmp_trial
        board_clone = board.clone()
        mc_trial(board_clone, player)
        if board_clone.check_win() != provided.DRAW:
            mc_update_scores(scores, board_clone, player)
    # make a move
    move = get_best_move(board, scores)
    return move


# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
