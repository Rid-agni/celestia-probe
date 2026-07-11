from pathlib import Path
from textwrap import dedent
import streamlit as st

from ui.components import (
    header,
    metadata,
    user_message,
    assistant_message,
    divider
)


def load_css():

    css_path = Path(__file__).parent / "styles.css"

    with open(css_path, encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


def render_terminal(messages, source="", entity=""):

    load_css()

    st.markdown("""
<div class="crt-frame">

<div class="crt-screen">

<h1 class="cp-title">
CELESTIA PROBE
</h1>

<div class="cp-status">
STATUS : ONLINE
</div>

</div>

</div>
""", unsafe_allow_html=True)