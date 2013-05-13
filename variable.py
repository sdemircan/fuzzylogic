class Variable:
    def __init__(self, name):
        self.name = name
        self.membershipFunctions = {}
        self.inputValue = 0;

    def fuzzify(self, membershipFunctionName):
        membershipFunction = self.membershipFunctions[membershipFunctionName]

        if ((membershipFunction.X0 <= self.inputValue) and (self.inputValue < membershipFunction.X1)):
            return (self.inputValue - membershipFunction.X0) / (membershipFunction.X1 - membershipFunction.X0)
        elif ((membershipFunction.X1 <= self.inputValue) and (self.inputValue <= membershipFunction.X2)):
            return 1;
        elif ((membershipFunction.X2 < self.inputValue) and (self.inputValue <= membershipFunction.X3)):
            return (membershipFunction.X3 - self.inputValue) / (membershipFunction.X3 - membershipFunction.X2)
        else:
            return 0;

    def minValue(self):
        minValue = self.membershipFunctions.values()[0].X0

        for membershipFunction in self.self.membershipFunctions.value():
            if membershipFunction.X0 < minValue:
                minValue = membershipFunction.X0

        return minValue
    
    def maxValue(self):
        maxValue = self.membershipFunctions.values()[0].X3

        for membershipFunction in self.self.membershipFunctions.value():
            if membershipFunction.X0 > maxValue:
                maxValue = membershipFunction.X0

        return maxValue

    def range(self):
        return self.maxValue() - self.minValue()
