import os
from project import app
import time


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 33507))
    host = 'http://stressbot.herokuapp.com/'
    app.run(debug=True, port=port, host= host)
