from flask import Flask
from celery_app import make_celery
from PIL import Image
from queue import Queue
from sqlalchemy import create_engine
from celery.result import AsyncResult
import redis
import os
import pickle

# broker_url = 'pyamqp://guest@localhost//'
# result_backend = 'db+sqlite:///results.db'
app = Flask(__name__)
# app.config['CELERY_BROKER_URL'] =broker_url
# app.config['CELERY_RESULT_BACKEND'] = result_backend
app.config.from_object('celery_settings')
celery = make_celery(app)
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL','redis://127.0.0.1:6379/0')
previous_statement = None
# engine = create_engine("sqlite:///results.db?check_same_thread=False")
# connection = engine.connect()
r_db = redis.StrictRedis.from_url(CELERY_RESULT_BACKEND,decode_responses= True)


@app.route('/<string:filename>')
def hello_world(filename):
    global previous_statement
    previous_statement = BFS_3.delay(filename)
    return str(previous_statement.task_id)


@app.route('/status/<string:filename>')
def check_status(filename):
    all_keys  = r_db.keys()
    received_key = "celery-task-meta-" + filename
    print(received_key)
    print(CELERY_RESULT_BACKEND)
    if r_db.get(received_key):
        the_result = r_db.get(received_key)
        if "null" in the_result:
            the_result = the_result.replace("null","False")
        result_dict = eval(the_result)
        return result_dict['result']
    else:
        return 'Not Ready'
    print(r_db.get(received_key))
    return r_db.get(received_key)
    # res = celery.AsyncResult(filename)
    # if res.ready():
    #     result = connection.execute("select * from celery_taskmeta")
    #     for row in result:
    #         if row['task_id'] == filename:
    #             return pickle.loads(row['result'])
    # else:
    #     return "Not Ready"

    # global previous_statement
    # print(previous_statement)
    # print(previous_statement.ready())
    # if previous_statement and previous_statement.ready():
    #     return str(previous_statement.get())
    # else:
    #     return "Not Ready"


def iswhite(value):
    distance_black = value[0]+value[1]+value[2]
    distance_white = 765 - (value[0]+value[1]+value[2])
    if value == (127, 127, 127) or distance_black < distance_white:
        return False
    return True

def getadjacent(n):
    x, y = n
    return [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)]


def BFS(query_string):
    query_list = query_string.split("_")
    start = (int(query_list[0]), int(query_list[1]))
    end = (int(query_list[2]), int(query_list[3]))
    filename = query_list[4]
    start = tuple(start)
    end = tuple(end)
    print(start)
    print(end)
    print(filename)
    # convert_to_bw(filename)
    base_img = Image.open(filename + ".jpg")
    # base_img.putpixel(start,(127,0,0))
    # base_img.putpixel(end, (127, 0, 0))
    # base_img.save('duplicate.jpg')
    pixels = base_img.load()
    # queue = Queue()
    queue = []
    # queue.put([start])  # Wrapping the start tuple in a list
    queue.append([start])
    last_path = []
    max_length = 0
    while len(queue):

        path = queue.pop(0)
        pixel = path[-1]
        if pixel == end:
            a = path
            str_a = ""
            for i in a:
                str_a += str(i) + " "
            str_a = str_a.replace('(', '')
            str_a = str_a.replace(')', '')
            str_a = str_a.replace(', ', ' ')
            str_a = str_a.rstrip()
            # return path
            return str_a


        for adjacent in getadjacent(pixel):
            x, y = adjacent
            if x < 750 and y < 1000 and iswhite(pixels[x, y]):
                pixels[x, y] = (127, 127, 127)  # see note
                new_path = list(path)
                new_path.append(adjacent)
                queue.append(new_path)
                last_path = new_path
    # print(queue)
    # print(last_path)
    return "Queue has been exhausted. No answer was found."


@celery.task()
def BFS_3(query_string):
    return BFS(query_string)


if __name__ == '__main__':
    app.run()
