import json
import logging
import numpy as np
import csv

from flask import request
from routes import CustomThread
from routes import app

def weigh_colony(colony:str, weight:int):
    additional_weight = 0
    new_str = ""

    for i in range(len(colony) - 1):
        signature = int(colony[i]) - int(colony[i+1])
        if signature < 0:
            signature += 10
        
        int_child = (signature + weight) % 10
        additional_weight += int_child

        new_str += colony[i]
        new_str += str(signature)

    new_str += colony[-1]
    return new_str, additional_weight

def weigh_colony_list(colony:str, weight:int):
    additional_weight = 0
    new_str = ""

    for i in range(len(colony) - 1):
        signature = int(colony[i]) - int(colony[i+1])
        if signature < 0:
            signature += 10
        
        int_child = (signature + weight) % 10
        additional_weight += int_child

        new_str += colony[i]
        new_str += str(int_child)

    new_str += colony[-1]

    halved_list = [new_str[i:i+2] for i in range(0, len(new_str)-1)]
    return halved_list, additional_weight

def get_pairs(pair:str,weight) -> list:
    num = int(pair[0]) - int(pair[1])
    if num < 0:
        num += 10
    
    num += weight
    num %= 10

    return [pair[0]+str(num), str(num)+pair[1]]

@app.route('/digital-colony', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("data received: {}".format(data))
    weight = 0

    result = []

    colony = data[0]["colony"]

    for num in colony:
        weight += int(num)

    pair_dict = {}

    for pair in [colony[:2], colony[1:3], colony[2:]]:
        if pair in pair_dict:
            pair_dict[pair] += 1
        else:
            pair_dict[pair] = 1

    logging.info("current dict: {}".format(pair_dict))

    for i in range(50):
        modulo_weight = weight % 10
        new_pair_dict = {}
        for pair, count in pair_dict.items():
            new_pairs = get_pairs(pair,modulo_weight)
            weight += count * int(new_pairs[0][1])
            
            for newpair in new_pairs:
                if newpair in new_pair_dict:
                    new_pair_dict[newpair] += count
                else:
                    new_pair_dict[newpair] = count

        pair_dict = new_pair_dict.copy()
        logging.info("current colony: {}".format(i))

    result.append(str(weight))

    # # reset weight, colonies
    # weight = 0
    # colony = [int(x) for x in data[1]["colony"]]

    # colony1 = np.array(colony[:2])
    # colony2 = np.array(colony[1:3])
    # colony3 = np.array(colony[2:])
    # np.savetxt("colony1.txt", colony1)
    # np.savetxt("colony2.txt", colony2)
    # np.savetxt("colony3.txt", colony3)

    # for num in colony:
    #     weight += num
    
    # for i in range(50):
    #     modulo_weight = weight % 10

    #     thread1 = CustomThread.CustomThread(file="colony1.txt", weight=modulo_weight)
    #     thread2 = CustomThread.CustomThread(file="colony2.txt", weight=modulo_weight)
    #     thread3 = CustomThread.CustomThread(file="colony3.txt", weight=modulo_weight)

    #     thread1.start()
    #     thread2.start()
    #     thread3.start()

    #     thread1.join()
    #     thread2.join()
    #     thread3.join()

    #     weight += thread1.value + thread2.value + thread3.value
    #     logging.info("current colony: {}".format(i))

    # result.append(str(weight))

    logging.info("My result :{}".format(result))
    return json.dumps(result)