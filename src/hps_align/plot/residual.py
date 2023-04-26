import ROOT as r
from ._plotter import Plotter, plotter
from . import alignment_utils
from .index_page import htmlWriter
from .._cfg import cfg


def single_residual_plot(p: Plotter, histo_name, title=""):
    """Plot a single 1D residual plot for the input sensor"""

    histos = [f.Get('res/'+histo_name) for f in p.input_files]

    canv = r.TCanvas("c1", "c1", 2200, 2000)

    if (title == ""):
        title = histo_name.split("_")[3] + "_" + histo_name.split("_")[5]

    maximum = -1.

    fitList = []
    plot_properties = []

    # Normalize and get maximum after normalisation
    for histo in histos:
        # Normalize the histogram to unity
        if abs(histo.Integral()) > 1e-8:
            histo.Scale(1./histo.Integral())
        # Get the maximum
        if (histo.GetMaximum() > maximum):
            maximum = histo.GetMaximum()

    if ("slot") in histo_name:
        title += "_slot"
    elif "hole" in histo_name:
        title += "_hole"

    for ihisto in range(len(histos)):
        p.set_histo_style(histos[ihisto], ihisto)

        # Fitting
        fitList.append(alignment_utils.make_fit(
            histos[ihisto], "singleGausIterative", [], p.colors[ihisto]))

        if (ihisto == 0):
            histos[ihisto].GetXaxis().SetTitle(title)
            histos[ihisto].GetXaxis().SetTitleSize(0.05)
            histos[ihisto].GetXaxis().SetTitleOffset(1.25)
            histos[ihisto].SetMaximum(maximum*1.5)
            histos[ihisto].GetYaxis().SetRangeUser(0.0, maximum*1.5)
            histos[ihisto].Draw("P")
        else:
            histos[ihisto].Draw("P SAME")

        fitList[ihisto].Draw("SAME")

        # Save fit properties
        mu = fitList[ihisto].GetParameter(1)
        sigma = fitList[ihisto].GetParameter(2)

        plot_properties.append((" #mu=%.3f" % round(mu, 3))
                               + (" #sigma=%.3f" % round(sigma, 3)))

    leg = p.do_legend(histos, p.legend_names, 3, plot_properties)

    if (leg is not None):
        leg.Draw()

    text = r.TLatex()
    text.SetNDC()
    text.SetTextFont(42)
    text.SetTextSize(0.04)
    text.SetTextColor(r.kBlack)
    text.DrawLatex(0.16, 0.89, '#bf{#it{HPS}} Work In Progress')

    canv.SaveAs(p.outdir + "/" + histo_name + p.oFext)

    if p.do_HTML:
        hw = htmlWriter(p.outdir)
        hw.add_images(p.outdir)
        hw.close_html()


@plotter()
def one_dim(p: Plotter):
    """Plot the 1D residuals for the sensors in the plot listing"""

    for plot in cfg.plot_list('1D_residual_plots'):
        single_residual_plot(plot)


@plotter()
def summary(p: Plotter):
    """!
    Plot the summary of residuals for all sensors

    @param out_dir_ext extension of the output directory, has to end in /
    """

    histos = [f.Get('res/uresidual_GBL_mod_p') for f in p.input_files]

    canv = r.TCanvas("c1", "c1", 2200, 2000)
    canv.SetGridx()

    for ihisto in range(len(histos)):
        p.set_histo_style(histos[ihisto], ihisto)

        if (ihisto == 0):
            for ibin in range(0, histos[ihisto].GetXaxis().GetNbins()):
                histos[ihisto].GetXaxis().SetBinLabel(
                    ibin+1, p.binLabels[ibin])
                histos[ihisto].GetXaxis().SetLabelSize(0.04)
                histos[ihisto].GetXaxis().ChangeLabel(ibin+1, 270)

            histos[ihisto].GetYaxis().SetRangeUser(-0.2, 0.2)
            histos[ihisto].GetYaxis().SetLabelSize(0.05)
            histos[ihisto].GetYaxis().SetTitle(
                "<unbiased local X residual> [mm]")
            histos[ihisto].GetYaxis().SetTitleSize(
                histos[ihisto].GetYaxis().GetTitleSize()*0.7)
            histos[ihisto].GetYaxis().SetTitleOffset(
                histos[ihisto].GetYaxis().GetTitleOffset()*1.65)

            histos[ihisto].Draw("P")
        else:
            histos[ihisto].Draw("P SAME")

    leg = p.do_legend(histos, p.legend_names,
                      leg_location=[0.5, 0.85])
    if (leg is not None):
        leg.Draw()

    text = r.TLatex()
    text.SetNDC()
    text.SetTextFont(42)
    text.SetTextSize(0.04)
    text.SetTextColor(r.kBlack)
    text.DrawLatex(0.52, 0.87, '#bf{#it{HPS} Work In Progress}')

    canv.SaveAs(p.outdir + "/" + "uresiduals" + p.oFext)

    if p.do_HTML:
        img_type = p.oFext.strip(".")
        hw = htmlWriter(p.outdir, img_type=img_type)
        hw.add_images(p.outdir)
        hw.close_html()
