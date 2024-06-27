import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import altair as alt
from st_aggrid import AgGrid, GridOptionsBuilder

if "info_added" not in st.session_state:
    st.session_state.info_added = False

if "info" not in st.session_state:
    st.session_state.info = None

# if st.session_state.info_added is None or st.session_state.info is None:
#     st.switch_page("main.py")


st.header("Analysis")

if st.session_state.info is not None:
    st.write(f"Input Data:")
    # st.write(st.session_state.info)

    grid_builder = GridOptionsBuilder.from_dataframe(st.session_state.info)
    grid_builder.configure_side_bar(filters_panel=True, columns_panel=False)
    for column in st.session_state.info.columns:
        grid_builder.configure_column(column, filter="agMultiColumnFilter")

    grid_options = grid_builder.build()

    grid_data = AgGrid(st.session_state.info, grid_options, enable_enterprise_modules=True, allow_unsafe_jscode=True)
    # st.markdown(grid_data, unsafe_allow_html=True)

    st.write("Aggregate By:")
    info = {"year": st.checkbox("Year"),
            "yearmonth": st.checkbox("Month"),
            "day": st.checkbox("Day", value=True)}

    # colors = ["#eae4e9", "#fff1e6", "#fde2e4", "#fad2e1", "#e2ece9", "#bee1e6", "#f0efeb", "#dfe7fd", "#cddafd"]
    colors = ["#822b34", "#e5d1ca", "#2a3245", "#d7bbc9", "#c7ad94"]
    reference_amount = st.number_input("Reference Amount")

    timescale_name = st.text_input("Timescale Name")
    amount_name = st.text_input("Amount Name")

    filtered_data = grid_data["data"]

    try:
        color_index = 0

        charts = list()

        if info["day"]:
            charts.append(alt.Chart(filtered_data).mark_point(color=colors[color_index]).encode(
                x=timescale_name + ":T",
                y=amount_name,
            ))
            color_index += 1

        for label, selection in info.items():
            if label is not "day" and selection:
                charts.append(alt.Chart(filtered_data).mark_line(color=colors[color_index]).encode(
                    x=f"{label}({timescale_name})",
                    y=f"sum({amount_name})")
                )
                color_index += 1

        if reference_amount:
            charts.append(alt.Chart(pd.DataFrame({'y': [reference_amount]})).mark_rule().encode(y='y'))
            color_index += 1

        c = alt.layer(*charts)
        st.altair_chart(c, use_container_width=True)

    except Exception as e:
        st.write(f"{e}\n\nWaiting for input.")

if st.button("Back"):
    st.session_state.info_added = False
    st.session_state.info = None
    st.switch_page("main.py")
