class MembershipFunction:
    def __init__(self, name, X0, X1, X2, X3):
        self.name = name
        self.X0 = X0 * 1.0
        self.X1 = X1 * 1.0
        self.X2 = X2 * 1.0
        self.X3 = X3 * 1.0
        self.value = 0.0
        
    def centorid(self):
        a = self.X2 - self.X1;
        b = self.X3 - self.X0;
        c = self.X1 - self.X0;

        return ((2 * a * c) + (a * a) + (c * b) + (a * b) + (b * b)) / (3 * (a + b)) + self.X0
        
    def area(self):
        a = self.centorid() - self.X0
        b = self.X3 - self.X0;

        return (self.value * (b + (b - (a * self.value)))) / 2;
        
