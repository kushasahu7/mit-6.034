from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.

#def rec(rules, check): 


def backchain_to_goal_tree(rules, hypothesis):
    #print("hyp to check", hypothesis)
    goalTree = [hypothesis];
    for rule in rules:
        consequents = rule.consequent()
        for e in consequents:
            #print("exp", e)
            r = match(e, hypothesis)
            #print("match re", r)
            if r is not None:
                antecedents = rule.antecedent()
                if isinstance(antecedents, str):
                    
                    statem = populate(antecedents, r)
                    #print("in if", statem)
                    goalTree.append(backchain_to_goal_tree(rules, statem))
                else:
                    subTree = []
                    for a in antecedents:
                        statem = populate(a, r)
                        #print("in else for loop", statem)
                        subTree.append(backchain_to_goal_tree(rules, statem))
                    if isinstance(antecedents, AND):
                        goalTree.append(AND(subTree))
                    else:
                        goalTree.append(OR(subTree))
                        
                    
    return simplify(OR(goalTree))           


    raise NotImplementedError

# Here's an example of running the backward chainer - uncomment
# it to see it work:
#print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
