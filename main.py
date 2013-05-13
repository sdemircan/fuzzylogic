from variable import Variable
from fuzzyengine import FuzzyEngine
from fuzzyrule import FuzzyRule
from membershipfunction import MembershipFunction

water = Variable("water")
water.membershipFunctions["Cold"] = MembershipFunction("Cold", 0, 0, 20, 40)
water.membershipFunctions["Tepid"] = MembershipFunction("Tepid", 30, 50, 50, 70)
water.membershipFunctions["Hot"] = MembershipFunction("Hot", 50, 80, 100, 100)

power = Variable("Power")
power.membershipFunctions["Low"] = MembershipFunction("Low", 0, 25, 25, 50)
power.membershipFunctions["High"] = MembershipFunction("High", 25, 50, 50, 75)
fe = FuzzyEngine()
fe.variables["Water"] = water
fe.variables["Power"] = power

fe.calculatedVariable = power

fe.fuzzyRules.append(FuzzyRule("IF (Water IS Cold) OR (Water IS Tepid) THEN Power IS High"))
fe.fuzzyRules.append(FuzzyRule("IF (Water IS Hot) THEN Power IS Low"))

water.inputValue = 60

print fe.defuzzify()


