from re import I
from classify import *
import math

##
## CSP portion of lab 4.
##
from csp import BinaryConstraint, CSP, CSPState, Variable,\
    basic_constraint_checker, solve_csp_problem

def check_for_y(con,state,value_x, var_name):
    y = con.get_variable_j_name()
    print("x,y", var_name, y)
    vy = state.get_variable_by_name(y)
    domain = vy.get_domain()
    for value_y in domain:
        statisfied = con.check(state, value_x, value_y)
        print("next ite,y,value,domainS,statis", y, value_y,vy.domain_size(), statisfied)
        if not statisfied:
            vy.reduce_domain(value_y)
        if vy.domain_size() ==0:
            return False
    return True

# Implement basic forward checking on the CSPState see csp.py
def forward_checking(state, verbose=False):
    # Before running Forward checking we must ensure
    # that constraints are okay for this state.
    basic = basic_constraint_checker(state, verbose)
    if not basic:
        return False
    #print("state", state)
    variable = state.get_current_variable()
    if variable is None:
        return True;
    value_x = variable.get_assigned_value()
    if value_x is not None: 
        x = variable.get_name()
        constraints = state.get_constraints_by_name(x)
        for con in constraints:
            i = con.get_variable_i_name()
            j = con.get_variable_j_name()
            y = i
            if y == x:
                y=j
            vy = state.get_variable_by_name(y)
            domain = vy.get_domain()
            for value_y in domain:
                if not con.check(state, value_x, value_y):
                    vy.reduce_domain(value_y)
                if vy.domain_size() ==0:
                    return False
    return True

def add_new_singletons(state, queue, visited):
    all_variables = state.get_all_variables()
    for v in all_variables:
        var_name = v.get_name()
        print("v.domain_size()", v.domain_size())
        if v.domain_size() ==1 and var_name not in visited:
            queue.append(v)
    return queue

# Now Implement forward checking + (constraint) propagation through
# singleton domains.
def forward_checking_prop_singleton(state, verbose=False):
    #Run forward checking first.
    fc_checker = forward_checking(state, verbose)
    if not fc_checker:
        return False
    
    visited = {}
    queue = add_new_singletons(state, [], visited)
    print("finalq",queue)
    while len(queue) > 0:
        var = queue.pop(0)
        var_name = var.get_name()
        print("all visited", visited, var_name)
        if var_name in visited and visited[var_name] is True:
            continue
        visited[var_name]=True
        print("all visited 2", visited[var_name])
        constraints = state.get_constraints_by_name(var_name)
        [value] = var.get_domain()
        for con in constraints:
            if not check_for_y(con,state,value,var_name):
                return False
        queue = add_new_singletons(state, queue, visited)
    return True




## The code here are for the tester
## Do not change.
from moose_csp import moose_csp_problem
from map_coloring_csp import map_coloring_csp_problem

def csp_solver_tree(problem, checker):
    problem_func = globals()[problem]
    checker_func = globals()[checker]
    answer, search_tree = problem_func().solve(checker_func)
    return search_tree.tree_to_string(search_tree)

##
## CODE for the learning portion of lab 4.
##

### Data sets for the lab
## You will be classifying data from these sets.
senate_people = read_congress_data('S110.ord')
senate_votes = read_vote_data('S110desc.csv')

house_people = read_congress_data('H110.ord')
house_votes = read_vote_data('H110desc.csv')

last_senate_people = read_congress_data('S109.ord')
last_senate_votes = read_vote_data('S109desc.csv')


### Part 1: Nearest Neighbors
## An example of evaluating a nearest-neighbors classifier.
senate_group1, senate_group2 = crosscheck_groups(senate_people)
#evaluate(nearest_neighbors(hamming_distance, 1), senate_group1, senate_group2, verbose=1)

## Write the euclidean_distance function.
## This function should take two lists of integers and
## find the Euclidean distance between them.
## See 'hamming_distance()' in classify.py for an example that
## computes Hamming distances.

def euclidean_distance(list1, list2):
    # this is not the right solution!
    return hamming_distance(list1, list2)

#Once you have implemented euclidean_distance, you can check the results:
#evaluate(nearest_neighbors(euclidean_distance, 1), senate_group1, senate_group2)

## By changing the parameters you used, you can get a classifier factory that
## deals better with independents. Make a classifier that makes at most 3
## errors on the Senate.

my_classifier = nearest_neighbors(hamming_distance, 1)
#evaluate(my_classifier, senate_group1, senate_group2, verbose=1)

### Part 2: ID Trees
#print CongressIDTree(senate_people, senate_votes, homogeneous_disorder)

## Now write an information_disorder function to replace homogeneous_disorder,
## which should lead to simpler trees.

def information_disorder(yes, no):
    return homogeneous_disorder(yes, no)

#print CongressIDTree(senate_people, senate_votes, information_disorder)
#evaluate(idtree_maker(senate_votes, homogeneous_disorder), senate_group1, senate_group2)

## Now try it on the House of Representatives. However, do it over a data set
## that only includes the most recent n votes, to show that it is possible to
## classify politicians without ludicrous amounts of information.

def limited_house_classifier(house_people, house_votes, n, verbose = False):
    house_limited, house_limited_votes = limit_votes(house_people,
    house_votes, n)
    house_limited_group1, house_limited_group2 = crosscheck_groups(house_limited)

    if verbose:
        print "ID tree for first group:"
        print CongressIDTree(house_limited_group1, house_limited_votes,
                             information_disorder)
        print
        print "ID tree for second group:"
        print CongressIDTree(house_limited_group2, house_limited_votes,
                             information_disorder)
        print
        
    return evaluate(idtree_maker(house_limited_votes, information_disorder),
                    house_limited_group1, house_limited_group2)

                                   
## Find a value of n that classifies at least 430 representatives correctly.
## Hint: It's not 10.
N_1 = 10
rep_classified = limited_house_classifier(house_people, house_votes, N_1)

## Find a value of n that classifies at least 90 senators correctly.
N_2 = 10
senator_classified = limited_house_classifier(senate_people, senate_votes, N_2)

## Now, find a value of n that classifies at least 95 of last year's senators correctly.
N_3 = 10
old_senator_classified = limited_house_classifier(last_senate_people, last_senate_votes, N_3)


## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = ""
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""


## This function is used by the tester, please don't modify it!
def eval_test(eval_fn, group1, group2, verbose = 0):
    """ Find eval_fn in globals(), then execute evaluate() on it """
    # Only allow known-safe eval_fn's
    if eval_fn in [ 'my_classifier' ]:
        return evaluate(globals()[eval_fn], group1, group2, verbose)
    else:
        raise Exception, "Error: Tester tried to use an invalid evaluation function: '%s'" % eval_fn

    
