import json
from tools.analysis.fee_momentum_plots import FeeMomentumPlots
from tools.analysis.track_plots import TrackPlots
from tools.analysis.residual_plots import ResidualPlots
from tools.analysis.kink_plots import KinkPlots
from tools.analysis.profile_plots import ProfilePlots
from tools.analysis.vertex_plots import VertexPlots
from tools.analysis.derivative_plots import DerivativePlots
from tools.analysis.tanL_plots import TanLambdaPlots
import tools.analysis.alignment_utils as alignUtils


def main():

    doTrackPlots = True
    doFEEs = True
    doResiduals = True
    doSummaryPlots = True
    doDerivatives = False  # note: this only works if root file has gbl_derivatives/
    doEoPPlots = False  # note: this only works if root file has EoP/
    is2016 = False
    do_vertex_plots = False  # note: this only works if root file has MultiEventVtx/

    f = open("plot_list.json", 'r')
    plot_list_config = json.load(f)

    # set style of histograms
    alignUtils.set_style()

    if doSummaryPlots:
        kink_plotter = KinkPlots()
        kink_plotter.plot_lambda_kinks()
        kink_plotter.plot_phi_kinks()

    tanL_plotter = TanLambdaPlots()
    tanL_plotter.plot_z0_vs_tanL_fit("z0_vs_tanLambda_top")
    tanL_plotter.plot_z0_vs_tanL_fit("z0_vs_tanLambda_bottom")

    if (doResiduals):
        res_plotter = ResidualPlots()
        res_plotter.plot_summary()
        res_plot_list = []
        if not is2016:
            if plot_list_config['1D_residual_plots']['not2016']:
                res_plot_list = plot_list_config['1D_residual_plots']['not2016']
            else:
                raise Exception("Plot list not found.")
        else:
            if plot_list_config['1D_residual_plots']['2016']:
                res_plot_list = plot_list_config['1D_residual_plots']['2016']
            else:
                raise Exception("Plot list not found.")

        for plot_name in res_plot_list:
            res_plotter.plot_1D_residuals(plot_name)

        profile_plotter = ProfilePlots()

        for vol in ["top", "bottom"]:
            if not is2016:
                ures_vs_u_plot_list = plot_list_config['ures_vs_u_plots']['not2016'][vol]['name']
                ures_vs_u_title_list = plot_list_config['ures_vs_u_plots']['not2016'][vol]['title']
                ures_vs_v_plot_list = plot_list_config['ures_vs_v_pred_plots']['not2016'][vol]['name']
                ures_vs_v_title_list = plot_list_config['ures_vs_v_pred_plots']['not2016'][vol]['title']
            else:
                ures_vs_u_plot_list = plot_list_config['ures_vs_u_plots']['2016'][vol]['name']
                ures_vs_u_title_list = plot_list_config['ures_vs_u_plots']['2016'][vol]['title']
                ures_vs_v_plot_list = plot_list_config['ures_vs_v_pred_plots']['2016'][vol]['name']
                ures_vs_v_title_list = plot_list_config['ures_vs_v_pred_plots']['2016'][vol]['title']

            if ures_vs_u_plot_list == [] or ures_vs_v_title_list == []:
                raise Exception("Plot list not found.")

            for ipl in range(len(ures_vs_u_plot_list)):
                if ipl == 0 or ipl == 1:
                    profile_plotter.plot_profileY(ures_vs_u_plot_list[ipl], xtitle=ures_vs_u_title_list[ipl], rangeX=[-10, 10], rangeY=[-0.2, 0.2])
                    profile_plotter.plot_profileY(ures_vs_v_plot_list[ipl], xtitle=ures_vs_v_title_list[ipl], rangeX=[-20, 20], rangeY=[-0.15, 0.15])
                else:
                    profile_plotter.plot_profileY(ures_vs_u_plot_list[ipl], xtitle=ures_vs_u_title_list[ipl], rangeY=[-0.2, 0.2])
                    profile_plotter.plot_profileY(ures_vs_v_plot_list[ipl], xtitle=ures_vs_v_title_list[ipl], rangeY=[-0.15, 0.15])

    if do_vertex_plots:
        vertex_plotter = VertexPlots()
        vertex_plotter.plot_multi_vtx()

    trk_profile_plotter = ProfilePlots("trk_params/")
    trk_profile_plotter.plot_profileY("p_vs_tanLambda_top", xtitle="tan(#lambda)", ytitle="p [GeV]", rangeY=[0., 5.], fit="[0] + [1]*x")
    trk_profile_plotter.plot_profileY("p_vs_tanLambda_bottom", xtitle="tan(#lambda)", ytitle="p [GeV]", rangeY=[0., 5.], fit="[0] + [1]*x")

    trk_profile_plotter.plot_profileY("d0_vs_tanLambda_top", xtitle="tan(#lambda) top", ytitle="d0 [mm]", rangeX=[0, 0.1], rangeY=[-1., 1.])
    trk_profile_plotter.plot_profileY("d0_vs_tanLambda_bottom", xtitle="tan(#lambda) bot", ytitle="d0 [mm]", rangeX=[-0.1, 0], rangeY=[-1., 1.])

    trk_profile_plotter.plot_profileY("d0_vs_phi_top", xtitle="#phi top", ytitle="d0 [mm]", rangeX=[0, 0.1], rangeY=[-1., 1.])
    trk_profile_plotter.plot_profileY("d0_vs_phi_bottom", xtitle="#phi bot", ytitle="d0 [mm]", rangeX=[-0.1, 0], rangeY=[-1., 1.])

    trk_profile_plotter.plot_profileY("p_vs_phi_top", xtitle="#phi", ytitle="p [GeV]", rangeY=[0., 5.], fit="[0] + [1]*x")
    trk_profile_plotter.plot_profileY("p_vs_phi_bottom", xtitle="#phi", ytitle="p [GeV]", rangeY=[0., 5.], fit="[0] + [1]*x")

    if (doEoPPlots):
        eop_profile_plotter = ProfilePlots("EoP/")
        eop_profile_plotter.plot_profileY("EoP_vs_trackP_top_fid", xtitle="Top track P [GeV]", rangeY=[0.7, 1.3], fit="[0]")

        eop_profile_plotter.plot_profileY("EoP_vs_trackP_ele_top_fid", xtitle="Top ele track P [GeV]", rangeY=[0.7, 1.3], fit="[0]", fitrange=[0.7, 1.2])

        eop_profile_plotter.plot_profileY("EoP_vs_trackP_pos_top_fid", xtitle="Top pos track P [GeV]", rangeY=[0.7, 1.3], fit="[0]")

        eop_profile_plotter.plot_profileY("EoP_vs_trackP_bottom_fid", xtitle="Bot track P [GeV]", rangeY=[0.7, 1.3], fit="[0]")

        eop_profile_plotter.plot_profileY("EoP_vs_trackP_ele_bottom_fid", xtitle="Bot ele track P [GeV]", rangeY=[0.7, 1.3], fit="[0]", fitrange=[0.7, 1.2])

        eop_profile_plotter.plot_profileY("EoP_vs_trackP_pos_bottom_fid", xtitle="Bot pos track P [GeV]", rangeY=[0.7, 1.3], fit="[0]")

        eop_profile_plotter.plot_profileY("EoP_vs_tanLambda_fid", xtitle="track tan(#lambda) [GeV]", rangeX=[-0.07, 0.07], rangeY=[0.7, 1.3], fit="[0]*x*x*x + [1]*x*x + [2]*x + [3]")

        eop_profile_plotter.plot_profileY("EoP_vs_phi_fid", xtitle="track #phi [GeV]", rangeY=[0.5, 1.3], fit="[0]*x*x*x + [1]*x*x + [2]*x + [3]")

        eop_profile_plotter.plot_profileY("EoP_vs_phi_top_fid", xtitle="Top track #phi [GeV]", rangeY=[0.5, 1.3], fit="[0]*x*x*x + [1]*x*x + [2]*x + [3]")

        eop_profile_plotter.plot_profileY("EoP_vs_phi_bottom_fid", xtitle="Bottom track #phi [GeV]", rangeY=[0.5, 1.3], fit="[0]*x*x*x + [1]*x*x + [2]*x + [3]")

    if (doTrackPlots):
        tp = TrackPlots()
        tp.plot_histos()

        fee_plots = FeeMomentumPlots()
        fee_plots.plot_histos("trk_params/z0_top")

        fee_plots.plot_histos("trk_params/z0_bottom")
        fee_plots.plot_histos("trk_params/d0_top")
        fee_plots.plot_histos("trk_params/d0_bottom")
        fee_plots.plot_histos("trk_params/trk_extr_bs_x_top")
        fee_plots.plot_histos("trk_params/trk_extr_bs_y_top")
        fee_plots.plot_histos("trk_params/trk_extr_bs_x_bottom")
        fee_plots.plot_histos("trk_params/trk_extr_bs_y_bottom")

    if (doFEEs):
        fee_plots = FeeMomentumPlots()
        fee_plots.plot_histos("trk_params/Chi2_top_neg", do_fit=False)
        fee_plots.plot_histos("trk_params/Chi2_top_pos", do_fit=False)
        fee_plots.plot_histos("trk_params/Chi2_bottom_neg", do_fit=False)
        fee_plots.plot_histos("trk_params/Chi2_bottom_pos", do_fit=False)
        fee_plots.plot_histos("trk_params/p_bottom")
        fee_plots.plot_histos("trk_params/p_top")
        fee_plots.plot_histos("trk_params/p_slot_top")
        fee_plots.plot_histos("trk_params/p_hole_top", xtitle="e^{-} Hole side p [GeV]")
        fee_plots.plot_histos("trk_params/p_slot_bottom", xtitle="e^{-} Slot side p [GeV]", ytitle="Tracks")
        fee_plots.plot_histos("trk_params/p_hole_bottom", xtitle="e^{-} Hole side p [GeV]", ytitle="Tracks")
        fee_plots.plot_histos("trk_params/p5h_top", xtitle="p [GeV]", ytitle="Tracks")
        fee_plots.plot_histos("trk_params/p6h_top", xtitle="p [GeV]", ytitle="Tracks")
        fee_plots.plot_histos("trk_params/p7h_top", xtitle="p [GeV]", ytitle="Tracks")
        # fee_plots.plot_histos("trk_params/p6h_top")
        # fee_plots.plot_histos("trk_params/p6h_bottom")
        # fee_plots.plot_histos("trk_params/p7h_bottom")

    if (doDerivatives):
        print("doDerivatives")
        deriv_plotter = DerivativePlots()

        # deriv_plotter.plot_derivatives("12101")
        # deriv_plotter.plot_derivatives("12201")
        deriv_plotter.plot_derivatives("12301")

        # deriv_plotter.plot_derivatives("22101")
        # deriv_plotter.plot_derivatives("22201")
        deriv_plotter.plot_derivatives("22301")

        # deriv_plotter.plot_derivatives("12105")
        # deriv_plotter.plot_derivatives("12205")
        deriv_plotter.plot_derivatives("12305")

        # deriv_plotter.plot_derivatives("22105")
        # deriv_plotter.plot_derivatives("22205")
        deriv_plotter.plot_derivatives("22305")

        # deriv_plotter.plot_derivatives("12110")
        # deriv_plotter.plot_derivatives("12210")
        deriv_plotter.plot_derivatives("12310")

        # deriv_plotter.plot_derivatives("22110")
        # deriv_plotter.plot_derivatives("22210")
        deriv_plotter.plot_derivatives("22310")


if __name__ == "__main__":
    main()
