import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
from datetime import time

def create_connection():#connecting into mysql database
    return mysql.connector.connect(host="localhost",
    user="root",
    password="dh@rsh73",
    auth_plugin="mysql_native_password",
    database='busdata'
    )
connection=create_connection()
st.title('🚌 **RedBus Booking Details**')

#defining bus_route and displaing it in selectbox 
        
def get_bus_routes(conn):
    query = "SELECT DISTINCT Route_Name FROM bus_routes"
    return pd.read_sql(query, conn)['Route_Name'].tolist()

bus_route = get_bus_routes(connection)#defining bus route
route_name = st.selectbox("Enter Route Name:",bus_route)#to display in a selectbox

#defining the price and star rating range
price_range = st.slider("Choose Price Range:", min_value=0.0, max_value=5000.0, value=(0.0, 100.0), format="%100f")# display in a slider
star_rating_range = st.slider("**Select Star Rating Range:**" , min_value=0.0, max_value=5.0, value=(0.0, 1.0), format="%.1f")# display in a slider

#defining bustype and displaying it in a selectbox
def get_bus_type(connection,price_range,star_rating_range):
    
    query=f"""
         Select Bustype 
         FROM bus_routes 
         WHERE Price BETWEEN %s AND %s
         AND Star_rating BETWEEN %s AND %s;
         """
    return pd.read_sql(query,connection,params=(price_range[0],price_range[1], star_rating_range[0], star_rating_range[1]))['Bustype'].tolist()

bus_type=get_bus_type(connection,price_range,star_rating_range)
Bustype=st.selectbox("**Select a Bustype**",bus_type)#to display in a selectbox

          
#defining departing_time
def get_departing_time(connection):
    query = f"SELECT Departing_time FROM bus_routes"
    return pd.read_sql(query,connection)['Departing_time'].tolist()
departing_time=get_departing_time(connection)


#defining duration   
def get_duration(connection):
    query = f"SELECT Duration FROM bus_routes"
    return pd.read_sql(query, connection)['Duration'].tolist()
duration=get_duration(connection)


#defining reaching_time
def get_reaching_time(connection):
    query = f"SELECT Reaching_time FROM bus_routes"
    return pd.read_sql(query, connection)['Reaching_time'].tolist()
reaching_time=get_reaching_time(connection)


#defining seats_available
def get_seat_available(connection):
    query=f"SELECT Seats_available FROM bus_routes"
    return pd.read_sql(query,connection)['Seats_available'].tolist()
seats_available=get_seat_available(connection)


#defining busname
def get_bus_name(connection,route_name,price_range,star_rating_range ):
    
    query = """
        SELECT Busname,Price,Departing_time,Duration,Reaching_time,Seats_available
        FROM bus_routes
        WHERE Route_Name = %s
        AND Price BETWEEN %s AND %s
        AND Star_rating BETWEEN %s AND %s;
        """
    return pd.read_sql(query,connection, params=(route_name, price_range[0],price_range[1], star_rating_range[0], star_rating_range[1])) 

bus_name=get_bus_name(connection,route_name,price_range,star_rating_range)



df=pd.DataFrame(bus_name)
st.dataframe(df)
connection.close()
