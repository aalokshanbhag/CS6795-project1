import sys
import queue as queue
import pandas as pd

class status:
    '''
    This calss is for a person's state
    '''
    def __init__(self, confidence_level, attention_level, interest_level, opinion):
        self.opinion = opinion         # totallyDisagree(-2), disagree(-1), neutral(0), agree(+1), totallyAgree(+2)
        self.initOpinion  = opinion    # totallyDisagree(-2), disagree(-1), neutral(0), agree(+1), totallyAgree(+2)
        self.cLevel = confidence_level # low(0), mid(1), high(2)
        self.aLevel = attention_level  # low(0), mid(1), high(2)
        self.iLevel = interest_level   # low(0), mid(1), high(2)
        
    def change(self, rule):
        if rule.oRate != None:
            self.opinion = self.opinion + rule.oRate
            if self.opinion > 2:
                self.opinion = 2
            if self.opinion < -2:
                self.opinion = -2
        if rule.cRate != None:
            self.cLevel = self.cLevel + rule.cRate
            if self.cLevel > 2:
                self.cLevel = 2
            if self.cLevel < 0:
                self.cLevel = 0
        if rule.aRate != None:
            self.aLevel = self.aLevel + rule.aRate
            if self.aLevel > 2:
                self.aLevel = 2
            if self.aLevel < 0:
                self.aLevel = 0
        if rule.iRate != None:
            self.iLevel = self.iLevel + rule.iRate
            if self.iLevel > 2:
                self.iLevel = 2
            if self.iLevel < 0:
                self.iLevel = 0
        
    def check(self):
        if (self.opinion >= 0 and self.initOpinion < 0) or \
        (self.opinion <= 0 and self.initOpinion > 0) or \
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
    '''
    This class is for an enviroment which represents quality of comments and majority opinion
    '''
    def __init__(self, q1, q2, q3, q4, q5):
        self.q1 = q1 #q1. Does the article have a bias? (yes, no, cantSay)
        self.q2 = q2 #q2. Which comments did you read? (all, sortedByLikes, sampledBothSidesOfArgument, unsorted, never)
        self.q3 = q3 #q3. Are the comments offensive? (notAtAll, little, neutral, quite, very)
        self.q4 = q4 #q4. Which way is the comment section leaning (stronglyAgainstYou, againstYou, neutral, withYou, stronglyWithYou)
        self.q5 = q5 #q5. Are the comments well reasoned ? (notAtAll, little, neutral, quite, very)

class rule:
    '''
    This class if for a rule. Each rules has different condtions.
    '''
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
        self.numCond = 0
        if opinion != None: self.numCond += 1
        if confidence_level != None: self.numCond += 1
        if attention_level != None: self.numCond += 1
        if interest_level != None: self.numCond += 1
        if q1 != None: self.numCond += 1
        if q2 != None: self.numCond += 1
        if q3 != None: self.numCond += 1
        if q4 != None: self.numCond += 1
        if q5 != None: self.numCond += 1
        
    def computeScore(self, status, env):
        '''
        Compute how many conditions are statisfied based on "state" and "environment"
        '''
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
    '''
    Note:
        This is the main function to be run
    '''
    num_rules = 95
    rule_data = pd.read_excel(r'Rules.xlsx', sheetname='Final')
    #rule_data = pd.read_excel(r'C:\Users\kamet\Dropbox (GaTech)\Summer 2018\CS 6795\Project1\CS6795-project1\Rules.xlsx', sheetname='Final')
    rule_data = rule_data.where((pd.notnull(rule_data)), None)
    rule_data = rule_data.as_matrix()
    
    rules = queue.PriorityQueue()
    
    q1 = input('q1. Does the article have a bias? (yes, no, cantSay) : ')
    q2 = input('q2. Which comments did you read? (all, sortedByLikes, sampledBothSidesOfArgument, unsorted, never) : ')
    q3 = input('q3. Are the comments offensive? (notAtAll, little, neutral, quite, very) : ')
    q4 = input('q4. Which way is the comment section leaning (stronglyAgainstYou, againstYou, neutral, withYou, stronglyWithYou) : ')
    q5 = input('q5. Are the comments well reasoned ? (notAtAll, little, neutral, quite, very) : ')
    #currEnv = env('no', 'all', 'notAtAll', 'stronglyAgainstYou', 'very')
    currEnv = env(q1, q2, q3, q4, q5)
    
    opinion = input('q6. input opinion : ')
    confidence_level = input('q7. input confidence_level : ')
    attention_level = input('q8. input attention_level : ')
    interest_level = input('q9. input interest_level : ')
    currStatus = status(int(confidence_level), int(attention_level), int(interest_level), int(opinion))
    
    for i in range(0,num_rules):
        '''
        Construc a set of rules
        '''
        curr_rule = rule(rule_data[i][0], rule_data[i][1], rule_data[i][2], \
        rule_data[i][3], rule_data[i][4], rule_data[i][5], rule_data[i][6], \
        rule_data[i][7], rule_data[i][8], rule_data[i][9], rule_data[i][10], \
        rule_data[i][11], rule_data[i][12], rule_data[i][13])
        curr_rule.computeScore(currStatus, currEnv)
        rules.put(curr_rule)

    while not rules.empty():
        '''
        Iterate until there is no rule whose conditions are satisfied by the current state and environment
        '''
        curr_rule = rules.get()
        if curr_rule.score != curr_rule.numCond:
            break
        curr_rule.isUsed = True
        print('Rule {} fired now in priority queue'.format(curr_rule.ID))
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
    
def runCase(rule_data, num_rules, currEnv, currStatus, debug):
    '''
    Input :
        rule_data = info of rules
        num_rules = total number of rules in rule_data
        currEnv = current environment 
        currStatus = current state of a person 
        debug = True is for debug mode
    Output:
        return "Opinion Changed!" or "Stick to the original opinion..." based on whether a person changes his or her opinion
    Note:
        This function is for runCases() to test large number of cases.
    '''
    rules = queue.PriorityQueue()
    
    for i in range(0,num_rules):
        curr_rule = rule(rule_data[i][0], rule_data[i][1], rule_data[i][2], \
        rule_data[i][3], rule_data[i][4], rule_data[i][5], rule_data[i][6], \
        rule_data[i][7], rule_data[i][8], rule_data[i][9], rule_data[i][10], \
        rule_data[i][11], rule_data[i][12], rule_data[i][13])
        curr_rule.computeScore(currStatus, currEnv)
        rules.put(curr_rule)

    while not rules.empty():
        curr_rule = rules.get()
        if curr_rule.score != curr_rule.numCond:
            break
        curr_rule.isUsed = True
        currStatus.change(curr_rule)
        tmp_rules = queue.PriorityQueue()
        while not rules.empty():
            tmp_rule = rules.get()
            tmp_rule.computeScore(currStatus, currEnv)
            tmp_rules.put(tmp_rule)
        rules = tmp_rules
    return currStatus.check()
    
def runCases():
    '''
    All answer options for each question is listed as follows
    q1 = ['yes', 'no', 'cantSay']
    q2 = ['all', 'sortedByLikes', 'sampledBothSidesOfArgument', 'unsorted', 'never']
    q3 = ['notAtAll', 'little', 'neutral', 'quite', 'very']
    q4 = ['stronglyAgainstYou', 'againstYou', 'neutral', 'withYou', 'stronglyWithYou']
    q5 = ['notAtAll', 'little', 'neutral', 'quite', 'very']
    
    but, based on our rules, people change their opinion only when 
    q1 = ['no']
    q3 = ['notAtAll']
    q4 = ['againstYou','stronglyAgainstYou']
    q5 = ['very']
    Thus, these values for each variables are focused in the discussion
    
    This is the function to test a large number of cases.
    Output:
        return tuple of results which store environment and state data (before and after) of case where a person changes his or her opinion
    '''
    debug = True
    
    q1 = ['no']
    q2 = ['all', 'sampledBothSidesOfArgument']
    q3 = ['notAtAll']
    q4 = ['againstYou','stronglyAgainstYou']
    q5 = ['very']
    
    num_rules = 95
    rule_data = pd.read_excel(r'Rules.xlsx', sheetname='Final')
    #rule_data = pd.read_excel(r'C:\Users\kamet\Dropbox (GaTech)\Summer 2018\CS 6795\Project1\CS6795-project1\Rules.xlsx', sheetname='Final')
    rule_data = rule_data.where((pd.notnull(rule_data)), None)
    rule_data = rule_data.as_matrix()
    
    case_num = 0
    change_case_num = 0
    result_before = []
    result_after = []
    for opinion in range(-2,3):
        for confidence_level in range(0,3):
            for attention_level in range (0,3):
                for interest_level in range (0,3):
                    for q1_answer in q1:
                        for q2_answer in q2:
                            for q3_answer in q3:
                                for q4_answer in q4:
                                    for q5_answer in q5:
                                        initEnv = env(q1_answer, q2_answer, q3_answer, q4_answer, q5_answer)
                                        currEnv = env(q1_answer, q2_answer, q3_answer, q4_answer, q5_answer)
                                        initStatus = status(confidence_level, attention_level, interest_level, opinion)
                                        currStatus = status(confidence_level, attention_level, interest_level, opinion)
                                        if runCase(rule_data, num_rules, currEnv, currStatus, debug) == "Opinion Changed!":
                                            print('case_num = {}, condition = {} {} {} {} {} {} {} {} {}'.format(case_num, opinion, confidence_level, attention_level, interest_level, q1_answer,q2_answer,q3_answer,q4_answer,q5_answer))
                                            change_case_num += 1
                                            result_before.append([initEnv, initStatus])
                                            result_after.append([currEnv, currStatus])
                                        case_num += 1
    print('total # of cases = {}, cases when a person changes an opinion = {}'.format(case_num, change_case_num))                
    return (result_before, result_after) 
    
def sort(result, sortType, beforeAfter):
    '''
    This function is used to show the data sorted by 
    Input:
        result = result from runCases()
        sortType = "opinion" or "confidence_level" or "attention_level" or "interest_level" based on which result you care about
        beforeAfter = "before" or "after" based on which result you care about
    '''
    if beforeAfter == 'before':
        currResult = result[0]
    else:
        currResult = result[1]
    
    lowCount, midCount, highCount = 0, 0, 0
    strDisagrCount, disagrCount, neutralCount, agrCount, strAgrCount =0, 0, 0, 0, 0
    if sortType == 'confidence_level':
        for res in currResult:
            #print(res[1])
            if res[1].cLevel == 0:
                lowCount += 1
            elif res[1].cLevel == 1:
                midCount += 1
            elif res[1].cLevel == 2:
                highCount += 1
        print('Summary\n lowCount = {}, midCount = {}, highCount = {}'.format(lowCount, midCount, highCount))
    if sortType == 'attention_level':
        for res in currResult:
            if res[1].aLevel == 0:
                lowCount += 1
            elif res[1].aLevel == 1:
                midCount += 1
            elif res[1].aLevel == 2:
                highCount += 1
        print('Summary\n lowCount = {}, midCount = {}, highCount = {}'.format(lowCount, midCount, highCount))
    if sortType == 'interest_level':
        for res in currResult:
            if res[1].iLevel == 0:
                lowCount += 1
            elif res[1].iLevel == 1:
                midCount += 1
            elif res[1].iLevel == 2:
                highCount += 1
        print('Summary\n lowCount = {}, midCount = {}, highCount = {}'.format(lowCount, midCount, highCount))
    if sortType == 'opinion':
        for res in currResult:
            if res[1].opinion == -2:
                strDisagrCount +=1
            elif res[1].opinion == -1:
                disagrCount +=1
            elif res[1].opinion == 0:
                neutralCount +=1
            elif res[1].opinion == 1:
                agrCount +=1
            elif res[1].opinion == 2:
                strAgrCount +=1
        print('Summary\n strDisagrCount = {}, disagrCount = {}, neutralCount = {}, agrCount = {}, strAgrCount = {}'.format(strDisagrCount, disagrCount, neutralCount, agrCount, strAgrCount))      
              
        
if __name__ == "__main__":
    isOpinionChanged = main()
    print(isOpinionChanged)
    # If you want to run all the cases I used in the report take out the comment-out sign below 
    #result = runCases()  


