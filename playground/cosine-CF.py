import numpy as np


def Cosine(dataA, dataB):
    arrayA = np.array(dataA)
    arrayB = np.array(dataB)
    sumData = arrayA.T.dot(arrayB)
    print(sumData)
    denom = np.linalg.norm(arrayA) * np.linalg.norm(arrayB)
    return 0.5 + 0.5 * (sumData / denom)


def CosineBeta(dataA, dataB):
    arrayA = np.mat(dataA)
    arrayB = np.mat(dataB)
    sumData = arrayA * arrayB.T  # 若列为向量则为 dataA.T * dataB
    denom = np.linalg.norm(arrayA) * np.linalg.norm(arrayB)
    return 0.5 + 0.5 * (sumData / denom)[0, 0]


if __name__ == "__main__":
    User_A = [1, 0, 1, 1]
    User_B = [1, 1, 0, 1]
    print('User_A与User_B的余弦相似度为: ', Cosine(User_A, User_B))
    print('User_A与User_B的余弦相似度为: ', CosineBeta(User_A, User_B))
