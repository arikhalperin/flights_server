class A:
    def __init__(self,a,b):
        self.a = a
        self.b = b

    def print_yourself(self):
        print(f"a={self.a} b={self.b}")



a = A(5,10)
b = A(6,8)

a.print_yourself()
b.print_yourself()