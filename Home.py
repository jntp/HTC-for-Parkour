import streamlit as st

## Streamlit App Configurations 
st.set_page_config(layout="wide")

st.sidebar.title("About")

st.sidebar.info(
    """
    ***Justin's Mapping Corner***
    
    **Contact:**
    - Justin Tang | jrtang@proton.me | [GitHub](https://github.com/jntp)
    """
)

st.title("☕")
st.header("Justin's Mapping Corner")

st.markdown(
    """
    Welcome to Justin's Mapping Corner! Here you can view the interactive web maps that I have created as personal projects. You may also
    view the source code in this [GitHub repository](https://github.com/jntp/HTC-for-Parkour). If you have any questions or feedback, please
    see the left sidebar for contact information. 🙂
    """
)
