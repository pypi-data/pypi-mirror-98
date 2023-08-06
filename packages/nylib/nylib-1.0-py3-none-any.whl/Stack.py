from logging import exception


class Stack():
    def __init__(self, size):
        self.size = size
        self.stack = []
        self.top = -1

    def push(self, ele):  # 入栈之前检查栈是否已满
        if self.isfull():
            raise exception("out of range")
        else:
            self.stack.append(ele)
            self.top = self.top + 1

    def pop(self):  # 出栈之前检查栈是否为空
        if self.isempty():
            raise exception("stack is empty")
        else:
            self.top = self.top - 1
            return self.stack.pop()

    def isfull(self):
        return self.top + 1 == self.size

    def isempty(self):
        return self.top == -1
