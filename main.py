# -*- encoding: utf-8 -*-

from lib.fuzzy.variable import Variable
from lib.fuzzy.fuzzyengine import FuzzyEngine
from lib.fuzzy.fuzzyrule import FuzzyRule
from lib.fuzzy.membershipfunction import MembershipFunction

request = Variable("Request")
request.membershipFunctions["Low"] = MembershipFunction("Low", 0, 0, 25, 50)
request.membershipFunctions["Middle"] = MembershipFunction("Middle", 20, 40, 75, 100)
request.membershipFunctions["High"] = MembershipFunction("Hot", 75, 100, 150, 1000)

degree = Variable("Degree")
degree.membershipFunctions["Low"] = MembershipFunction("Low", 0, 0, 5, 25)
degree.membershipFunctions["Middle"] = MembershipFunction("Middle", 25, 45, 55, 75)
degree.membershipFunctions["High"] = MembershipFunction("High", 75, 95, 100, 100)

fe = FuzzyEngine()
fe.variables["Request"] = request
fe.variables["Degree"] = degree

fe.calculatedVariable = degree

fe.fuzzyRules.append(FuzzyRule("IF (Request IS Low) THEN Degree IS Low"))
fe.fuzzyRules.append(FuzzyRule("IF (Request IS Middle) THEN Degree IS Middle"))
fe.fuzzyRules.append(FuzzyRule("IF (Request IS High) THEN Degree IS High"))

request.inputValue = 1.38129512476

print fe.defuzzify()
