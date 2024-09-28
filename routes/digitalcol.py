import json
import logging

from flask import request

from routes import app

def nextgeneration(current:list, weight: int) -> (list, int):

    last = current[-1]
    new_list = []

    modulo_weight = weight % 100

    for i in range(len(current)-1):
        int_p1 = current[i]
        int_p2 = current[i+1]

        signature = int_p1 - int_p2
        if signature < 0:
            signature += 10
        
        int_child = (signature + modulo_weight) % 10
        weight += int_child

        new_list.append(int_p1)
        new_list.append(int_child)

    new_list.append(current[-1])

    return new_list, weight


@app.route('/digital-colony', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("data received: {}".format(data))
    weight = 0

    colony = [int(x) for x in data[0]["colony"]]
    result = []

    for num in colony:
        weight += num
    
    for i in range(10):
        colony, weight = nextgeneration(colony, weight)
        logging.info("current colony: {}".format(i))

    result.append(str(weight))

    for i in range(40):
        colony, weight = nextgeneration(colony, weight % 100)
        logging.info("current colony: {}".format(10 + i))
    
    result.append(str(weight))

    logging.info("My result :{}".format(result))
    return json.dumps(result)