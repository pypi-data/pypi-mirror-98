# -*- coding: utf-8 -*-

from itertools import repeat

import matplotlib.pyplot as plt
from numpy import (
    ceil,
    argmin,
    abs,
    squeeze,
    split,
    ndarray,
    cumsum,
    zeros,
    shape,
)

from SciDataTool.Functions.Plot.init_fig import init_fig
from SciDataTool.Functions.Plot import COLORS, LINESTYLES


def plot_2D(
    Xdatas,
    Ydatas,
    legend_list=[""],
    color_list=None,
    linestyle_list=None,
    linewidth_list=[2],
    title="",
    xlabel="",
    ylabel="",
    fig=None,
    ax=None,
    is_logscale_x=False,
    is_logscale_y=False,
    is_disp_title=True,
    is_grid=True,
    type_plot="curve",
    fund_harm=None,
    x_min=None,
    x_max=None,
    y_min=None,
    y_max=None,
    xticks=None,
    save_path=None,
    barwidth=5,
    is_show_fig=None,
    win_title=None,
    font_name="arial",
    font_size_title=12,
    font_size_label=10,
    font_size_legend=8,
):
    """Plots a 2D graph (curve, bargraph or barchart) comparing fields in Ydatas

    Parameters
    ----------
    Xdatas : ndarray
        array of x-axis values
    Ydatas : list
        list of y-axes values
    legend_list : list
        list of legends
    color_list : list
        list of colors to use for each curve
    linewidth_list : list
        list of line width to use for each curve
    title : str
        title of the graph
    xlabel : str
        label for the x-axis
    ylabel : str
        label for the y-axis
    fig : Matplotlib.figure.Figure
        existing figure to use if None create a new one
    ax : Matplotlib.axes.Axes object
        ax on which to plot the data
    is_logscale_x : bool
        boolean indicating if the x-axis must be set in logarithmic scale
    is_logscale_y : bool
        boolean indicating if the y-axis must be set in logarithmic scale
    is_disp_title : bool
        boolean indicating if the title must be displayed
    is_grid : bool
        boolean indicating if the grid must be displayed
    type_plot : str
        type of 2D graph : "curve", "bargraph", "barchart" or "quiver"
    fund_harm : float
        frequency/order/wavenumber of the fundamental harmonic that must be displayed in red in the fft
    x_min : float
        minimum value for the x-axis
    x_max : float
        maximum value for the x-axis
    y_min : float
        minimum value for the y-axis
    y_max : float
        maximum value for the y-axis
    xticks : list
        list of ticks to use for the x-axis
    save_path : str
        full path including folder, name and extension of the file to save if save_path is not None
    barwidth : float
        barwidth scaling factor, only if type_plot = "bargraph"
    is_show_fig : bool
        True to show figure after plot
    win_title : str
        Title of the plot window
    """

    # Set is_show_fig if is None
    if is_show_fig is None:
        is_show_fig = True if fig is None else False

    # Set figure if needed
    if fig is None and ax is None:
        (fig, ax, _, _) = init_fig(fig=None, shape="rectangle")

    # Number of curves on a axe
    ndatas = len(Ydatas)

    # Retrocompatibility
    if isinstance(Xdatas, ndarray):
        Xdatas = [Xdatas]

    if len(Xdatas) == 1:
        i_Xdatas = [0 for i in range(ndatas)]
    else:
        i_Xdatas = range(ndatas)

    # Expand default arguments
    if color_list is None:
        color_list = COLORS
    if linestyle_list is None:
        linestyle_list = LINESTYLES
    if len(color_list) < ndatas:
        # Repeat colors and change linestyles
        l = len(color_list)
        n = int(ceil(ndatas / l))
        color_list = color_list * n
        if len(linestyle_list) < n:
            # Expand linestyles
            linestyle_list = linestyle_list + [
                linestyle for linestyle in LINESTYLES if linestyle not in linestyle_list
            ]
        if len(linestyle_list) < n:
            # Linestyles is still too small -> repeat
            m = int(ceil(n / len(linestyle_list)))
            linestyle_list = linestyle_list * m
        linestyles = []
        for i in range(n):
            linestyles += [linestyle_list[i] for j in range(l)]
        linestyle_list = linestyles
    if len(linestyle_list) < ndatas:
        # Repeat linestyles
        m = int(ceil(ndatas / len(linestyle_list)))
        linestyle_list = linestyle_list * m
    if len(linewidth_list) < ndatas:
        # Repeat linewidths
        m = int(ceil(ndatas / len(linewidth_list)))
        linewidth_list = linewidth_list * m
    if 1 == len(legend_list) < ndatas:
        # Set no legend for all curves
        legend_list = list(repeat("", ndatas))
        no_legend = True
    else:
        no_legend = False

    # Plot
    if type_plot == "curve":
        for i in range(ndatas):
            ax.plot(
                Xdatas[i_Xdatas[i]],
                Ydatas[i],
                color=color_list[i],
                label=legend_list[i],
                linewidth=linewidth_list[i],
                ls=linestyle_list[i],
            )
        if xticks is not None:
            ax.xaxis.set_ticks(xticks)
    elif type_plot == "bargraph":
        positions = range(-ndatas + 1, ndatas, 2)
        if x_max is not None:
            width = x_max / barwidth
        else:
            width = Xdatas[i_Xdatas[0]][-1] / barwidth
        for i in range(ndatas):
            # width = (Xdatas[i_Xdatas[i]][1] - Xdatas[i_Xdatas[i]][0]) / ndatas
            barlist = ax.bar(
                Xdatas[i_Xdatas[i]] + positions[i] * width / (2 * ndatas),
                Ydatas[i],
                color=color_list[i],
                width=width,
                label=legend_list[i],
            )
            if fund_harm is not None:  # Find fundamental
                imax = argmin(abs(Xdatas[i] - fund_harm))
                barlist[imax].set_edgecolor("k")
                barlist[imax].set_facecolor("k")

        if xticks is not None:
            ax.xaxis.set_ticks(xticks)
            plt.xticks(rotation=90, ha="center", va="top")
    elif type_plot == "barchart":
        for i in range(ndatas):
            if i == 0:
                ax.bar(
                    range(len(Xdatas[i_Xdatas[i]])),
                    Ydatas[i],
                    color=color_list[i],
                    width=0.5,
                    label=legend_list[i],
                )
            else:
                ax.bar(
                    range(len(Xdatas[i_Xdatas[i]])),
                    Ydatas[i],
                    edgecolor=color_list[i],
                    width=0.5,
                    fc="None",
                    lw=1,
                    label=legend_list[i],
                )
        plt.xticks(
            range(len(Xdatas[i_Xdatas[i]])),
            [str(f) for f in Xdatas[i_Xdatas[i]]],
            rotation=90,
        )
    elif type_plot == "quiver":
        for i in range(ndatas):
            x = [e[0] for e in Xdatas[i_Xdatas[i]]]
            y = [e[1] for e in Xdatas[i_Xdatas[i]]]
            vect_list = split(Ydatas[i], 2)
            ax.quiver(x, y, squeeze(vect_list[0]), squeeze(vect_list[1]))
            ax.axis("equal")
    elif type_plot == "curve_point":
        for i in range(ndatas):
            ax.plot(
                Xdatas[i_Xdatas[i]],
                Ydatas[i],
                color=color_list[i],
                label=legend_list[i],
                linewidth=linewidth_list[i],
            )
            ax.plot(
                Xdatas[i_Xdatas[i]],
                Ydatas[i],
                ".",
                markerfacecolor=color_list[i],
                markeredgecolor=color_list[i],
                markersize=10,
            )
    elif type_plot == "point":
        for i in range(ndatas):
            ax.plot(
                Xdatas[i_Xdatas[i]],
                Ydatas[i],
                ".",
                markerfacecolor=color_list[i],
                markeredgecolor=color_list[i],
                markersize=10,
            )
    elif type_plot == "barStackResultant":
        data = Ydatas[0:-1]

        def get_cumulated_array(data, **kwargs):
            cum = data.clip(**kwargs)
            cum = cumsum(cum, axis=0)
            d = zeros(shape(data))
            d[1:] = cum[:-1]
            return d

        cumulated_data = get_cumulated_array(data, min=0)
        cumulated_data_neg = get_cumulated_array(data, max=0)

        # Re-merge negative and positive data.
        row_mask = data < 0
        cumulated_data[row_mask] = cumulated_data_neg[row_mask]
        data_stack = cumulated_data

        for i in range(len(data)):
            ax.bar(
                x=Xdatas[0],
                height=data[i],
                bottom=data_stack[i],
                color=color_list[i],
                label=legend_list[i],
                width=barwidth,
            )

        ax.bar(
            x=Xdatas[1],
            height=Ydatas[-1],
            width=barwidth,
            color=["k"],
            label="Resultant",
        )

        ax.legend()

        if xticks is None:
            plt.xticks([])

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])

    if is_logscale_x:
        ax.set_xscale("log")

    if is_logscale_y:
        ax.set_yscale("log")

    if is_disp_title:
        ax.set_title(title)

    if is_grid:
        ax.grid()

    if ndatas > 1 and not no_legend:
        ax.legend(prop={"family": font_name, "size": font_size_legend})

    plt.tight_layout()
    for item in (
        [ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()
    ):
        item.set_fontname(font_name)
        item.set_fontsize(font_size_label)
    ax.title.set_fontname(font_name)
    ax.title.set_fontsize(font_size_title)

    if save_path is not None:
        save_path = save_path.replace("\\", "/")
        fig.savefig(save_path)
        plt.close()

    if is_show_fig:
        fig.show()

    if win_title:
        fig.canvas.set_window_title(win_title)
