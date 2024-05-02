import ROOT as r
from ._plotter import Plotter
from .index_page import htmlWriter
from . import alignment_utils


def get_2016_vtx_z_2D(infile, selection='vtxSelection', name='out_h'):
    """get vertex position plots for 2016 data"""
    if selection == 'Tight':
        tree = infile.Get("vtxana_Tight_L1L1_nvtx1/vtxana_Tight_L1L1_nvtx1_tree")
        tree.Draw("unc_vtx_z:unc_vtx_mass>>" + name + "(300, 0, 0.3, 200, -40, 40)", "")
        out_h = r.gDirectory.Get(name)
    else:
        out_h = r.TH2F(name, name, 100, 0, 0.2, 100, -10, 10)
    return out_h


def get_2016_vtx_z(infile, selection='vtxSelection', name='out_h'):
    """get vertex position plots for 2016 data"""
    if selection == 'Tight':
        tree = infile.Get("vtxana_Tight_L1L1_nvtx1/vtxana_Tight_L1L1_nvtx1_tree")
        tree.Draw("unc_vtx_z>>" + name + "(150, -30, 20)", "")
        out_h = r.gDirectory.Get(name)
    else:
        out_h = r.TH1F(name, name, 150, -15, 10)
    return out_h


@Plotter.user
def vtx_z(p: Plotter):
    """plot vertex z distributions

    input ROOT files have to contain the '' directory
    """

    p.make_1D_plots_with_fit(
        'vtxana_vtxSelection/vtxana_vtxSelection_vtx_Z_svt_h',
        xtitle='Vertex Z [mm]',
        ytitle='a.u.',
        scale_histos="maximum",
        is_vtxana=True,
        fit=False
    )
    additional_histos = []
    if p.additional_input_files:
        additional_histos = [get_2016_vtx_z(p.additional_input_files[0],
                                            selection='Tight', name='MC_histo'),
                             get_2016_vtx_z(p.additional_input_files[1],
                                            selection='Tight', name='data_histo')
                             ]
    histopaths = []
    for year in p.year:
        histopaths.append(f'vtxana_Tight_{year}/vtxana_Tight_{year}_vtx_Z_svt_h')
    p.make_1D_plots_with_fit(
        histopaths,
        xtitle='Vertex Z [mm]',
        ytitle='a.u.',
        scale_histos="maximum",
        is_vtxana=True,
        additional_histos=additional_histos,
        xrange=[-30, 20]
    )

    p.fit_2D_dist(histoname=['vtxana_vtxSelection/vtxana_vtxSelection_vtx_InvM_vtx_svt_z_hh'],
                  xtitle='M_inv [GeV]', ytitle_mu='#mu vertex z [mm]',
                  ytitle_sigma='#sigma vertex z [mm]',
                  outname=f'vtxana_vtxSelection_vtx_InvM_vtx_svt_z',
                  xrange_mu=[0, 0.3], yrange_mu=[-20, 0],
                  xrange_sigma=[0, 0.3], yrange_sigma=[0, 3])

    if p.additional_input_files:
        additional_histos = [get_2016_vtx_z_2D(p.additional_input_files[0],
                                               selection='Tight', name='MC_histo'),
                             get_2016_vtx_z_2D(p.additional_input_files[1],
                                               selection='Tight', name='data_histo')
                             ]
    histopaths = []
    for year in p.year:
        histopaths.append(f'vtxana_Tight_{year}/vtxana_Tight_{year}_vtx_InvM_vtx_svt_z_hh')
    p.fit_2D_dist(histoname=histopaths, xtitle='M_inv [GeV]', ytitle_mu='#mu vertex z [mm]',
                  ytitle_sigma='#sigma vertex z [mm]', outname=f'vtxana_Tight_vtx_InvM_vtx_svt_z',
                  xrange_mu=[0, 0.3], yrange_mu=[-20, 0], xrange_sigma=[0, 0.3], yrange_sigma=[0, 3],
                  additional_histos=additional_histos)

    p.fit_2D_dist(['vtxana_vtxSelection/vtxana_vtxSelection_vtx_p_sigmaZ_hh'], xtitle='p_{vtx} [GeV]',
                  ytitle_mu='#mu(#sigma z) [mm]', ytitle_sigma='#sigma(#sigma z) [mm]',
                  outname='vtxana_vtxSelection_vtx_p_sigmaZ', yrange_mu=[-20, 10])
    histopaths = []
    for year in p.year:
        histopaths.append(f'vtxana_Tight_{year}/vtxana_Tight_{year}_vtx_p_sigmaZ_hh')
    p.fit_2D_dist(histopaths, xtitle='p_{vtx} [GeV]', ytitle_mu='#mu(#sigma z) [mm]',
                  ytitle_sigma='#sigma(#sigma z) [mm]', outname='vtxana_Tight_vtx_p_sigmaZ',
                  yrange_mu=[-20, 10])

    p.fit_2D_dist(['vtxana_vtxSelection/vtxana_vtxSelection_vtx_p_svt_z_hh'], xtitle='p_{vtx} [GeV]',
                  ytitle_mu='#mu svt z [mm]', ytitle_sigma='#sigma svt z [mm]',
                  outname=f'vtxana_vtxSelection_vtx_p_svt_z', yrange_mu=[-8, -6], xrange_mu=[0.5, 5.5])
    histopaths = []
    for year in p.year:
        histopaths.append(f'vtxana_Tight_{year}/vtxana_Tight_{year}_vtx_p_svt_z_hh')
    p.fit_2D_dist(histopaths, xtitle='p_{vtx} [GeV]', ytitle_mu='#mu svt z [mm]',
                  ytitle_sigma='#sigma svt z [mm]', outname='vtxana_Tight_vtx_p_svt_z',
                  yrange_mu=[-8, -6], xrange_mu=[0.5, 5.5])


def get_2016_vtx_EoP(infile, charge='ele', selection='vtxSelection', name='hout'):
    """get EoP plots for 2016 data"""
    if selection == 'Tight':
        tree = infile.Get("vtxana_Tight_L1L1_nvtx1/vtxana_Tight_L1L1_nvtx1_tree")
        tree.Draw("unc_vtx_" + charge + "_clust_E/unc_vtx_" + charge + "_track_p>>" + name + "(100, 0, 2)", "")
        hout = r.gDirectory.Get(name)
    elif selection == 'Tight_pBot':
        tree = infile.Get("vtxana_Tight_L1L1_nvtx1/vtxana_Tight_L1L1_nvtx1_tree")
        tree.Draw("unc_vtx_" + charge + "_clust_E/unc_vtx_" + charge + "_track_p>>" + name + "(100, 0, 2)",
                  "unc_vtx_pos_track_tanLambda < 0")
        hout = r.gDirectory.Get(name)
    elif selection == 'Tight_pTop':
        tree = infile.Get("vtxana_Tight_L1L1_nvtx1/vtxana_Tight_L1L1_nvtx1_tree")
        tree.Draw("unc_vtx_" + charge + "_clust_E/unc_vtx_" + charge + "_track_p>>" + name + "(100, 0, 2)",
                  "unc_vtx_pos_track_tanLambda > 0")
        hout = r.gDirectory.Get(name)
    else:
        hout = r.TH1F(name, name, 100, 0, 2)
    return hout


@Plotter.user
def eop(p: Plotter):

    for charge in ['ele', 'pos']:
        p.make_1D_plots_with_fit(
            f'vtxana_vtxSelection/vtxana_vtxSelection_{charge}_EoP_h',
            xtitle=f'{charge} E/p',
            ytitle='a.u.',
            scale_histos="maximum",
            is_vtxana=True,
            fit=False
        )

        for selection in ['Tight', 'Tight_pBot', 'Tight_pTop']:
            additional_histos = []
            if p.additional_input_files:
                MC_histo = get_2016_vtx_EoP(p.additional_input_files[0], charge=charge, selection=selection, name='MC_histo')
                data_histo = get_2016_vtx_EoP(p.additional_input_files[1], charge=charge, selection=selection, name='data_histo')
                additional_histos = [MC_histo, data_histo]
            histopaths = []
            for year in p.year:
                histopaths.append(f'vtxana_{selection}_{year}/vtxana_{selection}_{year}_{charge}_EoP_h')
            p.make_1D_plots_with_fit(
                histopaths,
                xtitle=f'{charge} E/p',
                ytitle='a.u.',
                scale_histos="maximum",
                is_vtxana=True,
                additional_histos=additional_histos
            )


@Plotter.user
def momentum(p: Plotter):
    """Currently tailored to analysis for 2024 jeopardy psum plots"""
    additional_histos = []
    if p.additional_input_files:
        additional_histos = [p.additional_input_files[0].Get('tridentAllLayerCombos/pos1111_ele1111/tridentAllLayerCombos_pos1111_ele1111_vtx_p_std_vc_h')]

    p.make_1D_plots_with_fit(
        f'vtxana_Tight_2019/vtxana_Tight_2019_vtx_p_h',
        xtitle=f'P(e^{{+}}e^{{-}}) [GeV]',
        ytitle='a.u.',
        scale_histos="maximum",
        is_vtxana=True,
        fit=False,
        additional_histos=additional_histos,
        yrange=[0, 1.2], xrange=[1, 7]
    )


@Plotter.user
def chi2(p: Plotter):
    for selection in ['vtxSelection', 'Tight_2019']:
        for charge in ['ele', 'pos']:
            p.make_1D_plots_with_fit(
                f'vtxana_{selection}/vtxana_{selection}_{charge}_chi2ndf_h',
                xtitle=f'{charge} #chi^{2}/ndf',
                ytitle='arb. units',
                scale_histos="maximum",
                is_vtxana=True,
                fit=False
            )


@Plotter.user
def vtx_xy(p: Plotter):
    """plot vertex xy distributions"""

    p.fit_2D_dist(['vtxana_vtxSelection/vtxana_vtxSelection_vtx_p_svt_x_hh'],
                  xtitle='p_{vtx} [GeV]', ytitle_mu='#mu svt x [mm]', ytitle_sigma='#sigma svt x [mm]',
                  outname='vtxana_vtxSelection_vtx_p_svt_x')
    histopaths = []
    for year in p.year:
        histopaths.append(f'vtxana_Tight_{year}/vtxana_Tight_{year}_vtx_p_svt_x_hh')
    p.fit_2D_dist(histopaths, xtitle='p_{vtx} [GeV]',
                  ytitle_mu='#mu svt x [mm]', ytitle_sigma='#sigma svt x [mm]',
                  outname='vtxana_Tight_vtx_p_svt_x')

    p.fit_2D_dist(['vtxana_vtxSelection/vtxana_vtxSelection_vtx_p_svt_y_hh'],
                  xtitle='p_{vtx} [GeV]', ytitle_mu='#mu svt y [mm]', ytitle_sigma='#sigma svt y [mm]',
                  outname=f'vtxana_vtxSelection_vtx_p_svt_y')
    histopaths = []
    for year in p.year:
        histopaths.append(f'vtxana_Tight_{year}/vtxana_Tight_{year}_vtx_p_svt_y_hh')
    p.fit_2D_dist(histopaths, xtitle='p_{vtx} [GeV]',
                  ytitle_mu='#mu svt y [mm]', ytitle_sigma='#sigma svt y [mm]',
                  outname='vtxana_Tight_vtx_p_svt_y')

    p.make_1D_plots_with_fit(
        'vtxana_vtxSelection/vtxana_vtxSelection_vtx_X_h',
        xtitle='x_{vtx} [mm]',
        ytitle='a.u.',
        scale_histos="maximum",
        is_vtxana=True
    )
    histopaths = []
    for year in p.year:
        histopaths.append(f'vtxana_Tight_{year}/vtxana_Tight_{year}_vtx_X_h')
    p.make_1D_plots_with_fit(
        histopaths,
        xtitle='x_{vtx} [mm]',
        ytitle='a.u.',
        scale_histos="maximum",
        is_vtxana=True
    )

    p.make_1D_plots_with_fit(
        'vtxana_vtxSelection/vtxana_vtxSelection_vtx_Y_h',
        xtitle='y_{vtx} [mm]',
        ytitle='a.u.',
        scale_histos="maximum",
        is_vtxana=True
    )
    histopaths = []
    for year in p.year:
        histopaths.append(f'vtxana_Tight_{year}/vtxana_Tight_{year}_vtx_Y_h')
    p.make_1D_plots_with_fit(
        histopaths,
        xtitle='y_{vtx} [mm]',
        ytitle='a.u.',
        scale_histos="maximum",
        is_vtxana=True
    )
