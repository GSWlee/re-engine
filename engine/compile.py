from engine import nfamake
from engine import dfa
import copy
constchar = ('*', '+', '[', ']', '?', '\\', '.', '|', '(', ')')

# 将re变为后缀表达式,并逆序.方便后续处理.
def makePolishNotation(re):
    ans = list(re)
    charstack = list()
    operatorstack = list()
    while ans:
        if ans[0] not in constchar:
            charstack.append(ans[0])
            ans = ans[1:]
        else:
            if ans[0] in ('*', '+', '?', '.'):
                charstack.append(ans[0])
                ans = ans[1:]
            elif ans[0] == '[':
                e = ans.index(']')
                temp = ans[1:e]
                charstack.append("".join(temp))
                ans = ans[e + 1:]
            elif ans[0] == '\\':
                charstack.append(ans[0])
                charstack.append(ans[1])
                ans = ans[2:]
            elif ans[0] == '(':
                operatorstack.append(ans[0])
                ans = ans[1:]

            elif ans[0] == ')':
                while operatorstack:
                    if operatorstack[-1] is not '(':
                        charstack.append(operatorstack.pop())
                    else:
                        break
                operatorstack.pop()
                ans = ans[1:]
            else:
                if len(operatorstack) == 0 or operatorstack[-1] == '(':
                    operatorstack.append(ans[0])
                else:
                    charstack.append(ans[0])
                ans = ans[1:]
    while operatorstack:
        charstack.append(operatorstack.pop())

    charstack.reverse()

    return charstack

#将输入的正则表达式变为nfa
def mknfa(re):
    charstack = makePolishNotation(re)
    nfastack = list()
    while charstack:
        x = charstack.pop()
        if x not in constchar:
            x = nfamake.nfapic(x)
            nfastack.append(x)
        elif x is '*':
            temp = nfastack.pop()
            temp.caseone()
            nfastack.append(temp)
        elif x is '.':
            temp = nfastack.pop()
            temp.getnextcahr("any")
            nfastack.append(temp)
        elif x is '+':
            temp1 = nfastack.pop()
            temp2 = copy.deepcopy(temp1)
            temp1.caseone()
            temp2.addnfa(temp1)
            nfastack.append(temp2)
        elif x is '?':
            temp = nfastack.pop()
            temp.casetwo()
            nfastack.append(temp)
        elif x is '\\':
            x = charstack.pop()
            temp = nfastack.pop()
            temp.getnextcahr(x)
            nfastack.append(temp)
        else:
            temp1 = nfastack.pop()
            temp2 = nfastack.pop()
            temp2.casethree(temp1)
            nfastack.append(temp2)
    ans = nfastack[0]
    nfastack = nfastack[1:]
    while nfastack:
        ans.addnfa(nfastack[0])
        nfastack = nfastack[1:]

    return ans

#将输入的nfa变为dfa
def mkdfa(nfa):
    n=dfa.dfapic()
    n.dfatonfa(nfa)
    #n.makesimple()
    return n
