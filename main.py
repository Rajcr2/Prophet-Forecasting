import pandas as pd
import io
import streamlit as st
from prophet import Prophet
import mlflow
import mlflow.pyfunc
import matplotlib.pyplot as plt

# Streamlit Page Configuration
st.set_page_config(page_title="Prophet Forecasting Dashboard", layout="wide")

# Sidebar: Upload Data
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

# Use session state to store data and avoid reloads
if "data" not in st.session_state:
    st.session_state.data = None
if "processed_data" not in st.session_state:
    st.session_state.processed_data = None

if uploaded_file:
    # Step 1: Load the uploaded CSV file into a DataFrame
    st.session_state.data = pd.read_csv(uploaded_file)
    st.write("### Original Data:")
    st.write(st.session_state.data.head())

    # Step 2: Convert the data to Prophet format
    if st.button("Convert Data to Prophet Format"):
        try:
            data = st.session_state.data.copy()

            # Ensure 'Date' column is parsed correctly
            data['Year'] = data['Date'].apply(lambda x: str(x)[-4:])
            data['Month'] = data['Date'].apply(lambda x: str(x)[-7:-5])
            data['Day'] = data['Date'].apply(lambda x: str(x)[-10:-8])

            # Remove commas from 'Price' and convert to numeric
            data['Price'] = data['Price'].replace({',': ''}, regex=True).astype(float)

            # Create 'ds' and 'y' columns for Prophet
            data['ds'] = data['Year'] + '-' + data['Month'] + '-' + data['Day']
            #data['ds'] = pd.to_datetime(data['ds'], errors='coerce')  # Convert 'ds' to datetime format
            data['y'] = data['Price']
            data = data[['ds', 'y']].dropna()  # Keep only necessary columns and drop NaN

            # Validate the processed data
            if len(data) < 2:
                raise ValueError("Dataframe has less than 2 non-NaN rows after processing. Please check the input data.")

            # Save the processed data in session state
            st.session_state.processed_data = data

            # Display the converted data
            st.write("### Converted Data for Prophet:")
            st.write(st.session_state.processed_data.head())

            # Save processed data to CSV in memory
            buffer = io.StringIO()
            st.session_state.processed_data.to_csv(buffer, index=False)
            buffer.seek(0)
            with open('new_data.csv', 'w') as f:
                f.write(buffer.getvalue())

        except Exception as e:
            st.error(f"Error converting data: {e}")


# Step 3: Train Prophet Model
if st.session_state.processed_data is not None:
    st.sidebar.title("Model Parameters")
    changepoint_scale = st.sidebar.slider("Changepoint Prior Scale", 0.01, 0.5, 0.05)
    seasonality = st.sidebar.selectbox("Seasonality Mode", ["additive", "multiplicative"])
    forecast_periods = st.sidebar.slider("Forecast Periods (days)", 1, 365, 30)

    if st.button("Train Model"):
        try:
            with st.spinner("Training model..."):
                # Train the Prophet model
                model = Prophet(changepoint_prior_scale=changepoint_scale, seasonality_mode=seasonality)
                model.fit(st.session_state.processed_data)

                # Generate future dates for prediction
                future = model.make_future_dataframe(periods=forecast_periods)
                forecast = model.predict(future)

                # Display forecast results
                st.write("### Forecast Results")
                st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head())

                # Plot the forecast
                fig1 = model.plot(forecast)
                st.pyplot(fig1)

                # Plot forecast components
                fig2 = model.plot_components(forecast)
                st.pyplot(fig2)

                # Option to log to MLflow
                if st.checkbox("Log Model to MLflow"):
                    with mlflow.start_run():
                        mlflow.log_param("changepoint_prior_scale", changepoint_scale)
                        mlflow.log_param("seasonality_mode", seasonality)
                        mlflow.log_param("forecast_periods", forecast_periods)
                        
                        class ProphetWrapper(mlflow.pyfunc.PythonModel):
                            def __init__(self, model):
                                self.model = model

                            def predict(self, context, input_data):
                                forecast = self.model.predict(input_data)
                                return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
                        
                        # Log the Prophet model
                        mlflow.pyfunc.log_model("prophet_model", python_model=ProphetWrapper(model))
                        st.success("Model logged to MLflow successfully!")

                # Download forecast as CSV
                st.write("### Download Forecast Data")
                csv = forecast.to_csv(index=False)
                st.download_button("Download CSV", csv, "forecast.csv", "text/csv")

        except Exception as e:
            st.error(f"Error training the model: {e}")

