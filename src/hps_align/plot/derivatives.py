import os
import ROOT as r
from ._plotter import Plotter, plotter
from .index_page import htmlWriter


def single_derivative(p: Plotter, name: str):
    """Make a single derivative plot

    This is here instead of in the Plotter class since it is so
    specialized. We assume that the 'gbl_derivatives' directory
    exists in all the input ROOT files.

    Parameters
    ----------
    p : Plotter
        plotter instance with package of input files to compare
    name : str
        name of derivative to plot
    """

    outdir = os.path.join(p.outdir, 'derivatives')

    if (not os.path.exists(outdir)):
        os.mkdir(outdir)

    histos = []
    for infile in p.input_files:
        histos.append(infile.Get("gbl_derivatives/" + name))

    canv = r.TCanvas("c1", "c1", 2200, 2000)
    canv.SetGridx()
    canv.SetGridy()

    titleName = name
    maximum = -1.

    for histo in histos:
        print(type(histo))
        if abs(histo.Integral()) > 1e-8:
            histo.Scale(1./histo.Integral())

        # Get the maximum
        if (histo.GetMaximum() > maximum):
            maximum = histo.GetMaximum()

    for ihisto in range(len(histos)):
        p.set_histo_style(histos[ihisto], ihisto)

        if (ihisto == 0):
            histos[ihisto].GetXaxis().SetTitle(
                titleName + " global derivative")
            histos[ihisto].GetXaxis().SetTitleSize(0.05)
            histos[ihisto].GetXaxis().SetTitleOffset(0.9)
            histos[ihisto].SetMaximum(maximum*1.5)
            histos[ihisto].Draw("P")

            if "223" in name or "123" in name:
                if int(name[-2:]) < 4:
                    histos[ihisto].GetXaxis().SetRangeUser(-25, 25)
                else:
                    histos[ihisto].GetXaxis().SetRangeUser(-100, 100)
            else:
                histos[ihisto].GetXaxis().SetRangeUser(-5, 5)
        else:
            histos[ihisto].Draw("P SAME")

    leg = p.do_legend(histos, p.legend_names, 3)

    if (leg is not None):
        leg.Draw()

    canv.SaveAs(p.outdir + "/" + name + p.oFext)

    if p.do_HTML:
        img_type = p.oFext.strip(".")
        hw = htmlWriter(p.outdir, img_type=img_type)
        hw.add_images(p.outdir)
        hw.close_html()


@plotter()
def all(p: Plotter):
    """Plot all the derivatives in the plot listing"""
    for plot in p.plot_list('derivatives'):
        single_derivative(p, plot)
