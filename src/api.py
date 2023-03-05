from flask import Flask, request
from datetime import datetime
from filter_data import filter_main
from calculate_score import score_main
from sort_data import sort_main

app = Flask(__name__)

@app.route('/filter_score', methods=['GET'])
def filter_score():

    filter_main()
    score_main()

    # return result as JSON
    return {'result': 'done'}

@app.route('/sort', methods=['POST'])
def sort_data():
    # get data from request body as JSON
    data = request.get_json()
    print(data)
    # get id parameter from JSON data
    id_parameter = data.get('id')
    print (id_parameter)
    # call sort() function
    id_parameter = int(id_parameter)
    sorted_data = sort_main(id_parameter)

    # return result as JSON
    return sorted_data

if __name__ == '__main__':
    app.run(port=6969)
