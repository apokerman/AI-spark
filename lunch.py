from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import SparkApi  # 请确保SparkApi模块可用
app = Flask(__name__)
socketio = SocketIO(app)

# 配置Spark信息
appid = "2a3819f8"
api_secret = "MDJkYTFhMDcwMGRhM2JlZWIxNTM3N2U0"
api_key = "03dafe10751ca962a412faedf9fdbfb0"
domain = "generalv3.5"
Spark_url = "wss://spark-api.xf-yun.com/v3.5/chat"
spark_urls = [
    "ws://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/hh3j3w7vt7gc_v1",
    "ws://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/q55l2njozbkb_v1",
    "ws://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/7mwa3y984apl_v1",
    "ws://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/opti18im75q3_v1",
    "ws://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/ybrvtzo5dbfp_v1",
    "ws://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/z4xnahi2u44k_v1",
    "ws://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/pz43bn2twxd7_v1",
    "ws://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/1k64bz3x8lkb_v1",
    "ws://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/3cmhulwvw7wi_v1",
    "ws://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/f6h4ydayxolk_v1",
    "ws://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/x31vii89bgkc_v1",
    "ws://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/2b144osoco2u_v1",
    "ws://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/hokj3opaiq3q_v1",
    "ws://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/om7a2zgq41w1_v1",
    "ws://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/jwqi6a94f9gr_v1",
    "ws://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/3zpr1fc85su7_v1",
    "ws://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/2c3ef5gu9pl7_v1",
    "ws://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/phmcvs82r1kq_v1",
    "ws://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/haz5jyi8vg25_v1",
    "ws://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/r3gsip4fdnvr_v1",
    "ws://spark-openapi.cn-huabei-1.xf-yun.com/v1/assistants/teaiar991ugf_v1"
]


text = []


def getText(role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    while getlength(text) > 8000:
        del text[0]
    return text


@app.route('/')
def index():
    return render_template('index.html')

#连接
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('message', {'data': '连接成功！！！'})

@socketio.on('radio_click')
def handle_checkbox_click(message):
    global Spark_url  # 声明Spark_url为全局变量
    checkbox_number = message['data']
    Spark_url = spark_urls[checkbox_number]
    
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected!')

#input
@socketio.on('user_input')
def handle_user_input(message):
    user_input = message['data']
    question = checklen(getText("user", user_input))
    SparkApi.answer = ""
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
    assistant_response = SparkApi.answer
    text = getText("assistant", assistant_response)
    emit('message', {'data': '星火: ' + assistant_response, 'type': 'assistant'})
    emit('message', {'data': '用户: ' + user_input, 'type': 'user'})

if __name__ == '__main__':
    socketio.run(app, debug=True)