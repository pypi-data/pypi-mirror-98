import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from mpl_plotter.presets.publication.two_d import line
from mpl_plotter.setup import figure
from mpl_plotter.color.schemes import one

from Alexandria.general.console import print_color


class LinePlots:

    """
    Pane plots
    """

    def four_pane_single(self, t, y, labels, filename, where_does_this_go):
        """
        :param where_does_this_go: Are these plots of the numerical, analytical, or validation data
        """
        if where_does_this_go != "numerical" \
                and where_does_this_go != "analytical"\
                and where_does_this_go != "flight-data"\
                and where_does_this_go != "verification"\
                and where_does_this_go != "validation":
            self.problem(where_does_this_go)

        fig = figure((20, 4))
        ax0 = plt.subplot2grid((1, 4), (0, 0), rowspan=1, colspan=1)
        ax1 = plt.subplot2grid((1, 4), (0, 1), rowspan=1, colspan=1)
        ax2 = plt.subplot2grid((1, 4), (0, 2), rowspan=1, colspan=1)
        ax3 = plt.subplot2grid((1, 4), (0, 3), rowspan=1, colspan=1)

        line(x=t, y=y[0], color=one()[0], y_label=labels[0], ax=ax0, fig=fig)
        line(x=t, y=y[1], color=one()[1], y_label=labels[1], ax=ax1, fig=fig)
        line(x=t, y=y[2], color=one()[2], y_label=labels[2], ax=ax2, fig=fig)
        line(x=t, y=y[3], color=one()[3], y_label=labels[3], ax=ax3, fig=fig)

        plt.tight_layout()
        plt.savefig(f"results/{where_does_this_go}/{filename}.pdf")
        plt.show()

    def four_pane_comparison(self, t, y, y2, labels, legend_labels, filename, where_does_this_go):
        """
        :param where_does_this_go: Is this validation or verification
        """
        if where_does_this_go != "numerical" \
                and where_does_this_go != "analytical" \
                and where_does_this_go != "flight-data" \
                and where_does_this_go != "verification" \
                and where_does_this_go != "validation":
            self.problem(where_does_this_go)

        fig = figure((22, 4))
        ax0 = plt.subplot2grid((1, 4), (0, 0), rowspan=1, colspan=1)
        ax1 = plt.subplot2grid((1, 4), (0, 1), rowspan=1, colspan=1)
        ax2 = plt.subplot2grid((1, 4), (0, 2), rowspan=1, colspan=1)
        ax3 = plt.subplot2grid((1, 4), (0, 3), rowspan=1, colspan=1)

        self.comparison(t, [y[0], y2[0]], ax0, fig, labels[0])
        self.comparison(t, [y[1], y2[1]], ax1, fig, labels[1])
        self.comparison(t, [y[2], y2[2]], ax2, fig, labels[2])
        self.comparison(t, [y[3], y2[3]], ax3, fig, labels[3],
                        plot_label1=legend_labels[0], plot_label2=legend_labels[1],
                        legend=True, legend_loc=(0.875, 0.425))

        plt.subplots_adjust(left=0.1, right=0.85, wspace=0.6, hspace=0.35)
        legend = (c for c in ax3.get_children() if isinstance(c, mpl.legend.Legend))
        plt.savefig(f"results/{where_does_this_go}/{filename}.pdf",
                    bbox_extra_artists=legend, bbox_inches='tight')
        plt.show()

    """
    Single line plots
    """

    def single(self, t, y, label, filename=None, save=False):
        line(x=t, y=y, y_label=label)
        plt.tight_layout()
        if save:
            plt.savefig(f"results/analytical/{filename}.pdf")
        plt.show()

    def comparison(self, t, y,
                   ax, fig,
                   label=None,
                   plot_label1=None, plot_label2=None,
                   legend=False, legend_loc=None,):
        if np.all(y[0] == y[0][0]):
            a = y[0]
            b = y[1]
        elif np.all(y[1] == y[1][0]):
            a = y[1]
            b = y[0]
        else:
            a = y[0]
            b = y[1]
        line(x=t, y=a, color=one()[0], ax=ax, fig=fig,
             plot_label=plot_label1, resize_axes=False)
        line(x=t, y=b, color=one()[1], ax=ax, fig=fig,
             y_label=label, plot_label=plot_label2,
             legend=legend, legend_loc=legend_loc,
             y_bounds=[min(y[0].min(), y[1].min()), max(y[0].max(), y[1].max())],
             custom_y_tick_locations=[min(y[0].min(), y[1].min()), max(y[0].max(), y[1].max())])

    def problem(self, s):
        print("We got a problem\n")
        print("     Your 'where_does_this_go' variable,\n")
        print_color(f"          {s}\n", "red")
        print("is neither 'numerical', 'analytical', 'flight-data', 'verification' nor 'validation'."
              " Think about that\n")
