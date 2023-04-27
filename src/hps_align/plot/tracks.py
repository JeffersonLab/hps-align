import os
from ._plotter import Plotter, plotter
from .index_page import htmlWriter


@plotter()
def tracks(p: Plotter):
    """
    """
    if not os.path.exists(p.outdir + "/TrackPlots"):
        os.makedirs(p.outdir + "/TrackPlots")

    plotFolder = "trk_params/"
    charges = ["", "_neg", "_pos"]
    vols = ["_top", "_bottom"]
    variables = ["Chi2",
                 "nHits",
                 "phi",
                 "tanLambda",
                 #  "trk_extr_bs_x",
                 #  "trk_extr_bs_y",
                 #  "trk_extr_bs_x_rk",
                 #  "trk_extr_bs_y_rk",
                 #  "d0",
                 #  "z0",
                 "p"]

    for crg in charges:
        for vol in vols:
            for var in variables:
                hname = plotFolder + var + vol + crg

                if ("pos" in crg):
                    corrcrg = "q-"
                elif ("neg" in crg):
                    corrcrg = "q+"
                else:
                    corrcrg = "All"

                # File loop
                histos = [f.Get(hname) for f in p.input_files]
                p.make_1D_plots(histos,
                                out_name='TrackPlots/'+var+vol+crg,
                                xtitle=var + " " + vol + " " + corrcrg,
                                RebinFactor=1, yrange=[0, 0.05])

    if p.do_HTML:
        img_type = self.oFext.strip(".")
        hw = htmlWriter(p.outdir, img_type=img_type)
        hw.add_images(p.outdir)
        hw.close_html()


@plotter()
def profiles(p: Plotter):
    for half in ['top', 'bottom']:
        p.plot_profileY(
            f'trk_params/p_vs_tanLambda_{half}',
            xtitle=f"tan(#lambda) {half}", ytitle="p [GeV]",
            rangeY=[0., 5.], fit="[0] + [1]*x"
        )
        p.plot_profileY(
            f'trk_params/d0_vs_tanLambda_{half}',
            xtitle=f'tan(#lambda) {half}', ytitle='d0 [mm]',
            rangeX=[0, 0.1], rangeY=[-1., 1.]
        )
        p.plot_profileY(
            f'trk_params/d0_vs_phi_{half}',
            xtitle=f'#phi {half}', ytitle='d0 [mm]',
            rangeX=[0, 0.1], rangeY=[-1., 1.]
        )
        p.plot_profileY(
            f'trk_params/p_vs_phi_{half}',
            xtitle=f'#phi {half}', ytitle='p [GeV]',
            rangeY=[0., 5.],
            fit='[0] + [1]*x'
        )


@plotter()
def eop(p: Plotter):
    """EoP plots require the EoP directory in the ROOT files"""
    p.plot_profileY(
        "EoP_vs_trackP_top_fid", xtitle="Top track P [GeV]", rangeY=[0.7, 1.3], fit="[0]")

    p.plot_profileY("EoP_vs_trackP_ele_top_fid", xtitle="Top ele track P [GeV]", rangeY=[
        0.7, 1.3], fit="[0]", fitrange=[0.7, 1.2])

    p.plot_profileY(
        "EoP_vs_trackP_pos_top_fid", xtitle="Top pos track P [GeV]", rangeY=[0.7, 1.3], fit="[0]")

    p.plot_profileY(
        "EoP_vs_trackP_bottom_fid", xtitle="Bot track P [GeV]", rangeY=[0.7, 1.3], fit="[0]")

    p.plot_profileY("EoP_vs_trackP_ele_bottom_fid", xtitle="Bot ele track P [GeV]", rangeY=[
        0.7, 1.3], fit="[0]", fitrange=[0.7, 1.2])

    p.plot_profileY(
        "EoP_vs_trackP_pos_bottom_fid", xtitle="Bot pos track P [GeV]", rangeY=[0.7, 1.3], fit="[0]")

    p.plot_profileY("EoP_vs_tanLambda_fid", xtitle="track tan(#lambda) [GeV]", rangeX=[
        -0.07, 0.07], rangeY=[0.7, 1.3], fit="[0]*x*x*x + [1]*x*x + [2]*x + [3]")

    p.plot_profileY("EoP_vs_phi_fid", xtitle="track #phi [GeV]", rangeY=[
        0.5, 1.3], fit="[0]*x*x*x + [1]*x*x + [2]*x + [3]")

    p.plot_profileY("EoP_vs_phi_top_fid", xtitle="Top track #phi [GeV]", rangeY=[
        0.5, 1.3], fit="[0]*x*x*x + [1]*x*x + [2]*x + [3]")

    p.plot_profileY("EoP_vs_phi_bottom_fid", xtitle="Bottom track #phi [GeV]", rangeY=[
        0.5, 1.3], fit="[0]*x*x*x + [1]*x*x + [2]*x + [3]")
