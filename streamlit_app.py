# Importing the needed libraries
import streamlit as st
import pandas as pd

# Setting page configuration
st.set_page_config(
    layout = "wide",
    page_title = "Leeds Traffic Accidents"
)

# Defining the overview page
def overview_pg():
    st.title("Overview and Trends")

    # Reading the original dataset to a variable
    data =  pd.read_csv("Leeds_Traffic_Accidents_2019.csv")
    
    # Converting to datetime format to prevent errors
    data["Accident Date"] = pd.to_datetime(data["Accident Date"], dayfirst=True)
    
    # Separating page into columns to improve chart visibility 
    col1, col2 = st.columns(2)
    
    # Line chart column
    with col1:
        
        # Creating a filter for the date 
        min_date = data["Accident Date"].min()
        max_date = data["Accident Date"].max()
        line_chart_range = st.date_input(
            "Select date range:",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="line_date_filter"
        )
        
        # Creating a select box to choose chart info
        line_choice = st.selectbox(
            "Choose what data you wish to display below:",
            ["Daily Accident Count", "Number of Vehicles", "Average Age of Casualty"],
            key="line_chart_select"
        )
        
        # Filtering only the accidents that happened within the selected date range
        line_date = data[(data["Accident Date"] >= pd.to_datetime(line_chart_range[0])) & (data["Accident Date"] <= pd.to_datetime(line_chart_range[1]))]

        # Giving different instructions for each choice
        if line_choice == "Daily Accident Count":
            
            # Calculating the total accidents per day
            line_vis = line_date.groupby("Accident Date").size().reset_index(name="Accident Count")
            
            # Displaying the line chart
            st.subheader("Daily Accident Count Over Time")
            st.line_chart(line_vis.set_index("Accident Date"))
            
            # Displaying the average accidents per day
            st.metric("Average Daily Accidents", round(line_vis["Accident Count"].mean(), 2))

        elif line_choice == "Number of Vehicles":
            
            # Calculating the total vehicles in accidents per day
            line_vis = line_date.groupby("Accident Date")["Number of Vehicles"].sum().reset_index()
            
            # Displaying the line chart
            st.subheader("Vehicles Involved in Accidents Over Time")
            st.line_chart(line_vis.set_index("Accident Date"))
            
            # Displaying the average number of vehicles per accident
            st.metric("Average Number of Vehicles Involved in Accidents", round(line_vis["Number of Vehicles"].mean(), 2))
    
        elif line_choice == "Average Age of Casualty":
            
            # Calculating the average age of casualties per day 
            line_vis = line_date.groupby("Accident Date")["Age of Casualty"].mean().reset_index()
            
            # Displaying the line chart
            st.subheader("Average Age of Casualties Over Time")
            st.line_chart(line_vis.set_index("Accident Date"))
            
            # Displaying the overall average age of casualties
            st.metric("Overall Average Age of Casualty", round(line_vis["Age of Casualty"].mean()))

    # Bar chart column
    with col2:

        # Creating a filter for the date
        bar_chart_range = st.date_input(
            "Select date range:",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="bar_date_filter"
        )
        
        # Creating a select box to choose chart info
        bar_choice = st.selectbox(
            "Choose what data you wish to diplay below:",
            ["Casualty Severity", "Sex of Casualty", "Type of Vehicle", "1st Road Class", 
             "Road Surface", "Lighting Conditions", "Weather Conditions", "Casualty Class"],
            key="bar_chart_select"
        )

        # Filtering only the accidents that happened within the selected date range
        bar_date = data[(data["Accident Date"] >= pd.to_datetime(bar_chart_range[0])) & (data["Accident Date"] <= pd.to_datetime(bar_chart_range[1]))]

        # Counting traffic accidents by the chosen category
        bar_vis = bar_date[bar_choice].value_counts().sort_index()
    
        # Giving different instructions for each choice
        if bar_choice == "Casualty Severity":
            
            # Displaying the bar chart
            st.subheader("Frequency of Casualties by Severity")
            st.bar_chart(bar_vis)
            
            # Displaying the legend
            st.write("Bar Chart Legend")
            st.markdown("""
            - 1 -- Fatal
            - 2 -- Serious
            - 3 -- Slight
            """)

        elif bar_choice == "Sex of Casualty":
            
            # Displaying the bar chart
            st.subheader("Frequency of Casualties by Sex")
            st.bar_chart(bar_vis)

            # Displaying the legend
            st.write("Bar Chart Legend")
            st.markdown("""
            - 1 -- Male
            - 2 -- Female
            """)

        elif bar_choice == "Type of Vehicle":
            
            # Displaying the bar chart
            st.subheader("Frequency of Vehicle Types")
            st.bar_chart(bar_vis)
            
            # Separating legend into two columns to improve readability
            col1, col2 = st.columns(2)
            
            # Displaying the legend
            with col1:
                
                st.write("Bar Chart Legend")
                st.markdown("""
                - 1 -- Pedal cycle
                - 2 -- Motorcycle(≤ 50cc)
                - 3 -- Motorcycle(50-125cc)
                - 4 -- Motorcycle(125-500cc)
                - 5 -- Motorcycle(> 500cc)
                - 8 -- Taxi/Private hire car
                - 9 -- Car
                - 10 -- Minibus
                - 11 -- Bus/Coach
                """)

            with col2:
                
                st.write("")
                st.write("")
                st.markdown("""
                - 16 -- Ridden horse
                - 17 -- Agricultural vehicle
                - 19 -- Goods vehicle (≤ 3.5t)
                - 20 -- Goods vehicle (3.5-7.5t)
                - 21 -- Goods vehicle (≥ 7.5t)
                - 22 -- Mobility Scooter
                - 90 -- Other vehicle
                - 97 -- Motorcycle (Unknown CC)
                """)

        elif bar_choice == "1st Road Class":
            
            # Displaying the bar chart
            st.subheader("Frequency of Accidents by 1st Road Class")
            st.bar_chart(bar_vis)

            # Displaying the legend
            st.write("Bar Chart Legend")
            st.markdown("""
            - 1 -- Motorway
            - 2 -- A(M)
            - 3 -- A
            - 4 -- B
            - 5 -- C
            - 6 -- Unclassified
            """)
        
        elif bar_choice == "Road Surface":
            
            # Displaying the bar chart
            st.subheader("Frequency of Accidents by Road Surface")
            st.bar_chart(bar_vis)

            # Displaying the legend
            st.write("Bar Chart Legend")
            st.markdown("""
            - 1 -- Dry
            - 2 -- Wet/Damp
            - 3 -- Snow
            - 4 -- Frost/Ice
            - 5 -- Flood (surface water > 3cm)
            - 9 -- Unknown
            """)
        
        elif bar_choice == "Lighting Conditions":
            
            # Displaying the bar chart
            st.subheader("Frequency of Accidents by Lighting Conditions")
            st.bar_chart(bar_vis)

            # Displaying the legend
            st.write("Bar Chart Legend")
            st.markdown("""
            - 1 -- Daylight (street lights)
            - 4 -- Darkness (lit street lights)
            - 5 -- Darkness (unlit street lights)
            - 6 -- Darkness (no street lights)
            - 7 -- Darkness (unknown street lighitng)
            """)
        
        elif bar_choice == "Weather Conditions":
            
            # Displaying the bar chart
            st.subheader("Frequency of Accidents by Weather Conditions")
            st.bar_chart(bar_vis)

            # Displaying the legend
            st.write("Bar Chart Legend")
            st.markdown("""
            - 1 -- Fine (no high winds)
            - 2 -- Raining (no high winds)
            - 3 -- Snowing (no high winds)
            - 4 -- Fine (high winds)
            - 5 -- Raining (high winds)
            - 6 -- Snowing (High winds)
            - 7 -- Fog/Mist (hazardous)
            - 8 -- Other
            - 9 -- Unknown
            """)
        
        elif bar_choice == "Casualty Class":
            
            # Displaying the bar chart
            st.subheader("Frequency of Accidents by Casualty Class")
            st.bar_chart(bar_vis)

            # Displaying the legend
            st.write("Bar Chart Legend")
            st.markdown("""
            - 1 -- Driver/Rider
            - 2 -- Vehicle/Pillion passenger
            - 3 -- Pedestrian
            """)

#Defining the data insights page
def insights_pg():
    st.title("Data Insights")
    
    # Reading the original dataset to a variable
    data =  pd.read_csv("Leeds_Traffic_Accidents_2019.csv")

    # Converting to datetime format to prevent errors
    data['Accident Date'] = pd.to_datetime(data['Accident Date'], dayfirst=True)
    
    # Extracting month and year to a new column
    data['Month'] = data['Accident Date'].dt.to_period('M').astype(str)
    
    # Counting how many accidents happened in each lighting condition per month
    lighting_counts = data.groupby(['Month', 'Lighting Conditions']).size().unstack()

    # Displaying the stacked bar chart
    st.header("Frequency of Lighting Conditions Over Time")
    st.bar_chart(lighting_counts)

    # Displaying the legend
    st.write("Bar Chart Legend")
    st.markdown("""
    - 1 -- Daylight (street lights)
    - 4 -- Darkness (lit street lights)
    - 5 -- Darkness (unlit street lights)
    - 6 -- Darkness (no street lights)
    - 7 -- Darkness (unknown street lighitng)
    """)

    st.subheader("Findings")
    st.write("Although accidents are more often assumed to occur in poorly lit conditions, "
    "the data indicates that the highest number of accidents happened during daylight. "
    "Following this, darkness with lit street lights account for the second highest number "
    "of accidents, suggesting that lighting conditions are not the only factor affecting "
    "traffic accidents in Leeds.")
    st.write("")
    st.write("")
    st.write("")

    # Counting accidents by road surface and casualty severity
    severity_counts = data.groupby(['Road Surface', 'Casualty Severity']).size().unstack()

    # Displaying the stacked bar chart
    st.header("Frequency of Casualty Severity by Road Surface Conditions")
    st.bar_chart(severity_counts)

    # Separating legend into two columns to improve readability
    col1, col2 = st.columns(2)

    # Displaying the legend
    with col1:
        st.write("Bar Chart Legend ")
        st.write("Casualty Severity (color)")
        st.markdown("""
        - 1 -- Fatal
        - 2 -- Serious
        - 3 -- Slight
        """)

    with col2:
        st.write("")
        st.write("")
        st.write("")
        st.write("Road Surface (x-axis)")
        st.markdown("""
        - 1 -- Dry
        - 2 -- Wet/Damp
        - 3 -- Snow
        - 4 -- Frost/Ice
        - 5 -- Flood (surface water > 3cm)
        - 9 -- Unknown
        """)

    st.subheader("Findings")
    st.write("The stacked bar chart shows that the most accidents happen on dry roads and "
    "wet/damp roads respectively, with only a few occurrences happening in other road "
    "conditions. This may seem unexpected given the reduced traction of harsher conditions, "
    "however, this does suggest that drivers tend to be more cautious in hazardous weather "
    "and less cautious on dry roads as it may encourage higher speeds and riskier driving. "
    "The data also shows that casualties of slight severity occur the most out of other "
    "severity classes.")
    st.write("")
    st.write("")
    st.write("")

    # Displaying the bar chart
    st.header("Age of Casualty Distribution")
    st.bar_chart(data['Age of Casualty'].value_counts().sort_index())

    # Separating the age metrics into two columns to improve readability
    col1, col2 = st.columns(2)
    
    # Displaying the oldest and youngest casualty age
    with col1:
        st.metric("Youngest Casualty", f"{data['Age of Casualty'].min()} years old")

    with col2:
        st.metric("Oldest Casualty", f"{data['Age of Casualty'].max()} years old")

    st.subheader("Findings")
    st.write("The data shows that younger adults (20-30 years) experience the highest number "
    "of casualties, likely due to spending more time on the road than other age groups. Casualty "
    "frequency seems to generally decline with age, though older individuals may still face "
    "risks due to factors like reaction time. Children have the lowest reported casualties, "
    "most likely a result of protective measures being put in place.")

# Defining the raw data page
def data_pg():
    st.title("Raw Data")

    # Reading the original dataset to a variable
    data = pd.read_csv("Leeds_Traffic_Accidents_2019.csv")
    
    # Displaying the full dataset 
    st.write(data)

# Defining page names and linking them to repective page functions
pg_names = {
    "Overview": overview_pg,
    "Data Insights": insights_pg,
    "Raw Data": data_pg
}
# Creating a select box in the sidebar to choose what page to navigate to
pg_choice = st.sidebar.selectbox("Page Navigation", options = pg_names.keys())

# Displaying the chosen page 
pg_names[pg_choice]()
