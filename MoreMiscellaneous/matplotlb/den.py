"""
score = (60-(a+b+c+d+e))*F + a*ps1 + b*ps2 + c*ps3 + d*ps4 + e*ps5

Objective:
    Given values for F, psl, ps2, PS3, ps4, ps5
    Find values for a, b, c, d, e that maximize score
Constraints:
a, b, c, d, e are each 10 or 0
a + b + c + d + e >= 20


"""



def score_cal(F, pss:list, coof:list) -> int:
    return (60-(sum(coof)))*F + coof[0]*pss[0] + coof[1]*pss[1] + coof[2]*pss[2] + coof[3]*pss[3] + coof[4]*pss[4]



def process(F:int, ps:list):
    sorted_indices = sorted(range(len(ps)), key=lambda i: ps[i])
    
    coofs = [0, 0, 0, 0, 0]
    coofs[sorted_indices[-1]] = 10
    coofs[sorted_indices[-2]] = 10
    i = -3
    val = score_cal(F, ps, coofs)
    for _ in range(2):
        coofs[sorted_indices[i]] = 10
        next_val = score_cal(F, ps, coofs)
        if next_val>val:
            val=next_val
            i -= 1
        else:
            break
    return (val, coofs)

def f(F:int, ps:list):
    score = process(F, ps)
    print(f"Max Score of: (60 - (a + b + c + d + e))*{F} + a*{ps[0]} + b*{ps[1]} + c*{ps[2]} + d*{ps[3]} + e*{ps[4]}")
    print(f"a: {score[1][0]}, b: {score[1][1]}, c: {score[1][2]}, d: {score[1][3]}, e: {score[1][4]}")
    print(f"{score[0]} = (60 - ({score[1][0]} + {score[1][1]} + {score[1][2]} + {score[1][3]} + {score[1][4]}))*{F} + {score[1][0]}*{ps[0]} + {score[1][1]}*{ps[1]} + {score[1][2]}*{ps[2]} + {score[1][3]}*{ps[3]} + {score[1][4]}*{ps[4]}")

