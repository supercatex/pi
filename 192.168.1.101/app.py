from flask import Flask
import json


app = Flask(__name__)


@app.route('/')
def index():
        data = {}
        for key, filename in _filenames.items():
                file = open(filename, 'r')
                data[key] = file.readline()
        return json.dumps(data)


_filenames = {}
_filenames['conduct'] = '/home/pi/workspace/data/conduct.txt'
_filenames['do'] = '/home/pi/workspace/data/do.txt'
_filenames['ph'] = '/home/pi/workspace/data/ph.txt'
_filenames['temp'] = '/home/pi/workspace/data/temp.txt'

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', threaded=True)
