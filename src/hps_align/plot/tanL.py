import ROOT as r
from ._plotter import Plotter, plotter
from . import alignment_utils
from .index_page import htmlWriter
from .._cfg import cfg


def z0_vs_tanL_fit(p: Plotter, name: str):
    """!
    Plot z0 vs tanL and fit it

    root file has to contain directory "trk_params/"

    @param name  name of the histogram
    """

    histos = [f.Get('trk_params/'+name) for f in p.input_files]

    print("Histograms to fit:", len(histos))
    canv = r.TCanvas("c1", "c1", 2200, 2000)
    canv.SetGridx()
    canv.SetGridy()

    plotProperties = []

    histos_mu = []
    histos_sigma = []

    for ihisto in range(0, len(histos)):
        # Profile it
        histos_mu.append(r.TH1F(histos[ihisto].GetName()+"_mu"+str(ihisto), histos[ihisto].GetName()+"_mu"+str(
            ihisto), histos[ihisto].GetXaxis().GetNbins(), histos[ihisto].GetXaxis().GetXmin(), histos[ihisto].GetXaxis().GetXmax()))

        histos_sigma.append(r.TH1F(histos[ihisto].GetName()+"_sigma"+str(ihisto), histos[ihisto].GetName()+"_sigma"+str(
            ihisto), histos[ihisto].GetXaxis().GetNbins(), histos[ihisto].GetXaxis().GetXmin(), histos[ihisto].GetXaxis().GetXmax()))
        alignment_utils.profile_y_with_iterative_gauss_fit(
            histos[ihisto], histos_mu[ihisto], histos_sigma[ihisto], 1)

        hist = histos_mu[ihisto]
        hmin = hist.GetBinLowEdge(1)
        hmax = (hist.GetBinLowEdge(hist.GetNbinsX())) + \
            hist.GetBinWidth(hist.GetNbinsX())

        fitF = r.TF1("fit"+str(ihisto), "[1]*x + [0]", hmin, hmax)
        histos_mu[ihisto].Fit("fit" + str(ihisto), "QNR")
        string = ""
        for i in range(fitF.GetNpar()):
            if i < range(fitF.GetNpar())[-1]:
                string += str(round(fitF.GetParameter(i), 3)) + ","
            else:
                string += str(round(fitF.GetParameter(i), 3))
        plotProperties.append(string)

        p.set_histo_style(histos_mu[ihisto], ihisto)
        histos_mu[ihisto].GetYaxis().SetTitle("<z0> [mm]")
        histos_mu[ihisto].GetXaxis().SetTitle("tan(#lambda)")
        histos_mu[ihisto].GetYaxis().SetTitleSize(
            histos[ihisto].GetYaxis().GetTitleSize()*0.7)
        histos_mu[ihisto].GetYaxis().SetTitleOffset(
            histos[ihisto].GetYaxis().GetTitleOffset()*1.35)

        histos_mu[ihisto].GetYaxis().SetRangeUser(-2, 2)
        histos_mu[ihisto].GetXaxis().SetRangeUser(-2, 2)

        if (ihisto == 0):
            histos_mu[ihisto].Draw("P")
        else:
            histos_mu[ihisto].Draw("P SAME")

        fitF.SetLineColor(p.colors[ihisto])
        fitF.DrawClone("SAME")

    leg = p.do_legend(histos_mu, p.legend_names, 2, plotProperties)
    if (leg is not None):
        leg.Draw()

    canv.SaveAs(p.outdir + "/" + name + p.oFext)

    if p.do_HTML:
        img_type = p.oFext.strip(".")
        hw = htmlWriter(p.outdir, img_type=img_type)
        hw.add_images(p.outdir)
        hw.close_html()


@plotter()
def tanL(p: Plotter):
    z0_vs_tanL_fit(p, 'z0_vs_tanLambda_top')
    z0_vs_tanL_fit(p, 'z0_vs_tanLambda_bottom')
