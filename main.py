import pandas as pd
import statsmodels.api as sm
from datetime import datetime
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Head to endpoint /forecast_timeseries to fetch forecast data or to /docs to see documentation"}


@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

class Item(BaseModel):
    days: str

    class Config:
        orm_mode = True
@app.post("/forecast_future")
async def return_forecast(req:Item) :
    new_results = sm.load('model/myPredict.pickle')
    print(req.days)
    goal_time= datetime.strptime(req.days, '%Y-%m-%d')
    diff = goal_time-datetime.now()


    trend_line = pd.read_excel('model/trend_line.xlsx')
    test_trend0 = len(trend_line)+int(diff.days)
    x_test = trend_line.iloc[951]
    x_test=x_test.drop(['Unnamed: 0'])
    x_test['trend_0'] =test_trend0

    return new_results.get_prediction(x_test).summary_frame(alpha=0.05)['mean']['const']

# running the server
if __name__ == '__main__':
    uvicorn.run(app=app, host="127.0.0.1", port=8080, log_level="info")