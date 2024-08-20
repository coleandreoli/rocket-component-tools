from utils.nose_cone import Nose
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False, header=False).encode('utf-8')
@st.cache_data
def convert_df_txt(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(sep='\t', index=False, header=False).encode('utf-8')

def make_cone(diameter, constant, resolution, nose_type, aspect=None, length=None):
    if length is None:
        length = diameter * aspect
    itr = int(length / resolution)
    radius = diameter / 2
    x = np.linspace(0, length, itr)

    if nose_type == "Power":
        y = Nose.power_function(x, radius, length, constant)
    elif nose_type == "Parabolic":
        y = Nose.parabolic_function(x, radius, length, constant)
    elif nose_type == "Von Karman":
        y = Nose.von_karman_function(x, radius, length, constant)
    else:
        raise ValueError("Invalid nose type")

    z = np.zeros(len(x))
    return np.c_[x, y, z]


st.title("Nose Cone Page")
st.write("Use the exported data to create a nose cone in CAD software.\nhttps://en.wikipedia.org/wiki/Nose_cone_design")

# Inputs
flavor = st.sidebar.selectbox("Nose Cone Type", ["Von Karman", "Power", "Parabolic"])
diameter = st.number_input("Diameter", value=106.0)
length_type = st.radio("Length Type", ["Aspect Ratio", "Length"])

if length_type == "Aspect Ratio":
    aspect = st.number_input("Aspect Ratio", value=1.5)
    length = None
else:
    length = st.number_input("Length", value=159.0)
    aspect = None

if flavor == "Von Karman":
    constant = st.number_input("C", value=1 / 3)
elif flavor == "Power":
    constant = st.number_input("n", value=0.5)
elif flavor == "Parabolic":
    constant = st.number_input("K", value=.75)
else:
    raise ValueError("Invalid nose type")

resolution = st.number_input("Resolution", value=.3)

if length is None:
    num_points = (diameter * aspect) / resolution
else:
    num_points = length / resolution
max_points = 1000000
if num_points > max_points:
    raise ValueError(f"Too many points: the array contains {num_points} points, but the maximum allowed is {max_points}.")

# Calculate
out = make_cone(diameter, constant, resolution, flavor, aspect=aspect, length=length)
df = pd.DataFrame(out)

# Plot
fig = px.line(x=df[0], y=df[1])
fig.add_trace(px.line(x=df[0], y=-df[1]).data[0])
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
