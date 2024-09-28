import json
import logging

from flask import request
from flask import jsonify

from routes import app

logger = logging.getLogger(__name__)


@app.route('/the-clumsy-programmer', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    result = []
    for jsonData in data:
        correctionDict = {}
        corrections = []
        dictionary = jsonData["dictionary"]
        mistypes = jsonData["mistypes"]

        def search(error, dictionary):
            differences = 0
            for string in dictionary:
                differences = 0
                if (len(error) == len(string)):
                    for i in range(len(string)):
                        if string[i] != error[i]:
                            differences += 1
                if differences == 1:
                    return string

        for mistype in mistypes:
            corrections.append(search(mistype, dictionary))
            print(mistype)
        
        correctionDict["corrections"] = corrections
        result.append(correctionDict)

        # logging.info("efficiency :{}".format(result))
    return jsonify(result)