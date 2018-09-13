from engine import compile

if __name__ == ("__main__"):
    re = input()

    ans=compile.mknfa(re)
    ans=compile.mkdfa(ans)
    ans.polt()