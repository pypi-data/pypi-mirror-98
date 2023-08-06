from mpl_plotter.two_d import line as mpl_line, scatter as mpl_scatter


def line(x, y, aspect=1, demo_pad_plot=True,
         x_tick_number=20, tick_label_size_x=7,
         y_tick_number=20, tick_label_size_y=7,
         y_label_size=20, x_label_size=20, legend_size=15,
         tick_ndecimals_y=3, fine_tick_loactions=True,
         figsize=(15, 10), spines_removed=None,
         **kwargs):
    return mpl_line(x=x, y=y,
                    demo_pad_plot=demo_pad_plot,
                    x_tick_number=x_tick_number, tick_label_size_x=tick_label_size_x,
                    y_tick_number=y_tick_number, tick_label_size_y=tick_label_size_y,
                    y_label_size=y_label_size, x_label_size=x_label_size, legend_size=legend_size,
                    tick_ndecimals_y=tick_ndecimals_y,
                    fine_tick_locations=fine_tick_loactions,
                    spines_removed=spines_removed,
                    figsize=figsize, aspect=aspect,
                    **kwargs
                    )


def scatter(x, y, demo_pad_plot=True,
          x_tick_number=3, tick_label_size_x=15,
          y_tick_number=3, tick_label_size_y=15,
          y_label_size=20, x_label_size=20, legend_size=15,
          tick_ndecimals_y=3, fine_tick_locations=True,
          **kwargs):
    return mpl_scatter(x=x, y=y,
                    demo_pad_plot=demo_pad_plot,
                    x_tick_number=x_tick_number, tick_label_size_x=tick_label_size_x,
                    y_tick_number=y_tick_number, tick_label_size_y=tick_label_size_y,
                    y_label_size=y_label_size, x_label_size=x_label_size, legend_size=legend_size,
                    tick_ndecimals_y=tick_ndecimals_y,
                    fine_tick_locations=fine_tick_locations,
                    **kwargs
                    )
