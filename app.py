from fastapi import FastAPI 
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from model.predict import predict_output
from schema.prediction_response import PredictionResponse

app = FastAPI()

        
@app.get("/")
def home():
    return "This is the homepage for the premium predictor"

@app.get('/health')
def health():
    return {'status' : "OK" , 
            'version' : "1.0.0"}
        
@app.post('/predict' , response_model = PredictionResponse)
def predict_premium(data : UserInput):
    input_df = {
        'bmi' : data.bmi ,
        'age_group' : data.age_group ,
        'risk' : data.risk , 
        'city_tier' : data.city_tier , 
        'income_lpa' : data.income_lpa , 
        'occupation' : data.occupation
    }

    try:
        pred = predict_output(input_df)
        return JSONResponse(status_code = 200 , content = {'response' : f'{pred}'})
    except Exception as e:
        return JSONResponse(status_code = 500 , content = str(e))