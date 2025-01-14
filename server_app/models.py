from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exec_status = db.Column(db.String, primary_key=False)
    script_name = db.Column(db.String, primary_key=False)
    memory_usage = db.Column(db.Integer, primary_key=False)
    execution_time = db.Column(db.Integer, primary_key=False)
    cpu_usage = db.Column(db.Integer, primary_key=False)

    def __repr__(self):
        return f'<Data {self.id}>'