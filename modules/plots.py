import plotly.express as px
import streamlit as st


def create_bar_plot(data, x, y, orientation="v", text=None, showticklabels=False, **kwargs):
    fig = px.bar(
        data,
        x=x,
        y=y,
        orientation=orientation,
        text=text,
        color=y if orientation == "v" else x,
        color_continuous_scale='Turbo',
        **kwargs
    )
    fig.update_traces(
        textfont_size=12,
        textangle=0,
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    fig.update_layout(
        yaxis_title=None,
        coloraxis_showscale=False,
        xaxis=dict(
            showticklabels=showticklabels,
            title=None,
        )
    )
    st.plotly_chart(fig)


def create_choropleth_map(data, locations, location_mode, color, title=None, hover_name=None,
                          color_discrete_sequence=None, color_continuous_scale=None, labels=None,
                          legend_title=None, width=1400, height=800, **kwargs):
    fig = px.choropleth(
        data,
        locations=locations,
        locationmode=location_mode,
        color=color,
        hover_name=hover_name,
        color_discrete_sequence=color_discrete_sequence,
        color_continuous_scale=color_continuous_scale,
        labels=labels,
        title=title,
        hover_data={'Country': False},
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


def create_bubble_plot(data, x, y, size, color=None, text=None, yaxis_title=None, **kwargs):
    fig = px.scatter(
        data,
        x=x,
        y=y,
        size=size,
        color=y,
        color_continuous_scale='Turbo',
        text=text,
        size_max=80,
        **kwargs
    )
    fig.update_traces(
        textfont_size=12,
        textposition='bottom center',
        textfont_color='black',
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    fig.update_layout(
        xaxis_title=None,
        yaxis_title=yaxis_title,
        height=600,
        margin=dict(l=20, r=20, t=20, b=20),
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig)


def create_scatter_plot(data, x, y, color, hover_data, symbol, color_map):
    fig = px.scatter(
        data,
        x=x,
        y=y,
        color=color,
        hover_data=hover_data,
        symbol=symbol,
        trendline="lowess",
        opacity=0.5,
        color_discrete_map=color_map,
    )
    fig.update_traces(showlegend=True)
    fig.update_layout(height=600)

    st.plotly_chart(fig)


def create_histogram(data, x, nbins=10, color=None, yaxis_title='Count', **kwargs):
    fig = px.histogram(
        data,
        x=x,
        color=color,
        nbins=nbins,
        barmode='overlay' if color else 'group',
        color_discrete_sequence=['#109618'],
        **kwargs
    )
    fig.update_layout(
        yaxis_title=yaxis_title,
        bargap=0.05,
        yaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig)


def create_histogram_normal_distribution(data, x, country, mean, median, one_std_dev, two_std_dev,
                                         three_std_dev, nbins=10, yaxis_title='Count', **kwargs):
    fig = px.histogram(
        data,
        x=x,
        nbins=nbins,
        title=f"Track Popularity Distribution in Top 50 - {country}",
        opacity=0.7,
        color_discrete_sequence=['#109618'],
        **kwargs
    )
    fig.update_layout(
        yaxis_title=yaxis_title,
        bargap=0.05,
        yaxis=dict(showgrid=False),
    )
    fig.add_vline(
        x=mean,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Mean: {mean:.2f}",
        annotation_position="top right",
        annotation_font_color="black"
    )
    fig.add_vline(
        x=median,
        line_dash="dot",
        line_color="orange",
        annotation_text=f"Median: {median:.2f}",
        annotation_position="bottom left",
        annotation_font_color="black",
    )
    fig.update_layout(
        bargap=0.05,
        yaxis=dict(showgrid=False),
    )
    fig.add_vrect(
        x0=one_std_dev[0], x1=one_std_dev[1],
        fillcolor="blue", opacity=0.1,
        layer="below", line_width=0,
        annotation_text="1 Std Dev",
        annotation_position="top left",
        annotation_font_color="black",
    )
    fig.add_vrect(
        x0=two_std_dev[0], x1=two_std_dev[1],
        fillcolor="green", opacity=0.1,
        layer="below", line_width=0,
        annotation_text="2 Std Dev",
        annotation_position="top left",
        annotation_font_color="black",
    )
    fig.add_vrect(
        x0=three_std_dev[0], x1=three_std_dev[1],
        fillcolor="yellow", opacity=0.1,
        layer="below", line_width=0,
        annotation_text="3 Std Dev",
        annotation_position="top left",
        annotation_font_color="black",
    )
    st.plotly_chart(fig)


def create_pie_chart(data, names, **kwargs):
    fig = px.pie(
        data,
        names=names,
        color_discrete_sequence=px.colors.qualitative.Vivid,
        **kwargs
    )
    fig.update_traces(
        textinfo='percent+label',
    )
    fig.update_layout(
        showlegend=False
    )
    st.plotly_chart(fig)


def create_boxplot(data, x, y, color_discrete_map=None, color_discrete_sequence=None, **kwargs):
    fig = px.box(
        data,
        x=x,
        y=y,
        color=x,
        color_discrete_map=color_discrete_map,
        color_discrete_sequence=color_discrete_sequence,
        **kwargs
    )
    st.plotly_chart(fig)


def create_polar_chart(data, r, theta, height=550):
    fig = px.line_polar(
        data,
        r=r,
        theta=theta,
        line_close=True,
        color_discrete_sequence=['#109618'],
    )
    fig.update_traces(
        mode='lines+markers',
        fill='toself',
        marker=dict(size=8, line=dict(color='black', width=1))
    )
    fig.update_layout(
        autosize=True,
        height=height,
        polar=dict(
            radialaxis=dict(visible=True, title=r, showticklabels=True)
        )
    )
    st.plotly_chart(fig)


def create_heatmap(data, x, y, z, label_z, height=600):
    fig = px.density_heatmap(
        data,
        x=x,
        y=y,
        z=z,
        labels={z: label_z},
        color_continuous_scale='Turbo',
    )
    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        xaxis=dict(tickangle=45),
        height=height,
        coloraxis_colorbar=dict(title="Frequency"),
    )
    st.plotly_chart(fig)


def create_line_chart(data, x, y, text=None, log_y=True, yaxis_title=None, **kwargs):
    fig = px.line(
        data,
        x=x,
        y=y,
        text=text,
        log_y=log_y,
        color_discrete_sequence=['#109618'],
        **kwargs
    )
    fig.update_traces(
        textposition='top center',
        textfont=dict(size=12, color='black'),
        line=dict(width=3, color='rgba(0, 0, 255, 0.3)'),
        marker=dict(size=8, color='green', opacity=1),
    )
    fig.update_layout(
        yaxis_title=yaxis_title,
    )
    st.plotly_chart(fig)
