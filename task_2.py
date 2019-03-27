import argparse
import re

class Conversion:

    # Constructor to initialize the class variables
    def __init__(self, capacity):
        self.top = -1
        self.capacity = capacity
        # This array is used a stack
        self.array = []
        # Precedence setting
        self.output = []
        self.precedence = {'+':1, '-':1, '*':2, '/':2, '^':3}

    # check if the stack is empty
    def isEmpty(self):
        return True if self.top == -1 else False

    # Return the value of the top of the stack
    def peek(self):
        return self.array[-1]

    # Pop the element from the stack
    def pop(self):
        if not self.isEmpty():
            self.top -= 1
            return self.array.pop()
        else:
            return "$"

    # Push the element to the stack
    def push(self, op):
        self.top += 1
        self.array.append(op)

    # A utility function to check is the given character
    # is operand
    def isOperand(self, ch):
        return ch.isalnum()

    # Check if the precedence of operator is strictly
    # less than top of stack or not
    def notGreater(self, i):
        try:
            a = self.precedence[i]
            b = self.precedence[self.peek()]
            return True if a  <= b else False
        except KeyError:
            return False

    # The main function that converts given infix expression
    # to postfix expression
    def infixToPostfix(self, exp):

        # Iterate over the expression for conversion
        for i in exp:
            # If the character is an operand,
            # add it to output
            if self.isOperand(i) or  i=="+" or i=="?" or i == "*" or i==" " :
                self.output.append(i)

            # If the character is an '(', push it to stack
            elif i  == '(':
                self.push(i)

            # If the scanned character is an ')', pop and
            # output from the stack until and '(' is found
            elif i == ')':
                while( (not self.isEmpty()) and self.peek() != '('):
                    a = self.pop()
                    self.output.append(a)

                if (not self.isEmpty() and self.peek() != '('):
                    return -1
                else:
                    self.pop()

            # An operator is encountered
            else:
                while(not self.isEmpty() and self.notGreater(i)):
                    self.output.append(self.pop())

                self.push(i)

        # pop all the operator from the stack
        while not self.isEmpty():

            self.output.append(self.pop())



        #print ("".join(self.output))
        return  self.output
        #return "" .join(self.output)

class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?",
                        metavar="file")

    args = parser.parse_args()

    print(args.file)

    output_file = open("task_2_result.txt","w+")


def preProcessRegex(regex):
    newRegex = ""
    for i in range(len(regex)-1):
        #if( not regex[i] == "(" and not regex[i] == "|" and regex[i+1].isalnum()):
        #print(regex[i].isalnum())
        if ( (regex[i].isalnum() and regex[i+1].isalnum()) or (regex[i].isalnum() and regex[i+1]=="(" ) or (regex[i]==")" and regex[i+1]==" ") or ( regex[i] == ")"
            and regex[i+1].isalnum()) or (regex[i] == ")" and regex[i+1]=="(") or ((regex[i]=="*" or regex[i]=="+") and (regex[i+1] == "(" or regex[i+1].isalnum())) or
                (regex[i]==" " and regex[i+1]==" ") or(regex[i]==" " and regex[i+1].isalnum()) or (regex[i].isalnum() and regex[i+1]==" ") or
        (regex[i]==" " and regex[i+1]=="(")):
            newRegex = newRegex + regex[i] + "^"
        else:
            newRegex = newRegex + regex[i]

    return newRegex+regex[len(regex)-1]


class State :
    def __init__(self,name):
        self.name = name
        self.ec = []
        self. transitions = dict()
        self.isAcceptState = False


class NFA :
    def __init__(self):
        self.states = []
        self.startState = None
        self.acceptState = None
        self.alphabet = None
        #self.Alphabet = alphabet

def addCommas(currentstring , stringToBeAdded):
    i = 0

    while(i<len(stringToBeAdded)-1):
        currentstring = currentstring + stringToBeAdded[i] + ","
        i=i+1
    currentstring = currentstring + stringToBeAdded[i] + "\n"
    return  currentstring


def convertToNFA(regex):
    regex = preProcessRegex(regex)
    regex = Conversion(len(regex)).infixToPostfix(regex)
    #print(regex)
    counter = 0
    stack = Stack()
    for character in regex:
        if(character.isalnum()):
            state1 = State("s" + str(counter))
            state2 = State("s"+ str(counter+1))
            state1.transitions.update({character: state2})
            state2.isAcceptState = True
            currentNFA = NFA()
            currentNFA.startState = state1
            currentNFA.acceptState = state2
            currentNFA.states.append(state1)
            currentNFA.states.append(state2)
            stack.push(currentNFA)
            counter = counter +2
        if(character==" "):
            #print("epsilon is encountered")
            state1 = State("s" + str(counter))
            state2 = State("s"+ str(counter+1))
            state1.ec.append(state2)
            state2.isAcceptState = True
            currentNFA = NFA()
            currentNFA.startState = state1
            currentNFA.acceptState = state2
            currentNFA.states.append(state1)
            currentNFA.states.append(state2)
            stack.push(currentNFA)
            counter = counter +2
        if(character == "^"):
            NFA2 = stack.pop()
            NFA1 = stack.pop()
            newNFA = NFA()
            newMidState = State("newMiddlestate" + str(counter))
            counter +=1
            newNFA.startState = NFA1.startState
            newNFA.acceptState = NFA2.acceptState
            state1 = NFA1.acceptState
            state2 = NFA2.startState
            #state1.isAcceptState = False
            NFA1.acceptState = newMidState
            NFA2.startState = newMidState
            state1.name = newMidState.name
            state2.name = newMidState.name
            newMidState.transitions.update(state1.transitions)
            newMidState.transitions.update(state2.transitions)
            newMidState.ec = newMidState.ec + state1.ec + state2.ec
            #print(newMidState.ec)
            #newMidState.transitions = NFA1.acceptState.transitions
            #newMidState.transitions.update(NFA2.startState.transitions)
            for i in NFA1.states:
                if((not i==state1)and(not i in newNFA.states)):
                    newNFA.states.append(i)
            newNFA.states.append(newMidState)
            for i in NFA2.states:
                if((not i==state2)and(not i in newNFA.states)):
                    newNFA.states.append(i)
            stack.push(newNFA)
        if(character=="|"):
            NFA2 = stack.pop()
            NFA1 = stack.pop()
            newNFA = NFA()
            newStartState = State("newStartState" + str(counter))
            counter+=1
            newStartState.ec.append(NFA1.startState)
            newStartState.ec.append(NFA2.startState)
            newNFA.startState = newStartState
            newNFA.states.append(newStartState)
            for i in NFA1.states:
                if(not i in newNFA.states):
                    newNFA.states.append(i)
            for i in NFA2.states:
                if(not i in newNFA.states):
                    newNFA.states.append(i)
            newEndState = State("newEndState" + str(counter))
            counter+=1
            newEndState.isAcceptState = True
            #NFA1.acceptState.isAcceptState = False
            #NFA2.acceptState.isAcceptState = False
            NFA1.acceptState.ec.append(newEndState)
            NFA2.acceptState.ec.append(newEndState)
            newNFA.states.append(newEndState)
            newNFA.acceptState = newEndState
            stack.push(newNFA)
        if(character=="*"):
            NFA1 = stack.pop()
            newNFA = NFA()
            newStartState = State("newStartState" + str(counter))
            counter+=1
            newEndState = State("newEndState"+str(counter))
            counter+=1
            newStartState.ec.append(newEndState)
            newStartState.ec.append(NFA1.startState)
            newNFA.startState = newStartState
            newNFA.acceptState = newEndState
            newEndState.isAcceptState= True
            newNFA.states.append(newStartState)
            NFA1.acceptState.ec.append(newEndState)
            NFA1.acceptState.ec.append(NFA1.startState)
            NFA1.acceptState.isAcceptState = False
            for i in NFA1.states:
                if(not i in newNFA.states):
                    newNFA.states.append(i)
            newNFA.states.append(newEndState)
            stack.push(newNFA)
        if(character=="+"):
            NFA1 = stack.pop()
            newNFA = NFA()
            newStartState = State("newStartState" + str(counter))
            counter+=1
            newEndState = State("newEndState"+str(counter))
            counter+=1
            newStartState.ec.append(NFA1.startState)
            newNFA.startState = newStartState
            newNFA.acceptState = newEndState
            newEndState.isAcceptState= True
            newNFA.states.append(newStartState)
            NFA1.acceptState.ec.append(newEndState)
            NFA1.acceptState.ec.append(NFA1.startState)
            NFA1.acceptState.isAcceptState = False
            for i in NFA1.states:
                if(not i in newNFA.states):
                    newNFA.states.append(i)
            newNFA.states.append(newEndState)
            stack.push(newNFA)
        if(character=="?"):
            NFA1 = stack.pop()
            newNFA = NFA()
            newStartState = State("newStartState" + str(counter))
            counter+=1
            newEndState = State("newEndState"+str(counter))
            counter+=1
            newStartState.ec.append(newEndState)
            newStartState.ec.append(NFA1.startState)
            newNFA.startState = newStartState
            newNFA.acceptState = newEndState
            newEndState.isAcceptState= True
            newNFA.states.append(newStartState)
            NFA1.acceptState.ec.append(newEndState)
            NFA1.acceptState.isAcceptState = False
            for i in NFA1.states:
                if(not i in newNFA.states):
                    newNFA.states.append(i)
            newNFA.states.append(newEndState)
            stack.push(newNFA)



    while not(stack.isEmpty()):
        x = stack.pop()
        states = x.states
        startStateName = x.startState.name
        endStateName = x.acceptState.name
        dict = {}
        ec = []
        alphabet = []
        stateTransitions = []
        ij = 0
        field= ""
        transits = ""
        while (ij<len(states)-1):
            field= field + states[ij].name + ","
            ij+=1
        field = field + states[ij].name + "\n"
        for i in x.states:
            #print(i.name)
            #print(i.name)
          #print(" Number of States :" + str(len(x.states)) )
            #states.append(i.name)
            dict = i.transitions
            ec = i.ec
            for j in dict:
                #print ("From State :" + i.name +  " using :" +j + " to State " + dict[j].name)
                #transits = transits + "("+ i.name + "," + j + ", ["+ dict[j].name+"]" + ")" + ","
                transits = "("+ i.name + "," + j + ", ["+ dict[j].name+"]" + ")"
                stateTransitions.append(transits)
                if(j not in alphabet):
                    alphabet.append(j)
                #print (dict[j].ec)
                #for z in dict[j].ec:
                   #print ("From State :" + i.name +  " using :" " epsilon " + " to State " + z.name)
            for m in ec:
                a = 0
                if(a<len(ec)-1):
                    #transits = transits + "("+ i.name + "," + " " + ",["+ m.name + "]" + ")" + ","
                    transits =  "("+ i.name + "," + " " + ",["+ m.name + "]" + ")"
                    #print ("From State :" + i.name +  " using :" " epsilon " + " to State " + m.name)
                    stateTransitions.append(transits)
                    a+=1
                else:
                    #transits = transits + "("+ i.name + "," + " " + ",["+ m.name + "]" + ")"
                    transits =  "("+ i.name + "," + " " + ",["+ m.name + "]" + ")"
                    stateTransitions.append(transits)



                if(" " not in alphabet):
                   alphabet.append(" ")




        field = addCommas(field,alphabet)
        field =  field + startStateName + "\n"
        field = field + endStateName + "\n"
        #field = field + transits
        l = 0
        while l<len(stateTransitions)-1:
            field = field + stateTransitions[l] + ","
            l+=1
        field = field + stateTransitions[l]
        #print(field)
        #print(alphabet)
        return  field

        #output_file.write(field)






with open(args.file,"r")as file :
   field = ""
   for line in file:
        field = convertToNFA(line)
        output_file.write(field + "\n")



#exp = "a+b*(c^d-e)^(f+g*h)-i"
#exp2 ="a+b+c"
#obj = Conversion(len(exp2)).infixToPostfix(exp2)
#print(obj)

#output = preProcessRegex("a(ba)(babab*)+")
#output2 = Conversion(100).infixToPostfix("(a|b)|c")
#output= Conversion(100).infixToPostfix("a+b*")
#print(output2)
#s = convertToNFA("1|(01)")
#for state in s:
   #print(state.name)










