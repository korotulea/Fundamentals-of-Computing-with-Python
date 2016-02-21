"""
Min-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    #tmp_board = board.clone()
    score_moves = []
    #print tmp_board
    #print tmp_board.get_empty_squares()
    #while the is empty squares --> pick a square --> if it wins / lose / draws --> return the score and grid ref
    #if game is still playing --> recursion with updated board and player switch
    
    
    for cell in board.get_empty_squares():
        tmp_board = board.clone()
        ##print tmp_board
        tmp_board.move(cell[0], cell[1], player)
        winner = tmp_board.check_win()       
        if winner == provided.DRAW:
            ##print "DRAW"
            ##print tmp_board
            return (0, (-1,-1))
        elif winner:
            #print "Win"
            #print tmp_board
            
            return (SCORES[winner], cell)
        else:
            
            score_move = (mm_move(tmp_board, provided.switch_player(player))[0], cell)
            score_moves.append(score_move) 
        ##print "scores_moves in", score_moves
    
    ##print "scores_moves out", score_moves
    
    if player == provided.PLAYERX:
        return max(score_moves)
    else:
        return min(score_moves)


def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(move_wrapper, 1, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)

#print mm_move(provided.TTTBoard(3, False,
#                               [[provided.PLAYERX, provided.EMPTY, provided.EMPTY],
#                                [provided.PLAYERO, provided.PLAYERO, provided.EMPTY],
#                                [provided.EMPTY, provided.PLAYERX, provided.EMPTY]]),
#             provided.PLAYERX)
#returned bad move (1, (0, 2))

#mm_move(provided.TTTBoard(3, False, [[provided.EMPTY, provided.EMPTY, provided.PLAYERX], [provided.EMPTY, provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY, provided.EMPTY]]), provided.PLAYERO)
#expected score 0 but received (-1, (1, 2)) 