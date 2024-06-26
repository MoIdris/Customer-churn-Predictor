
import streamlit as st
import plotly.express as px
import pandas as pd
import altair as alt
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Page configurations
st.set_page_config(
    page_title ='Dashboard Page',
    page_icon ='📈',
    layout="wide"
)


#### User Authentication
# load the config.yaml file 
with open('./Utils/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Create an authentication object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# invoke the login authentication
name, authentication_status, username = authenticator.login(location="sidebar")

if st.session_state["authentication_status"] is None:
    st.warning("Please Log in to get access to the App")
    test_code = '''
    Test Account
    username: analystidris
    password: 456123
    '''
    st.code(test_code)
        
elif st.session_state["authentication_status"] == False:
    st.error("Wrong username or password")
    st.info("Please Try Again")
    test_code = '''
    Test Account
    username: analystidris
    password: 456123
    '''
    st.code(test_code)
else:
    #st.info("Login Successful")
    st.write(f'Welcome *{username}*')
    # logout user using streamlit authentication logout
    authenticator.logout('Logout', 'sidebar')

    st.title("Dashboard")

    # set page theme
    alt.themes.enable("dark")
    color_map = {"Yes":"blue","No":"skyblue"}
    # read data for dashboard
    df = pd.read_csv('./Data/Customer_churn_Deployment_data.csv')

    # Create a function to view the EDA
    def eda_dashboard():
        st.markdown("### Exploratory Data Analysis ")
                    
        selected = option_menu(None, options=["Univariate Analysis", "Bivariate Analysis", "Multivariate Analysis"], 
            #icons=['single','gear' 'cloud-upload'], 
            menu_icon="cast", default_index=0, orientation="horizontal")
        selected
        #st.markdown("#### Univariate Analysis")

        if selected == "Univariate Analysis":
        # manually set color map
            col1,col2 = st.columns(2)
            with col1:
                monthlycharges_histogram = px.histogram(df,x="monthlycharges",title="Distribution of MonthlyCharges")
                st.plotly_chart(monthlycharges_histogram)
            with col2:
                totalcharges_histgram = px.histogram(df,x="totalcharges",title="Distribution of TotalCharges")
                st.plotly_chart(totalcharges_histgram)

            col3,col4 = st.columns(2)
            with col3:
                # plot a histogram of Tenure
                tenure_histogram = px.histogram(df,x="tenure",title="Distribution of Tenure")
                st.plotly_chart(tenure_histogram)
            with col4:
                pieplot = px.pie(df,names="churn",title="Churn by InternetService",color="churn",color_discrete_map=color_map,hole=0.3)
                st.plotly_chart(pieplot)
                
            col5,col6 = st.columns(2)
            with col5:
                boxplot = px.box(df,x="totalcharges",title="BoxPlot of TotalCharges")
                st.plotly_chart(boxplot)
            with col6:
                boxplot = px.box(df,x="tenure",title="BoxPlot of Tenure")
                st.plotly_chart(boxplot)

            boxplot = px.box(df,x="monthlycharges",title="Boxplot of MonthlyCharges")
            st.plotly_chart(boxplot)

        if selected == "Bivariate Analysis":
            # st.write("#")
            # st.markdown("#### Bivariate Analysis")
            col1,col2 = st.columns(2)
            with col1:
                boxplot = px.box(df,x="monthlycharges",y="churn",color="churn",color_discrete_map=color_map,title="Distribution of Churn by MonthlyCharges")
                st.plotly_chart(boxplot)
            with col2:
                boxplot = px.box(df,x="totalcharges",y="churn",color="churn",color_discrete_map=color_map,title="Distribution of Churn by TotalCharges")
                st.plotly_chart(boxplot)

            col3,col4 = st.columns(2)
            with col3:
                boxplot = px.box(df,x="tenure",y="churn",color="churn",color_discrete_map=color_map,title="Distribution of Churn by Tenure")
                st.plotly_chart(boxplot)
            with col4:
                barplot = px.bar(df,x="internetservice",y="monthlycharges",color="churn",color_discrete_map=color_map)
                st.plotly_chart(barplot)
                
        if selected == "Multivariate Analysis":
            # st.write("#")
            # st.markdown("#### Multivariate Analysis")
            col1,col2 = st.columns(2)
            with col1:
                scatter_plot = px.scatter(df,x="monthlycharges",y="totalcharges",color="churn",color_discrete_map=color_map,title="Relation Between Churn and Charges")
                st.plotly_chart(scatter_plot)
            with col2:
                numerical_data = df.select_dtypes("number")
                #numerical_data.drop(columns=["Unnamed: 0"],inplace=True)
                cor_matrix = numerical_data.corr()
                heat_map = px.imshow(cor_matrix,text_auto=True,aspect="auto",title="Correlation Matrix")
                st.plotly_chart(heat_map)
            

    def kpi_dashboard():
        st.markdown(" ### Key Performance Indicators")
        
    # KPIs Section
        met1, met2, met3, met4 = st.columns(4)

    # Compute key metrics from the DataFrame
        avg_tenure = df['tenure'].mean()
        avg_monthly_charges = df['monthlycharges'].mean()
        churn_rate = df['churn'].value_counts(normalize=True).get('Yes', 0) * 100
        contract_count = df['contract'].value_counts()

    # Display KPIs
        met1.metric("Average Tenure", f"{avg_tenure:.2f} months", delta=-24)
        met2.metric("Average Monthly Charges", f"${avg_monthly_charges:.2f}", delta=18.0)
        met3.metric("Churn Rate",f"{churn_rate:.2f}%", delta=-11.0)
        met4.metric("Total Customers", len(df), delta=len(df) - 1000)

        col1, col2, col3 = st.columns(3)
        with col1: 
            violin_plot = px.bar(df, x="gender", y="seniorcitizen",
                            title="Impact of Monthly Charges On Customer Churn",
                            color="churn", color_discrete_map=color_map)

    # Display the plot in Streamlit
            st.plotly_chart(violin_plot)

        with col2:
            violin_plot = px.violin(df,x="churn",y="monthlycharges",title="Impact of Monthly Charges On Customer Churn",color="churn",color_discrete_map=color_map)
            st.plotly_chart(violin_plot)
        with col3:
            churn_by_mu_multipleLiservice = px.bar(df,x="multiplelines",y="monthlycharges",color="churn",color_discrete_map=color_map,title="Churn by Multiple Services and Monthly Charges")
            st.plotly_chart(churn_by_mu_multipleLiservice)

        col4,col5,col6 = st.columns(3)
        with col4:
            churn_by_contract= px.bar(df,x="contract",y="monthlycharges",color="churn",color_discrete_map=color_map,title="Churn by Contract Type and Monthly Charges")
            st.plotly_chart(churn_by_contract)
        with col5:
            churn_by_streaming_tv = px.bar(df,x="streamingtv",y="monthlycharges",color="churn",color_discrete_map=color_map,title="Churn by Streaming TV and Monthly Charges")
            st.plotly_chart(churn_by_streaming_tv)
        with col6:
            churn_by_techsupport = px.bar(df,x="techsupport",y="monthlycharges",color="churn",color_discrete_map=color_map,title="Churn by Tech Support and Monthly Charges")
            st.plotly_chart(churn_by_techsupport)

        col7,col8,col9 = st.columns(3)
        with col7:
            monthly_charges_and_tenure = px.scatter(df,x="tenure",y="monthlycharges",color="churn",color_discrete_map=color_map,title="Relationship Between Monthly Charges and Tenure")
            st.plotly_chart(monthly_charges_and_tenure)
        with col8:
            total_charges_and_tenure = px.scatter(df,x="tenure",y="totalcharges",color="churn",color_discrete_map=color_map,title="Relationship Between Total Charges and Tenure")
            st.plotly_chart(total_charges_and_tenure)
        with col9:
            tenure_versus_charges = px.density_contour(df,x="tenure",color="churn",color_discrete_map=color_map,marginal_x="histogram",marginal_y="histogram",title="Tenure by Churn Status")
            st.plotly_chart(tenure_versus_charges)

    # Sidebar
        st.sidebar.title("Navigation")
        dashboard_type = st.sidebar.radio("Choose Dashboard", ("EDA", "KPIs"), key='dashboard_type')

    if __name__ == "__main__":
        # set page title
        #st.title("Dashboard Page📈")

        col1,col2 = st.columns(2)
        with col1:
            st.selectbox("Select Dashboard Type",options=["EDA","KPI"],key="selected_dashboard_type")
        with col2:
            pass
        
        if st.session_state.selected_dashboard_type == "EDA":
            eda_dashboard()
        else:
            kpi_dashboard()
