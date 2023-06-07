import json
import csv
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flasgger import Swagger
import bcrypt #additional encryption

app = Flask(__name__)
auth = HTTPBasicAuth()
swagger = Swagger(app)


########## CSV to JSON + Store JSON + View JSON ############

def csv_to_json(csv_file):
    data = []
    with open(csv_file, 'r') as file:
        csv_data = csv.DictReader(file)
        for row in csv_data:
            data.append(row)
    return data

def format_nested_json(data):
    formatted_data = {}
    for row in data:
        sno = row['S.No.']
        year = row['Year']
        month = row['Month']
        date = row['Date']
        reason = row['Reason']
        sex = row['Sex']
        age = row['Age']
        race = row['Race']
        education = row['Education']
        hispanic = row['Hispanic']
        place_of_incident = row['Place of incident']
        police_involvement = row['Police involvement']

        if sno not in formatted_data:
            formatted_data = {
                'sno': sno,
                'year': year,
                'Identification': []
            }

        formatted_data['Identification'].append({
            'sex': sex,
            'age': age,
            'race': race,
            'hispanic': hispanic,
            'education': education,
            'police_involvement': police_involvement,
            'Offence Details':
                {
                    'month': month,
                    'date': date,
                    'reason': reason,
                    'place_of_incident': place_of_incident
                }
        })
    return formatted_data


######################## Save and Update #############################

def save_to_file(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


# View Data
@app.route('/data', methods=['GET'])
def view_data():

    """
    View incidents data.
    ---
    responses:
      200:
        description: Incidents data.
    """

    with open('guns_incident.json', 'r') as file:
        json_data = json.load(file)
    return jsonify(json_data)


################### Data Validation ############################

from datetime import datetime

def validate_data(data):
    if 'S.No.' not in data:
        return False

    # if 'Year' in data and not data['Year'].isdigit():
    #     return False

    # if 'Sex' in data and data['Sex'].upper() not in ['Male', 'Female', 'Others']:
    #     return False

    # if 'Police involvement' in data and data['Police involvement'] not in ['0', '1']:
    #     return False

    # # Additional data type validations for other fields
    # if 'Age' in data and not data['Age'].isdigit():
    #     return False

    # if 'Date' in data:
    #     try:
    #         datetime.strptime(data['Date'], '%d-%m-%Y')
    #     except ValueError:
    #         return False

    # if 'Education' in data and not isinstance(data['Education'], str):
    #     return False

    # if 'Hispanic' in data and not isinstance(data['Hispanic'], str):
    #     return False

    # if 'Month' in data and not isinstance(data['Month'], str):
    #     return False

    # if 'Place of incident' in data and not isinstance(data['Place of incident'], str):
    #     return False

    # if 'Race' in data and not isinstance(data['Race'], str):
    #     return False

    # if 'Reason' in data and not isinstance(data['Reason'], str):
    #     return False

    return True



################### Posting Data #######################

@app.route('/data', methods=['POST'])
def receive_data():

    """
    Receive incidents data.
    ---
    parameters:
      - in: body
        name: data
        schema:
          type: object
          properties:
            S.No.:
              type: integer
              example: 1
            Year:
              type: string
              example: "2023"
            Month:
              type: string
              example: "May"
            Date:
              type: string
              format: date
              example: "24-05-2023"
            Reason:
              type: string
              example: "Public safety concern"
            Education:
              type: string
              example: "High School"
            Sex:
              type: string
              example: "Male"
            Age:
              type: integer
              example: 30
            Race:
              type: string
              example: "White"
            Hispanic:
              type: string
              example: "No"
            Place of incident:
              type: string
              example: "Park"
            Police involvement:
              type: string
              example: "1"
        required: true
    responses:
      200:
        description: Data saved successfully.
      400:
        description: Invalid data format.
      401:
        description: Request content must be in JSON format.
    """



    if request.is_json:
        data = request.get_json()
        if validate_data(data):
            save_to_file(data, 'guns_incident1.json')
            return jsonify({'message': 'Data saved successfully.'}), 200
        else:
            return jsonify({'error': 'Invalid data format.'}), 400
    else:
        return jsonify({'error': 'Request content must be in JSON format.'}), 401


################### Auth #######################

# Hashed password for comparison
hashed_password = bcrypt.hashpw(b'jayed778', bcrypt.gensalt())

@app.route('/auth')
@auth.login_required
def get_response():

    """
    Get authenticated response.
    ---
    responses:
      200:
        description: Welcome message.
    """

    return jsonify('Welcome Aboard!!')

@auth.verify_password
def authenticate(username, password):
    if username and password:
        if username == 'jayed' and bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return True
        else:
            return False
    return False

################### Index #######################

@app.route('/', methods=['GET'])
def index():

    """
    Index page.
    ---
    responses:
      200:
        description: API description.
    """

    return 'API Test'


################### Main #######################

if __name__ == '__main__':
    csv_file = 'data/guns_incident.csv'
    json_data = csv_to_json(csv_file)
    formatted_json_data = format_nested_json(json_data)
    save_to_file(formatted_json_data, 'guns_incident.json')
    app.run(debug=True)