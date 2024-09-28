import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)

def find_safe(map:list) -> list:
    safe = []
    unsafe = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == "r":
                for k in range(j,len(map[i])):
                    if (i,k) not in unsafe:
                        unsafe.append((i,k))    
            elif map[i][j] == "l":
                for k in range(0,j+1):
                    if (i,k) not in unsafe:
                        unsafe.append((i,k))    
            elif map[i][j] == "d":
                for k in range(i,len(map)):
                    if (k,j) not in unsafe:
                        unsafe.append((k,j))  
            elif map[i][j] == "u":
                for k in range(0,i+1):
                    if (k,j) not in unsafe:
                        unsafe.append(k,j)  
            elif map[i][j] == ".":
                safe.append((i,j))
    
    safe = [x for x in safe if x not in unsafe]

    return safe

def action(map:list, man:tuple) -> list:
    
    unsafe = []




@app.route('/dodge', methods=['POST'])
def evaluate():
    data = request.data.decode().replace("\r\n","N")
    logging.info("data received: {}".format(data))
    map = []
    row = []
    for char in data:
        if char == "N":
            map.append(row)
            row = []
        else:
            row.append(char)

    map.append(row)
    print(map)

    safe = find_safe(map)

    logging.info("data received: {}".format(safe))

    result = "none"

    logging.info("My result :{}".format(result))
    return json.dumps(result)

