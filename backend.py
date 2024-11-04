from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://miniapp:Zty1234!@10.22.100.117:3306/flask_demo'  # 替换为你的连接信息
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 定义 Ticket 模型
class Ticket(db.Model):
    __tablename__ = 'ticket'
    no = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(64), nullable=False)
    text = db.Column(db.String(4096), nullable=False)
    createtime = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updatetime = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

# 创建数据库表
with app.app_context():
    db.create_all()

@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.json
    if not data or 'type' not in data or 'text' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    new_ticket = Ticket(type=data['type'], text=data['text'])
    db.session.add(new_ticket)
    db.session.commit()
    
    return jsonify({
        "no": new_ticket.no,
        "type": new_ticket.type,
        "text": new_ticket.text,
        "create_time": new_ticket.createtime,
        "update_time": new_ticket.updatetime
    }), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
