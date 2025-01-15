# Prophet based Stock Forecasting.

## Introduction

In this project, I have developed a scalable time-series forecasting pipeline using Prophet, designed to predict the future stock price of a given company or entity specifically focusing on its performance one year ahead. The pipeline integrates critical features such as seasonality, holiday effects, and trend analysis to provide accurate and actionable forecasts.

## Objectives

The primary goal of this project is to create a time-series forecasting system that can:
   1. Analyze historical data to predict future trends.
   2. Enable easy parameter tuning to improve model performance.
   3. Provide seamless tracking, logging, and deployment of forecasting models using MLflow.

### Prerequisites
To run this project, you need to install the following libraries:
### Required Libraries

- **Python 3.12+**
- **Pandas**: This library performs data manipulation and analysis also provides powerful data structures like dataframes.
- **Prophet**: A forecasting tool for time-series data, designed to handle trends, seasonality and holidat effects.
- **Streamlit**: Streamlit is a framework that builds interactive, data-driven web applications directly in python. 
- **MLFlow**: An Open-source platform for tracking, managing and deploying machine learning workflows.

Other Utility Libraries : **Matplotlib**, **io**.

### Installation

   ```
   pip install pandas
   pip install streamlit
   pip install prophet
   pip install mlflow
   pip install matplotlib
   ```

### Procedure

1.   Create new directory **'Prophet_Forecasting'**.
2.   Inside that directory/folder create new environment.
   
   ```
   python -m venv mlflowpf
   ```

  Now, activate this **'mlflowpf'** venv.
  
4.   Clone this Repository :

   ```
   https://github.com/Rajcr2/Prophet-Forecasting.git
   ```
5.   Now, Install all mentioned required libraries in your environment.
6.   After, that Run **'main.py'** file from Terminal. To activate the dashboard on your browser.
   ```
   streamlit run main.py
   ``` 
7. Now, move to your browser.
8. Upload the csv file from your local machine or you can use sample csv file given here.
9. After, uploading set the model parameters such as changepoint or forecast period.
10. Then convert data into prophet preffered format i.e **'ds'** and **'y'** format.
11. and then just **'Train Model'** and see the forecast results and also, don't forgot to verify model forecast results after 365 days or your mentioned period 😁. 



### Output

Results of MODEL :

https://github.com/user-attachments/assets/e63e357a-aae7-4dc9-8bf5-4e07b7928a27






#### Entities Forecast By MODEL :
#### 1. USD-INR 
Model has predicted INR has expected to maintain stability against USD by end of 2025, showing minimal fluctuations in its exchange rate indicating a stable currency.

![usd(1)](https://github.com/user-attachments/assets/9c0648b7-c976-4a41-b660-7395b356e6fb)

#### 2. TCS

As per Model, TCS Stock is projected to experience a 1.58% change by the end of 2025, indicating slight growth or decline which reflecting steady market trend for company.

![TCS 1](https://github.com/user-attachments/assets/95ff449f-f5d9-49ce-9b01-9b72f0d02514)

#### 3. INFOSYS

Infosys stock is expected to undergo an 8.19% change by end of 2025, reflecting a moderate but significant movement in the company's market performance over the period.

![infosys 1](https://github.com/user-attachments/assets/fbd9f707-ed57-457d-a574-3096ebc026dc)


