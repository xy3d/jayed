import re
from datetime import datetime
from flask import *
from distutils.log import debug
from fileinput import filename
import pandas as pd
import os

# DATA_FOLDER = os.path.join('data', 'dataset')

app = Flask(__name__, template_folder="templates")
# app.config['DATA_FOLDER'] = DATA_FOLDER

@app.route('/')
def home():
    # read csv
    data_file_path = os.path.join('data', 'salary_data.csv') 
    dataset = pd.read_csv(data_file_path, encoding='unicode_escape')
    x = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, 1].values

    
    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 1/3)
    from sklearn.linear_model import LinearRegression
    lr = LinearRegression()
    lr.fit(x_train, y_train)
    y_pred = lr.predict(x_test)



    import matplotlib.pyplot as plt
    plt.scatter(x_train, y_train, color = "red")
    plt.plot(x_train, lr.predict(x_train), color = "green")
    plt.title("Salary vs Experience (Training set)")
    plt.xlabel("Years of Experience")
    plt.ylabel("Salary")
     # Save the figure in the static directory 
    plt.savefig(os.path.join('static', 'images', 'plot.png'))
    # plt.show()
    plt.close()

    return render_template('graph.html')
    #return "Hello"


@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content


if __name__ == '__main__':
    app.run(debug=True)