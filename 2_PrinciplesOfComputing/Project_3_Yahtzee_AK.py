"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    hand_dic = {}
    for tmp_number in hand:
        if hand_dic.has_key(tmp_number):
            hand_dic[tmp_number] = hand_dic[tmp_number] + tmp_number 
        else:
            hand_dic[tmp_number] = tmp_number
    return max(hand_dic.values())


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcomes = range(1, num_die_sides + 1, 1)
    # generate all possible sequences for free dice
    all_free = gen_all_sequences(outcomes, num_free_dice)
    sum_all = 0
    held_dice = list(held_dice)
    # calculate values
    for tmp_ind in all_free:
        tmp_list = list(tmp_ind)
        tmp_list.extend(held_dice)
        sum_all += score(tmp_list)
    return float(sum_all) / len(all_free)

#print expected_value((2, 2), 6, 2) #expected 5.83333333333 but received 11.0
#print expected_value((), 6, 1) # 3.5
#print expected_value((3, 3), 8, 5) #expected 11.3590087891 but received 9.16546630859
#print expected_value ((), 6, 2) # expected result is 5.05555555556

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    #generate all possible combination using indexes
    tmp_index = gen_all_sequences(range(2), len(hand))
    # convert set of indexes into hands
    tmp_hands = []
    for comb in tmp_index:
        tmp_hand = []
        for index_comb in range(len(comb)):
            if comb[index_comb] == 1:
                tmp_hand.append(hand[index_comb])
            tmp_hands.append(tuple(sorted(tmp_hand)))
    return set(sorted(tmp_hands))

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    max_exp_outcome = []
    set_hold = tuple(gen_all_holds(hand))
    for hands in set_hold:
        max_exp_outcome.append(expected_value(hands, num_die_sides, len(hand)-len(hands)))
    max_index = max_exp_outcome.index(max(max_exp_outcome))
    return (max_exp_outcome[max_index], set_hold[max_index])


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()


#print strategy((1, 2), 6) #expected (5.0555555555555554, ()) but received (3.6666666666666665, (1,))
#print strategy((1,), 6) #expected (3.5, ()) but received (8.7538580246913575, ())

#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



