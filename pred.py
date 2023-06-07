from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier

app = Flask(__name__)

# Load the CSV file
data = pd.read_csv('data/jobPlace_td.csv')

# Separate features (X) and target variable (y)
X = data.drop('PlacedOrNot', axis=1)
y = data['PlacedOrNot']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Gradient Boosting classifier
model = GradientBoostingClassifier()
model.fit(X_train, y_train)

# Function to preprocess user input
def preprocess_input(Age, Gender, Stream, Internships, CGPA, Hostel, HistoryOfBacklogs):
    return Age, Gender, Stream, Internships, CGPA, Hostel, HistoryOfBacklogs

# Function to predict placement based on user input
def predict_placement(Age, Gender, Stream, Internships, CGPA, Hostel, HistoryOfBacklogs):
    input_data = preprocess_input(Age, Gender, Stream, Internships, CGPA, Hostel, HistoryOfBacklogs)
    prediction = model.predict([input_data])
    probability = model.predict_proba([input_data])[0]
    if prediction[0] == 1:
        return "Candidate Should Be Placed!!", probability[1]
    else:
        return "Candidate Should Not Be Placed!!", probability[0]

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        Age = request.form['Age']
        Gender = request.form['Gender']
        Stream = request.form['Stream']
        Internships = request.form['Internships']
        CGPA = request.form['CGPA']
        Hostel = request.form['Hostel']
        HistoryOfBacklogs = request.form['HistoryOfBacklogs']

        result, probability = predict_placement(Age, Gender, Stream, Internships, CGPA, Hostel, HistoryOfBacklogs)

        # Prepare the response JSON
        response = {
            'result': result,
            'probability': "{:.2f}%".format(probability * 100)
        }
        return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
