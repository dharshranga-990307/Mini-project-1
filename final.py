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

#displaying in streamlit using sidebar navigation
st.sidebar.title('Navigation')

#dividing the pages into three tabs Home,Booking page,About me
selection=st.sidebar.radio('Go to',['Home','Booking Page'])

#Writing for first page
if selection == 'Home':
    st.title('**RedBus Booking Site**')
    st.write("**India's No. 1 Online Bus Ticket Booking Site**")
    st.image(r"C:\Users\Dharshinee R\Desktop\108561103.webp",use_container_width=True)
    st.write("RedBus is the world's largest online bus ticket booking service trusted by over 25 million happy customers globally. RedBus offers bus ticket booking through its website, iOS and Android mobile apps for all major routes.")

#writing for the second page
if selection =='Booking Page':
  st.title("Bus Booking Page")#title for second page
  col1, col2, col3 = st.columns([5,5,5])#dividing them into columns
  
  #selection for state
  state_select=get_state(mycursor)#calling the function
  state_sb=st.sidebar.selectbox("**Select a state**",state_select)#displaying in a selectbox
  
  with col1: #column 1 filters
   bus_route = get_bus_routes(mycursor,state_sb)
   route_name = st.selectbox("**Enter Route Name:**",bus_route)#defining the selectbox

#streamlit filter for star_rating_Range
   star_rating_range = st.slider("**Select Star Rating Range:**" ,min_value=0, max_value=5, value=(0,5),format="%1f",step=1)
   min_star,max_star=star_rating_range
  
  with col2: #column 2 filters
   price_range = st.slider("**Choose Price Range:**", min_value=0, max_value=5000, value=(0, 5000), format="%1f",step=100)
   min_price,max_price=price_range
   Dept_time=st.selectbox("**Select Departure Time Range**",["All Times","12am-3am","3am-6am","6am-9am","9am-12pm","12pm-3pm","3pm-6pm","6pm-9pm","After 9pm"])

   if Dept_time =="12am-3am":
    start_time,end_time= "00:00:00", "03:00:00"
   elif Dept_time =="3am-6am":
    start_time,end_time= "03:01:00", "06:00:00"
   elif Dept_time =="6am-9am":
    start_time,end_time= "06:01:00", "09:00:00"
   elif Dept_time =="9am-12pm":
    start_time,end_time= "09:01:00", "12:00:00"
   elif Dept_time =="12pm-3pm":
    start_time,end_time= "12:01:00", "15:00:00"
   elif Dept_time =="3pm-6pm":
    start_time,end_time= "15:00:00", "18:00:00"
   elif Dept_time =="6pm-9pm":
    start_time,end_time= "18:01:00", "21:00:00"
   elif Dept_time =="  After 9pm":
    start_time,end_time= "21:01:00", "23:59:59"
   elif Dept_time =="All Times":
    start_time,end_time="00:01:00","23:59:00"

  with col3:
   Seats=st.number_input("**Select No. of Seats:**",step=1)
   Bus_type=st.selectbox("Choose a Bustype:",["A/C","NON A/C","Seater","Sleeper","Push Back","Semi Sleeper"])

  
#sql query to filter the data based on the filters and display them in a dataframe
  sql_query="""
      SELECT 
        States AS State,  
        Route_name AS 'Bus_Route',
        Route_link AS Route_Link,
        Busname AS BUSNAME,
        Bus_type AS Bustype,
        Departing_time AS Departing_Time,
        Duration AS Journey_Time,
        Reaching_time AS Reach_time,
        Star_rating AS Rating,
        Price AS Bus_Fare,
        Seats_available AS Seats_availability
      FROM bus_routes 
      WHERE States=%s
      AND Route_name =%s 
      AND Price BETWEEN %s AND %s
      AND Star_rating BETWEEN %s AND %s
      AND Seats_available >=%s
      AND Departing_time BETWEEN %s AND %s
      
  """
  
  params=[state_sb,route_name,min_price,max_price,min_star,max_star,Seats,start_time,end_time]

#filter the departing_time
  if start_time and end_time:
   sql_query += "AND Departing_time BETWEEN %s AND %s"
   params.extend([start_time,end_time])

  if Bus_type=="A/C":
     sql_query += "AND(Bus_type LIKE %s OR Bus_type LIKE %s)AND Bus_type NOT LIKE %s AND Bus_type NOT LIKE %s AND Bus_type NOT Like %s AND Bus_type NOT Like %s "
     params.extend(["%A/C%","%AC%","%Non AC%","%Non A/C%","%NON-AC%","%NON-A/C%"])
  elif Bus_type=="NON A/C":
      sql_query += "AND (Bus_type LIKE %s OR Bus_type LIKE %s OR Bus_type LIKE %s OR Bus_type LIKE %s)"
      params.extend(["%NON A/C%","%Non A/C%","%NON-AC%","%NON-A/C%"])
  elif Bus_type=="Seater":
      sql_query +="AND Bus_type LIKE %s"
      params.append("%Seater%")
  elif Bus_type=="Sleeper":
      sql_query +="AND Bus_type LIKE %s"
      params.append("%Sleeper%")
  elif Bus_type=="Push Back":
      sql_query+="AND( Bus_type LIKE %s OR Bus_type LIKE %s)"
      params.extend(["%Push Back%","%PUSH BA/CK%"])
  else:
      Bus_type=="Semi Sleeper"
      sql_query +="AND Bus_type LIKE %s"
      params.append("%Semi Sleeper%")

   
  def format_timedelta(td):
    total_seconds = td.total_seconds()
    hours = int(total_seconds // 3600)  # Total hours
    minutes = int((total_seconds % 3600) // 60)  # Remaining minutes
    return f"{hours:02}:{minutes:02}"# Return in HH:MM format 
  mycursor.execute(sql_query,params)
  data=mycursor.fetchall()
  columns = ['State', 'Bus_Route', 'Route_Link', 'BUSNAME', 'Bustype', 
           'Departing_Time', 'Journey_Time', 'Reach_time', 
           'Rating', 'Bus_Fare', 'Seats_availability']
  df = pd.DataFrame(data, columns=columns)
  
  df['Departing_Time'] = df['Departing_Time'].apply(format_timedelta)
  df['Reach_time']=df['Reach_time'].apply(format_timedelta)

  if st.button("Search Buses"):
    st.write(df)
   




