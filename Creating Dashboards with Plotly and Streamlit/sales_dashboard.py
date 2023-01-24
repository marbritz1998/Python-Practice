#Doing a Guided Project on creating interactive dashboards in python using Plotly and streamlit

#Coming from the video: https://www.youtube.com/watch?v=Sb0A9i6d320&ab_channel=CodingIsFun

#importing packages
import pandas as pd
import plotly.express as px
import streamlit as st

#setting up page configuration
st.set_page_config(page_title = "Sales Dashboard", page_icon = "bar_chart:", layout = "wide")

#reading in data
#for improving efficiency, going to store the dataframe information to a cache
@st.cache
def get_data_from_excel():  
    data = pd.read_excel("supermarkt_sales.xlsx", 
                         engine = 'openpyxl', 
                         sheet_name = 'Sales', 
                         skiprows = 3, 
                         usecols = 'B:R', 
                         nrows = 1000
    )

    # Add 'hour' column to data
    data['hour'] = pd.to_datetime(data['Time'], format = "%H:%M:%S").dt.hour
    return data
data = get_data_from_excel()

# NOTE!!! in order to run a streamlit application, must go to command line and run "streamlit run file_name.py"

#---SIDEBAR---
st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options = data["City"].unique(),
    default = data["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options = data["Customer_type"].unique(),
    default = data["Customer_type"].unique()
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options = data["Gender"].unique(),
    default = data["Gender"].unique()
)


data_selection = data.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)

# NOTE!!! you can use @variable to refer to a variable! really cool!


#---MainPage
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# Top KPI's
total_sales = int(data_selection["Total"].sum())
average_rating = round(data_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sales_by_transaction = round(data_selection["Total"].mean(),2)

# the columns act as containers inserted side by side
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}") #using fstrings to format the already calculated values
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction")
    st.subheader(f"US $ {average_sales_by_transaction}")

st.markdown("---")


# Sales By Product Line bar graphs
sales_by_product_line = data_selection.groupby(["Product line"]).sum()[["Total"]].sort_values("Total", ascending = False)

fig_product_sales = px.bar(
    sales_by_product_line,
    x = "Total",
    y = sales_by_product_line.index,
    orientation = 'h',
    title = "<b>Sales by Product Line</b>", # NOTE!!! can use HTML in the title, this will make the title appear bold
    color_discrete_sequence = ["#0083B8"] * len(sales_by_product_line),
    template = "plotly_white"
)
fig_product_sales.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis = (dict(showgrid=False))
)

#st.plotly_chart(fig_product_sales)

# sales by hour
sales_by_hour = data_selection.groupby(["hour"]).sum()[['Total']]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x = sales_by_hour.index,
    y = "Total",
    title = "<b>Sales by hour</b>",
    color_discrete_sequence = ["#0083B8"] * len(sales_by_hour),
    template = "plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis = dict(tickmode='linear'),
    plot_bgcolor = "rgba(0,0,0,0)",
    yaxis = (dict(showgrid=False)),
) 
#st.plotly_chart(fig_hourly_sales)
 
 
 #positioning charts together
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)  

# ---- HIDE STREAMLIT STYLE----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)
