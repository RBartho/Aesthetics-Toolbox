import streamlit as st
import numpy as np


def custom_round(num):
    '''
    if values are smaler than 1, round to 3 digits after the first nonzero digit,
    since measures have very different range
    '''
    if num < 1:
        ### convert to scientific_notation
        scientific_notation = "{:e}".format(num)
        ### get the e-value 
        e_val = scientific_notation[-2:]
        return np.round(num , 3 + int(e_val))
    
    else:
        return np.round(num,3)


def click_sub_SIPs(check_dict):
    st.session_state.commit_sips = True
    st.session_state.check_dict = check_dict
    
def click_sub_params():
    st.session_state.params_submitted = True
    

def click_sub_scaling(check_dict_scaling):
    st.session_state.commit_scaling = True
    st.session_state.check_dict_scaling = check_dict_scaling

def click_sub_params_resizing():
    st.session_state.params_resizing_submitted = True
