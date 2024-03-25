import streamlit as st
import numpy as np
from utils.nose_cone import Nose
import pandas as pd
import plotly.express as px


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False, header=False).encode('utf-8')


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
d = st.number_input("Diameter", value=106)
length_type = st.radio("Length Type", ["Aspect Ratio", "Length"])
if length_type == "Aspect Ratio":
    aspect = st.number_input("Aspect Ratio", value=1.5)
    length = None
else:
    length = st.number_input("Length", value=159)
    aspect = None

if flavor == "Von Karman":
    C = st.number_input("C", value=1 / 3)
elif flavor == "Power":
    C = st.number_input("n", value=0.75)
elif flavor == "Parabolic":
    C = st.number_input("K", value=.75)

resolution = st.select_slider("Resolution", options=[0.1, 0.2, 0.3, 0.4, 0.5], value=0.3)

# Calculate
out = make_cone(d, C, resolution, flavor, aspect=aspect, l=length)

# Download
df = pd.DataFrame(out)
csv = convert_df(df)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='nosecone.csv',
    mime='text/csv',
)


# Plot
fig = px.line(x=df[0], y=df[1])
fig.update_yaxes(
    scaleanchor="x",
    scaleratio=1,
)
st.plotly_chart(fig)
