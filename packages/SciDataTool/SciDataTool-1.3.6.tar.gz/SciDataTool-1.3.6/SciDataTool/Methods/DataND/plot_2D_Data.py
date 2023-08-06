# -*- coding: utf-8 -*-

from SciDataTool.Functions.Plot.plot_2D import plot_2D
from SciDataTool.Functions.Plot import (
    unit_dict,
    norm_dict,
    axes_dict,
    COLORS,
    LINESTYLES,
)
from numpy import squeeze, split, array, where, unique, max as np_max, array2string


def plot_2D_Data(
    self,
    *arg_list,
    is_norm=False,
    unit="SI",
    data_list=[],
    legend_list=[],
    color_list=None,
    curve_colors=None,
    phase_colors=None,
    linestyles=None,
    linewidth_list=[2],
    save_path=None,
    x_min=None,
    x_max=None,
    y_min=None,
    y_max=None,
    is_logscale_x=False,
    is_logscale_y=False,
    is_disp_title=True,
    is_grid=True,
    is_auto_ticks=True,
    is_auto_range=True,
    fig=None,
    ax=None,
    barwidth=100,
    type_plot=None,
    fund_harm_dict=None,
    is_show_fig=None,
    win_title=None,
    thresh=0.02,
    font_name="arial",
    font_size_title=12,
    font_size_label=10,
    font_size_legend=8,
):
    """Plots a field as a function of time

    Parameters
    ----------
    data : Data
        a Data object
    *arg_list : list of str
        arguments to specify which axes to plot
    is_norm : bool
        boolean indicating if the field must be normalized
    unit : str
        unit in which to plot the field
    data_list : list
        list of Data objects to compare
    legend_list : list
        list of legends to use for each Data object (including reference one) instead of data.name
    color_list : list
        list of colors to use for each Data object
    save_path : str
        full path including folder, name and extension of the file to save if save_path is not None
    x_min : float
        minimum value for the x-axis
    x_max : float
        maximum value for the x-axis
    y_min : float
        minimum value for the y-axis
    y_max : float
        maximum value for the y-axis
    is_logscale_x : bool
        boolean indicating if the x-axis must be set in logarithmic scale
    is_logscale_y : bool
        boolean indicating if the y-axis must be set in logarithmic scale
    is_disp_title : bool
        boolean indicating if the title must be displayed
    is_grid : bool
        boolean indicating if the grid must be displayed
    is_auto_ticks : bool
        in fft, adjust ticks to freqs (deactivate if too close)
    is_auto_range : bool
        in fft, display up to 1% of max
    fig : Matplotlib.figure.Figure
        existing figure to use if None create a new one
    ax : Matplotlib.axes.Axes object
        ax on which to plot the data
    barwidth : float
        barwidth scaling factor, only if type_plot = "bargraph"
    type_plot : str
        type of 2D graph : "curve", "bargraph", "barchart" or "quiver"
    fund_harm_dict : dict
        Dict containing axis name as key and frequency/order/wavenumber of fundamental harmonic as value to display fundamental harmonic in red in the fft
    is_show_fig : bool
        True to show figure after plot
    win_title : str
        Title of the plot window
    thresh : float
        threshold for automatic fft ticks
    """

    # Extract arg_list it the function called from another script with *arg_list
    if len(arg_list) == 1 and type(arg_list[0]) == tuple:
        arg_list = arg_list[0]

    if color_list == []:
        color_list = COLORS

    # Set unit
    if unit == "SI":
        unit = self.unit

    # Detect if is fft, build first title part and ylabel
    is_fft = False
    if any("wavenumber" in s for s in arg_list) or any("freqs" in s for s in arg_list):
        is_fft = True
        if "dB" in unit:
            unit_str = (
                "[" + unit + " re. " + str(self.normalizations["ref"]) + self.unit + "]"
            )
        else:
            unit_str = "[" + unit + "]"
        if self.symbol == "Magnitude":
            ylabel = "Magnitude " + r"$[" + unit + "]$"
        else:
            ylabel = r"$|\widehat{" + self.symbol + "}|$ " + unit_str
        if data_list == []:
            title1 = "FFT of " + self.name.lower() + " "
        else:
            title1 = "Comparison of " + self.name.lower() + " FFT "
    else:
        if data_list == []:
            # title = data.name.capitalize() + " for " + ', '.join(arg_list_str)
            title1 = self.name.capitalize() + " "
        else:
            # title = data.name.capitalize() + " for " + ', '.join(arg_list_str)
            title1 = "Comparison of " + self.name.lower() + " "
        if is_norm:
            ylabel = (
                r"$\frac{" + self.symbol + "}{" + self.symbol + "_0}\, [" + unit + "]$"
            )
        else:
            if self.symbol == "Magnitude":
                ylabel = "Magnitude " + r"$[" + unit + "]$"
            else:
                ylabel = r"$" + self.symbol + "\, [" + unit + "]$"

    # Extract field and axes
    Xdatas = []
    Ydatas = []
    data_list2 = [self] + data_list
    for i, d in enumerate(data_list2):
        if is_fft:
            result = d.get_magnitude_along(arg_list, unit=unit, is_norm=is_norm)
            if i == 0:
                axes_list = result.pop("axes_list")
                axes_dict_other = result.pop("axes_dict_other")
                result_0 = result
            Ydatas.append(result.pop(d.symbol))
            Xdatas.append(result[list(result)[0]])
        else:
            result = d.get_along(arg_list, unit=unit, is_norm=is_norm)
            if i == 0:
                axes_list = result.pop("axes_list")
                axes_dict_other = result.pop("axes_dict_other")
                result_0 = result
            Ydatas.append(result.pop(d.symbol))
            Xdatas.append(result[list(result)[0]])

    # Find main axis as the axis with the most values
    # main_axis = axes_list[0]  # max(axes_list, key=lambda x: x.values.size)

    # Build xlabel and title parts 2 and 3
    title2 = ""
    title3 = " for "
    for axis in axes_list:
        # Title part 2
        if axis.unit in norm_dict:
            name = norm_dict[axis.unit].split(" [")[0]
        elif axis.name in axes_dict:
            name = axes_dict[axis.name]
        else:
            name = axis.name
        if (
            axis.extension
            in [
                "whole",
                "interval",
                "oneperiod",
                "antiperiod",
                "smallestperiod",
            ]
            and len(axis.values) > 1
        ):
            title2 = "over " + name.lower()
            if axis.unit == "SI":
                unit = unit_dict[axis.name]
                xlabel = name.capitalize() + " [" + unit + "]"
                main_axis_name = name
            elif axis.unit in norm_dict:
                xlabel = norm_dict[axis.unit]
                main_axis_name = axis.unit
            else:
                unit = axis.unit
                xlabel = name.capitalize() + " [" + unit + "]"
                main_axis_name = name
            if (
                axis.name == "angle"
                and axis.unit == "°"
                and round(np_max(axis.values) / 6) % 5 == 0
            ):
                xticks = [i * round(np_max(axis.values) / 6) for i in range(7)]
            else:
                xticks = None
        else:
            if axis.unit == "SI":
                unit = unit_dict[axis.name]
            elif axis.unit in norm_dict:
                unit = norm_dict[axis.unit]
            else:
                unit = axis.unit

            axis_str = array2string(
                result_0[axis.name], formatter={"float_kind": "{:.2g}".format}
            ).replace(" ", ", ")
            if len(result_0[axis.name]) == 1:
                axis_str = axis_str.strip("[]")

            title3 += name + "=" + axis_str.rstrip(", ") + " [" + unit + "], "

    # Title part 4 containing axes that are here but not involved in requested axes
    title4 = ""
    for axis_name in axes_dict_other:
        title4 += (
            axis_name
            + "="
            + array2string(
                axes_dict_other[axis_name][0],
                formatter={"float_kind": "{:.2g}".format},
            ).replace(" ", ", ")
            + " ["
            + axes_dict_other[axis_name][1]
            + "], "
        )

    if title3 == " for " and title4 == "":
        title3 = ""

    # Concatenate all title parts
    title = title1 + title2 + title3 + title4

    # Remove last coma due to title3 or title4
    title = title.rstrip(", ")
    
    # Remove dimless and quotes
    title = title.replace("[]", "")
    title = title.replace("'", "")

    # Detect how many curves are overlaid, build legend and color lists
    if legend_list == [] and data_list != []:
        legend_list = ["[" + d.name + "] " for d in data_list2]
    elif legend_list == []:
        legend_list = ["" for d in data_list2]
    else:
        legend_list = ["[" + leg + "] " for leg in legend_list]
    legends = []
    # Prepare colors
    if curve_colors is None:
        curve_colors = COLORS
    linestyle_list = linestyles
    for i, d in enumerate(data_list2):
        is_overlay = False
        for axis in axes_list:
            if axis.extension == "list":
                is_overlay = True
                if phase_colors is None:
                    phase_colors = COLORS
                    if linestyles is None:
                        linestyles = ["dashed"]
                n_curves = len(axis.values)
                if axis.unit == "SI":
                    unit = unit_dict[axis.name]
                elif axis.unit in norm_dict:
                    unit = norm_dict[axis.unit]
                else:
                    unit = axis.unit
                if len(d.axes[axis.index].get_values()) > 1:
                    legends += [
                        legend_list[i]
                        + axis.name
                        + "="
                        + axis.values.tolist()[j]
                        + " "
                        + unit
                        if isinstance(axis.values.tolist()[j], str)
                        else legend_list[i]
                        + axis.name
                        + "="
                        + "%.2g" % axis.values.tolist()[j]
                        + " "
                        + unit
                        for j in range(n_curves)
                    ]
                else:
                    legends += [legend_list[i]]

        if not is_overlay:
            legends += [legend_list[i]]

    # Split Ydatas if the plot overlays several curves
    if is_overlay:
        Ydata = []
        for d in Ydatas:
            if d.ndim != 1:
                axis_index = where(array(d.shape) == n_curves)[0]
                if axis_index.size > 1:
                    print("WARNING, several axes with same dimensions")
                Ydata += split(d, n_curves, axis=axis_index[0])
            else:
                Ydata += [d]
        Ydatas = [squeeze(d) for d in Ydata]
        Xdata = []
        for i in range(len(data_list2)):
            Xdata += [Xdatas[i] for x in range(n_curves)]
        Xdatas = Xdata

    # Call generic plot function
    if is_fft:
        freqs = Xdatas[0]
        indices = [
            ind
            for ind, y in enumerate(Ydatas[0])
            if abs(y) > abs(0.02 * np_max(Ydatas[0]))
        ]
        xticks = unique(freqs[indices])

        if is_auto_range:
            if len(xticks) > 0:
                x_min = -xticks[-1] * 0.1
                x_max = xticks[-1] * 1.1

        if not is_auto_ticks:
            xticks = None

        # Force bargraph for fft if type_graph not specified
        if type_plot is None:
            type_plot = "bargraph"

        # Option to draw fundamental harmonic in red
        if not fund_harm_dict:
            fund_harm = None
        else:
            # Activate the option only if main axis is in dict and only one Data is plotted
            if main_axis_name in fund_harm_dict and len(Ydatas) == 1:
                fund_harm = fund_harm_dict[main_axis_name]
            else:
                # Deactivate the option
                fund_harm = None

        plot_2D(
            Xdatas,
            Ydatas,
            legend_list=legends,
            color_list=color_list,
            linestyle_list=linestyle_list,
            linewidth_list=linewidth_list,
            fig=fig,
            ax=ax,
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            type_plot=type_plot,
            x_min=x_min,
            x_max=x_max,
            y_min=y_min,
            y_max=y_max,
            is_logscale_x=is_logscale_x,
            is_logscale_y=is_logscale_y,
            is_disp_title=is_disp_title,
            is_grid=is_grid,
            xticks=xticks,
            save_path=save_path,
            barwidth=barwidth,
            fund_harm=fund_harm,
            is_show_fig=is_show_fig,
            win_title=win_title,
            font_name=font_name,
            font_size_title=font_size_title,
            font_size_label=font_size_label,
            font_size_legend=font_size_legend,
        )

    else:

        # Force curve plot if type_plot not specified
        if type_plot is None:
            type_plot = "curve"

        plot_2D(
            Xdatas,
            Ydatas,
            legend_list=legends,
            color_list=color_list,
            fig=fig,
            ax=ax,
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            type_plot=type_plot,
            x_min=x_min,
            x_max=x_max,
            y_min=y_min,
            y_max=y_max,
            is_logscale_x=is_logscale_x,
            is_logscale_y=is_logscale_y,
            is_disp_title=is_disp_title,
            is_grid=is_grid,
            xticks=xticks,
            linestyle_list=linestyle_list,
            linewidth_list=linewidth_list,
            save_path=save_path,
            is_show_fig=is_show_fig,
            win_title=win_title,
            font_name=font_name,
            font_size_title=font_size_title,
            font_size_label=font_size_label,
            font_size_legend=font_size_legend,
        )
