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
        # color_continuous_scale='Greens',
        # color_continuous_scale='YlGn',
        **kwargs

    )
    fig.update_traces(
        textfont_size=14,
        textangle=0,
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    fig.update_layout(xaxis_title=None, yaxis_title=None)

    mean_value = int(round(data[y].mean())) if orientation == "v" else int(round(data[x].mean()))
    median_value = int(round(data[y].median())) if orientation == "v" else int(round(data[x].median()))

    if orientation == "v":
        fig.add_hline(
            y=mean_value,
            line_dash="dot",
            line_color="orange",
            line_width=2,
            opacity=0.5,
            label=dict(
                text=f"Mean: {mean_value}",
                textposition="end",
                # textposition="start" if mean_value > median_value else "end",
                font=dict(size=15, color="orange"),
                yanchor="bottom",
            )
        )
        fig.add_hline(
            y=median_value,
            line_dash="dash",
            line_color="green",
            line_width=2,
            opacity=0.5,
            label=dict(
                text=f"Median: {median_value}",
                textposition="end",
                # textposition="start" if median_value > mean_value else "end",
                font=dict(size=15, color="green"),
                yanchor="top",
            )
        )
    else:
        fig.add_vline(
            x=mean_value,
            line_dash="dot",
            line_color="orange",
            line_width=2,
            opacity=0.5,
            label=dict(
                text=f"Mean: {int(round(mean_value))}",
                textposition="end",
                font=dict(size=15, color="orange"),
                xanchor="right" if mean_value < median_value else "left",
            ),
        )
        fig.add_vline(
            x=median_value,
            line_dash="dash",
            line_color="green",
            line_width=2,
            opacity=0.5,
            label=dict(
                text=f"Median: {int(round(median_value))}",
                textposition="start",
                font=dict(size=15, color="green"),
                xanchor="left" if mean_value < median_value else "right",
            ),
        )
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

    # Update layout for consistent styling
    fig.update_layout(
        legend_title_text=legend_title,
        legend=dict(
            y=0.5,
        ),
        width=width,
        height=height,
    )

    st.plotly_chart(fig)

