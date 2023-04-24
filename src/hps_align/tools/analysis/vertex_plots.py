import os
import ROOT as r
from .base_plotter import BasePlotter
from .index_page import htmlWriter


class VertexPlots(BasePlotter):
    """! Class for plotting vertex distributions"""

    def __init__(self, legend_names=[], infile_names=[], outdir="", do_HTML=False, oFext=".png", config_file="", indir=""):
        super().__init__(legend_names=legend_names, infile_names=infile_names, outdir=outdir, do_HTML=do_HTML, oFext=oFext, config_file=config_file, indir="MultiVtx_plots/")
        ## add /MultiVtx_plots/ to output directory
        self.outdir = self.outdir + "/MultiVtx_plots/"

    def plot_multi_vtx(self):
        """!
        Plot multi vertex distributions

        input root file has to contain the /MultiEventVtx/ directory
        """

        histos_top = []
        histos_bot = []
        histos_total = []

        for infile in self.input_files:
            histos_top.append(infile.Get(self.indir + "vtx_z_top"))
            histos_bot.append(infile.Get(self.indir + "vtx_z_bottom"))
            histos_total.append(infile.Get(self.indir + "vtx_z"))

        canv = r.TCanvas("c1", "c1", 2200, 2000)
        canv.SetGridx()
        canv.SetGridy()

        if (not os.path.exists(self.outdir)):
            os.mkdir(self.outdir)

        maximum = 150

        hist_arr = [histos_total, histos_top, histos_bot]
        save_names = ["MultiEventVtx_z", "MultiEventVtx_z_top", "MultiEventVtx_z_bottom"]
        for iarr in range(len(hist_arr)):
            histos = hist_arr[iarr]
            for ihisto in range(len(histos)):
                self.set_histo_style(histos[ihisto], ihisto, line_width=2)
                histos[ihisto].Rebin(1)

                if (ihisto == 0):
                    title_size = histos[ihisto].GetYaxis().GetTitleSize()
                    title_offset = histos[ihisto].GetYaxis().GetTitleOffset()
                    histos[ihisto].GetXaxis().SetRangeUser(-15, 0)
                    histos[ihisto].SetMaximum(maximum*5)
                    histos[ihisto].GetXaxis().SetTitle("Multi Evt Vtx_{z} [mm]")
                    histos[ihisto].GetXaxis().SetTitleSize(title_size*0.6)
                    histos[ihisto].GetXaxis().SetTitleOffset(title_offset*1.35)
                    histos[ihisto].Draw("P")
                else:
                    histos[ihisto].Draw("P SAME")

            leg = self.do_legend(histos, self.legend_names, 4)
            if (leg is not None):
                leg.Draw()
            canv.SaveAs(self.outdir + save_names[iarr] + self.oFext)

        histos2d_top = []
        for infile in self.input_files:
            histos2d_top.append(infile.Get(self.indir + "vtx_x_y_top"))
        self.make_2D_plots(histos2d_top, out_name="vtx_x_y_top", xtitle="MultiEvt Vtx V_{x} [mm]", ytitle="MultiEvt Vtx V_{y} [mm]")

        histos2d_bot = []
        for infile in self.input_files:
            histos2d_bot.append(infile.Get(self.indir + "/vtx_x_y_bottom"))
        self.make_2D_plots(histos2d_bot, out_name="vtx_x_y_bottom", xtitle="Multi Vtx FEE V_{x} [mm]", ytitle="Multi Vtx FEE V_{y} [mm]")

        histos2d = []
        for infile in self.input_files:
            histos1 = infile.Get(self.indir + "/vtx_x_y_top")
            histos2 = infile.Get(self.indir + "/vtx_x_y_bottom")
            histos1.Add(histos2)
            histos2d.append(histos1)
        self.make_2D_plots(histos2d, out_name="vtx_x_y_top_bot", xtitle="MultiEvt Vtx V_{x} [mm]", ytitle="MultiEvt Vtx V_{y} [mm]")

        histos2d = []
        for infile in self.input_files:
            histo = infile.Get(self.indir + "/vtx_x_y")
            histos2d.append(histo)
        self.make_2D_plots(histos2d, out_name="vtx_x_y_combined", xtitle="MultiEvt Vtx V_{x} [mm]", ytitle="MultiEvt Vtx V_{y} [mm]")

        if self.do_HTML:
            img_type = self.oFext.strip(".")
            hw = htmlWriter(self.outdir, img_type=img_type)
            hw.add_images(self.outdir)
            hw.close_html()
