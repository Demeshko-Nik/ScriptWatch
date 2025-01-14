from flask import Flask, request, jsonify
from config import config
from models import db, Data

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/data', methods=['POST'])
    def add_data():
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        app_data = Data(script_name=data['script_name'],exec_status=data['exec_status'],memory_usage=data['memory_usage'],execution_time=data['execution_time'],cpu_usage=data['cpu_usage'])
        db.session.add(app_data)
        db.session.commit()

        return jsonify({'message': 'Data added successfully', 'id': data.id}), 201

    @app.route('/data/<int:id>', methods=['GET'])
    def get_data(id):
        data = Data.query.get_or_404(id)
        return jsonify(data.content)

    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(host="0.0.0.0", port=5000,debug=app.config['DEBUG'])