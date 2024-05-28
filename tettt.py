import numpy as np
import itertools
import time
from tqdm import tqdm


def read_data(file_path):
    # CSV 파일에서 데이터를 읽어들임
    data = np.loadtxt(file_path, delimiter=',', skiprows=1)
    return data

def calculate_volume(matrix):
    # 행렬의 볼륨 계산
    return abs(np.linalg.det(matrix))

def find_max_volume_subset(data, subset_size):
    max_volume = 0
    max_subset = None

    # 모든 가능한 부분집합에 대해 반복
    for subset in tqdm(itertools.combinations(range(data.shape[1]), subset_size), desc="Processing"):
        subset_matrix = data[:, subset]
        volume = calculate_volume(subset_matrix)

        if volume > max_volume:
            max_volume = volume
            max_subset = subset

    return max_volume, max_subset

# 데이터 파일 경로
file_path = 'input.csv'

# 데이터 읽기
data = read_data(file_path)

# 볼륨을 계산할 벡터의 수 (이 경우는 20)
subset_size = 20

# 타이머 시작
start_time = time.time()

# 최대 볼륨 및 해당 부분집합 찾기
max_volume, max_subset = find_max_volume_subset(data, subset_size)

# 타이머 종료
end_time = time.time()

# 결과 출력
print("Maximum Volume:", max_volume)
print("Subset of Vectors:", max_subset)
print("Execution Time (seconds):", end_time - start_time)
