import json
import logging
import regex as re

from flask import request
from flask import jsonify

from routes import app

logger = logging.getLogger(__name__)


@app.route('/the-clumsy-programmer', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    correctionDict = {}
    corrections = []
    
    dictionary = data.get("dictionary")
    mistypes = data.get("mistypes")

 

        

    return jsonify(result)