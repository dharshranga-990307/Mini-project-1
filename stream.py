#importing libaries
import streamlit as st
import mysql.connector
import pandas as pd




#connecting to mysql database
connection=mysql.connector.connect(host="localhost",
    user="root",
    password="dh@rsh73",
    auth_plugin="mysql_native_password",
    database='redbus'
    )
mycursor=connection.cursor()

#defining the parameters

def get_state(mycursor):
    sql="SELECT DISTINCT States from bus_routes ORDER BY States"
    mycursor.execute(sql)
    data=mycursor.fetchall()
    state_names = [name[0] for name in data]
    return(state_names)
    

def get_bus_routes(mycursor,state_sb):

    sql="SELECT Distinct Route_Name FROM bus_routes WHERE States = %s ORDER BY Route_name"
    mycursor.execute(sql, (state_sb,))#executing the sql query
    data=mycursor.fetchall() #fetching the details
    route_names = [route[0] for route in data]
    return(route_names)

def get_bus_type(mycursor,route_name,price_range,star_rating_range):
    mycursor=connection.cursor()
    sql="""
         Select DISTINCT Bus_type 
         FROM bus_routes
         WHERE Route_name =%s 
         AND Price BETWEEN %s AND %s
         AND Star_rating BETWEEN %s AND %s;
    """
    params = ( route_name, price_range[0], price_range[1], star_rating_range[0], star_rating_range[1])#passing the parameters with respect to each %s value
    mycursor.execute(sql,params)#executing the sql query
    data=mycursor.fetchall()#fetching the details
    bus_types = [type[0] for type in data]
    return(bus_types)

  
       
def get_details(mycursor,state_sb,route_name,price_range,star_rating_range,Dept,Seats):
    mycursor=connection.cursor()
    sql = """
        SELECT * 
        FROM bus_routes
        WHERE States=%s
        AND Route_name =%s
        AND Price BETWEEN %s AND %s
        AND Star_rating BETWEEN %s AND %s
        AND Departing_time =%s
        AND Seats_available BETWEEN %s AND %s
        """
        
    
    seats_min, seats_max = Seats
    params=state_sb,route_name,price_range[0],price_range[1],star_rating_range[0], star_rating_range[1],Dept,seats_min,seats_max
    
    mycursor.execute(sql,params)
    data=mycursor.fetchall()
    columns = mycursor.column_names
    return pd.DataFrame(data, columns=columns)

#streamlit application

#assigning the title for the page
st.sidebar.title('Navigation')

#dividing the pages into three tabs Home,Booking page,About me
selection=st.sidebar.radio('Go to',['Home','Booking Page','About Me'])

#Writing for first page
if selection == 'Home':
    st.title('**RedBus Site**')
    st.write("**India's No. 1 Online Bus Ticket Booking Site**")
    st.image(r"C:\Users\Dharshinee R\Desktop\108561103.webp",use_column_width=True)
    st.write("RedBus is the world's largest online bus ticket booking service trusted by over 25 million happy customers globally. RedBus offers bus ticket booking through its website, iOS and Android mobile apps for all major routes.")

#writing for the second page
if selection =='Booking Page':
  #choosing the first filter of state
  state_select=get_state(mycursor)
  state_sb=st.selectbox("Select a state",state_select)

  bus_route = get_bus_routes(mycursor,state_sb)#calling the function again
  route_name = st.selectbox("Enter Route Name:",bus_route)#defining the selectbox

 #setting the price range and star rating range
  price_range = st.slider("Choose Price Range:", min_value=0.0, max_value=5000.0, value=(0.0, 100.0), format="%100f")
  star_rating_range = st.slider("**Select Star Rating Range:**" ,min_value=0.0, max_value=5.0, value=(0.0, 1.0), format="%.1f")
 #defining the bustype filter
  bus_type = get_bus_type(mycursor, route_name, price_range, star_rating_range)#calling the bustype function
  Bustype=st.selectbox("**Select a Bustype**",bus_type)#assigning a streamlit selectbox
  

  Dept=st.time_input("select a time:" )#giving an input filter for departing time


  Seats=st.slider("select the seats availability:",min_value=0, max_value=75,value=(0,75),format="%d")#giving slider input for seats availability
 
  if st.button("Search Buses"):#giving a search button for getting further details
    data = get_details(mycursor,state_sb, route_name,price_range,star_rating_range,Dept,Seats)
    st.dataframe(data)#Displaying the filtered details in a dataframe

#writing for the third page    
if selection =='About Me':
  st.title('**ABOUT ME**')
  st.write("My Name is Dharshinee R, I have done my Post Graduation in Economics.Currently i have enrolled myself in a Data Science Course for a good future career path. I am good at learning things quickly and adopting to different suituation")
  st.write("linkedin url - 'www.linkedin.com/in/dharshinee-r-695719238' ")


mycursor.close()
 