import sys
import queue as queue

class status:
    def __init__(self, confidence_level, attention_level, interest_level, opinion):
        self.opinion = opinion         # totallyDisagree(-2), disagree(-1), neutral(0), agree(+1), totallyAgree(+2)
        self.initOpinion  = opinion    # totallyDisagree(-2), disagree(-1), neutral(0), agree(+1), totallyAgree(+2)
        self.cLevel = confidence_level # low(0), mid(1), high(2)
        self.aLevel = attention_level  # low(0), mid(1), high(2)
        self.iLevel = interest_level   # low(0), mid(1), high(2)
        
    def change(self, rule):
        self.opinion = self.opinion + rule.oRate
        if self.opinion > 2:
            self.opinion = 2
        if self.opinion < -2:
            self.opinion = -2
        self.cLevel = self.cLevel + rule.cRate
        if self.cLevel > 2:
            self.cLevel = 2
        if self.cLevel < 0:
            self.cLevel = 0
        self.aLevel = self.aLevel + rule.aRate
        if self.aLevel > 2:
            self.aLevel = 2
        if self.aLevel < 0:
            self.aLevel = 0
        self.iLevel = self.iLevel + rule.iRate
        if self.iLevel > 2:
            self.iLevel = 2
        if self.iLevel < 0:
            self.iLevel = 0
        
    def check(self):
        if (self.opinion > 0 and self.initOpinion < 0) or \
        (self.opinion < 0 and self.initOpinion > 0) or \
        (self.opinion != 0 and self.initOpinion == 0):
            return "Opinion Changed!"
        return "Stick to the original opinion..."
        
    def __str__(self):
        return 'Current State Summary \n' \
        + 'current opinion = {}\n'.format(self.opinion) \
        + 'original opinion = {}\n'.format(self.initOpinion) \
        + 'confidence level = {}\n'.format(self.cLevel) \
        + 'attention level = {}\n'.format(self.aLevel) \
        + 'interset level = {}\n'.format(self.iLevel) 
    
class env:
    def __init__(self, q1, q2, q3, q4, q5):
        self.q1 = q1 #q1. Does the article have a bias? (yes, no, cantSay)
        self.q2 = q2 #q2. Which comments did you read? (every, sortedByLikes, sampledBothSidesOfArgument, unsorted, never)
        self.q3 = q3 #q3. Are the comments offensive? (notAtAll, little, neutral, quite, very)
        self.q4 = q4 #q4. Which way is the comment section leaning (stronglyAgainstYou, againstYou, neutral, withYou, stronglyWithYou)
        self.q5 = q5 #q5. Are the comments well reasoned ? (notAtAll, little, neutral, quite, very)

class rule:
    def __init__(self, rule_id, opinion, confidence_level, attention_level, interest_level,\
    q1, q2, q3, q4, q5, opinion_changeRate, confidence_changeRate, attention_changeRate, interest_changeRate):
        """Conditions where the rule is fired"""
        self.ID = rule_id
        self.opinion = opinion
        self.cLevel = confidence_level
        self.aLevel = attention_level
        self.iLevel = interest_level
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4
        self.q5 = q5
        self.oRate = opinion_changeRate
        self.cRate = confidence_changeRate
        self.aRate = attention_changeRate
        self.iRate = interest_changeRate
        self.score = 0
        self.isUsed = False
        
    def computeScore(self, status, env):
        score = 0
        if self.opinion != None and self.opinion == status.opinion:
            score += 1
        if self.cLevel != None and self.cLevel == status.cLevel:
            score += 1
        if self.aLevel != None and self.aLevel == status.aLevel:
            score += 1
        if self.iLevel != None and self.iLevel == status.iLevel:
            score += 1
        if self.q1 != None and self.q1 == env.q1:
            score += 1
        if self.q2 != None and self.q2 == env.q2:
            score += 1
        if self.q3 != None and self.q3 == env.q3:
            score += 1
        if self.q4 != None and self.q4 == env.q4:
            score += 1
        if self.q5 != None and self.q5 == env.q5:
            score += 1
        self.score = score
    
    def __lt__(self, other):
        """intentionally reverse the inequality for the priority queue use"""
        return (self.score > other.score)
           
    def __str__(self):
        return 'Rule {} Summary \n'.format(self.ID) \
        + 'This rule is fired if \n' \
        + 'opinion = {}\n'.format(self.opinion) \
        + 'confidence level = {}\n'.format(self.cLevel) \
        + 'attention level = {}\n'.format(self.aLevel) \
        + 'interset level = {}\n'.format(self.iLevel) \
        + 'answer of q1 = {}\n'.format(self.q1) \
        + 'answer of q2 = {}\n'.format(self.q2) \
        + 'answer of q3 = {}\n'.format(self.q3) \
        + 'answer of q4 = {}\n'.format(self.q4) \
        + 'answer of q5 = {}\n'.format(self.q5) \
        + 'oRate = {}\n'.format(self.oRate)\
        + 'cRate = {}\n'.format(self.cRate)\
        + 'aRate = {}\n'.format(self.aRate)\
        + 'iRate = {}\n'.format(self.iRate)\
        + 'score = {}\n'.format(self.score)\
        + 'isUsed = {}\n'.format(self.isUsed)
    
def main():
    
    num_rules = 2
    rule_data = [
    [1, 0, 3, 3, 3, None, None, None, 'stronglyAgainstYou', 'notAtAll', -1, -1, -1, -1],\
    [2, 3, 1, 1, 1, 'yes', 'every', 'notAtAll', 'stronglyWithYou', 'notAtAll', 2, 1, 1, 2]
    ]
    
    rules = queue.PriorityQueue()
    
    currEnv = env('yes', 'every', 'notAtAll', 'stronglyAgainstYou', 'notAtAll')
    currStatus = status(0, 0, 0, 0)
    print(currStatus)
    
    
    for i in range(0,num_rules):
        curr_rule = rule(rule_data[i][0], rule_data[i][1], rule_data[i][2], \
        rule_data[i][3], rule_data[i][4], rule_data[i][5], rule_data[i][6], \
        rule_data[i][7], rule_data[i][8], rule_data[i][9], rule_data[i][10], \
        rule_data[i][11], rule_data[i][12], rule_data[i][13])
        curr_rule.computeScore(currStatus, currEnv)
        rules.put(curr_rule)

    while not rules.empty():
        curr_rule = rules.get()
        curr_rule.isUsed = True
        print('Rule {} fired now in priority queue \n'.format(curr_rule.ID))
        print(curr_rule)
        currStatus.change(curr_rule)
        print(currStatus)
        tmp_rules = queue.PriorityQueue()
        #print("Remaining Rules in priority queue \n")
        while not rules.empty():
            tmp_rule = rules.get()
            #print(tmp_rule)
            tmp_rule.computeScore(currStatus, currEnv)
            tmp_rules.put(tmp_rule)
        rules = tmp_rules
        
    return currStatus.check()
        
if __name__ == "__main__":
    isOpinionChanged = main()
    print(isOpinionChanged)


