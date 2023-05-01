import ROOT as r
from ._plotter import Plotter
from . import alignment_utils
from .index_page import htmlWriter


@Plotter.user
def Lambda(p: Plotter):
    """Create lambda-kink summary plots

    Unfortunately, we have to break name convention since 'lambda' is
    a reserved word in Python.
    """

    histos = []
    for infile in p.input_files:
        histos.append(infile.Get("gbl_kinks/lambda_kink_mod_p"))

    canv = r.TCanvas("c1", "c1", 2200, 2000)
    canv.SetGridx()
    canv.SetGridy()

    for ihisto in range(len(histos)):
        p.set_histo_style(histos[ihisto], ihisto)

        if (ihisto == 0):

            for ibin in range(0, histos[ihisto].GetXaxis().GetNbins()):
                histos[ihisto].GetXaxis().SetBinLabel(
                    ibin+1, p.binLabels[ibin])
                histos[ihisto].GetXaxis().SetLabelSize(0.04)
                histos[ihisto].GetXaxis().ChangeLabel(ibin+1, 270)

            histos[ihisto].GetYaxis().SetRangeUser(-0.0006, 0.0006)
            histos[ihisto].GetYaxis().SetTitle("<#lambda kink>")
            histos[ihisto].GetYaxis().SetLabelSize(0.05)
            histos[ihisto].GetYaxis().SetTitleSize(
                histos[ihisto].GetYaxis().GetTitleSize()*0.7)
            histos[ihisto].GetYaxis().SetTitleOffset(
                histos[ihisto].GetYaxis().GetTitleOffset()*1.35)
            histos[ihisto].Draw("P")
        else:
            histos[ihisto].Draw("P SAME")

    leg = p.do_legend(histos, p.legend_names, 2)
    if (leg is not None):
        leg.Draw()
    canv.SaveAs(p.outdir + "/" + "lambda_kinks" + p.oFext)

    # Put plots in a webpage
    if p.do_HTML:
        hw = htmlWriter(p.outdir)
        hw.add_images(p.outdir)
        hw.close_html()


@Plotter.user
def phi(p: Plotter):
    """Create and save the phi kink summary plots"""

    histos = []
    for infile in p.input_files:
        histos.append(infile.Get("gbl_kinks/phi_kink_mod_p"))

    canv = r.TCanvas("c1", "c1", 2200, 2000)
    canv.SetGridx()
    canv.SetGridy()

    for ihisto in range(len(histos)):
        p.set_histo_style(histos[ihisto], ihisto)

        if (ihisto == 0):
            for ibin in range(0, histos[ihisto].GetXaxis().GetNbins()):
                histos[ihisto].GetXaxis().SetBinLabel(
                    ibin+1, p.binLabels[ibin])
                histos[ihisto].GetXaxis().SetLabelSize(0.04)
                histos[ihisto].GetXaxis().ChangeLabel(ibin+1, 270)
            histos[ihisto].GetYaxis().SetLabelSize(0.05)
            histos[ihisto].GetYaxis().SetTitle("<#phi kink>")
            histos[ihisto].GetYaxis().SetTitleSize(
                histos[ihisto].GetYaxis().GetTitleSize()*0.7)
            histos[ihisto].GetYaxis().SetTitleOffset(
                histos[ihisto].GetYaxis().GetTitleOffset()*1.35)
            histos[ihisto].GetYaxis().SetRangeUser(-0.00099, 0.00099)
            histos[ihisto].Draw("P")
        else:
            histos[ihisto].Draw("P SAME")

    leg = p.do_legend(histos, p.legend_names, 2)
    if (leg is not None):
        leg.Draw()
    canv.SaveAs(p.outdir + "/" + "phi_kinks" + p.oFext)

    # Profile with gaussian
    histos = []
    histos_mu = []
    for infile in p.input_files:
        histos.append(infile.Get("gbl_kinks/phi_kink_mod"))

    for ihisto in range(len(histos)):
        histos_mu.append(r.TH1F(histos[ihisto].GetName() + "_mu" + str(ihisto), histos[ihisto].GetName() + "_mu" + str(
            ihisto), histos[ihisto].GetXaxis().GetNbins(), histos[ihisto].GetXaxis().GetXmin(), histos[ihisto].GetXaxis().GetXmax()))
        sigma_graph = r.TH1F(histos[ihisto].GetName() + "_sigma" + str(ihisto), histos[ihisto].GetName() + "_sigma" + str(
            ihisto), histos[ihisto].GetXaxis().GetNbins(), histos[ihisto].GetXaxis().GetXmin(), histos[ihisto].GetXaxis().GetXmax())
        alignment_utils.profile_y_with_iterative_gauss_fit(
            histos[ihisto], histos_mu[ihisto], sigma_graph, 1)

        p.set_histo_style(histos_mu[ihisto], ihisto)

        if (ihisto == 0):
            for ibin in range(0, histos[ihisto].GetXaxis().GetNbins()):
                histos_mu[ihisto].GetXaxis().SetBinLabel(
                    ibin+1, p.binLabels[ibin])
                histos_mu[ihisto].GetXaxis().SetLabelSize(0.04)
                histos_mu[ihisto].GetXaxis().ChangeLabel(ibin+1, 270)
            histos_mu[ihisto].GetYaxis().SetLabelSize(0.05)
            histos_mu[ihisto].GetYaxis().SetTitle("<#phi kink> gauss")
            histos_mu[ihisto].GetYaxis().SetTitleSize(
                histos[ihisto].GetYaxis().GetTitleSize()*0.7)
            histos_mu[ihisto].GetYaxis().SetTitleOffset(
                histos[ihisto].GetYaxis().GetTitleOffset()*1.35)
            histos_mu[ihisto].GetYaxis().SetRangeUser(-0.00099, 0.00099)
            histos_mu[ihisto].Draw("P")
        else:
            histos_mu[ihisto].Draw("P SAME")

    leg = p.do_legend(histos_mu, p.legend_names, 2)
    if (leg is not None):
        leg.Draw()
    canv.SaveAs(p.outdir + "/" + "phi_kinks_gaus" + p.oFext)

    if p.do_HTML:
        img_type = p.oFext.strip(".")
        hw = htmlWriter(p.outdir, img_type=img_type)
        hw.add_images(p.outdir)
        hw.close_html()
