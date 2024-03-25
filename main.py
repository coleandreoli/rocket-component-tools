import streamlit as st
from streamlit.components.v1 import html
import numpy as np
from utils.nose_cone import Nose
import pandas as pd
import plotly.express as px


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False, header=False).encode('utf-8')
@st.cache_data
def convert_df_txt(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(sep='\t', index=False, header=False).encode('utf-8')

def make_cone(d, C, resolution, nose_type, aspect=None, l=None):
    # Calculations
    if l is None:
        l = d * aspect

    itr = int(l / resolution)
    R = d / 2

    # Define numpy arrays
    x = np.linspace(0, l, itr)

    # Calculate y values using numpy
    if nose_type == "Power":
        y = Nose.power_function(x, R, l, C)
    elif nose_type == "Parabolic":
        y = Nose.parabolic_function(x, R, l, C)
    elif nose_type == "Von Karman":
        y = Nose.von_karman_function(x, R, l, C)

    z = np.zeros(len(x))
    # np.savetxt(rf"C:\Users\colea\PycharmProjects\SugarRocket\{name}.txt", np.c_[x, y, z], delimiter='\t')

    return np.c_[x, y, z]


st.title("Nose Cone Page")
st.write("Use the exported data to create a nose cone in CAD software.\nhttps://en.wikipedia.org/wiki/Nose_cone_design")

# Inputs
flavor = st.sidebar.selectbox("Nose Cone Type", ["Von Karman", "Power", "Parabolic"])
d = st.number_input("Diameter", value=106.0)
length_type = st.radio("Length Type", ["Aspect Ratio", "Length"])
if length_type == "Aspect Ratio":
    aspect = st.number_input("Aspect Ratio", value=1.5)
    length = None
else:
    length = st.number_input("Length", value=159.0)
    aspect = None

if flavor == "Von Karman":
    C = st.number_input("C", value=1 / 3)
elif flavor == "Power":
    C = st.number_input("n", value=0.5)
elif flavor == "Parabolic":
    C = st.number_input("K", value=.75)

resolution = st.number_input("Resolution", value=.3)

# Calculate
out = make_cone(d, C, resolution, flavor, aspect=aspect, l=length)
df = pd.DataFrame(out)

# Plot
fig = px.line(x=df[0], y=df[1])
fig.update_yaxes(
    scaleanchor="x",
    scaleratio=1,
)
st.plotly_chart(fig)

# Download
csv = convert_df(df)
txt = convert_df_txt(df)
st.download_button(label="Download data as CSV",data=csv,file_name='nosecone.csv',mime='text/csv',)
st.download_button(label="Download data as txt", data=txt, file_name='nosecone.txt', mime='text/plain')


button = """
<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="niles55" data-color="#FFDD00" data-emoji=""  data-font="Cookie" data-text="Buy me a coffee" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#ffffff" ></script>
"""

html(button, height=70, width=220)

st.markdown(
    """
    <style>
        iframe[width="220"] {
            position: fixed;
            bottom: 60px;
            right: 40px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)