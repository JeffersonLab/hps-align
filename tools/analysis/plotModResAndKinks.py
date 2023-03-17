from fee_momentum_plots import FeeMomentumPlots
from track_plots import TrackPlots
from index_page import htmlWriter
import commonConfig as config
import utilities as utils
import ROOT as r
import os
from residual_plots import ResidualPlots
from kink_plots import KinkPlots
from profile_plots import ProfilePlots
from vertex_plots import VertexPlots
from derivative_plots import DerivativePlots
from tanL_plots import TanLambdaPlots


r.gStyle.SetOptStat(0)


def main():

    doTrackPlots = False ## \todo FIXME: AttributeError: 'NoneType' object has no attribute 'SaveAs'
    doFEEs = True
    doResiduals = False
    doSummaryPlots = True
    doDerivatives = False
    outputFolder = "AlignmentResults"
    doEoPPlots = False  ## \todo: FIXME eop broken because EoP/EoP_vs_trackP_top_fid NOT FOUND
    is2016 = False
    do_vertex_plots = False
    set_style = False

    outdir = "translations"
    if (not os.path.exists(outputFolder)):
        os.mkdir(outputFolder)

    outFolder = outputFolder + "/" + outdir

    if (not os.path.exists(outFolder)):
        os.mkdir(outFolder)

    print("STORING RESULTS IN::", outFolder)

    # Style of plots
    if set_style:
        utils.SetStyle()

    inputFiles = config.args.inputFiles
    legends = config.args.legend

    # inputFiles = inFiles
    # legends = inLegends

    inputF = []
    for inputFile in inputFiles:
        inputF.append(r.TFile(inputFile))

    if doSummaryPlots:
        kink_plotter = KinkPlots()
        kink_plotter.plot_lambda_kinks()
        kink_plotter.plot_phi_kinks()
        # plotLambdaKinks(inputF, legends, outFolder)
        # plotPhiKinks(inputF, legends, outFolder)

    tanL_plotter = TanLambdaPlots()
    tanL_plotter.plot_z0_vs_tanL_fit("z0_vs_tanLambda_top")
    tanL_plotter.plot_z0_vs_tanL_fit("z0_vs_tanLambda_bottom")

    if (doResiduals):
        res_plotter = ResidualPlots()
        res_plotter.plot_summary()
        res_plotter.plot_1D_residuals("uresidual_GBL_module_L1b_halfmodule_axial_sensor0")
        res_plotter.plot_1D_residuals("uresidual_GBL_module_L1b_halfmodule_stereo_sensor0")
        res_plotter.plot_1D_residuals("uresidual_GBL_module_L2b_halfmodule_axial_sensor0")
        res_plotter.plot_1D_residuals("uresidual_GBL_module_L2b_halfmodule_stereo_sensor0")
        res_plotter.plot_1D_residuals("uresidual_GBL_module_L3b_halfmodule_axial_sensor0")
        res_plotter.plot_1D_residuals("uresidual_GBL_module_L3b_halfmodule_stereo_sensor0")

        if not is2016:
            res_plotter.plot_1D_residuals("uresidual_GBL_module_L4b_halfmodule_axial_sensor0")
            res_plotter.plot_1D_residuals("uresidual_GBL_module_L4b_halfmodule_stereo_sensor0")
        else:
            res_plotter.plot_1D_residuals("uresidual_GBL_module_L4b_halfmodule_axial_hole_sensor0")
            res_plotter.plot_1D_residuals("uresidual_GBL_module_L4b_halfmodule_axial_slot_sensor0")
            res_plotter.plot_1D_residuals("uresidual_GBL_module_L4b_halfmodule_stereo_hole_sensor0")
            res_plotter.plot_1D_residuals("uresidual_GBL_module_L4b_halfmodule_stereo_slot_sensor0")

        res_plotter.plot_1D_residuals("uresidual_GBL_module_L5b_halfmodule_axial_hole_sensor0")
        res_plotter.plot_1D_residuals("uresidual_GBL_module_L5b_halfmodule_axial_slot_sensor0")
        res_plotter.plot_1D_residuals("uresidual_GBL_module_L5b_halfmodule_stereo_hole_sensor0")
        res_plotter.plot_1D_residuals("uresidual_GBL_module_L5b_halfmodule_stereo_slot_sensor0")

        res_plotter.plot_1D_residuals("uresidual_GBL_module_L6b_halfmodule_axial_hole_sensor0")
        res_plotter.plot_1D_residuals("uresidual_GBL_module_L6b_halfmodule_axial_slot_sensor0")
        res_plotter.plot_1D_residuals("uresidual_GBL_module_L6b_halfmodule_stereo_hole_sensor0")
        res_plotter.plot_1D_residuals("uresidual_GBL_module_L6b_halfmodule_stereo_slot_sensor0")

        if not is2016:
            res_plotter.plot_1D_residuals("uresidual_GBL_module_L7b_halfmodule_axial_hole_sensor0")
            res_plotter.plot_1D_residuals("uresidual_GBL_module_L7b_halfmodule_axial_slot_sensor0")
            res_plotter.plot_1D_residuals("uresidual_GBL_module_L7b_halfmodule_stereo_hole_sensor0")
            res_plotter.plot_1D_residuals("uresidual_GBL_module_L7b_halfmodule_stereo_slot_sensor0")

        res_plotter.plot_1D_residuals("uresidual_GBL_module_L1t_halfmodule_axial_sensor0")
        res_plotter.plot_1D_residuals("uresidual_GBL_module_L1t_halfmodule_stereo_sensor0")
        res_plotter.plot_1D_residuals("uresidual_GBL_module_L2t_halfmodule_axial_sensor0")
        res_plotter.plot_1D_residuals("uresidual_GBL_module_L2t_halfmodule_stereo_sensor0")
        res_plotter.plot_1D_residuals("uresidual_GBL_module_L3t_halfmodule_axial_sensor0")
        res_plotter.plot_1D_residuals("uresidual_GBL_module_L3t_halfmodule_stereo_sensor0")

        if not is2016:
            res_plotter.plot_1D_residuals("uresidual_GBL_module_L4t_halfmodule_axial_sensor0")
            res_plotter.plot_1D_residuals("uresidual_GBL_module_L4t_halfmodule_stereo_sensor0")
        else:
            res_plotter.plot_1D_residuals("uresidual_GBL_module_L4t_halfmodule_axial_hole_sensor0")
            res_plotter.plot_1D_residuals("uresidual_GBL_module_L4t_halfmodule_axial_slot_sensor0")
            res_plotter.plot_1D_residuals("uresidual_GBL_module_L4t_halfmodule_stereo_hole_sensor0")
            res_plotter.plot_1D_residuals("uresidual_GBL_module_L4t_halfmodule_stereo_slot_sensor0")

        res_plotter.plot_1D_residuals("uresidual_GBL_module_L5t_halfmodule_axial_hole_sensor0")
        res_plotter.plot_1D_residuals("uresidual_GBL_module_L5t_halfmodule_axial_slot_sensor0")
        res_plotter.plot_1D_residuals("uresidual_GBL_module_L5t_halfmodule_stereo_hole_sensor0")
        res_plotter.plot_1D_residuals("uresidual_GBL_module_L5t_halfmodule_stereo_slot_sensor0")

        res_plotter.plot_1D_residuals("uresidual_GBL_module_L6t_halfmodule_axial_hole_sensor0")
        res_plotter.plot_1D_residuals("uresidual_GBL_module_L6t_halfmodule_axial_slot_sensor0")
        res_plotter.plot_1D_residuals("uresidual_GBL_module_L6t_halfmodule_stereo_hole_sensor0")
        res_plotter.plot_1D_residuals("uresidual_GBL_module_L6t_halfmodule_stereo_slot_sensor0")

        if not is2016:
            res_plotter.plot_1D_residuals("uresidual_GBL_module_L7t_halfmodule_axial_hole_sensor0")
            res_plotter.plot_1D_residuals("uresidual_GBL_module_L7t_halfmodule_axial_slot_sensor0")
            res_plotter.plot_1D_residuals("uresidual_GBL_module_L7t_halfmodule_stereo_hole_sensor0")
            res_plotter.plot_1D_residuals("uresidual_GBL_module_L7t_halfmodule_stereo_slot_sensor0")

        profile_plotter = ProfilePlots()
        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L1t_halfmodule_axial_sensor0", xtitle="L1t Axial - hit u-pos [mm]", rangeX=[-10, 10], rangeY=[-0.2, 0.2])

        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L1t_halfmodule_stereo_sensor0", xtitle="L1t Stereo - hit u-pos [mm]", rangeX=[-10, 10], rangeY=[-0.2, 0.2])

        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L2t_halfmodule_axial_sensor0", xtitle="L2t Axial - hit u-pos [mm]", rangeY=[-0.2, 0.2])
        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L2t_halfmodule_stereo_sensor0", xtitle="L2t Stereo - hit u-pos [mm]", rangeY=[-0.2, 0.2])

        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L3t_halfmodule_axial_sensor0", xtitle="L3t Axial - hit u-pos [mm]", rangeY=[-0.2, 0.2])
        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L3t_halfmodule_stereo_sensor0", xtitle="L3t Stereo - hit u-pos [mm]", rangeY=[-0.2, 0.2])

        if not is2016:
            profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L4t_halfmodule_axial_sensor0", xtitle="L4t Axial - hit u-pos [mm]", rangeY=[-0.2, 0.2])
            profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L4t_halfmodule_stereo_sensor0", xtitle="L4t Stereo - hit u-pos [mm]", rangeY=[-0.2, 0.2])
        else:
            profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L4t_halfmodule_axial_hole_sensor0", xtitle="L5t Axial hole - hit u-pos [mm]", rangeY=[-0.2, 0.2])
            profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L4t_halfmodule_stereo_hole_sensor0", xtitle="L5t Stereo hole - hit u-pos [mm]", rangeY=[-0.2, 0.2])
            profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L4t_halfmodule_axial_slot_sensor0", xtitle="L5t Axial slot - hit u-pos [mm]", rangeY=[-0.2, 0.2])
            profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L4t_halfmodule_stereo_slot_sensor0", xtitle="L5t Stereo slot - hit u-pos [mm]", rangeY=[-0.2, 0.2])

        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L5t_halfmodule_axial_hole_sensor0", xtitle="L5t Axial hole - hit u-pos [mm]", rangeY=[-0.2, 0.2])
        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L5t_halfmodule_stereo_hole_sensor0", xtitle="L5t Stereo hole - hit u-pos [mm]", rangeY=[-0.2, 0.2])
        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L5t_halfmodule_axial_slot_sensor0", xtitle="L5t Axial slot - hit u-pos [mm]", rangeY=[-0.2, 0.2])
        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L5t_halfmodule_stereo_slot_sensor0", xtitle="L5t Stereo slot - hit u-pos [mm]", rangeY=[-0.2, 0.2])

        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L6t_halfmodule_axial_hole_sensor0", xtitle="L6t Axial hole - hit u-pos [mm]", rangeY=[-0.2, 0.2], rebin=2)
        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L6t_halfmodule_stereo_hole_sensor0", xtitle="L6t Stereo hole - hit u-pos [mm]", rangeY=[-0.2, 0.2], rebin=2)
        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L6t_halfmodule_axial_slot_sensor0", xtitle="L6t Axial slot - hit u-pos [mm]", rangeY=[-0.2, 0.2], rebin=2)
        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L6t_halfmodule_stereo_slot_sensor0", xtitle="L6t Stereo slot - hit u-pos [mm]", rangeY=[-0.2, 0.2], rebin=2)

        if not is2016:
            profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L7t_halfmodule_axial_hole_sensor0", xtitle="L7t Axial hole - hit u-pos [mm]", rangeY=[-0.2, 0.2])
            profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L7t_halfmodule_stereo_hole_sensor0", xtitle="76t Stereo hole - hit u-pos [mm]", rangeY=[-0.2, 0.2])
            profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L7t_halfmodule_axial_slot_sensor0", xtitle="L7t Axial slot - hit u-pos [mm]", rangeY=[-0.2, 0.2])
            profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L7t_halfmodule_stereo_slot_sensor0", xtitle="L7t Stereo slot - hit u-pos [mm]", rangeY=[-0.2, 0.2])

        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L1b_halfmodule_axial_sensor0", xtitle="L1b Axial - hit u-pos [mm]", rangeX=[-10, 10], rangeY=[-0.2, 0.2])
        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L1b_halfmodule_stereo_sensor0", xtitle="L1b Stereo - hit u-pos [mm]", rangeX=[-10, 10], rangeY=[-0.2, 0.2])

        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L2b_halfmodule_axial_sensor0", xtitle="L2b Axial - hit u-pos [mm]", rangeY=[-0.2, 0.2])
        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L2b_halfmodule_stereo_sensor0", xtitle="L2b Stereo - hit u-pos [mm]", rangeY=[-0.2, 0.2])

        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L3b_halfmodule_axial_sensor0", xtitle="L3b Axial - hit u-pos [mm]", rangeY=[-0.2, 0.2])
        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L3b_halfmodule_stereo_sensor0", xtitle="L3b Stereo - hit u-pos [mm]", rangeY=[-0.2, 0.2])

        if not is2016:
            profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L4b_halfmodule_axial_sensor0", xtitle="L4b Axial - hit u-pos [mm]", rangeY=[-0.2, 0.2])
            profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L4b_halfmodule_stereo_sensor0", xtitle="L4b Stereo - hit u-pos [mm]", rangeY=[-0.2, 0.2])
        else:
            profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L4b_halfmodule_axial_hole_sensor0", xtitle="L5b Axial hole - hit u-pos [mm]", rangeY=[-0.2, 0.2])
            profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L4b_halfmodule_stereo_hole_sensor0", xtitle="L5b Stereo hole - hit u-pos [mm]", rangeY=[-0.2, 0.2])
            profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L4b_halfmodule_axial_slot_sensor0", xtitle="L5b Axial slot - hit u-pos [mm]", rangeY=[-0.2, 0.2])
            profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L4b_halfmodule_stereo_slot_sensor0", xtitle="L5b Stereo slot - hit u-pos [mm]", rangeY=[-0.2, 0.2])

        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L5b_halfmodule_axial_hole_sensor0", xtitle="L5b Axial hole - hit u-pos [mm]", rangeY=[-0.2, 0.2])
        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L5b_halfmodule_stereo_hole_sensor0", xtitle="L5b Stereo hole - hit u-pos [mm]", rangeY=[-0.2, 0.2])
        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L5b_halfmodule_axial_slot_sensor0", xtitle="L5b Axial slot - hit u-pos [mm]", rangeY=[-0.2, 0.2])
        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L5b_halfmodule_stereo_slot_sensor0", xtitle="L5b Stereo slot - hit u-pos [mm]", rangeY=[-0.2, 0.2])

        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L6b_halfmodule_axial_hole_sensor0", xtitle="L6b Axial hole - hit u-pos [mm]", rangeY=[-0.2, 0.2])
        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L6b_halfmodule_stereo_hole_sensor0", xtitle="L6b Stereo hole - hit u-pos [mm]", rangeY=[-0.2, 0.2])
        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L6b_halfmodule_axial_slot_sensor0", xtitle="L6b Axial slot - hit u-pos [mm]", rangeY=[-0.2, 0.2])
        profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L6b_halfmodule_stereo_slot_sensor0", xtitle="L6b Stereo slot - hit u-pos [mm]", rangeY=[-0.2, 0.2])

        if not is2016:
            profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L7b_halfmodule_axial_hole_sensor0", xtitle="L7b Axial hole - hit u-pos [mm]", rangeY=[-0.2, 0.2])
            profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L7b_halfmodule_stereo_hole_sensor0", xtitle="L7b Stereo hole - hit u-pos [mm]", rangeY=[-0.2, 0.2])
            profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L7b_halfmodule_axial_slot_sensor0", xtitle="L7b Axial slot - hit u-pos [mm]", rangeY=[-0.2, 0.2])
            profile_plotter.plot_profileY("uresidual_GBL_vs_u_hit_module_L7b_halfmodule_stereo_slot_sensor0", xtitle="L7b Stereo slot - hit u-pos [mm]", rangeY=[-0.2, 0.2])

        v_min = -0.15
        v_max = 0.15

        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L1t_halfmodule_axial_sensor0", xtitle="L1t Axial - v predicted [mm]", rangeX=[-20, 20], rangeY=[v_min, v_max])
        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L1t_halfmodule_stereo_sensor0", xtitle="L1t Stereo - v predicted [mm]", rangeX=[-20, 20], rangeY=[v_min, v_max])

        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L2t_halfmodule_axial_sensor0", xtitle="L2t Axial -v predicted [mm]", rangeY=[v_min, v_max])
        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L2t_halfmodule_stereo_sensor0", xtitle="L2t Stereo -v predicted [mm]", rangeY=[v_min, v_max])

        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L3t_halfmodule_axial_sensor0", xtitle="L3t Axial -v predicted [mm]", rangeY=[v_min, v_max])
        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L3t_halfmodule_stereo_sensor0", xtitle="L3t Stereo -v predicted [mm]", rangeY=[v_min, v_max])

        if not is2016:
            profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L4t_halfmodule_axial_sensor0", xtitle="L4t Axial -v predicted [mm]", rangeX=[-30, 30], rangeY=[v_min, v_max])
            profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L4t_halfmodule_stereo_sensor0", xtitle="L4t Stereo -v predicted [mm]", rangeX=[-30, 30], rangeY=[v_min, v_max])
        else:
            profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L4t_halfmodule_axial_hole_sensor0", xtitle="L5t Axial hole-v predicted [mm]", rangeY=[v_min, v_max], rebin=2)
            profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L4t_halfmodule_stereo_hole_sensor0", xtitle="L5t Stereo hole-v predicted [mm]", rangeY=[v_min, v_max], rebin=2)
            profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L4t_halfmodule_axial_slot_sensor0", xtitle="L5t Axial slot-v predicted [mm]", rangeY=[v_min, v_max], rebin=2)
            profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L4t_halfmodule_stereo_slot_sensor0", xtitle="L5t Stereo slot-v predicted [mm]", rangeY=[v_min, v_max], rebin=2)

        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L5t_halfmodule_axial_hole_sensor0", xtitle="L5t Axial hole-v predicted [mm]", rangeY=[v_min, v_max], rebin=2)
        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L5t_halfmodule_stereo_hole_sensor0", xtitle="L5t Stereo hole-v predicted [mm]", rangeY=[v_min, v_max], rebin=2)
        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L5t_halfmodule_axial_slot_sensor0", xtitle="L5t Axial slot-v predicted [mm]", rangeY=[v_min, v_max], rebin=2)
        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L5t_halfmodule_stereo_slot_sensor0", xtitle="L5t Stereo slot-v predicted [mm]", rangeY=[v_min, v_max], rebin=2)

        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L6t_halfmodule_axial_hole_sensor0", xtitle="L6t Axial hole-v predicted [mm]", rangeY=[v_min, v_max], rebin=2)
        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L6t_halfmodule_stereo_hole_sensor0", xtitle="L6t Stereo hole-v predicted [mm]", rangeY=[v_min, v_max], rebin=2)
        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L6t_halfmodule_axial_slot_sensor0", xtitle="L6t Axial slot-v predicted [mm]", rangeY=[v_min, v_max], rebin=2)
        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L6t_halfmodule_stereo_slot_sensor0", xtitle="L6t Stereo slot-v predicted [mm]", rangeY=[v_min, v_max], rebin=2)

        if not is2016:
            profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L7t_halfmodule_axial_hole_sensor0", xtitle="L7t Axial hole-v predicted [mm]", rangeY=[v_min, v_max], rebin=2)
            profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L7t_halfmodule_stereo_hole_sensor0", xtitle="L7t Stereo hole-v predicted [mm]", rangeY=[v_min, v_max], rebin=2)
            profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L7t_halfmodule_axial_slot_sensor0", xtitle="L7t Axial slot-v predicted [mm]", rangeY=[v_min, v_max], rebin=2)
            profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L7t_halfmodule_stereo_slot_sensor0", xtitle="L7t Stereo slot-v predicted [mm]", rangeY=[v_min, v_max], rebin=2)

        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L1b_halfmodule_axial_sensor0", xtitle="L1b Axial - v predicted [mm]", rangeY=[v_min, v_max])
        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L1b_halfmodule_stereo_sensor0", xtitle="L1b Stereo - v predicted [mm]", rangeY=[v_min, v_max])

        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L2b_halfmodule_axial_sensor0", xtitle="L2b Axial -v predicted [mm]", rangeY=[v_min, v_max])
        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L2b_halfmodule_stereo_sensor0", xtitle="L2b Stereo -v predicted [mm]", rangeY=[v_min, v_max])

        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L3b_halfmodule_axial_sensor0", xtitle="L3b Axial -v predicted [mm]", rangeY=[v_min, v_max])
        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L3b_halfmodule_stereo_sensor0", xtitle="L3b Stereo -v predicted [mm]", rangeY=[v_min, v_max])

        if not is2016:
            profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L4b_halfmodule_axial_sensor0", xtitle="L4b Axial -v predicted [mm]", rangeX=[-30, 30], rangeY=[v_min, v_max])
            profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L4b_halfmodule_stereo_sensor0", xtitle="L4b Stereo -v predicted [mm]", rangeX=[-30, 30], rangeY=[v_min, v_max])
        else:
            profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L4b_halfmodule_axial_hole_sensor0", xtitle="L5b Axial hole-v predicted [mm]", rangeY=[v_min, v_max])
            profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L4b_halfmodule_stereo_hole_sensor0", xtitle="L5b Stereo hole-v predicted [mm]", rangeY=[v_min, v_max])
            profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L4b_halfmodule_axial_slot_sensor0", xtitle="L5b Axial slot-v predicted [mm]", rangeY=[v_min, v_max])
            profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L4b_halfmodule_stereo_slot_sensor0", xtitle="L5b Stereo slot-v predicted [mm]", rangeY=[v_min, v_max])

        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L5b_halfmodule_axial_hole_sensor0", xtitle="L5b Axial hole-v predicted [mm]", rangeY=[v_min, v_max])
        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L5b_halfmodule_stereo_hole_sensor0", xtitle="L5b Stereo hole-v predicted [mm]", rangeY=[v_min, v_max])
        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L5b_halfmodule_axial_slot_sensor0", xtitle="L5b Axial slot-v predicted [mm]", rangeY=[v_min, v_max])
        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L5b_halfmodule_stereo_slot_sensor0", xtitle="L5b Stereo slot-v predicted [mm]", rangeY=[v_min, v_max])

        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L6b_halfmodule_axial_hole_sensor0", xtitle="L6b Axial hole-v predicted [mm]", rangeY=[v_min, v_max])
        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L6b_halfmodule_stereo_hole_sensor0", xtitle="L6b Stereo hole-v predicted [mm]", rangeY=[v_min, v_max])
        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L6b_halfmodule_axial_slot_sensor0", xtitle="L6b Axial slot-v predicted [mm]", rangeY=[v_min, v_max])
        profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L6b_halfmodule_stereo_slot_sensor0", xtitle="L6b Stereo slot-v predicted [mm]", rangeY=[v_min, v_max])

        if not is2016:
            profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L7b_halfmodule_axial_hole_sensor0", xtitle="L7b Axial hole-v predicted [mm]", rangeX=[-60, 60], rangeY=[v_min, v_max])
            profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L7b_halfmodule_stereo_hole_sensor0", xtitle="L7b Stereo hole-v predicted [mm]", rangeX=[-60, 60], rangeY=[v_min, v_max])
            profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L7b_halfmodule_axial_slot_sensor0", xtitle="L7b Axial slot-v predicted [mm]", rangeX=[-60, 60], rangeY=[v_min, v_max])
            profile_plotter.plot_profileY("uresidual_GBL_vs_v_pred_module_L7b_halfmodule_stereo_slot_sensor0", xtitle="L7b Stereo slot-v predicted [mm]", rangeX=[-60, 60], rangeY=[v_min, v_max])

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
        # fee_plots.plot_histos(inputF,legends,"trk_params/p6h_top",outFolder,config.args.oFext)
        # fee_plots.plot_histos(inputF,legends,"trk_params/p6h_bottom",outFolder,config.args.oFext)
        # fee_plots.plot_histos(inputF,legends,"trk_params/p7h_bottom")

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

    # Put plots in a webpage
    if config.args.doHTML:
        hw = htmlWriter(outFolder)
        hw.add_images(outFolder)
        hw.close_html()


if __name__ == "__main__":
    main()
