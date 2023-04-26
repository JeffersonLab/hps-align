import os
import ROOT as r
from ._plotter import Plotter, plotter
from .index_page import htmlWriter


@plotter()
def multi_vtx(p):
    """plot multi-vertex distributions

    input ROOT files have to contain the '/MultiEventVtx/' directory
    """

    histos_top = []
    histos_bot = []
    histos_total = []

    for infile in p.input_files:
        histos_top.append(infile.Get("MultiEventVtx/vtx_z_top"))
        histos_bot.append(infile.Get("MultiEventVtx/vtx_z_bottom"))
        histos_total.append(infile.Get("MultiEventVtx/vtx_z"))

    canv = r.TCanvas("c1", "c1", 2200, 2000)
    canv.SetGridx()
    canv.SetGridy()

    if (not os.path.exists(p.outdir)):
        os.mkdir(p.outdir)

    maximum = 150

    hist_arr = [histos_total, histos_top, histos_bot]
    save_names = ["MultiEventVtx_z",
                  "MultiEventVtx_z_top", "MultiEventVtx_z_bottom"]
    for iarr in range(len(hist_arr)):
        histos = hist_arr[iarr]
        for ihisto in range(len(histos)):
            p.set_histo_style(histos[ihisto], ihisto, line_width=2)
            histos[ihisto].Rebin(1)

            if (ihisto == 0):
                title_size = histos[ihisto].GetYaxis().GetTitleSize()
                title_offset = histos[ihisto].GetYaxis().GetTitleOffset()
                histos[ihisto].GetXaxis().SetRangeUser(-15, 0)
                histos[ihisto].SetMaximum(maximum*5)
                histos[ihisto].GetXaxis().SetTitle(
                    "Multi Evt Vtx_{z} [mm]")
                histos[ihisto].GetXaxis().SetTitleSize(title_size*0.6)
                histos[ihisto].GetXaxis().SetTitleOffset(title_offset*1.35)
                histos[ihisto].Draw("P")
            else:
                histos[ihisto].Draw("P SAME")

        leg = p.do_legend(histos, p.legend_names, 4)
        if (leg is not None):
            leg.Draw()
        canv.SaveAs(p.outdir + save_names[iarr] + p.oFext)

    histos2d_top = []
    for infile in p.input_files:
        histos2d_top.append(infile.Get("MultiEventVtx/vtx_x_y_top"))
    p.make_2D_plots(histos2d_top, out_name="vtx_x_y_top",
                    xtitle="MultiEvt Vtx V_{x} [mm]", ytitle="MultiEvt Vtx V_{y} [mm]")

    histos2d_bot = []
    for infile in p.input_files:
        histos2d_bot.append(infile.Get("MultiEventVtx/vtx_x_y_bottom"))
    p.make_2D_plots(histos2d_bot, out_name="vtx_x_y_bottom",
                    xtitle="Multi Vtx FEE V_{x} [mm]", ytitle="Multi Vtx FEE V_{y} [mm]")

    histos2d = []
    for infile in p.input_files:
        histos1 = infile.Get("MultiEventVtx/vtx_x_y_top")
        histos2 = infile.Get("MultiEventVtx/vtx_x_y_bottom")
        histos1.Add(histos2)
        histos2d.append(histos1)
    p.make_2D_plots(histos2d, out_name="vtx_x_y_top_bot",
                    xtitle="MultiEvt Vtx V_{x} [mm]", ytitle="MultiEvt Vtx V_{y} [mm]")

    histos2d = []
    for infile in p.input_files:
        histo = infile.Get("MultiEventVtx/vtx_x_y")
        histos2d.append(histo)
    p.make_2D_plots(histos2d, out_name="vtx_x_y_combined",
                    xtitle="MultiEvt Vtx V_{x} [mm]", ytitle="MultiEvt Vtx V_{y} [mm]")

    if p.do_HTML:
        img_type = p.oFext.strip(".")
        hw = htmlWriter(p.outdir, img_type=img_type)
        hw.add_images(p.outdir)
        hw.close_html()
