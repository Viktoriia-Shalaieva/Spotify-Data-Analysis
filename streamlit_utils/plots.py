import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st


def create_bar_plot(data, x, y, orientation="v", text=None, showticklabels=False, **kwargs):
    """
    Create and display a bar plot using Plotly Express.

    This function generates a bar plot based on the provided data and customization options.
    The plot is displayed using Streamlit's `st.plotly_chart`.

    Args:
        data (DataFrame): The dataset used to generate the bar plot.
        x (str): The column name for the x-axis values.
        y (str): The column name for the y-axis values.
        orientation (str, optional): Orientation of the bars; "v" for vertical (default) or "h" for horizontal.
        text (str, optional): Column name for displaying text values on the bars.
        showticklabels (bool, optional): Whether to display tick labels on the x-axis. Defaults to False.
        **kwargs: Additional keyword arguments passed to `plotly.express.bar` for further customization.

    Returns:
        None: This function does not return a value. It directly displays the bar plot in the Streamlit app.
    """
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
    """
    Create and display a choropleth map using Plotly Express.

    This function generates a choropleth map to visualize geographical data based on the provided parameters.
    The map is displayed using Streamlit's `st.plotly_chart`.

    Args:
        data (DataFrame): The dataset used to generate the choropleth map.
        locations (str): The column name containing location codes or names.
        location_mode (str): Determines the interpretation of location codes.
        color (str): The column name determining the data values used for coloring the map.
        title (str, optional): Title of the map. Defaults to None.
        hover_name (str, optional): Column name for hover text information. Defaults to None.
        color_discrete_sequence (list, optional): List of colors for discrete values. Defaults to None.
        color_continuous_scale (str or list, optional): Color scale for continuous values. Defaults to None.
        labels (dict, optional): Dictionary mapping column names to labels for display purposes. Defaults to None.
        legend_title (str, optional): Title for the legend. Defaults to None.
        width (int, optional): Width of the map in pixels. Defaults to 1400.
        height (int, optional): Height of the map in pixels. Defaults to 800.
        **kwargs: Additional keyword arguments passed to `plotly.express.choropleth` for further customization.

    Returns:
        None: This function does not return a value. It directly displays the choropleth map in the Streamlit app.
    """
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


def create_bubble_plot(data, x, y, size, text=None, yaxis_title=None, **kwargs):
    """
    Create and display a bubble plot using Plotly Express.

    This function generates a scatter plot where marker sizes are determined by a specified column,
    creating a "bubble plot." The plot is displayed using Streamlit's `st.plotly_chart`.

    Args:
        data (DataFrame): The dataset used to generate the bubble plot.
        x (str): The column name for the x-axis values.
        y (str): The column name for the y-axis values.
        size (str): The column name determining the size of the bubbles.
        text (str, optional): Column name for displaying text inside or near the bubbles. Defaults to None.
        yaxis_title (str, optional): Title for the y-axis. Defaults to None.
        **kwargs: Additional keyword arguments passed to `plotly.express.scatter` for further customization.

    Returns:
        None: This function does not return a value. It directly displays the bubble plot in the Streamlit app.
    """
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
    """
    Create and display a scatter plot using Plotly Express.

    This function generates a scatter plot with options for coloring, hover data, symbol markers,
    and a LOWESS trendline. The plot is displayed using Streamlit's `st.plotly_chart`.

    Args:
        data (DataFrame): The dataset used to generate the scatter plot.
        x (str): The column name for the x-axis values.
        y (str): The column name for the y-axis values.
        color (str): The column name for coloring the points.
        hover_data (list or dict): Additional data to display when hovering over a point.
        symbol (str): The column name for determining the marker symbol.
        color_map (dict): A dictionary mapping color values to specific colors.

    Returns:
        None: This function does not return a value. It directly displays the scatter plot in the Streamlit app.
    """
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
    """
    Create and display a histogram using Plotly Express.

    This function generates a histogram to visualize the distribution of a specified column in the dataset.
    The plot is displayed using Streamlit's `st.plotly_chart`.

    Args:
        data (DataFrame): The dataset used to generate the histogram.
        x (str): The column name for the variable to be plotted on the x-axis.
        nbins (int, optional): Number of bins for the histogram. Defaults to 10.
        color (str, optional): The column name for grouping data by color. Defaults to None.
        yaxis_title (str, optional): Title for the y-axis. Defaults to 'Count'.
        **kwargs: Additional keyword arguments passed to `plotly.express.histogram` for further customization.

    Returns:
        None: This function does not return a value. It directly displays the histogram in the Streamlit app.
    """
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
    """
    Create and display a histogram with normal distribution indicators using Plotly Express.

    This function generates a histogram for a specified variable and overlays visual elements
    to represent the mean, median, and standard deviations. The plot is displayed using Streamlit's `st.plotly_chart`.

    Args:
        data (DataFrame): The dataset used to generate the histogram.
        x (str): The column name for the variable to be plotted on the x-axis.
        country (str): The name of the country for display in the plot title.
        mean (float): The mean value of the distribution.
        median (float): The median value of the distribution.
        one_std_dev (tuple): The range representing one standard deviation (min, max).
        two_std_dev (tuple): The range representing two standard deviations (min, max).
        three_std_dev (tuple): The range representing three standard deviations (min, max).
        nbins (int, optional): Number of bins for the histogram. Defaults to 10.
        yaxis_title (str, optional): Title for the y-axis. Defaults to 'Count'.
        **kwargs: Additional keyword arguments passed to `plotly.express.histogram` for further customization.

    Returns:
        None: This function does not return a value. It directly displays the histogram in the Streamlit app.
    """
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
    """
    Create and display a pie chart using Plotly Express.

    This function generates a pie chart to visualize the proportion of categories in the dataset.
    The chart is displayed using Streamlit's `st.plotly_chart`.

    Args:
        data (DataFrame): The dataset used to generate the pie chart.
        names (str): The column name representing the categories to be displayed as slices of the pie.
        **kwargs: Additional keyword arguments passed to `plotly.express.pie` for further customization.

    Returns:
        None: This function does not return a value. It directly displays the pie chart in the Streamlit app.
    """
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
    """
    Create and display a box plot using Plotly Express.

    This function generates a box plot to visualize the distribution of a numeric variable
    across different categories. The plot is displayed using Streamlit's `st.plotly_chart`.

    Args:
        data (DataFrame): The dataset used to generate the box plot.
        x (str): The column name representing the categorical variable on the x-axis.
        y (str): The column name representing the numeric variable on the y-axis.
        color_discrete_map (dict, optional): A dictionary mapping category names to specific colors. Defaults to None.
        color_discrete_sequence (list, optional): A list of colors for the categories. Defaults to None.
        **kwargs: Additional keyword arguments passed to `plotly.express.box` for further customization.

    Returns:
        None: This function does not return a value. It directly displays the box plot in the Streamlit app.
    """
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
    """
    Create and display a polar chart using Plotly Express.

    This function generates a polar chart to visualize data in a circular coordinate system,
    connecting points with lines and markers. The chart is displayed using Streamlit's `st.plotly_chart`.

    Args:
        data (DataFrame): The dataset used to generate the polar chart.
        r (str): The column name representing the radial axis values.
        theta (str): The column name representing the angular axis values.
        height (int, optional): The height of the chart in pixels. Defaults to 550.

    Returns:
        None: This function does not return a value. It directly displays the polar chart in the Streamlit app.
    """
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
    """
    Create and display a heatmap using Plotly Express.

    This function generates a density heatmap to visualize the relationship between two variables
    and their aggregated values. The heatmap is displayed using Streamlit's `st.plotly_chart`.

    Args:
        data (DataFrame): The dataset used to generate the heatmap.
        x (str): The column name representing the variable on the x-axis.
        y (str): The column name representing the variable on the y-axis.
        z (str): The column name representing the values to aggregate for the heatmap intensity.
        label_z (str): Label for the color scale representing the aggregated values.
        height (int, optional): The height of the heatmap in pixels. Defaults to 600.

    Returns:
        None: This function does not return a value. It directly displays the heatmap in the Streamlit app.
    """
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
    """
    Create and display a line chart using Plotly Express.

    This function generates a line chart to visualize trends over time or another continuous variable.
    The chart is displayed using Streamlit's `st.plotly_chart`.

    Args:
        data (DataFrame): The dataset used to generate the line chart.
        x (str): The column name for the x-axis values.
        y (str): The column name for the y-axis values.
        text (str, optional): The column name for text annotations on the points. Defaults to None.
        log_y (bool, optional): Whether to use a logarithmic scale for the y-axis. Defaults to True.
        yaxis_title (str, optional): Title for the y-axis. Defaults to None.
        **kwargs: Additional keyword arguments passed to `plotly.express.line` for further customization.

    Returns:
        None: This function does not return a value. It directly displays the line chart in the Streamlit app.
    """
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


def create_boxplot_subplots(x, y, y2, title, categoryarray):
    """
    Create and display a subplot of box plots using Plotly.

    This function generates two side-by-side box plots: one for categorized data and another for overall data.
    The plots share a y-axis for easier comparison. The visualization is displayed using Streamlit's `st.plotly_chart`.

    Args:
        x (array-like): The categorical variable for the x-axis in the first box plot.
        y (array-like): The numeric variable for the y-axis in the first box plot.
        y2 (array-like): The numeric variable for the second (overall) box plot.
        title (str): Title for the y-axis, describing the variable being compared.
        categoryarray (list): Custom order for the x-axis categories.

    Returns:
        None: This function does not return a value. It directly displays the box plot subplots in the Streamlit app.
    """
    fig = make_subplots(
        rows=1, cols=2,
        shared_yaxes=True,
        horizontal_spacing=0.02,
        column_widths=[0.94, 0.06],
    )
    fig.add_trace(
        go.Box(
            x=x,
            y=y,
            marker=dict(color='#109618'),
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Box(
            y=y2,
            name="Overall",
            marker=dict(color='orange'),
        ),
        row=1, col=2
    )
    fig.update_layout(
        height=700,
        showlegend=False,
        yaxis=dict(title=title),
        xaxis=dict(
            categoryorder='array',
            categoryarray=categoryarray
        )
    )
    st.plotly_chart(fig)
