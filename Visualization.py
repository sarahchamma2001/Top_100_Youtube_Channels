import requests
import streamlit as st
# data
import pandas as pd
import numpy as np
from streamlit_lottie import st_lottie

#For Visualization
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu

# Display lottie animations
def load_lottieurl(url):

    # get the url
    r = requests.get(url)
    # if error 200 raised return Nothing
    if r.status_code !=200:
        return None
    return r.json()
# Extract Lottie Animations
lottie_home = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_uhydirrs.json")
lottie_dataset = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_ej2lfhv2.json")
lottie_prediction= load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_T1SlYO.json")

#Title
st.set_page_config(page_title='Top 100 Youtube Channels',  layout='wide')

#header
t1, t2 = st.columns((0.4,1)) 
t2.title("Top 100 Youtube Channels")

#Hydralit Navbar
# define what option labels and icons to display
Menu = option_menu(None, ["Home", "Dataset",  "EDA"], 
    icons=['house', 'cloud-upload', "bar-chart-line","clipboard-check"], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "black", "font-size": "25px"}, 
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "red"},
    }
)
# Home Page
if Menu == "Home":
      # Display Introduction
    st.markdown("""
    <article>
  <header class="bg-gold sans-seSans Serif">
    <div class="mw9 center pa4 pt5-ns ph7-l">
      <h3 class="f2 f1-m f-headline-l measure-narrow lh-title mv0">
        <span class="bg-black-90 lh-copy white pa1 tracked-tight">
        </span>
      </h3>
      <h4 class="f3 fw1 Sans Serif i">Analyzing the top 100 Youtube Channels</h4>
      <h5 class="f6 ttu tracked black-80">By Sarah Chamma</h5>
      </div>
      </p>
      </div>
      </article>""",unsafe_allow_html=True)
#Upload Image
    from PIL import Image
    title_container = st.container()
    col1, mid, col2 = st.columns([30,3,35])
    with title_container:
      with col1:
        st_lottie(lottie_home, key = "upload",width = 500)
      with col2:
        st.write('YouTube has social impact which has influenced internet trends, popular culture, and the rise of billionaire celebrities. In this application, we will explore the top 100 Youtube Channels.')

# Dataset page

if Menu == "Dataset":
#data
# 2 Column Layouts of Same Size
    col4,col5 = st.columns([1,1])

    # First Column - Shows Description of EDA
    with col4:
        st.markdown("""
        <h3 class="f2 f1-m f-headline-l measure-narrow lh-title mv0">
         Know Your Data
         </h3>
         <p class="f5 f4-ns lh-copy measure mb4" style="text-align: justify;font-family: Sans Serif">
          It is important at the initial stage to explore the data and understand and try to gather as many insights from it. The dataset contains 7 columns:

rank: rank of youtuber

youtuber: name of youtuber

subscribers: number of subscribers

video views: total views of video

video count: number of uploaded videos

category: category of video

started: started year
         </p>
            """,unsafe_allow_html = True)
        global eda_button
# Display customer churn animation
    with col5:
        st_lottie(lottie_dataset, key = "eda",height = 400, width = 700)
    df=pd.read_csv("YouTube.csv")
    st.dataframe(df)

# EDA page
df=pd.read_csv("YouTube.csv")
if Menu == "EDA":
  st.header("Visualizations")

#Visualization
  g1,g2,g3= st.columns((1,1,1))
  k1,k2,k3=st.columns((0.5,9,0.5))
  s1,s2=st.columns((1,1))
  w1,w2=st.columns((1,1))


#Categories of Top 100 Youtube Channel
  category = df['category_'].value_counts()
  fig = px.pie(values=category.values, 
             names=category.index,
             color_discrete_sequence=px.colors.sequential.Reds,
             title='Category Pie Graph')
  fig.update_traces(textposition='inside',
                  textfont_size=11,
                  textinfo='percent+label')
  fig.update_layout(uniformtext_minsize=12, 
                  uniformtext_mode='hide')
  g1.plotly_chart(fig, use_container_width=True) 

#Mean of subscribers by category
  categories = df.groupby('category_').mean().subscribers_.sort_values(ascending=False)
  fig = go.Figure(data=px.bar(x=categories.index, 
                            y=categories.values,
                            color_discrete_sequence=px.colors.sequential.RdBu,
                            
                            title='Mean of subscribers by category',
                            text = np.round(categories.values/1000000,2),
                            height=500))
  fig.data[0].marker.line.width = 2
  fig.data[0].marker.line.color = "black"                            

  g2.plotly_chart(fig, use_container_width=True) 
  
#Relation between Category and Youtuber
  fig=px.sunburst(df, path=['category_','youtuber'],
                  title='Relation between Category and Youtuber',
                  color_discrete_sequence=px.colors.sequential.Reds)
  g3.plotly_chart(fig, use_container_width=True)

  g1.write("The first graph show that music, entertainment, and People & Blogs ranked top 3 highest percentage of category proportion.")
  g2.write("We can see that the Sports, Shows, and Education categories ranked top 3 means of subscribers.")
  
#Boxplot of Video Views & Video Counts & Subscribers
  fig = make_subplots(rows=1, cols=3)
  fig.update_layout(title_text="Boxplot of video views & video count & subscribers",
                  uniformtext_minsize=12, 
                  uniformtext_mode='hide')

  fig.add_trace(go.Box(y=df.video_views_,
                    name="video views boxplot",
                    marker_color = 'indianred',
                    boxpoints='outliers'),row=1,col=1)


  fig.add_trace(go.Box(y=df.video_count_,
                     name="video count boxplot",
                     boxpoints='outliers', 
                     marker_color = 'indianred'),row=1,col=2)

  fig.add_trace(go.Box(y=df.subscribers_,
                    name="subscribers boxplot",
                    boxpoints='outliers', 
                    marker_color = 'indianred'),row=1,col=3)
  k2.plotly_chart(fig, use_container_width=True)
  k2.write("The maximum number of views is 188B")
  k2.write("The maximum number of videos is 209K")
  k2.write("The maximum number of subscribers in 213M")

#Explore youtuber with most subscribers by category
  a = df.groupby(['category_'])['subscribers_'].max()
  most = df[df['subscribers_'].isin(a.values)]

  fig = go.Figure(data=px.bar(x=most.category_, 
                            y=most.subscribers_,
                            text = most.youtuber, 
                            orientation='v',
                            color=most.category_,
                            color_discrete_sequence=px.colors.sequential.Reds,
                            title='Youtuber with most susbcribers in eacy categories',
                            
                            height=600))
  s1.plotly_chart(fig, use_container_width=True) 

#Explore youtuber with most subscribers by category
# plt.figure(figsize=(10,5))
  fig = px.treemap(most, 
                 path=['category_','youtuber'],
                 values='subscribers_', 
                 title = ' Youtuber with most subscribers in each category',
                 color_discrete_sequence=px.colors.sequential.Reds,
                 width=1000, height=500)
  s2.plotly_chart(fig, use_container_width=True)
  s1.write("The two graphs above show that music, education, and shows are top the 3 categories that have the most subscribers.")
#Categories with video views and video counts
  fig = px.scatter(df, x="video_count_", y="video_views_",
                 size="video_views_", color="category_",
                 log_x=True, size_max=60,
                 title="categories with video views and video counts",
                 color_discrete_sequence=px.colors.sequential.Reds)

  lst = [4,5]
  for idx in lst:
    fig.data[idx].marker.line.width = 3
    fig.data[idx].marker.line.color = 'black'
  w1.plotly_chart(fig, use_container_width=True)
#Top categories each Year
  fig = px.bar(df, x="category_", y="started_", animation_frame="started_",
             color="category_",title="Top categories each Year",
             color_discrete_sequence=px.colors.sequential.Reds)
  w2.plotly_chart(fig, use_container_width=True)

  title_container = st.container()
  col1, mid, col2 = st.columns([30,30,35])
  with title_container:
      with mid:
        st_lottie(lottie_prediction, key = "upload",width = 500)
