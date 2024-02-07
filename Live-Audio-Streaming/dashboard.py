# # dashboard.py
# from flask import Flask, render_template, jsonify
# from flask_sse import sse
# import os
# import time

# app = Flask(__name__)
# app.config["REDIS_URL"] = "redis://localhost"  # You need to have Redis installed

# # Initialize SSE
# app.register_blueprint(sse, url_prefix='/stream')

# # Variable to store predicted class
# predicted_class = "No Prediction Yet"
# predicted_class_list = []  # Initialize an empty list

# @app.route('/')
# def index():
#     return render_template('dashboard.html', predicted_class=predicted_class)

# @app.route('/get_predicted_class_list')
# def get_predicted_class_list():
#     global predicted_class_list
#     return jsonify(predicted_class_list)

# def update_predicted_class():
#     global predicted_class
#     global predicted_class_list
#     last_modified = 0
#     while True:
#         try:
#             # Get the last modified time of the file
#             modified_time = os.path.getmtime('predicted_class.txt')
#             if modified_time != last_modified:
#                 last_modified = modified_time
#                 with open('predicted_class.txt', 'r') as file:
#                     predicted_class_list = [eval(line.strip())[0] for line in file]

#                 if "drinking_sipping" in predicted_class_list:
#                     result_value = 'danger'
#                     with open('i.txt', 'a') as file:
#                         file.write(f"{result_value}\n")
#                     sse.publish({"result_value": result_value}, type='predicted_class_update')
#                 else:
#                     print('none')

#         except FileNotFoundError:
#             pass

#         time.sleep(1)  # Adjust the sleep time as needed

# if __name__ == '__main__':
#     # Start a separate thread to continuously update the predicted class
#     from threading import Thread
#     update_thread = Thread(target=update_predicted_class)
#     update_thread.start()

#     # Run the Flask app
#     app.run(debug=True, port=8000)

from flask import Flask, render_template
import redis

app = Flask(__name__)

# Redis client configuration
redis_client = redis.Redis(
    host='redis-16452.c56.east-us.azure.cloud.redislabs.com',
    port=16452,
    password='DNPVZUZSLaDnrvZydsunVG1p9fTV3YF8'
)

@app.route('/')
def index():
    # Get the value of 'predicted_class' key from Redis
    predicted_class = redis_client.get('predicted_class')
    predicted_class = predicted_class.decode('utf-8') if predicted_class else "No Prediction Yet"
    return render_template('dashboard.html', predicted_class=predicted_class)

if __name__ == '__main__':
    app.run(debug=True,port=8000)
