import os
import ROOT as r
from ._plotter import Plotter
from .index_page import htmlWriter
from . import alignment_utils

def fit_2D_dist(p: Plotter, histoname: str, xtitle="", ytitle="", fitfunc="[1]*x + [0]", outname="out"):
    """!
    Plot z0 vs tanL and fit it

    root file has to contain directory "trk_params/"

    @param name  name of the histogram
    """

    histos = [f.Get(histoname) for f in p.vtxana_input_files]

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

        fitF = r.TF1("fit"+str(ihisto), fitfunc, hmin, hmax)
        histos_mu[ihisto].Fit("fit" + str(ihisto), "QNR")
        string = ""
        for i in range(fitF.GetNpar()):
            if i < range(fitF.GetNpar())[-1]:
                string += str(round(fitF.GetParameter(i), 3)) + ","
            else:
                string += str(round(fitF.GetParameter(i), 3))
        plotProperties.append(string)

        p.set_histo_style(histos_mu[ihisto], ihisto)
        histos_mu[ihisto].GetYaxis().SetTitle(ytitle)
        histos_mu[ihisto].GetXaxis().SetTitle(xtitle)
        histos_mu[ihisto].GetYaxis().SetTitleSize(
            histos[ihisto].GetYaxis().GetTitleSize()*0.7)
        histos_mu[ihisto].GetYaxis().SetTitleOffset(
            histos[ihisto].GetYaxis().GetTitleOffset()*1.35)

        histos_mu[ihisto].GetYaxis().SetRangeUser(-20, 0)
        histos_mu[ihisto].GetXaxis().SetRangeUser(0, 0.3)

        if (ihisto == 0):
            histos_mu[ihisto].Draw("P")
        else:
            histos_mu[ihisto].Draw("P SAME")

        fitF.SetLineColor(p.colors[ihisto])
        fitF.DrawClone("SAME")

    leg = p.do_legend(histos_mu, p.legend_names, 3, plotProperties)
    if (leg is not None):
        leg.Draw()

    canv.Update()
    canv.SaveAs(p.outdir + "/" + outname + p.oFext)


@Plotter.user
def vtx_z(p: Plotter):
    """plot vertex z distributions

    input ROOT files have to contain the '' directory
    """
    for selection in ['vtxSelection', 'Tight_2019']:
        p.make_1D_plots_with_fit(
            f'vtxana_{selection}/vtxana_{selection}_vtx_Z_svt_h',
            xtitle='Vertex Z [mm]',
            ytitle='arb. units',
            scale_histos=True,
            is_vtxana=True
        )

        fit_2D_dist(p, f'vtxana_{selection}/vtxana_{selection}_vtx_InvM_vtx_svt_z_hh', xtitle='M_inv [GeV]', ytitle='vertex z [mm]', outname=f'vtxana_{selection}_vtx_InvM_vtx_svt_z')

@Plotter.user
def eop(p: Plotter):
    for selection in ['vtxSelection', 'Tight_2019']:
        for charge in ['ele', 'pos']:
            p.make_1D_plots_with_fit(
                f'vtxana_{selection}/vtxana_{selection}_{charge}_EoP_h',
                xtitle=f'{charge} E/p',
                ytitle='arb. units',
                scale_histos=True,
                is_vtxana=True
            )

        # fit_2D_dist(p, f'vtxana_{selection}/vtxana_{selection}_vtx_InvM_vtx_svt_z_hh', xtitle='M_inv [GeV]', ytitle='vertex z [mm]', outname=f'vtxana_{selection}_vtx_InvM_vtx_svt_z')
    
   