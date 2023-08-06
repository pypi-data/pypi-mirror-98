from matplotlib import pyplot as plt
from matplotlib import gridspec
from .ec_plotter import ECPlotter
from .ms_plotter import MSPlotter


class ECMSPlotter:
    """A matplotlib plotter for EC-MS measurements."""

    def __init__(self, measurement=None):
        """Initiate the ECMSPlotter with its default Meausurement to plot"""
        self.measurement = measurement

    def plot_measurement(
        self,
        *,
        measurement=None,
        axes=None,
        mass_list=None,
        mass_lists=None,
        tspan=None,
        tspan_bg=None,
        unit="A",
        V_str=None,
        J_str=None,
        V_color="k",
        J_color="r",
        logplot=None,
        legend=True,
        **kwargs,
    ):
        """Make an EC-MS plot vs time and return the axis handles.

        Allocates tasks to ECPlotter.plot_measurement() and MSPlotter.plot_measurement()

        TODO: add all functionality in the legendary plot_experiment() in EC_MS.Plotting
            - variable subplot sizing (emphasizing EC or MS)
            - plotting of calibrated data (mol_list instead of mass_list)
            - units!
        Args:
            measurement (ECMSMeasurement): defaults to the measurement to which the
                plotter is bound (self.measurement)
            axes (list of three matplotlib axes): axes[0] plots the MID data,
                axes[1] the variable given by V_str (potential), and axes[2] the
                variable given by J_str (current). By default three axes are made with
                axes[0] a top panel with 3/5 the area, and axes[1] and axes[2] are
                the left and right y-axes of the lower panel with 2/5 the area.
            mass_list (list of str): The names of the m/z values, eg. ["M2", ...] to
                plot. Defaults to all of them (measurement.mass_list)
            mass_lists (list of list of str): Alternately, two lists can be given for
                masses in which case one list is plotted on the left y-axis and the other
                on the right y-axis of the top panel.
            tspan (iter of float): The time interval to plot, wrt measurement.tstamp
            tspan_bg (timespan): A timespan for which to assume the signal is at its
                background. The average signals during this timespan are subtracted.
                If `mass_lists` are given rather than a single `mass_list`, `tspan_bg`
                must also be two timespans - one for each axis. Default is `None` for no
                background subtraction.
            unit (str): the unit for the MS data. Defaults to "A" for Ampere
            V_str (str): The name of the value to plot on the lower left y-axis.
                Defaults to the name of the series `measurement.potential`
            J_str (str): The name of the value to plot on the lower right y-axis.
                Defaults to the name of the series `measurement.current`
            V_color (str): The color to plot the variable given by 'V_str'
            J_color (str): The color to plot the variable given by 'J_str'
            logplot (bool): Whether to plot the MS data on a log scale (default True
                unless mass_lists are given)
            legend (bool): Whether to use a legend for the MS data (default True)
            kwargs (dict): Additional kwargs go to all calls of matplotlib's plot()
        """
        measurement = measurement or self.measurement

        logplot = (not mass_lists) if logplot is None else logplot

        if not axes:
            gs = gridspec.GridSpec(5, 1)
            # gs.update(hspace=0.025)
            axes = [plt.subplot(gs[0:3, 0])]
            axes += [plt.subplot(gs[3:5, 0])]
            axes += [axes[1].twinx()]

        if not tspan:
            if hasattr(measurement, "potential") and measurement.potential:
                t, _ = measurement.grab("potential")
                tspan = [t[0], t[-1]]
            else:
                tspan = measurement.tspan

        if hasattr(measurement, "potential") and measurement.potential:
            # then we have EC data!
            ECPlotter().plot_measurement(
                measurement=measurement,
                axes=[axes[1], axes[2]],
                tspan=tspan,
                V_str=V_str,
                J_str=J_str,
                V_color=V_color,
                J_color=J_color,
                **kwargs,
            )
        if mass_list or hasattr(measurement, "mass_list"):
            # then we have MS data!
            ms_axes = MSPlotter().plot_measurement(
                measurement=measurement,
                ax=axes[0],
                tspan=tspan,
                tspan_bg=tspan_bg,
                mass_list=mass_list,
                mass_lists=mass_lists,
                unit=unit,
                logplot=logplot,
                legend=legend,
            )
            try:
                ms_axes.set_ylabel(f"signal / [{unit}]")
            except AttributeError:
                for ax in ms_axes:
                    ax.set_ylabel(f"signal / [{unit}]")
                    if ax not in axes:
                        axes.append(ax)
        axes[0].xaxis.set_label_position("top")
        axes[0].tick_params(
            axis="x", top=True, bottom=False, labeltop=True, labelbottom=False
        )
        axes[1].set_xlim(axes[0].get_xlim())
        return axes

    def plot_vs_potential(self):
        """FIXME: This is needed due to assignment in ECMeasurement.__init__"""
