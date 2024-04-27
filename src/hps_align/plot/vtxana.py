import os
import ROOT as r
from ._plotter import Plotter
from .index_page import htmlWriter
from . import alignment_utils

def fit_2D_dist(p: Plotter, histoname: str, xtitle="", ytitle_mu="", ytitle_sigma="", fitfunc="", outname="out", xrange_mu=[], yrange_mu=[], xrange_sigma=[], yrange_sigma=[], additional_histos=[]):
    """!
    Plot z0 vs tanL and fit it

    root file has to contain directory "trk_params/"

    @param name  name of the histogram
    """

    histos = [f.Get(histoname) for f in p.vtxana_input_files]
    histos.extend(additional_histos)

    print("Histograms to fit:", len(histos))

    canv = r.TCanvas("c1", "c1", 2200, 2000)
    canv.SetGridx()
    canv.SetGridy()

    plotProperties = []

    histos_mu = []
    histos_sigma = []

    for ihisto in range(0, len(histos)):

        # Rebin it
        histos[ihisto].Rebin(10)
                
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
            
    leg = p.do_legend(histos_mu, p.legend_names, 2, plotProperties)
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

    leg2 = p.do_legend(histos_sigma, p.legend_names, 2, plotProperties)
    if (leg2 is not None):
        leg2.Draw()
        
    canv2.Update()
    canv2.SaveAs(p.outdir + "/" + outname + "_sigma" + p.oFext)


def get_2016_vtx_z_2D(infile, selection='vtxSelection', name='out_h'):
    """get vertex position plots for 2016 data"""
    if selection=='Tight_2019':
        tree = infile.Get("vtxana_Tight_L1L1_nvtx1/vtxana_Tight_L1L1_nvtx1_tree")
        tree.Draw("unc_vtx_z:unc_vtx_mass>>"+name+"(300, 0, 0.3, 200, -40, 40)","")
        out_h = r.gDirectory.Get(name)
    else:
        out_h = r.TH2F(name, name, 100, 0, 0.2, 100, -10, 10) 
    return out_h


def get_2016_vtx_z(infile, selection='vtxSelection', name='out_h'):
    """get vertex position plots for 2016 data"""
    if selection=='Tight_2019':
        tree = infile.Get("vtxana_Tight_L1L1_nvtx1/vtxana_Tight_L1L1_nvtx1_tree")
        tree.Draw("unc_vtx_z>>"+name+"(150, -30, 20)","")
        out_h = r.gDirectory.Get(name)
    else:
        out_h = r.TH1F(name, name, 150, -15, 10) 
    return out_h


@Plotter.user
def vtx_pos(p: Plotter):
    """plot vertex z distributions

    input ROOT files have to contain the '' directory
    """
    canv1 = r.TCanvas("c", "c", 2200, 2000)
    get_2016_vtx_z_2D(p.additional_input_files[0], selection='Tight_2019', name='MC_histo').Draw("colz")
    canv1.SaveAs("MC_histo.png")

    for selection in ['vtxSelection', 'Tight_2019']:
        p.make_1D_plots_with_fit(
            f'vtxana_{selection}/vtxana_{selection}_vtx_Z_svt_h',
            xtitle='Vertex Z [mm]',
            ytitle='arb. units',
            scale_histos=True,
            is_vtxana=True,
            additional_histos=[get_2016_vtx_z(p.additional_input_files[0], selection=selection, name='MC_histo'), get_2016_vtx_z(p.additional_input_files[1], selection=selection, name='data_histo')],
            xrange=[-30, 20]
        )

        fit_2D_dist(p, f'vtxana_{selection}/vtxana_{selection}_vtx_InvM_vtx_svt_z_hh', xtitle='M_inv [GeV]', ytitle_mu='#mu vertex z [mm]', ytitle_sigma='#sigma vertex z [mm]', outname=f'vtxana_{selection}_vtx_InvM_vtx_svt_z', xrange_mu=[0, 0.3], yrange_mu=[-20, 0], xrange_sigma=[0, 0.3], yrange_sigma=[0, 3], additional_histos=[get_2016_vtx_z_2D(p.additional_input_files[0], selection=selection, name='MC_histo'), get_2016_vtx_z_2D(p.additional_input_files[1], selection=selection, name='data_histo')])

        fit_2D_dist(p, f'vtxana_{selection}/vtxana_{selection}_vtx_p_sigmaZ_hh', xtitle='p_{vtx} [GeV]', ytitle_mu='#mu(#sigma z) [mm]', ytitle_sigma='#sigma(#sigma z) [mm]', outname=f'vtxana_{selection}_vtx_p_sigmaZ', yrange_mu=[-20,10])

        fit_2D_dist(p, f'vtxana_{selection}/vtxana_{selection}_vtx_p_svt_z_hh', xtitle='p_{vtx} [GeV]', ytitle_mu='#mu svt z [mm]', ytitle_sigma='#sigma svt z [mm]', outname=f'vtxana_{selection}_vtx_p_svt_z', yrange_mu=[-8, -6], xrange_mu=[0.5, 5.5])

        fit_2D_dist(p, f'vtxana_{selection}/vtxana_{selection}_vtx_p_svt_x_hh', xtitle='p_{vtx} [GeV]', ytitle_mu='#mu svt x [mm]', ytitle_sigma='#sigma svt x [mm]', outname=f'vtxana_{selection}_vtx_p_svt_x')

        fit_2D_dist(p, f'vtxana_{selection}/vtxana_{selection}_vtx_p_svt_y_hh', xtitle='p_{vtx} [GeV]', ytitle_mu='#mu svt y [mm]', ytitle_sigma='#sigma svt y [mm]', outname=f'vtxana_{selection}_vtx_p_svt_y')

        # p.make_1D_plots_with_fit(
        #     f'vtxana_{selection}/vtxana_{selection}_vtx_sigma_Z_h',
        #     xtitle='#sigma z_{vtx} [mm]',
        #     ytitle='arb. units',
        #     scale_histos=True,
        #     is_vtxana=True
        # )

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


def get_2016_vtx_EoP(infile, charge='ele', selection='vtxSelection', name='hout'):
    """get EoP plots for 2016 data"""
    if selection=='Tight_2019':
        tree = infile.Get("vtxana_Tight_L1L1_nvtx1/vtxana_Tight_L1L1_nvtx1_tree")
        tree.Draw("unc_vtx_"+charge+"_clust_E/unc_vtx_"+charge+"_track_p>>"+name+"(100, 0, 2)","")
        hout = r.gDirectory.Get(name)
    elif selection=='Tight_pBot_2019':
        tree = infile.Get("vtxana_Tight_L1L1_nvtx1/vtxana_Tight_L1L1_nvtx1_tree")
        tree.Draw("unc_vtx_"+charge+"_clust_E/unc_vtx_"+charge+"_track_p>>"+name+"(100, 0, 2)","unc_vtx_pos_track_tanLambda < 0")
        hout = r.gDirectory.Get(name)
    elif selection=='Tight_pTop_2019':
        tree = infile.Get("vtxana_Tight_L1L1_nvtx1/vtxana_Tight_L1L1_nvtx1_tree")
        tree.Draw("unc_vtx_"+charge+"_clust_E/unc_vtx_"+charge+"_track_p>>"+name+"(100, 0, 2)","unc_vtx_pos_track_tanLambda > 0")
        hout = r.gDirectory.Get(name)
    else:
        hout = r.TH1F(name, name, 100, 0, 2) 
    return hout


@Plotter.user
def eop(p: Plotter):
    for selection in ['vtxSelection', 'Tight_2019','Tight_pBot_2019','Tight_pTop_2019']:
        for charge in ['ele', 'pos']:
            MC_histo = get_2016_vtx_EoP(p.additional_input_files[0], charge=charge, selection=selection, name='MC_histo')
            data_histo = get_2016_vtx_EoP(p.additional_input_files[1], charge=charge, selection=selection, name='data_histo')
            p.make_1D_plots_with_fit(
                f'vtxana_{selection}/vtxana_{selection}_{charge}_EoP_h',
                xtitle=f'{charge} E/p',
                ytitle='arb. units',
                scale_histos=True,
                is_vtxana=True,
                additional_histos=[MC_histo, data_histo],
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
