# -*- coding: utf-8 -*-

from numpy import min as np_min, max as np_max, abs as np_abs, log10

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d
from matplotlib.image import NonUniformImage

from SciDataTool.Functions.Plot.init_fig import init_fig
from SciDataTool.Functions.Plot import COLORS


def plot_3D(
    Xdata,
    Ydata,
    Zdata,
    colormap="RdBu_r",
    color_list=None,
    x_min=None,
    x_max=None,
    y_min=None,
    y_max=None,
    z_min=None,
    z_max=None,
    title="",
    xlabel="",
    ylabel="",
    zlabel="",
    xticks=None,
    yticks=None,
    fig=None,
    ax=None,
    is_logscale_x=False,
    is_logscale_y=False,
    is_logscale_z=False,
    is_disp_title=True,
    type_plot="stem",
    save_path=None,
    is_show_fig=None,
    is_switch_axes=False,
    win_title=None,
    font_name="arial",
    font_size_title=12,
    font_size_label=10,
    font_size_legend=8,
):
    """Plots a 3D graph ("stem", "surf" or "pcolor")

    Parameters
    ----------
    Xdata : ndarray
        array of x-axis values
    Ydata : ndarray
        array of y-axis values
    Zdata : ndarray
        array of z-axis values
    colormap : colormap object
        colormap prescribed by user
    x_min : float
        minimum value for the x-axis (no automated scaling in 3D)
    x_max : float
        maximum value for the x-axis (no automated scaling in 3D)
    y_min : float
        minimum value for the y-axis (no automated scaling in 3D)
    y_max : float
        maximum value for the y-axis (no automated scaling in 3D)
    z_min : float
        minimum value for the z-axis (no automated scaling in 3D)
    z_max : float
        maximum value for the z-axis (no automated scaling in 3D)
    title : str
        title of the graph
    xlabel : str
        label for the x-axis
    ylabel : str
        label for the y-axis
    zlabel : str
        label for the z-axis
    xticks : list
        list of ticks to use for the x-axis
    fig : Matplotlib.figure.Figure
        existing figure to use if None create a new one
    ax : Matplotlib.axes.Axes object
        ax on which to plot the data
    is_logscale_x : bool
        boolean indicating if the x-axis must be set in logarithmic scale
    is_logscale_y : bool
        boolean indicating if the y-axis must be set in logarithmic scale
    is_logscale_z : bool
        boolean indicating if the z-axis must be set in logarithmic scale
    is_disp_title : bool
        boolean indicating if the title must be displayed
    type : str
        type of 3D graph : "stem", "surf", "pcolor" or "scatter"
    save_path : str
        full path including folder, name and extension of the file to save if save_path is not None
    is_show_fig : bool
        True to show figure after plot
    is_switch_axes : bool
        to switch x and y axes
    """

    # Set if figure must be shown if is_show_fig is None
    if is_show_fig is None:
        is_show_fig = True if fig is None else False

    # Set if figure is 3D
    if type_plot != "pcolor" and type != "scatter":
        is_3d = True
    else:
        is_3d = False

    # Set figure if needed
    if fig is None and ax is None:
        (fig, ax, _, _) = init_fig(fig=None, shape="rectangle", is_3d=is_3d)

    if color_list is None:
        color_list = COLORS

    # Calculate z limits
    if z_min is None:
        z_min = np_min(Zdata)
    if z_max is None:
        z_max = np_max(Zdata)

    # Check logscale on z axis
    if is_logscale_z:
        Zdata = 10 * log10(np_abs(Zdata))
        clb_format = "%0.0f"
    else:
        clb_format = "%.4g"

    # Switch axes
    if is_switch_axes:
        Xdata, Ydata = Ydata, Xdata
        if len(Xdata.shape) > 1:
            Xdata = Xdata.T
        if len(Ydata.shape) > 1:
            Ydata = Ydata.T
        if len(Zdata.shape) > 1:
            Zdata = Zdata.T
        x_min, y_min = y_min, x_min
        x_max, y_max = y_max, x_max
        xlabel, ylabel = ylabel, xlabel
        xticks, yticks = yticks, xticks
        is_logscale_x, is_logscale_y = is_logscale_y, is_logscale_x

    # Plot
    if type_plot == "stem":
        for xi, yi, zi in zip(Xdata, Ydata, Zdata):
            line = art3d.Line3D(
                *zip((xi, yi, 0), (xi, yi, zi)),
                linewidth=2.0,
                marker="o",
                markersize=3.0,
                markevery=(1, 1),
                color=COLORS[0]
            )
            ax.add_line(line)
        ax.set_xlim3d(x_max, x_min)
        ax.set_ylim3d(y_min, y_max)
        ax.set_zlim3d(z_min, z_max)
        # set correct angle
        ax.view_init(elev=20.0, azim=45)
        ax.zaxis.set_rotate_label(False)
        ax.set_zlabel(zlabel, rotation=0)
        ax.xaxis.labelpad = 5
        ax.yaxis.labelpad = 5
        ax.zaxis.labelpad = 5
        if xticks is not None:
            ax.xaxis.set_ticks(xticks)
        if yticks is not None:
            ax.yaxis.set_ticks(yticks)
        # white background
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor("w")
        ax.yaxis.pane.set_edgecolor("w")
        ax.zaxis.pane.set_edgecolor("w")
        if is_logscale_z:
            ax.zscale("log")
    elif type_plot == "surf":
        ax.plot_surface(Xdata, Ydata, Zdata, cmap=colormap)
        ax.set_xlim3d(x_max, x_min)
        ax.set_ylim3d(y_min, y_max)
        ax.set_zlim3d(z_min, z_max)
        ax.zaxis.set_rotate_label(False)
        ax.set_zlabel(zlabel, rotation=0)
        ax.xaxis.labelpad = 5
        ax.yaxis.labelpad = 5
        ax.zaxis.labelpad = 5
        if xticks is not None:
            ax.xaxis.set_ticks(xticks)
        if yticks is not None:
            ax.yaxis.set_ticks(yticks)
        # white background
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor("w")
        ax.yaxis.pane.set_edgecolor("w")
        ax.zaxis.pane.set_edgecolor("w")
        if is_logscale_z:
            ax.zscale("log")
    elif type_plot == "pcolor":
        im = NonUniformImage(
            ax,
            interpolation="bilinear",
            extent=(x_min, x_max, y_max, y_min),
            cmap=colormap,
        )
        im.set_data(Xdata, Ydata, Zdata.T)
        ax.images.append(im)
        clb = fig.colorbar(im, ax=ax, format=clb_format)
        clb.ax.set_title(zlabel, fontsize=font_size_legend, fontname=font_name)
        clb.ax.tick_params(labelsize=font_size_legend)
        for l in clb.ax.yaxis.get_ticklabels():
            l.set_family(font_name)
        if xticks is not None:
            ax.xaxis.set_ticks(xticks)
        if yticks is not None:
            ax.yaxis.set_ticks(yticks)
        ax.set_xlim([x_min, x_max])
        ax.set_ylim([y_min, y_max])
    elif type_plot == "scatter":
        c = ax.scatter(
            Xdata, Ydata, c=Zdata, marker="s", cmap=colormap, vmin=z_min, vmax=z_max
        )
        clb = fig.colorbar(c, ax=ax)
        clb.ax.set_title(zlabel, fontsize=font_size_legend, fontname=font_name)
        clb.ax.tick_params(labelsize=font_size_legend)
        for l in clb.ax.yaxis.get_ticklabels():
            l.set_family(font_name)
        if xticks is not None:
            ax.xaxis.set_ticks(xticks)
        if yticks is not None:
            ax.yaxis.set_ticks(yticks)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if is_logscale_x:
        ax.xscale("log")

    if is_logscale_y:
        ax.yscale("log")

    if is_disp_title:
        ax.set_title(title)

    if is_3d:
        for item in (
            [ax.xaxis.label, ax.yaxis.label, ax.zaxis.label]
            + ax.get_xticklabels()
            + ax.get_yticklabels()
            + ax.get_zticklabels()
        ):
            item.set_fontsize(font_size_label)
    else:
        for item in (
            [ax.xaxis.label, ax.yaxis.label]
            + ax.get_xticklabels()
            + ax.get_yticklabels()
        ):
            item.set_fontsize(font_size_label)
            item.set_fontname(font_name)
    ax.title.set_fontsize(font_size_title)
    ax.title.set_fontname(font_name)

    if save_path is not None:
        save_path = save_path.replace("\\", "/")
        fig.savefig(save_path)
        plt.close()

    if is_show_fig:
        fig.show()
        
    if win_title:
        fig.canvas.set_window_title(win_title)
