#Yes, i don`t use comments, sorry.

import random
import copy

def strict_shuffle(array):
    if len(array) <= 1:
        raise Exception("the length of the array must be greater than 1")

    array_tmp = copy.deepcopy(array)
    array_dict = []

    for i in range(len(array) - 2):
        x = copy.deepcopy(array_tmp)
        try:
            x.remove(array[i])
        except:
            pass

        y = random.choice(x)
        array_dict.append(y)
        array_tmp.remove(y)

    if array_tmp[0] == array[-2]:
        array_dict.append(array_tmp[1])
        array_dict.append(array_tmp[0])
    else:
        array_dict.append(array_tmp[0])
        array_dict.append(array_tmp[1])

    return array_dict
