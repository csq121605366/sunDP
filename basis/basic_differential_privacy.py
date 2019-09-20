# -*- coding: utf-8 -*-
# @Time    : 2019-05-31 12:48
# @Author  : ForestNeo
# @Email   : dr.forestneo@gmail.com
# @Software: PyCharm

#
import numpy as np


def epsilon2probability(epsilon, n=2):
    return np.e ** epsilon / (np.e ** epsilon + n - 1)


def discretization(value, lower, upper):
    """discretiza values
    :param value: value that needs to be discretized
    :param lower, the lower bound of discretized value
    :param upper: the upper bound of discretized value
    :return: the discretized value
    """
    if value > upper or value < lower:
        raise Exception("the range of value is not valid in Function @Func: discretization")

    p = (value - lower) / (upper - lower)
    rnd = np.random.random()
    return upper if rnd < p else lower


def perturbation(value, perturbed_value, epsilon):
    """
    perturbation, (random response is a kind of perturbation)
    :param value: the original value
    :param perturbed_value: the perturbed value
    :param epsilon: privacy budget
    :return: dp version of perturbation
    """
    p = epsilon2probability(epsilon)
    rnd = np.random.random()
    return value if rnd < p else perturbed_value


def random_response_basic(bit, epsilon):
    if bit not in [0, 1]:
        raise Exception("The input value is not in [0, 1] @Func: random_response.")
    return perturbation(value=bit, perturbed_value=1 - bit, epsilon=epsilon)


def random_response_pq(bits, probability_p, probability_q):
    """
    This is the generalized version of random response. When p+q=1, this mechanism turns to be the basic random response.
    See this paper: Locally Differentially Private Protocols for Frequency Estimation
    :param bits: the original data.
    :param probability_p: the probability of 1->1
    :param probability_q: the probability of 0->1
    :return: the perturbed bis
    """
    if not isinstance(bits, np.ndarray):
        raise Exception("the input type is not illegal @Func: random_response_pq.")

    index_one, index_zero = (bits == 1), (bits == 0)
    # flags is used to represent flip or not, 1 represents unchanged, 0 represents flipping.
    flags = np.zeros([bits.size], dtype=int)
    flags[index_one] = np.random.binomial(n=1, p=probability_p)
    flags[index_zero] = np.random.binomial(n=1, p=1-probability_q)
    res = 1 - (bits + flags) % 2
    return res


def random_response_pq_reverse(sum_of_bits, num_of_records, probability_p, probability_q):
    """
    decoder for function @random_response_pq
    :param sum_of_bits:
    :param num_of_records:
    :param probability_p: the probability of 1->1
    :param probability_q: the probability of 0->1
    :return:
    """
    return (sum_of_bits - num_of_records * probability_q) / (probability_p - probability_q)


def coin_flip(bits, epsilon):
    """
    the coin flip process for bit array, it is random response with length = len(bits).
    :param bits: the original data
    :param epsilon: privacy budget
    :return: the perturbed data
    example, bits = [1,1,0,0], flags = [0,1,0,1], res = [0,1,1,0]
    """
    flags = np.random.binomial(n=1, p=epsilon2probability(epsilon), size=len(bits))
    res = 1 - (bits + flags) % 2
    return res


def random_response_adjust(sum, N, epsilon):
    """
    对random response的结果进行校正
    :param sum: 收到数据中1的个数
    :param N: 总的数据个数
    :return: 实际中1的个数
    """
    p = epsilon2probability(epsilon)
    return (sum + p*N - N) / (2*p - 1)


def k_random_response(value, values, epsilon):
    """
    the k-random response
    :param value: current value
    :param values: the possible value
    :param epsilon: privacy budget
    :return:
    """
    if not isinstance(values, list):
        raise Exception("The values should be list")
    if value not in values:
        raise Exception("Errors in k-random response")
    p = np.e ** epsilon / (np.e ** epsilon + len(values) - 1)
    if np.random.random() < p:
        return value

    values.remove(value)
    return values[np.random.randint(low=0, high=len(values))]


if __name__ == '__main__':
    a = np.asarray([1, 1, 1, 0, 0, 1, 0])
    print(random_response_pq(bits=a, probability_p=1, probability_q=0.9))


