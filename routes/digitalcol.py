import json
import logging

from flask import request

from routes import app

WEIGHT = 0

def nextgeneration(current:str) -> str:
    global WEIGHT 
    currList = list()

    modulo_weight = WEIGHT % 100

    for i in range(len(current)-1):
        char_p1 = current[i]
        currList.append(char_p1)

        int_p1 = int(char_p1)
        int_p2 = int(current[i+1])

        signature = int_p1 - int_p2
        if signature < 0:
            signature += 10
        
        int_child = (signature + modulo_weight) % 10
        WEIGHT += int_child

        currList.append(str(int_child))

    currList.append(current[-1])

    return "".join(currList)


@app.route('/digital-colony', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("data received: {}".format(data))
    global WEIGHT

    colony = data[0]["colony"]

    result = []

    for num in colony:
        WEIGHT += int(num)
        logging.info("current weight: {}".format(WEIGHT))
    
    for i in range(10):
        colony = nextgeneration(colony)
        logging.info("current colony: {}".format(colony))

    result.append(str(WEIGHT))

    for i in range(40):
        colony = nextgeneration(colony)
        logging.info("current colony: {}".format(colony))
    
    result.append(str(WEIGHT))

    logging.info("My result :{}".format(result))
    return json.dumps(result)