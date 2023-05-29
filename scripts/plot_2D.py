
import json
from tools.analysis.residual_plots2D import ResidualPlots2D

def main():
    res_plotter2D = ResidualPlots2D(config_file="/Users/schababi/Desktop/config/2DPlot.json")

    is2016 = False

    f = open("plot_list_2D.json", 'r')
    plot_list_config = json.load(f)

    if not is2016:
        if plot_list_config['2D_residual_plots']['not2016']:
            res_plot_list = plot_list_config['2D_residual_plots']['not2016']
        else:
            raise Exception("Plot list not found.")
    else:
        if plot_list_config['2D_residual_plots']['2016']:
                res_plot_list = plot_list_config['2D_residual_plots']['2016']
        else:
            raise Exception("Plot list not found.")

    for plot_name in res_plot_list:
        res_plotter2D.plot_2D_residuals(plot_name)


if __name__ == "__main__":
    main()
