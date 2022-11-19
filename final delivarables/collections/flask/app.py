from flask import Flask, request, render_template
import joblib
import requests
# import jsonify
from flask import jsonify

app = Flask(__name__)  # initialising flask app

model = joblib.load('Loan Predection') # load machine learning  model
@app.route('/', methods=['GET'])

def home():
    return render_template('index2.html')
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
        prediction = model.predict([[GENDER, MARRIED, int(DEPENDENTS), EDUCATION, SELF_EMPLOYES, int(APPLICANTINCOME), int(COAAPLICANTINCOME), int(LOANAMOUNT), int(LOAN_AMOUNT_TERM), CREDIT_HISTORY, PROPERTY_AREA]])
        output=prediction[0]
        if(output==0):
            return render_template('submit2.html', prediction_text="Congratulations Your are Eligible for LOAN")
        else:
            return render_template('submit2.html', prediction_text="Sorry, Your are Not Eligible for LOAN")
    else:
        return render_template('predict1.html')

if __name__ == '__main__':
    app.run(debug=True)
