from flask import Flask, request, render_template
import requests
# import jsonify
from flask import jsonify
API_KEY = "mv6fCKTByg6_1zZoG2D2XI0ngui-UUq9MQ8IKSN4HNYa"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)  # initialising flask app

@app.route('/', methods=['GET'])

def home():
    return render_template('/index2.html')

@app.route('/predict2.html')
def formpg():
    return render_template('predict2.html')


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        GENDER = request.form['Gender']
        MARRIED=request.form['Married']
        DEPENDENTS=request.form['Dependents']
        EDUCATION = request.form['Education']
        SELF_EMPLOYES=request.form['Self_Employes']
        APPLICANTINCOME=request.form['ApplicantIncome']
        COAAPLICANTINCOME=request.form['CoaaplicantIncome']
        LOANAMOUNT= request.form['LoanAmount']
        LOAN_AMOUNT_TERM=request.form['Loan_Amount_Term']
        CREDIT_HISTORY=request.form['Credit_History']
        PROPERTY_AREA=request.form['Property_Area']
        if GENDER == 'Male':
            GENDER = 1
        else:
            GENDER = 0
        if MARRIED == 'yes':
            MARRIED = 1
        else:
            MARRIED = 0
        if DEPENDENTS == '3+':
            DEPENDENTS = 3
        if EDUCATION == 'Graduate':
            EDUCATION = 0
        else:
            EDUCATION = 1
        if SELF_EMPLOYES == 'yes':
            SELF_EMPLOYES = 1
        else:
            SELF_EMPLOYES = 0
        if CREDIT_HISTORY == 'yes':
            CREDIT_HISTORY = 1
        else:
            CREDIT_HISTORY = 0
        if  PROPERTY_AREA == 'Urban':
            PROPERTY_AREA = 2
        elif PROPERTY_AREA == 'Semiurban':
            PROPERTY_AREA = 1
        else:
            PROPERTY_AREA = 0

        X = [[GENDER, MARRIED, int(DEPENDENTS), EDUCATION, SELF_EMPLOYES, int(APPLICANTINCOME), int(COAAPLICANTINCOME), int(LOANAMOUNT), int(LOAN_AMOUNT_TERM), CREDIT_HISTORY, PROPERTY_AREA]]
        

        payload_scoring = {"input_data": [{"fields": [['Gender','Married','Dependents','Education','Self_Employes','ApplicantIncome','CoaaplicantIncome','LoanAmount','Loan_Amount_Term','Credit_History','Property_Area']], "values": X}]}

        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/aeea24d1-5ece-4f3e-975a-696619e6b85e/predictions?version=2022-11-15', json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
# print("Scoring response")
        predictions =response_scoring.json()
        output=predictions['predictions'][0]['values'][0][0]
        if(output==0):
            return render_template('submit2.html', prediction_text="Congratulations Your are Eligible for LOAN")
        else:
            return render_template('submit2.html', prediction_text="Sorry, Your are Not Eligible for LOAN")
    else:
        return render_template('predict1.html')

if __name__ == '__main__':
    app.run(debug=True)
