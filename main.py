import os
from project import app
import time


# if __name__ == '__main__':
#     port = int(os.environ.get("PORT", 33507))
#     host = 'http://instarem-bot.herokuapp.com/'
#     app.run(debug=True, port=port, host= host)


if __name__ == '__main__':
   port = int(os.environ.get("PORT", 8081))
   app.run(debug=True, port=port, host='0.0.0.0')
