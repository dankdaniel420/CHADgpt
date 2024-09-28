import json
import logging

from flask import request
from routes import app

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

    for i in range(10):
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



    colony = data[1]["colony"]

    weight = 0

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

    

    logging.info("My result :{}".format(result))
    return json.dumps(result)