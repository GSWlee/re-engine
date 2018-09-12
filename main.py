from engine import nfamake

if __name__ == ("__main__"):
    re = input()
    ans = list(re)
    x = nfamake.nfapic(ans[0])
    for i in ans[1:]:
        if i is '*':
            x.caseone()
        elif i is '+':
            x.addnfa()
            x.caseone()
        else:
            x.getnextcahr(i)

    x.plot()
