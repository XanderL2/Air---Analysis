from flask import Flask, render_template, request, make_response, redirect, url_for, session
from analysis.PollutionAnalytics import GetDailyPollutionGraph

app = Flask(__name__)

# Routes
@app.route("/", methods=['GET'])
def root():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)

