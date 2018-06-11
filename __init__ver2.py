import sys
import queue as queue

class status:
    def __init__(self, confidence_level, attention_level, interest_level):
        self.cLevel = confidence_level
        self.aLevel = attention_level
        self.iLevel = interest_level
        
    def change(self, rule):
        self.cLevel = self.cLevel + rule.cRate
        self.aLevel = self.aLevel + rule.aRate
        self.iLevel = self.iLevel + rule.iRate
        
    def check(self):
        if self.cLevel <= 0.2 and self.aLevel >= 0.8 and self.iLevel >= 0.8:
            return True
        return False 

class rule:
    def __init__(self, rule_id, confidence_interval, attention_interval, interest_interval,\
    confidence_changeRate, attention_changeRate, interest_changeRate):
        self.ID = rule_id
        self.cInterval = confidence_interval
        self.aInterval = attention_interval
        self.iInterval = interest_interval
        self.cRate = confidence_changeRate
        self.aRate = attention_changeRate
        self.iRate = interest_changeRate
        self.primary_score = 0
        self.isUsed = False
        
    def computeScore(self, status):
        self.primary_score = 0
        cIntervalLength = self.cInterval[1] - self.cInterval[0]
        aIntervalLength = self.aInterval[1] - self.aInterval[0]
        iIntervalLength = self.iInterval[1] - self.iInterval[0] 
        cIntervalMean = self.cInterval[0] + 0.5 * cIntervalLength
        aIntervalMean = self.aInterval[0] + 0.5 * aIntervalLength
        iIntervalMean = self.iInterval[0] + 0.5 * iIntervalLength
        
        if self.cInterval[0] <= status.cLevel and status.cLevel <= self.cInterval[1]:
            self.primary_score += (status.cLevel - cIntervalMean)/cIntervalLength/20
        else:
            self.primary_score += 1
        if self.aInterval[0] <= status.aLevel and status.aLevel <= self.aInterval[1]:
            self.primary_score += (status.aLevel - aIntervalMean)/aIntervalLength/20 
        else:
            self.primary_score += 1
        if self.iInterval[0] <= status.iLevel and status.iLevel <= self.iInterval[1]:
            self.primary_score += (status.iLevel - iIntervalMean)/iIntervalLength/20
        else:
            self.primary_score += 1
    
    def __lt__(self, other):
        return (self.primary_score < other.primary_score)
           
    def __str__(self):
        return 'Rule {} \n'.format(self.ID) \
        + 'confidence interval = [{}, {}]\n'.format(self.cInterval[0], self.cInterval[1]) \
        + 'attention interval = [{}, {}]\n'.format(self.aInterval[0], self.aInterval[1]) \
        + 'interest interval = [{}, {}]\n'.format(self.iInterval[0], self.cInterval[1]) \
        + 'is already fired? = {} \n'.format(self.isUsed)


def main():
    num_rules = 3
    rule_data = [[1, [0.1, 0.3], [0.1, 0.3], [0.1, 0.3], 0.2, 0.2, 0.2], \
    [2, [0.3, 0.5], [0.3, 0.5], [0.3, 0.5], 0.2, 0.2, 0.2], \
    [3, [0.5, 0.7], [0.5, 0.7], [0.5, 0.7], 0.2, 0.2, 0.2]]
    rules = queue.PriorityQueue()
    currStatus = status(0.2, 0.2, 0.2)
    
    for i in range(0,num_rules):
        curr_rule = rule(rule_data[i][0], rule_data[i][1], rule_data[i][2], \
        rule_data[i][3], rule_data[i][4], rule_data[i][5], rule_data[i][6])
        curr_rule.computeScore(currStatus)
        rules.put(curr_rule)

    while not rules.empty():
        curr_rule = rules.get()
        curr_rule.isUsed = True
        print("Rule fired now in priority queue \n")
        print(curr_rule)
        currStatus.change(curr_rule)
        tmp_rules = queue.PriorityQueue()
        print("Remaining Rules in priority queue \n")
        while not rules.empty():
            tmp_rule = rules.get()
            print(tmp_rule)
            tmp_rule.computeScore(currStatus)
            tmp_rules.put(tmp_rule)
        rules = tmp_rules
        
        if currStatus.check():
            return True
    return False
        
if __name__ == "__main__":
    isOpinionChanged = main()
    print(isOpinionChanged)


