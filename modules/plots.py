import plotly.express as px
import pandas as pd
import streamlit as st


def create_bar_plot(data, x, y, orientation="v",  **kwargs):
    fig = px.bar(
        data,
        x=x,
        y=y,
        orientation=orientation,
        text_auto=True,
        color=y if orientation == "v" else x,
        color_continuous_scale='speed',
        # color_continuous_scale='algae',
        # color_continuous_scale='Viridis',
        # color_continuous_scale='Plasma',
        # color_continuous_scale='Aggrnyl',
        **kwargs
    )
    fig.update_traces(
        textfont_size=14,
        textangle=0,
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    fig.update_layout(xaxis_title=None, yaxis_title=None)

    st.plotly_chart(fig)


def create_choropleth_map(data, locations, location_mode, color, title=None, hover_name=None, color_discrete_map=None,
                          color_continuous_scale=None, labels=None, legend_title=None, width=1200, height=600,
                          **kwargs):
    fig = px.choropleth(
        data,
        locations=locations,
        locationmode=location_mode,
        color=color,
        hover_name=hover_name,
        color_discrete_map=color_discrete_map,
        color_continuous_scale=color_continuous_scale,
        labels=labels,
        title=title,
        **kwargs
    )

    fig.update_layout(
        legend_title_text=legend_title,
        legend=dict(
            y=0.5,
        ),
        width=width,
        height=height,
    )

    st.plotly_chart(fig)


def create_bubble_plot(data, x, y, size, color=None, text=None, **kwargs):
    if text:
        data['formatted_text'] = data[text].apply(
            lambda x: f"{x / 1e6:.1f}M" if x >= 1e6 else (f"{x / 1e3:.1f}K" if x >= 1e3 else str(x))
        )
    else:
        data['formatted_text'] = None
    fig = px.scatter(
        data,
        x=x,
        y=y,
        size=size,
        color=color,
        text='formatted_text',
        size_max=100,
        color_continuous_scale='speed',
        **kwargs
    )

    fig.update_traces(
        textfont_size=12,
        textposition='bottom center',
    )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        height=600,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(fig)

