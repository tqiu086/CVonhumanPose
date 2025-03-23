from flask import Flask, request, jsonify
import threading

# 全局共享变量
password_storage = {
    'password': None,  # 设置的密码
    'submitted': False  # 是否已经提交
}

# 服务1：设置密码
app_set = Flask("set_password")

@app_set.route('/set_password', methods=['POST'])
def set_password():
    data = request.json
    pwd = data.get('password')
    if not isinstance(pwd, str) or len(pwd) != 4 or not all(c in '0123' for c in pwd):
        return jsonify({'status': 'error', 'message': '密码必须是4位，仅包含0~3'}), 400
    password_storage['password'] = pwd
    password_storage['submitted'] = True
    return jsonify({'status': 'ok', 'message': '密码已设置'})


# 服务2：输入密码尝试验证
app_try = Flask("try_password")

@app_try.route('/try_password', methods=['POST'])
def try_password():
    if not password_storage['submitted']:
        return jsonify({'status': 'waiting', 'message': '尚未设置密码，请稍后'}), 400

    data = request.json
    attempt = data.get('password')
    if not isinstance(attempt, str) or len(attempt) != 4 or not all(c in '0123' for c in attempt):
        return jsonify({'status': 'error', 'message': '尝试密码必须是4位，仅包含0~3'}), 400

    if attempt == password_storage['password']:
        return jsonify({'status': 'success', 'message': '密码正确！通过！'})
    else:
        return jsonify({'status': 'fail', 'message': '密码错误，请重试'})


# 多线程启动两个服务
def run_app1():
    app_set.run(port=5000)

def run_app2():
    app_try.run(port=5001)

if __name__ == '__main__':
    t1 = threading.Thread(target=run_app1)
    t2 = threading.Thread(target=run_app2)
    t1.start()
    t2.start()
