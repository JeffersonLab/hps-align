import os
import ROOT as r
from ._plotter import Plotter
from .index_page import htmlWriter
from . import alignment_utils

def fit_2D_dist(p: Plotter, histoname: str, xtitle="", ytitle_mu="", ytitle_sigma="", fitfunc="", outname="out", xrange_mu=[], yrange_mu=[], xrange_sigma=[], yrange_sigma=[]):
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

        # Rebin it
        histos[ihisto].Rebin(4)
                
        # Profile it
        histos_mu.append(r.TH1F(histos[ihisto].GetName() + "_mu" + str(ihisto), histos[ihisto].GetName() + "_mu" + str(
            ihisto), histos[ihisto].GetXaxis().GetNbins(), histos[ihisto].GetXaxis().GetXmin(), histos[ihisto].GetXaxis().GetXmax()))
        
        histos_sigma.append(r.TH1F(histos[ihisto].GetName() + "_sigma" + str(ihisto), histos[ihisto].GetName() + "_sigma" + str(
            ihisto), histos[ihisto].GetXaxis().GetNbins(), histos[ihisto].GetXaxis().GetXmin(), histos[ihisto].GetXaxis().GetXmax()))
        alignment_utils.profile_y_with_iterative_gauss_fit(
            histos[ihisto], histos_mu[ihisto], histos_sigma[ihisto], 1)

        hist = histos_mu[ihisto]
        hmin = hist.GetBinLowEdge(1)
        hmax = (hist.GetBinLowEdge(hist.GetNbinsX())) + \
            hist.GetBinWidth(hist.GetNbinsX())

        if fitfunc:
            fitF = r.TF1("fit" + str(ihisto), fitfunc, hmin, hmax)
            histos_mu[ihisto].Fit("fit" + str(ihisto), "QNR")
            string = ""
            for i in range(fitF.GetNpar()):
                if i < range(fitF.GetNpar())[-1]:
                    string += str(round(fitF.GetParameter(i), 3)) + ","
                else:
                    string += str(round(fitF.GetParameter(i), 3))
            plotProperties.append(string)

        p.set_histo_style(histos_mu[ihisto], ihisto)
        histos_mu[ihisto].GetYaxis().SetTitle(ytitle_mu)
        histos_mu[ihisto].GetXaxis().SetTitle(xtitle)
        histos_mu[ihisto].GetYaxis().SetTitleSize(
            histos[ihisto].GetYaxis().GetTitleSize()*0.7)
        histos_mu[ihisto].GetYaxis().SetTitleOffset(
            histos[ihisto].GetYaxis().GetTitleOffset()*1.35)

        if xrange_mu:
            histos_mu[ihisto].GetXaxis().SetRangeUser(xrange_mu[0], xrange_mu[1])
        if yrange_mu:
            histos_mu[ihisto].GetYaxis().SetRangeUser(yrange_mu[0], yrange_mu[1])

        if (ihisto == 0):
            histos_mu[ihisto].Draw("P")
        else:
            histos_mu[ihisto].Draw("P SAME")

        if fitfunc:    
            fitF.SetLineColor(p.colors[ihisto])
            fitF.DrawClone("SAME")
            
    leg = p.do_legend(histos_mu, p.legend_names, 3, plotProperties)
    if (leg is not None):
        leg.Draw()

    canv.Update()
    canv.SaveAs(p.outdir + "/" + outname + "_mu" + p.oFext)
    
    #Now plot the sigma
    canv2 = r.TCanvas("c2", "c2", 2200, 2000)
    canv2.SetGridx()
    canv2.SetGridy()
    
    for ihisto in range(0, len(histos)):

        p.set_histo_style(histos_sigma[ihisto], ihisto)
        canv2.cd()
        histos_sigma[ihisto].GetYaxis().SetTitle(ytitle_sigma)
        histos_sigma[ihisto].GetXaxis().SetTitle(xtitle)
        histos_sigma[ihisto].GetYaxis().SetTitleSize(
            histos[ihisto].GetYaxis().GetTitleSize()*0.7)
        histos_sigma[ihisto].GetYaxis().SetTitleOffset(
            histos[ihisto].GetYaxis().GetTitleOffset()*1.35)

        if xrange_sigma:
            histos_sigma[ihisto].GetXaxis().SetRangeUser(xrange_sigma[0], xrange_sigma[1])
        if yrange_sigma:
            histos_sigma[ihisto].GetYaxis().SetRangeUser(yrange_sigma[0], yrange_sigma[1])
        
        if (ihisto == 0):
            histos_sigma[ihisto].Draw("P")
        else:
            histos_sigma[ihisto].Draw("P SAME")

    leg = p.do_legend(histos_sigma, p.legend_names, 3, plotProperties)
    if (leg is not None):
        leg.Draw()
        
    canv2.Update()
    canv2.SaveAs(p.outdir + "/" + outname + "_sigma" + p.oFext)
    
@Plotter.user
def vtx_pos(p: Plotter):
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

        fit_2D_dist(p, f'vtxana_{selection}/vtxana_{selection}_vtx_InvM_vtx_svt_z_hh', xtitle='M_inv [GeV]', ytitle_mu='#mu vertex z [mm]', ytitle_sigma='#sigma vertex z [mm]', outname=f'vtxana_{selection}_vtx_InvM_vtx_svt_z', xrange_mu=[0, 0.3], yrange_mu=[-20, 0], xrange_sigma=[0, 0.3])

        fit_2D_dist(p, f'vtxana_{selection}/vtxana_{selection}_vtx_p_sigmaZ_hh', xtitle='p_{vtx} [GeV]', ytitle_mu='#mu(#sigma z) [mm]', ytitle_sigma='#sigma(#sigma z) [mm]', outname=f'vtxana_{selection}_vtx_p_sigmaZ', yrange_mu=[-20,10])

        fit_2D_dist(p, f'vtxana_{selection}/vtxana_{selection}_vtx_p_svt_z_hh', xtitle='p_{vtx} [GeV]', ytitle_mu='#mu svt z [mm]', ytitle_sigma='#sigma svt z [mm]', outname=f'vtxana_{selection}_vtx_p_svt_z', yrange_mu=[-8, -6], xrange_mu=[0.5, 5.5])

        fit_2D_dist(p, f'vtxana_{selection}/vtxana_{selection}_vtx_p_svt_x_hh', xtitle='p_{vtx} [GeV]', ytitle_mu='#mu svt x [mm]', ytitle_sigma='#sigma svt x [mm]', outname=f'vtxana_{selection}_vtx_p_svt_x')

        fit_2D_dist(p, f'vtxana_{selection}/vtxana_{selection}_vtx_p_svt_y_hh', xtitle='p_{vtx} [GeV]', ytitle_mu='#mu svt y [mm]', ytitle_sigma='#sigma svt y [mm]', outname=f'vtxana_{selection}_vtx_p_svt_y')

        p.make_1D_plots_with_fit(
            f'vtxana_{selection}/vtxana_{selection}_vtx_Z_h',
            xtitle='z_{vtx} [mm]',
            ytitle='arb. units',
            scale_histos=True,
            is_vtxana=True
        )

        p.make_1D_plots_with_fit(
            f'vtxana_{selection}/vtxana_{selection}_vtx_sigma_Z_h',
            xtitle='#sigma z_{vtx} [mm]',
            ytitle='arb. units',
            scale_histos=True,
            is_vtxana=True
        )

        p.make_1D_plots_with_fit(
            f'vtxana_{selection}/vtxana_{selection}_vtx_X_h',
            xtitle='x_{vtx} [mm]',
            ytitle='arb. units',
            scale_histos=True,
            is_vtxana=True
        )

        p.make_1D_plots_with_fit(
            f'vtxana_{selection}/vtxana_{selection}_vtx_Y_h',
            xtitle='y_{vtx} [mm]',
            ytitle='arb. units',
            scale_histos=True,
            is_vtxana=True
        )


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


@Plotter.user
def momentum(p: Plotter):
    for selection in ['vtxSelection', 'Tight_2019']:
        for charge in ['ele', 'pos']:
            p.make_1D_plots_with_fit(
                f'vtxana_{selection}/vtxana_{selection}_{charge}_p_h',
                xtitle=f'{charge} p [GeV]',
                ytitle='arb. units',
                scale_histos=True,
                is_vtxana=True,
                fit=False
            )

        p.make_1D_plots_with_fit(
            f'vtxana_{selection}/vtxana_{selection}_Psum_h',
            xtitle='psum [GeV]',
            ytitle='arb. units',
            scale_histos=True,
            is_vtxana=True,
            fit=False
        )

        p.make_1D_plots_with_fit(
            f'vtxana_{selection}/vtxana_{selection}_vtx_Psum_h',
            xtitle='vtx psum [GeV]',
            ytitle='arb. units',
            scale_histos=True,
            is_vtxana=True,
            fit=False
        )


@Plotter.user
def chi2(p: Plotter):
    for selection in ['vtxSelection', 'Tight_2019']:
        for charge in ['ele', 'pos']:
            p.make_1D_plots_with_fit(
                f'vtxana_{selection}/vtxana_{selection}_{charge}_chi2ndf_h',
                xtitle=f'{charge} #chi^{2}/ndf',
                ytitle='arb. units',
                scale_histos=True,
                is_vtxana=True,
                fit=False
            )
