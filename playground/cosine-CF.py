import numpy as np


def cosine(data_a, data_b):
    array_a = np.array(data_a)
    array_b = np.array(data_b)
    sum_data = array_a.T.dot(array_b)
    print(sum_data)
    denom = np.linalg.norm(array_a) * np.linalg.norm(array_b)
    return 0.5 + 0.5 * (sum_data / denom)


def cosine_beta(data_a, data_b):
    array_a = np.mat(data_a)
    array_b = np.mat(data_b)
    sum_data = array_a * array_b.T  # 若列为向量则为 data_a.T * data_b
    denom = np.linalg.norm(array_a) * np.linalg.norm(array_b)
    return 0.5 + 0.5 * (sum_data / denom)[0, 0]


if __name__ == "__main__":
    User_A = [0.01, 0, 0.01, 0.01]
    User_B = [100, 100, 0, 100]
    print('User_A与User_B的余弦相似度为: ', cosine(User_A, User_B))
    print('User_A与User_B的余弦相似度为: ', cosine_beta(User_A, User_B))
