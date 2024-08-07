#Importing all the libraries
import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import plotly.express as px

#-- Main Screen
header_main = st.header("Dashboard Critical Alerts :sunglasses:", divider="gray")
explanation_filters = st.text("You can change parameters to simulate the alerts")
explanation_dash = st.text("⚠️ The number of alerts and the accountids were created by Faker, only for ilustrative purposes.")

df = pd.read_csv('alerts.csv')

# -- Side bar
st.sidebar.title('Filters for Simulation: ')

# All columns name
columns_of_dataframe = df.drop(columns=['AccountId']).keys()

columns_of_dataframe = df.columns.tolist()
columns_of_available = [col for col in columns_of_dataframe if col not in ['AccountId', 'QttUserReference','QttUserWithAlerts', 'TotalAlerts']]
default_columns_of_dataframe = [col for col in columns_of_dataframe if col not in ['AccountId', 'TotalUsers',	'QttUserReference','QttUserWithAlerts', 'TotalAlerts','AlertDescription']]

criterias_cols = st.sidebar.multiselect('1. Select fields that will prioritize the accounts:',columns_of_available,  default_columns_of_dataframe)

st.sidebar.write('You selected fields: ', ", ".join(str(item) for item in criterias_cols), 'for prioritization.')


filtered_df = df.copy()
filtered_df = filtered_df[filtered_df['TotalAlerts'] >0]

if 'MRR' in  criterias_cols and 'TotalUsers' not in criterias_cols and 'AlertDescription' not in criterias_cols and 'UsersWithAlertPerc' not in criterias_cols: 
    st.sidebar.title('High Priority Criteria')
    mrr_high_selected = st.sidebar.slider('Select the interval of MRR that is considered high priority:', min_value=df['MRR'].min(), max_value =df['MRR'].max(), value=(df['MRR'].quantile(q=.75).astype(int), df['MRR'].max()))
    
    st.sidebar.title('Medium Priority Criteria')
    mrr_medium_selected = st.sidebar.slider('Select the interval of MRR that is considered medium priority:', min_value=df['MRR'].min(), max_value =df['MRR'].max(), value=(df['MRR'].quantile(q=.25).astype(int), mrr_high_selected[0]))

    filtered_df['AlertPriority'] = np.where((filtered_df['MRR'] >= mrr_high_selected[0]) & (filtered_df['MRR'] <= mrr_high_selected[1]), "1 - High",
                                   np.where((filtered_df['MRR'] < mrr_high_selected[0]) & (filtered_df['MRR'] >= mrr_medium_selected[0]), "2 - Medium", 
                                   "3 - Low"))

elif 'MRR' not in  criterias_cols and 'TotalUsers' in criterias_cols and 'AlertDescription' not in criterias_cols and 'UsersWithAlertPerc' not in criterias_cols:
    st.sidebar.title('High Priority Criteria')
    total_users_high_selected = st.sidebar.slider('Select the interval of total users that is considered high priority:', min_value=df['TotalUsers'].min(), max_value=df['TotalUsers'].max(), value=(df['TotalUsers'].quantile(q=.75).astype(int), df['TotalUsers'].max()))

    st.sidebar.title('Medium Priority Criteria')
    total_users_medium_selected = st.sidebar.slider('Select the interval of total users that is considered medium priority:', min_value=df['TotalUsers'].min(), max_value=df['TotalUsers'].max(), value=(df['TotalUsers'].quantile(q=.25).astype(int), total_users_high_selected[0]))


    filtered_df['AlertPriority'] = np.where((filtered_df['TotalUsers'] >= total_users_high_selected[0]) & (filtered_df['TotalUsers'] <= total_users_high_selected[1]), "1 - High", 
                                   np.where((filtered_df['TotalUsers'] < total_users_high_selected[0]) & (filtered_df['TotalUsers'] >= total_users_medium_selected[0]), "2 - Medium",
                                   "3 - Low"))

elif 'MRR' not in  criterias_cols and 'TotalUsers' not in criterias_cols and 'AlertDescription' in criterias_cols and 'UsersWithAlertPerc' not in criterias_cols:
    st.sidebar.title('High Priority Criteria')
    alert_description_high_selected = st.sidebar.multiselect('Select the alert description that is considered high priority:', df['AlertDescription'].unique())

    st.sidebar.title('Medium Priority Criteria')
    alert_description_medium_selected = st.sidebar.multiselect('Select the alert description that is considered medium priority:', df['AlertDescription'].unique())
    
    filtered_df['AlertPriority'] = np.where(filtered_df['AlertDescription'].isin(alert_description_high_selected), "1 - High", 
                                   np.where(filtered_df['AlertDescription'].isin(alert_description_medium_selected), "2 - Medium",
                                   "3 - Low"))

elif 'MRR' not in  criterias_cols and 'TotalUsers' not in criterias_cols and 'AlertDescription' not in criterias_cols and 'UsersWithAlertPerc' in criterias_cols:
    st.sidebar.title('High Priority Criteria')
    users_with_alert_high_perc = st.sidebar.slider('Select the interval of users with alerts percentage that is considered high priority:', min_value=df['UsersWithAlertPerc'].min(), max_value=df['UsersWithAlertPerc'].max(), value=(70.00,100.00))

    st.sidebar.title('Medium Priority Criteria')
    users_with_alert_medium_perc = st.sidebar.slider('Select the interval of users with alerts percentage that is considered medium priority:', min_value=df['UsersWithAlertPerc'].min(), max_value=df['UsersWithAlertPerc'].max(), value=(30.00,users_with_alert_high_perc[0]))

    filtered_df['AlertPriority'] = np.where((filtered_df['UsersWithAlertPerc'] >= users_with_alert_high_perc[0]) & (filtered_df['UsersWithAlertPerc'] <= users_with_alert_high_perc[1]), "1 - High", 
                                   np.where((filtered_df['UsersWithAlertPerc'] < users_with_alert_high_perc[0]) & (filtered_df['UsersWithAlertPerc'] <= users_with_alert_medium_perc[0]), "2 - Medium",
                                   "3 - Low"))

elif 'MRR' in  criterias_cols and 'TotalUsers' in criterias_cols and 'AlertDescription' not in criterias_cols and 'UsersWithAlertPerc' not in criterias_cols: 
    st.sidebar.title('High Priority Criteria')
    mrr_high_selected = st.sidebar.slider('Select the interval of MRR that is considered high priority:', min_value=df['MRR'].min(), max_value =df['MRR'].max(), value=(df['MRR'].quantile(q=.75).astype(int), df['MRR'].max()))
    total_users_high_selected = st.sidebar.slider('Select the interval of total users that is considered high priority:', min_value=df['TotalUsers'].min(), max_value=df['TotalUsers'].max(), value=(df['TotalUsers'].quantile(q=.75).astype(int), df['TotalUsers'].max()))

    st.sidebar.title('Medium Priority Criteria')
    mrr_medium_selected = st.sidebar.slider('Select the interval of MRR that is considered medium priority:', min_value=df['MRR'].min(), max_value =df['MRR'].max(), value=(df['MRR'].quantile(q=.25).astype(int), mrr_high_selected[0]))
    total_users_medium_selected = st.sidebar.slider('Select the interval of total users that is considered medium priority:', min_value=df['TotalUsers'].min(), max_value=df['TotalUsers'].max(), value=(df['TotalUsers'].quantile(q=.25).astype(int), total_users_high_selected[0]))

    filtered_df['AlertPriority'] = np.where((filtered_df['MRR'] >= mrr_high_selected[0]) & (filtered_df['MRR'] <= mrr_high_selected[1]), "1 - High",
                                   np.where((filtered_df['TotalUsers'] >= total_users_high_selected[0]) & (filtered_df['TotalUsers'] <= total_users_high_selected[1]), "1 - High",
                                   np.where((filtered_df['MRR'] < mrr_high_selected[0]) & (filtered_df['MRR'] >= mrr_medium_selected[0]), "2 - Medium",
                                   np.where((filtered_df['TotalUsers'] < total_users_high_selected[0]) & (filtered_df['TotalUsers'] >= total_users_medium_selected[0]), "2 - Medium",
                                   "3 - Low"))))

elif 'MRR' in  criterias_cols and 'TotalUsers' not in criterias_cols and 'AlertDescription' in criterias_cols and 'UsersWithAlertPerc' not in criterias_cols: 
    st.sidebar.title('High Priority Criteria')
    mrr_high_selected = st.sidebar.slider('Select the interval of MRR that is considered high priority:', min_value=df['MRR'].min(), max_value =df['MRR'].max(), value=(df['MRR'].quantile(q=.75).astype(int), df['MRR'].max()))
    alert_description_high_selected = st.sidebar.multiselect('Select the alert description that is considered high priority:', df['AlertDescription'].unique())

    st.sidebar.title('Medium Priority Criteria')
    mrr_medium_selected = st.sidebar.slider('Select the interval of MRR that is considered medium priority:', min_value=df['MRR'].min(), max_value =df['MRR'].max(), value=(df['MRR'].quantile(q=.25).astype(int), mrr_high_selected[0]))
    alert_description_medium_selected = st.sidebar.multiselect('Select the alert description that is considered medium priority:', df['AlertDescription'].unique())

    filtered_df['AlertPriority'] = np.where((filtered_df['MRR'] >= mrr_high_selected[0]) & (filtered_df['MRR'] <= mrr_high_selected[1]), "1 - High",
                                   np.where(filtered_df['AlertDescription'].isin(alert_description_high_selected), "1 - High",
                                   np.where((filtered_df['MRR'] < mrr_high_selected[0]) & (filtered_df['MRR'] >= mrr_medium_selected[0]), "2 - Medium",
                                   np.where(filtered_df['AlertDescription'].isin(alert_description_medium_selected), "2 - Medium",
                                   "3 - Low"))))

elif 'MRR' in  criterias_cols and 'TotalUsers' not in criterias_cols and 'AlertDescription' not in criterias_cols and 'UsersWithAlertPerc' in criterias_cols: 
    st.sidebar.title('High Priority Criteria')
    mrr_high_selected = st.sidebar.slider('Select the interval of MRR that is considered high priority:', min_value=df['MRR'].min(), max_value =df['MRR'].max(), value=(df['MRR'].quantile(q=.75).astype(int), df['MRR'].max()))
    users_with_alert_high_perc = st.sidebar.slider('Select the interval of users with alerts percentage that is considered high priority:', min_value=df['UsersWithAlertPerc'].min(), max_value=df['UsersWithAlertPerc'].max(), value=(70.00,100.00))

    st.sidebar.title('Medium Priority Criteria')
    mrr_medium_selected = st.sidebar.slider('Select the interval of MRR that is considered medium priority:', min_value=df['MRR'].min(), max_value =df['MRR'].max(), value=(df['MRR'].quantile(q=.25).astype(int), mrr_high_selected[0]))
    users_with_alert_medium_perc = st.sidebar.slider('Select the interval of users with alerts percentage that is considered medium priority:', min_value=df['UsersWithAlertPerc'].min(), max_value=df['UsersWithAlertPerc'].max(), value=(30.00,users_with_alert_high_perc[0]))

    filtered_df['AlertPriority'] = np.where((filtered_df['MRR'] >= mrr_high_selected[0]) & (filtered_df['MRR'] <= mrr_high_selected[1]), "1 - High",
                                   np.where((filtered_df['UsersWithAlertPerc'] >= users_with_alert_high_perc[0]) & (filtered_df['UsersWithAlertPerc'] <= users_with_alert_high_perc[1]), "1 - High",
                                   np.where((filtered_df['MRR'] < mrr_high_selected[0]) & (filtered_df['MRR'] >= mrr_medium_selected[1]), "2 - Medium",
                                   np.where((filtered_df['UsersWithAlertPerc'] < users_with_alert_high_perc[0]) & (filtered_df['UsersWithAlertPerc'] >= users_with_alert_medium_perc[0]), "2 - Medium",
                                   "3 - Low"))))

elif 'MRR' in  criterias_cols and 'TotalUsers' in criterias_cols and 'AlertDescription' in criterias_cols and 'UsersWithAlertPerc' not in criterias_cols: 
    st.sidebar.title('High Priority Criteria')
    mrr_high_selected = st.sidebar.slider('Select the interval of MRR that is considered high priority:', min_value=df['MRR'].min(), max_value =df['MRR'].max(), value=(df['MRR'].quantile(q=.75).astype(int), df['MRR'].max()))
    total_users_high_selected = st.sidebar.slider('Select the interval of total users that is considered high priority:', min_value=df['TotalUsers'].min(), max_value=df['TotalUsers'].max(), value=(df['TotalUsers'].quantile(q=.75).astype(int), df['TotalUsers'].max()))
    alert_description_high_selected = st.sidebar.multiselect('Select the alert description that is considered high priority:', df['AlertDescription'].unique())

    st.sidebar.title('Medium Priority Criteria')
    mrr_medium_selected = st.sidebar.slider('Select the interval of MRR that is considered medium priority:', min_value=df['MRR'].min(), max_value =df['MRR'].max(), value=(df['MRR'].quantile(q=.25).astype(int), mrr_high_selected[0]))
    total_users_medium_selected = st.sidebar.slider('Select the interval of total users that is considered medium priority:', min_value=df['TotalUsers'].min(), max_value=df['TotalUsers'].max(), value=(df['TotalUsers'].quantile(q=.25).astype(int), total_users_high_selected[0]))
    alert_description_medium_selected = st.sidebar.multiselect('Select the alert description that is considered medium priority:', df['AlertDescription'].unique())


    filtered_df['AlertPriority'] = np.where((filtered_df['MRR'] >= mrr_high_selected[0]) & (filtered_df['MRR'] <= mrr_high_selected[1]), "1 - High",
                                   np.where((filtered_df['TotalUsers'] >= total_users_high_selected[0]) & (filtered_df['TotalUsers'] <= total_users_high_selected[1]), "1 - High",
                                   np.where(filtered_df['AlertDescription'].isin(alert_description_high_selected), "1 - High",
                                   np.where((filtered_df['MRR'] < mrr_high_selected[0]) & (filtered_df['MRR'] >= mrr_medium_selected[0]), "2 - Medium",
                                   np.where((filtered_df['TotalUsers'] < total_users_high_selected[0]) & (filtered_df['TotalUsers'] >= total_users_medium_selected[0]), "2 - Medium",
                                   np.where(filtered_df['AlertDescription'].isin(alert_description_medium_selected), "2 - Medium",
                                   "3 - Low"))))))

elif 'MRR' in  criterias_cols and 'TotalUsers' in criterias_cols and 'AlertDescription' not in criterias_cols and 'UsersWithAlertPerc' in criterias_cols: 
    st.sidebar.title('High Priority Criteria')
    mrr_high_selected = st.sidebar.slider('Select the interval of MRR that is considered high priority:', min_value=df['MRR'].min(), max_value =df['MRR'].max(), value=(df['MRR'].quantile(q=.75).astype(int), df['MRR'].max()))
    total_users_high_selected = st.sidebar.slider('Select the interval of total users that is considered high priority:', min_value=df['TotalUsers'].min(), max_value=df['TotalUsers'].max(), value=(df['TotalUsers'].quantile(q=.75).astype(int), df['TotalUsers'].max()))
    users_with_alert_high_perc = st.sidebar.slider('Select the interval of users with alerts percentage that is considered high priority:', min_value=df['UsersWithAlertPerc'].min(), max_value=df['UsersWithAlertPerc'].max(), value=(70.00,100.00))

    st.sidebar.title('Medium Priority Criteria')
    mrr_medium_selected = st.sidebar.slider('Select the interval of MRR that is considered medium priority:', min_value=df['MRR'].min(), max_value =df['MRR'].max(), value=(df['MRR'].quantile(q=.25).astype(int), mrr_high_selected[0]))
    total_users_medium_selected = st.sidebar.slider('Select the interval of total users that is considered medium priority:', min_value=df['TotalUsers'].min(), max_value=df['TotalUsers'].max(), value=(df['TotalUsers'].quantile(q=.25).astype(int), total_users_high_selected[0]))
    users_with_alert_medium_perc = st.sidebar.slider('Select the interval of users with alerts percentage that is considered medium priority:', min_value=df['UsersWithAlertPerc'].min(), max_value=df['UsersWithAlertPerc'].max(), value=(30.00,users_with_alert_high_perc[0]))

    filtered_df['AlertPriority'] = np.where((filtered_df['MRR'] >= mrr_high_selected[0]) & (filtered_df['MRR'] <= mrr_high_selected[1]), "1 - High",
                                   np.where((filtered_df['TotalUsers'] >= total_users_high_selected[0]) & (filtered_df['TotalUsers'] <= total_users_high_selected[1]), "1 - High",
                                   np.where((filtered_df['UsersWithAlertPerc'] >= users_with_alert_high_perc[0]) & (filtered_df['UsersWithAlertPerc'] <= users_with_alert_high_perc[1]), "1 - High", 
                                   np.where((filtered_df['MRR'] < mrr_high_selected[0]) & (filtered_df['MRR'] >= mrr_medium_selected[0]), "2 - Medium",
                                   np.where((filtered_df['TotalUsers'] < total_users_high_selected[0]) & (filtered_df['TotalUsers'] >= total_users_high_selected[0]), "2 - Medium",
                                   np.where((filtered_df['UsersWithAlertPerc'] < users_with_alert_high_perc[0]) & (filtered_df['UsersWithAlertPerc'] >= users_with_alert_high_perc[0]), "2 - Medium", 
                                   "3 - Low"))))))

elif 'MRR' in  criterias_cols and 'TotalUsers' not in criterias_cols and 'AlertDescription' in criterias_cols and 'UsersWithAlertPerc' in criterias_cols: 
    st.sidebar.title('High Priority Criteria')
    mrr_high_selected = st.sidebar.slider('Select the interval of MRR that is considered high priority:', min_value=df['MRR'].min(), max_value =df['MRR'].max(), value=(df['MRR'].quantile(q=.75).astype(int), df['MRR'].max()))
    alert_description_high_selected = st.sidebar.multiselect('Select the alert description that is considered high priority:', df['AlertDescription'].unique())
    users_with_alert_high_perc = st.sidebar.slider('Select the interval of users with alerts percentage that is considered high priority:', min_value=df['UsersWithAlertPerc'].min(), max_value=df['UsersWithAlertPerc'].max(), value=(70.00,100.00))

    st.sidebar.title('Medium Priority Criteria')
    mrr_medium_selected = st.sidebar.slider('Select the interval of MRR that is considered medium priority:', min_value=df['MRR'].min(), max_value =df['MRR'].max(), value=(df['MRR'].quantile(q=.25).astype(int), mrr_high_selected[0]))
    alert_description_medium_selected = st.sidebar.multiselect('Select the alert description that is considered medium priority:', df['AlertDescription'].unique())
    users_with_alert_medium_perc = st.sidebar.slider('Select the interval of users with alerts percentage that is considered medium priority:', min_value=df['UsersWithAlertPerc'].min(), max_value=df['UsersWithAlertPerc'].max(), value=(30.00,users_with_alert_high_perc[0]))


    filtered_df['AlertPriority'] = np.where((filtered_df['MRR'] >= mrr_high_selected[0]) & (filtered_df['MRR'] <= mrr_high_selected[1]), "1 - High",
                                   np.where(filtered_df['AlertDescription'].isin(alert_description_high_selected), "1 - High",
                                   np.where((filtered_df['UsersWithAlertPerc'] >= users_with_alert_high_perc[0]) & (filtered_df['UsersWithAlertPerc'] <= users_with_alert_high_perc[1]), "1 - High", 
                                   np.where((filtered_df['MRR'] < mrr_high_selected[0]) & (filtered_df['MRR'] >= mrr_medium_selected[0]), "2 - Medium",
                                   np.where(filtered_df['AlertDescription'].isin(alert_description_medium_selected), "2 - Medium",
                                   np.where((filtered_df['UsersWithAlertPerc'] < users_with_alert_high_perc[0]) & (filtered_df['UsersWithAlertPerc'] >= users_with_alert_medium_perc[1]), "2 - Medium", 
                                   "3 - Low"))))))

elif 'MRR' not in  criterias_cols and 'TotalUsers' in criterias_cols and 'AlertDescription' in criterias_cols and 'UsersWithAlertPerc' not in criterias_cols: 
    st.sidebar.title('High Priority Criteria')
    total_users_high_selected = st.sidebar.slider('Select the interval of total users that is considered high priority:', min_value=df['TotalUsers'].min(), max_value=df['TotalUsers'].max(), value=(df['TotalUsers'].quantile(q=.75).astype(int), df['TotalUsers'].max()))
    alert_description_high_selected = st.sidebar.multiselect('Select the alert description that is considered high priority:', df['AlertDescription'].unique())

    st.sidebar.title('Medium Priority Criteria')
    total_users_medium_selected = st.sidebar.slider('Select the interval of total users that is considered medium priority:', min_value=df['TotalUsers'].min(), max_value=df['TotalUsers'].max(), value=(df['TotalUsers'].quantile(q=.25).astype(int), total_users_high_selected[0]))
    alert_description_medium_selected = st.sidebar.multiselect('Select the alert description that is considered medium priority:', df['AlertDescription'].unique())

    filtered_df['AlertPriority'] = np.where((filtered_df['TotalUsers'] >= total_users_high_selected[0]) & (filtered_df['TotalUsers'] <= total_users_high_selected[1]), "1 - High",
                                   np.where(filtered_df['AlertDescription'].isin(alert_description_high_selected), "1 - High",
                                   np.where((filtered_df['TotalUsers'] < total_users_high_selected[0]) & (filtered_df['TotalUsers'] >= total_users_medium_selected[0]), "2 - Medium",
                                   np.where(filtered_df['AlertDescription'].isin(alert_description_medium_selected), "2 - Medium",
                                   "3 - Low"))))

elif 'MRR' not in  criterias_cols and 'TotalUsers' in criterias_cols and 'AlertDescription' not in criterias_cols and 'UsersWithAlertPerc' in criterias_cols: 
    st.sidebar.title('High Priority Criteria')
    total_users_high_selected = st.sidebar.slider('Select the interval of total users that is considered high priority:', min_value=df['TotalUsers'].min(), max_value=df['TotalUsers'].max(), value=(df['TotalUsers'].quantile(q=.75).astype(int), df['TotalUsers'].max()))
    users_with_alert_high_perc = st.sidebar.slider('Select the interval of users with alerts percentage that is considered high priority:', min_value=df['UsersWithAlertPerc'].min(), max_value=df['UsersWithAlertPerc'].max(), value=(70.00,100.00))

    st.sidebar.title('Medium Priority Criteria')
    total_users_medium_selected = st.sidebar.slider('Select the interval of total users that is considered medium priority:', min_value=df['TotalUsers'].min(), max_value=df['TotalUsers'].max(), value=(df['TotalUsers'].quantile(q=.25).astype(int), total_users_high_selected[0]))
    users_with_alert_medium_perc = st.sidebar.slider('Select the interval of users with alerts percentage that is considered medium priority:', min_value=df['UsersWithAlertPerc'].min(), max_value=df['UsersWithAlertPerc'].max(), value=(30.00,users_with_alert_high_perc[0]))

    filtered_df['AlertPriority'] = np.where((filtered_df['TotalUsers'] >= total_users_high_selected[0]) & (filtered_df['TotalUsers'] <= total_users_high_selected[1]), "1 - High",
                                   np.where((filtered_df['UsersWithAlertPerc'] >= users_with_alert_high_perc[0]) & (filtered_df['UsersWithAlertPerc'] <= users_with_alert_high_perc[1]), "1 - High", 
                                   np.where((filtered_df['TotalUsers'] < total_users_high_selected[0]) & (filtered_df['TotalUsers'] >= total_users_medium_selected[0]), "2 - Medium",
                                   np.where((filtered_df['UsersWithAlertPerc'] < users_with_alert_high_perc[0]) & (filtered_df['UsersWithAlertPerc'] >= users_with_alert_medium_perc[0]), "2 - Medium", 
                                   "3 - Low"))))

elif 'MRR' not in  criterias_cols and 'TotalUsers' in criterias_cols and 'AlertDescription' in criterias_cols and 'UsersWithAlertPerc' in criterias_cols: 
    st.sidebar.title('High Priority Criteria')
    total_users_high_selected = st.sidebar.slider('Select the interval of total users that is considered high priority:', min_value=df['TotalUsers'].min(), max_value=df['TotalUsers'].max(), value=(df['TotalUsers'].quantile(q=.75).astype(int), df['TotalUsers'].max()))
    alert_description_high_selected = st.sidebar.multiselect('Select the alert description that is considered high priority:', df['AlertDescription'].unique())
    users_with_alert_high_perc = st.sidebar.slider('Select the interval of users with alerts percentage that is considered high priority:', min_value=df['UsersWithAlertPerc'].min(), max_value=df['UsersWithAlertPerc'].max(), value=(70.00,100.00))

    st.sidebar.title('Medium Priority Criteria')
    total_users_medium_selected = st.sidebar.slider('Select the interval of total users that is considered medium priority:', min_value=df['TotalUsers'].min(), max_value=df['TotalUsers'].max(), value=(df['TotalUsers'].quantile(q=.25).astype(int), total_users_high_selected[0]))
    alert_description_medium_selected = st.sidebar.multiselect('Select the alert description that is considered medium priority:', df['AlertDescription'].unique())
    users_with_alert_medium_perc = st.sidebar.slider('Select the interval of users with alerts percentage that is considered medium priority:', min_value=df['UsersWithAlertPerc'].min(), max_value=df['UsersWithAlertPerc'].max(), value=(30.00,users_with_alert_high_perc[0]))

    filtered_df['AlertPriority'] = np.where((filtered_df['TotalUsers'] >= total_users_high_selected[0]) & (filtered_df['TotalUsers'] <= total_users_high_selected[1]), "1 - High",
                                   np.where(filtered_df['AlertDescription'].isin(alert_description_high_selected), "1 - High",
                                   np.where((filtered_df['UsersWithAlertPerc'] >= users_with_alert_high_perc[0]) & (filtered_df['UsersWithAlertPerc'] <= users_with_alert_high_perc[1]), "1 - High", 
                                   np.where((filtered_df['TotalUsers'] < total_users_high_selected[0]) & (filtered_df['TotalUsers'] >= total_users_medium_selected[0]), "2 - Medium",
                                   np.where(filtered_df['AlertDescription'].isin(alert_description_medium_selected), "2 - Medium",
                                   np.where((filtered_df['UsersWithAlertPerc'] < users_with_alert_high_perc[0]) & (filtered_df['UsersWithAlertPerc'] >= users_with_alert_medium_perc[0]), "2 - Medium", 
                                   "3 - Low"))))))

elif 'MRR' not in  criterias_cols and 'TotalUsers' not in criterias_cols and 'AlertDescription' in criterias_cols and 'UsersWithAlertPerc' in criterias_cols:
    st.sidebar.title('High Priority Criteria')
    alert_description_high_selected = st.sidebar.multiselect('Select the alert description that is considered high priority:', df['AlertDescription'].unique())
    users_with_alert_high_perc = st.sidebar.slider('Select the interval of users with alerts percentage that is considered high priority:', min_value=df['UsersWithAlertPerc'].min(), max_value=df['UsersWithAlertPerc'].max(), value=(70.00,100.00))

    st.sidebar.title('Medium Priority Criteria')
    alert_description_medium_selected = st.sidebar.multiselect('Select the alert description that is considered medium priority:', df['AlertDescription'].unique())
    users_with_alert_medium_perc = st.sidebar.slider('Select the interval of users with alerts percentage that is considered medium priority:', min_value=df['UsersWithAlertPerc'].min(), max_value=df['UsersWithAlertPerc'].max(), value=(30.00,users_with_alert_high_perc[0]))

    filtered_df['AlertPriority'] = np.where(filtered_df['AlertDescription'].isin(alert_description_high_selected), "1 - High",
                                   np.where((filtered_df['UsersWithAlertPerc'] >= users_with_alert_high_perc[0]) & (filtered_df['UsersWithAlertPerc'] <= users_with_alert_high_perc[1]), "1 - High", 
                                   np.where(filtered_df['AlertDescription'].isin(alert_description_medium_selected), "2 - Medium",
                                   np.where((filtered_df['UsersWithAlertPerc'] < users_with_alert_high_perc[0]) & (filtered_df['UsersWithAlertPerc'] >= users_with_alert_medium_perc[0]), "2 - Medium", 
                                   "3 - Low"))))

elif 'MRR' in  criterias_cols and 'TotalUsers' in criterias_cols and 'AlertDescription' in criterias_cols and 'UsersWithAlertPerc' in criterias_cols: 
    st.sidebar.title('High Priority Criteria')
    mrr_high_selected = st.sidebar.slider('Select the interval of MRR that is considered high priority:', min_value=df['MRR'].min(), max_value =df['MRR'].max(), value=(df['MRR'].quantile(q=.75).astype(int), df['MRR'].max()))
    total_users_high_selected = st.sidebar.slider('Select the interval of total users that is considered high priority:', min_value=df['TotalUsers'].min(), max_value=df['TotalUsers'].max(), value=(df['TotalUsers'].quantile(q=.75).astype(int), df['TotalUsers'].max()))
    alert_description_high_selected = st.sidebar.multiselect('Select the alert description that is considered high priority:', df['AlertDescription'].unique())
    users_with_alert_high_perc = st.sidebar.slider('Select the interval of users with alerts percentage that is considered high priority:', min_value=df['UsersWithAlertPerc'].min(), max_value=df['UsersWithAlertPerc'].max(), value=(70.00,100.00))

    st.sidebar.title('Medium Priority Criteria')
    mrr_medium_selected = st.sidebar.slider('Select the interval of MRR that is considered medium priority:', min_value=df['MRR'].min(), max_value =df['MRR'].max(), value=(df['MRR'].quantile(q=.25).astype(int), mrr_high_selected[0]))
    total_users_medium_selected = st.sidebar.slider('Select the interval of total users that is considered medium priority:', min_value=df['TotalUsers'].min(), max_value=df['TotalUsers'].max(), value=(df['TotalUsers'].quantile(q=.25).astype(int), total_users_high_selected[0]))
    alert_description_medium_selected = st.sidebar.multiselect('Select the alert description that is considered medium priority:', df['AlertDescription'].unique())
    users_with_alert_medium_perc = st.sidebar.slider('Select the interval of users with alerts percentage that is considered medium priority:', min_value=df['UsersWithAlertPerc'].min(), max_value=df['UsersWithAlertPerc'].max(), value=(30.00,users_with_alert_high_perc[0]))
    
    filtered_df['AlertPriority'] = np.where((filtered_df['MRR'] >= mrr_high_selected[0]) & (filtered_df['MRR'] <= mrr_high_selected[1]), "1 - High",
                                   np.where((filtered_df['TotalUsers'] >= total_users_high_selected[0]) & (filtered_df['TotalUsers'] <= total_users_high_selected[1]), "1 - High",
                                   np.where(filtered_df['AlertDescription'].isin(alert_description_high_selected), "1 - High",
                                   np.where((filtered_df['UsersWithAlertPerc'] >= users_with_alert_high_perc[0]) & (filtered_df['UsersWithAlertPerc'] <= users_with_alert_high_perc[1]), "1 - High", 
                                   np.where((filtered_df['MRR'] < mrr_high_selected[0]) & (filtered_df['MRR'] >= mrr_medium_selected[0]), "2 - Medium",
                                   np.where((filtered_df['TotalUsers'] < total_users_high_selected[0]) & (filtered_df['TotalUsers'] >= total_users_medium_selected[0]), "2 - Medium",
                                   np.where(filtered_df['AlertDescription'].isin(alert_description_medium_selected), "2 - Medium",
                                   np.where((filtered_df['UsersWithAlertPerc'] < users_with_alert_high_perc[0]) & (filtered_df['UsersWithAlertPerc'] >= users_with_alert_medium_perc[0]), "2 - Medium", 
                                   "3 - Low"))))))))

header_table = st.header("Table with applied filters :clipboard:", divider = "gray")
gb = GridOptionsBuilder.from_dataframe(filtered_df)
gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=50) #Add pagination
gb.configure_side_bar() #Add a sidebar
gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
gridOptions = gb.build()

grid_response = AgGrid(
    filtered_df,
    gridOptions=gridOptions,
    #data_return_mode='AS_INPUT',
    update_mode='MODEL_CHANGED',
    fit_columns_on_grid_load=False,
    theme='streamlit', #Add theme color to the table
    enable_enterprise_modules=True,
    height=350,
    width='100%',
    reload_data=True,
    custom_css={"#gridToolBar": {"padding-bottom": "0px !important"}},
    data_return_mode = DataReturnMode.FILTERED_AND_SORTED)

qtt_accounts_with_high_alerts = filtered_df[filtered_df['AlertPriority']=='1 - High']['AccountId'].nunique()
qtt_accounts_with_medium_alerts = filtered_df[filtered_df['AlertPriority']=='2 - Medium']['AccountId'].nunique()
qtt_accounts_with_low_alerts = filtered_df[filtered_df['AlertPriority']=='3 - Low']['AccountId'].nunique()

qtt_alerts_with_high_alerts = filtered_df[filtered_df['AlertPriority']=='1 - High']['TotalAlerts'].sum()
qtt_alerts_with_medium_alerts = filtered_df[filtered_df['AlertPriority']=='2 - Medium']['TotalAlerts'].sum()
qtt_alerts_with_low_alerts = filtered_df[filtered_df['AlertPriority']=='3 - Low']['TotalAlerts'].sum()

header_main = st.header("Metrics :bar_chart:", divider="gray")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<h1 style="color:#dc2626;font-size:24px;">{"1 - High"}</h3>', unsafe_allow_html=True)
    st.metric("Num. Accounts", qtt_accounts_with_high_alerts)
    st.metric("Qtt. Alerts", qtt_alerts_with_high_alerts)
with col2:
    st.markdown(f'<h1 style="color:#FDD835;font-size:24px;">{"2 - Medium"}</h3>', unsafe_allow_html=True)
    st.metric("Num. Accounts", qtt_accounts_with_medium_alerts)
    st.metric("Qtt. Alerts", qtt_alerts_with_medium_alerts)
with col3:
    st.markdown(f'<h1 style="color:#957EBE;font-size:24px;">{"3 - Low"}</h3>', unsafe_allow_html=True)
    st.metric("Num. Accounts", qtt_accounts_with_low_alerts)
    st.metric("Qtt. Alerts", qtt_alerts_with_low_alerts)

# st.bar_chart(filtered_df, x="AlertDescription", y="TotalAlerts", stack=False)
fig = px.bar(filtered_df, x="AlertDescription", y="TotalAlerts", color="AlertDescription")
st.plotly_chart(fig)

