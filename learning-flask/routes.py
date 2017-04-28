from flask import Flask, render_template, request, session, redirect, url_for

from models import db, User, Place, Classifcation
from forms import SignupForm, LoginForm, AddressForm,ClassifcationForm,RegressionForm

import urllib2
import json


from models import db, User, Place
from forms import SignupForm, LoginForm, AddressForm



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/learningflask'


db.init_app(app)

app.secret_key = "development-key"

@app.route("/")
def index():
  return render_template("index.html")


@app.route("/regression", methods=["GET", "POST"])
def regression():
  
  return render_template("regression.html")

@app.route("/success", methods=["GET", "POST"])
def success():

  form=RegressionForm()
  actual_rate_interest='0'
  if request.method == "POST":
    if form.validate() == False:
      print('failed')
      return render_template('success.html', form=form)
    else:
      width = form.width.data 
      mid = form.mid.data
      mid30 = form.mid30.data
      imbalance2 = form.imbalance2.data
      adj_price2 = form.adj_price2.data
      imbalance4 = form.imbalance4.data 
      adj_price4 = form.adj_price4.data
      imbalance8 = form.imbalance8.data
      adj_price8 = form.adj_price8.data

      t30_count = form.t30_count.data
      t30_av = form.t30_av.data 
      agg30 = form.agg30.data
      trend30 = form.trend30.data

      t60_count = form.t60_count.data
      t60_av = form.t60_av.data 
      agg60 = form.agg60.data
      trend60 = form.trend60.data


      t120_count = form.t120_count.data
      t120_av = form.t120_av.data 
      agg120 = form.agg120.data
      trend120 = form.trend120.data

      t180_count = form.t180_count.data
      t180_av = form.t180_av.data 
      agg180 = form.agg180.data
      trend180= form.trend180.data



      data = {
              "Inputs": {
                      "input1":
                      [
                          {
                                  'Column 0': "0",   
                                  '_id': "1493266294.35",   
                                  'width': width,   
                                  'mid': mid,   
                                  'mid30': mid30,   
                                  'imbalance2': imbalance2,   
                                  'adj_price2': adj_price2,   
                                  'imbalance4': imbalance4,   
                                  'adj_price4': adj_price4,   
                                  'imbalance8': imbalance8,   
                                  'adj_price8': adj_price8,   
                                  't30_count': t30_count,   
                                  't30_av': t30_av,   
                                  'agg30': agg30,   
                                  'trend30': trend30,   
                                  't60_count': t60_count,   
                                  't60_av': t60_av,   
                                  'agg60': agg60,   
                                  'trend60': trend60,   
                                  't120_count': t120_count,   
                                  't120_av': t120_av,   
                                  'agg120': agg120,   
                                  'trend120': trend120,   
                                  't180_count': t180_count,   
                                  't180_av': t180_av,   
                                  'agg180': agg180,   
                                  'trend180': trend180,   
                          }
                      ],
              },
          "GlobalParameters":  {
          }
      }



      body = str.encode(json.dumps(data))
      #first service
      url = 'https://ussouthcentral.services.azureml.net/workspaces/f28500a2409240e0912181212c9e7c5e/services/4d873d1de32f4a57b0550f8c1b14b511/execute?api-version=2.0&format=swagger'
      api_key = 'swpXT4QjxL2tNeP2mqWyCwiw+/4FQgarE++f0aanDQ15FUrY6KSk6OH0YQSXtAia6PeG6FErmqo/Oo0kfL67eA=='
      headers= {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

      req = urllib2.Request(url, body, headers)


      

        


      try:
          response = urllib2.urlopen(req)

          result = response.read()
          resp_dict = json.loads(result)
          print(result)
          bitcoinPrice=resp_dict['Results']['output1'][0]['Scored Label Mean']
          
          print("Bit coin price",bitcoinPrice)



          
      except urllib2.HTTPError, error:
          print("The request failed with status code: " + str(error.code))

          # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
          print(error.info())
          print(json.loads(error.read())) 



    return render_template('regression.html',bitcoinPrice=bitcoinPrice,mid=mid)

  elif request.method == 'GET':
    return render_template('success.html',form=form)













  

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/fetch")
def fetch():
  return render_template("fetch.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
  if 'email' in session:
    return redirect(url_for('home'))

  form = SignupForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()

      session['email'] = newuser.email
      return redirect(url_for('home'))

  elif request.method == "GET":
    return render_template('signup.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
  if 'email' in session:
    return redirect(url_for('home'))

  form = LoginForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template("login.html", form=form)
    else:
      email = form.email.data 
      password = form.password.data 

      user = User.query.filter_by(email=email).first()
      if user is not None and user.check_password(password):
        session['email'] = form.email.data 
        return redirect(url_for('home'))
      else:
        return redirect(url_for('login'))

  elif request.method == 'GET':
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
  session.pop('email', None)
  return redirect(url_for('index'))


@app.route("/classification",methods=["GET", "POST"])
def classification():


  form = ClassifcationForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template("classification.html", form=form)
    else:

      amount_requested = form.amount_requested.data 
      risk_score = form.risk_score.data
      debt_to_income_ratio = form.debt_to_income_ratio.data
      zip_code = form.zip_code.data
      employment_length = form.employment_length.data


      data = {
          "Inputs": {
                  "input1":
                  [
                      {
                              'Amount_Requested': amount_requested,   
                              'Loan_Title': "1",   
                              'Risk_Score': risk_score,   
                              'Debt-To-Income_Ratio': "10",   
                              'Zip_Code': zip_code,   
                              'Employment_Length': employment_length,   
                              'Policy_Code': "1",   
                              'accept_reject_loan': "1",   
                              'State': "1",   
                      }
                  ],
          },
      "GlobalParameters":  {
      }
      }

      body = str.encode(json.dumps(data))

      url = 'https://ussouthcentral.services.azureml.net/workspaces/f28500a2409240e0912181212c9e7c5e/services/9aab259ced0b46dc96788ef0708269be/execute?api-version=2.0&format=swagger'
      api_key = 'yLH77qMmvFBxsqnSP37eIOEvk4wcV1CedkbwZOcptB92eOu48Gu6IQ9Hi7AQsurxpI82Qk+W+O89+sMyj1pvfw=='
      headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

      req = urllib2.Request(url, body, headers)

      try:
        response = urllib2.urlopen(req)

        result = response.read()
        resp_dict = json.loads(result)
        print(result)
        loaneligibilty=resp_dict['Results']['output1'][0]['Scored Labels']
        
        print(loaneligibilty)
        c= Classifcation()
        print(c)
        status=c.get_status(loaneligibilty)
      except urllib2.HTTPError, error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read()))
      #return  redirect(url_for('success'))
      if(status=='Accepted'):
        return redirect(url_for('success'))
      else:
        return redirect(url_for('fetch'))


  elif request.method == 'GET':
    return render_template('classification.html', form=form)


@app.route("/home", methods=["GET", "POST"])
def home():
  if 'email' not in session:
    return redirect(url_for('login'))

  form = AddressForm()

  places = []
  my_coordinates = (53.2734, -7.778320310000026)

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('home.html', form=form)
    else:
      # get the address
      address = form.address.data 

      # query for places around it
      p = Place()
      my_coordinates = p.address_to_latlng(address)
      places = p.query(address)

      # return those results
      return render_template('home.html', form=form, my_coordinates=my_coordinates, places=places)

  elif request.method == 'GET':
    return render_template("home.html", form=form, my_coordinates=my_coordinates, places=places)



  

if __name__ == "__main__":
  app.run(debug=True)