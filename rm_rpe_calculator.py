# O'Conner >> 반복 횟수가 높을 수록 정확
def estimate_1rm_oconner(weight, reps):
  return weight * (1 + reps / 40)

def convert_oc_1rm_to_nrm(orm, n):
    return orm/(1+n/40)

# 맷브리키 >> 반복 횟수 낮을 떄 정확
def estimate_1rm_matt(weight, reps):
  return weight * 36 / (37 - reps)


def convert_matt_1rm_to_nrm(orm, n):
    return orm * (37 - n) / 36

def convert_orm_to_reps_rpe(orm, reps, rpe):
    # ex) rpe 8이면 n+2 reps max 를 측정한다
    return convert_matt_1rm_to_nrm(orm, reps + (10-rpe))



# 예시
weight = 130 # 100kg으로 들 수 있는 중량
reps = 3 # 5회 반복 가능

# 5회 이하는 matt, 이상은 o'conner
orm = estimate_1rm_matt(weight, reps)
print(orm)
for i in range (1, 10):
    print(i, ">> ", convert_matt_1rm_to_nrm(orm, i))

print(convert_orm_to_reps_rpe(orm, 3, 9))


def all(weight, nrm, reps, rpe):
    orm = estimate_1rm_matt(weight, nrm)
    return convert_orm_to_reps_rpe(orm, reps, rpe)


print(all(130, 3, 3, 9))
