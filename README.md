# Pollution_Prediction_ML_Ericsson

ML Hackathon 2019 by Ericsson

## Dataset

Reports on the weather and the level of pollution each hour for five years

## Goal

- Unlock further possibilities and benefits
- Send alarms to people who work outside
  Smart home air systems could decide, for example, if windows must be closed for the next few hours

## Run the server

1. Run in terminal `pip3 install "pyramid==1.10.4" waitress`
2. run `python3 ./web/server.py`
3. Open browser `localhost:9090/hello` and `localhost:9090/predict`

## Run the Angular front-end

1. Under the predictPMAngularApp directory, `ng serve`
2. Check the landing page and navigate `http://localhost:4200/predict`
3. Check where the default PM value come from, and click the button more than one time. See what happen and understand why!
4. Make this app look good and edit this readMe again. (could consider add those fancy UI from our lovely designer). Make sure this repo is ready for presentation in interview
5. After this fork one copy to your repo and maintain it there. (Please fork after you have made this site fully functional and you like it)
