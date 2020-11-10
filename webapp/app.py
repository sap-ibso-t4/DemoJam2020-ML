from flask import Flask, abort, jsonify
from main import CostOptimizer

app = Flask(__name__)


@app.route('/mbom/v1', methods=['GET'])
def get_purchase_mbom():
    opt = CostOptimizer(1)
    return jsonify(opt.get_tree())


@app.route('/mbom/v2', methods=['GET'])
def get_in_house_mbom():
    abort(500)
    return {
        "user": "Andy2"
    }


if __name__ == '__main__':
    app.run()
