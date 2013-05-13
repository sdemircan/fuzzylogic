class FuzzyEngine:
    def __init__(self):
        self.variables = {}
        self.calculatedVariable = None
        self.fuzzyRules = []

    def evaluate(self, text):
        tokens = text.split()
        connective = ""
        value = 0
        for i in range(0, len(tokens) / 2 + 2, 2):
            tokenValue = float(tokens[i])
            if connective == "AND":
                if (tokenValue < value):
                    value = tokenValue
            elif connective == "OR":
                if (tokenValue > value):
                    value = tokenValue
            else:
                value = tokenValue;
                
            if ((i + 1) < len(tokens)):
                connective = tokens[i + 1]
        
        return value;
    
    def parse(self, text):
        counter = 0;
        firstMatch = 0;
        if not text.startswith("("):
            tokens = text.split();
            return self.variables[tokens[0]].fuzzify(tokens[2]);

        l = len(text)
        i = 0
        while i < l:
            if text[i] == '(':
                counter += 1
                if counter == 1:
                    firstMatch = i
            elif text[i] == ')':
                counter -= 1
                if (counter == 0) and (i > 0):
                    substring = text[firstMatch + 1:(firstMatch + 1) + i - firstMatch - 1]
                    substringBrackets = text[firstMatch:(firstMatch) + i - firstMatch + 1]
                    length = len(substringBrackets)
                    text = text.replace(substringBrackets, str(self.parse(substring)));
                    l = len(text)
                    i = i - (length - 1)
            i += 1
        return self.evaluate(text)
    
    def defuzzify(self):

        numerator = 0
        denominator = 0
        
        #Reset values.
        for membershipFunction in self.calculatedVariable.membershipFunctions.values():
            membershipFunction.value = 0

        for fuzzyRule in self.fuzzyRules:
            fuzzyRule.value = self.parse(fuzzyRule.contidions())
            
            tokens = fuzzyRule.text.split()
            membershipFunction = self.calculatedVariable.membershipFunctions[tokens[-1]]

            if fuzzyRule.value > membershipFunction.value:
                membershipFunction.value = fuzzyRule.value
                
        
        for membershipFunction in self.calculatedVariable.membershipFunctions.values():
            numerator += membershipFunction.centorid() * membershipFunction.area()
            denominator += membershipFunction.area()

        
        return numerator / denominator;
            
