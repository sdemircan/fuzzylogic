class FuzzyRule:
    def __init__(self, text):
        self.text = self.validate(text)
        self.value = 0
		
    def validate(self, text):
	count = 0
	position = text.find("(")
	tokens = text.replace("(", "").replace(")", "").split();
	
	while(position >= 0):
            count+=1
	    position = text.find("(", position + 1)
	
	position = text.find(")")
	
	while(position >= 0):
            count-=1
	    position = text.find(")", position + 1)
			
        if count > 0:
            raise Exception("missing right parenthesis: " + text)
	elif count < 0:
	    raise Exception("missing left parenthesis: " + text)
		
	if tokens[0] != "IF":
	    raise Exception("'IF' not found: " + text)
	if tokens[-4] != "THEN":
	    raise Exception("'THEN' not found: " + text)
	if tokens[-2] != "IS":
	    raise Exception("'IS' not found: " + text)
		
	for i in range(2, len(tokens) -5, 2):
	    if (tokens[i] != "IS") and (tokens[i] != "AND") and (tokens[i] != "OR"):
	        raise Exception("Syntax error: " + tokens[i])
					
	return text
		

	
	
    def contidions(self):
        return self.text[self.text.find("IF ") + 3: (self.text.find("IF ") + 3) + self.text.find(" THEN") -3]
    
