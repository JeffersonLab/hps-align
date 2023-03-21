import os
import ROOT as r
import utilities as utils
from base_plotter import BasePlotter
from index_page import htmlWriter


class VertexPlots(BasePlotter):

    def __init__(self):
        super().__init__()
        self.outdir = self.outdir + "/MultiVtx_plots/"

    def do_legend(self, histos, legend_names, location=1, plot_properties=[], leg_location=[]):
        """! Create legend"""
        # leg = super().do_legend(histos, legend_names, location, leg_location)
        if len(legend_names) < len(histos):
            raise Exception("WARNING:: size of legends doesn't match the size of histos")

        leg = None
        xshift = 0.3
        yshift = 0.3
        if (location == 1):
            leg = r.TLegend(0.6, 0.35, 0.90, 0.15)
        if (location == 2):
            leg = r.TLegend(0.40, 0.3, 0.65, 0.2)
        if (location == 3):
            leg = r.TLegend(0.20, 0.90, 0.20+xshift, 0.90-yshift)
        if (location == 4):
            xmin = 0.6
            leg = r.TLegend(xmin, 0.90, xmin+xshift, 0.90-yshift)

        if len(leg_location) == 2:
            leg = r.TLegend(leg_location[0], leg_location[1], leg_location[0]+xshift, leg_location[1]-yshift*0.6)
        for ihist in range(len(histos)):
            if (len(plot_properties) != len(histos)):
                leg.AddEntry(histos[ihist], legend_names[ihist], 'lpf')
            else:
                # splitline{The Data }{slope something }
                entry = "#splitline{" + legend_names[ihist] + "}{" + plot_properties[ihist] + "}"
                leg.AddEntry(histos[ihist], entry, 'lpf')
        leg.SetBorderSize(0)

        return leg

    def plot_multi_vtx(self):

        print("--- MultiVtxPlots --- ")
        histos_top = []
        histos_bot = []
        histos = []
        f_path = "MultiEventVtx/"

        for infile in self.input_files:
            histos_top.append(infile.Get("MultiEventVtx/vtx_z_top"))
            histos_bot.append(infile.Get("MultiEventVtx/vtx_z_bottom"))
            histos.append(infile.Get("MultiEventVtx/vtx_z"))

        c = r.TCanvas("c1", "c1", 2200, 2000)
        c.SetGridx()
        c.SetGridy()

        if (not os.path.exists(self.outdir)):
            os.mkdir(self.outdir)

        maximum = 150

        for ihisto in range(len(histos)):
            self.set_histo_style(histos[ihisto], ihisto, line_width=2)
            histos[ihisto].Rebin(1)

            if (ihisto == 0):
                # histos[ihisto].GetYaxis().SetRangeUser(0.,1.)
                histos[ihisto].Draw("P")
                histos[ihisto].GetXaxis().SetRangeUser(-15, 0)
                histos[ihisto].SetMaximum(maximum*5)
                histos[ihisto].GetXaxis().SetLabelSize(0.055)
                histos[ihisto].GetYaxis().SetLabelSize(0.055)
                histos[ihisto].GetXaxis().SetTitle("Multi Evt Vtx_{z} [mm]")
                histos[ihisto].GetXaxis().SetTitleSize(histos[ihisto].GetYaxis().GetTitleSize()*0.6)
                histos[ihisto].GetXaxis().SetTitleOffset(histos[ihisto].GetYaxis().GetTitleOffset()*1.35)

            else:
                histos[ihisto].Draw("P SAME")

        leg = self.do_legend(histos, self.legend_names, 4)
        if (leg is not None):
            leg.Draw()
        c.SaveAs(self.outdir + "MultiEventVtx_z" + self.oFext)

        c = r.TCanvas("c1", "c1", 2200, 2000)
        c.SetGridx()
        c.SetGridy()

        for ihisto in range(len(histos_top)):
            self.set_histo_style(histos_top[ihisto], ihisto, line_width=2)
            histos_top[ihisto].Rebin(1)

            if (ihisto == 0):
                # histos[ihisto].GetYaxis().SetRangeUser(0.,1.)
                histos_top[ihisto].Draw("P")
                histos_top[ihisto].GetXaxis().SetRangeUser(-10, 0)
                histos_top[ihisto].SetMaximum(maximum)
                histos_top[ihisto].GetXaxis().SetLabelSize(0.055)
                histos_top[ihisto].GetYaxis().SetLabelSize(0.055)
                histos_top[ihisto].GetXaxis().SetTitle("Vtx_{z} [mm]")
                histos_top[ihisto].GetXaxis().SetTitleSize(histos_top[ihisto].GetXaxis().GetTitleSize()*0.6)
                histos_top[ihisto].GetXaxis().SetTitleOffset(histos_top[ihisto].GetXaxis().GetTitleOffset()*0.87)
                histos_top[ihisto].GetYaxis().SetTitle("Multi Evt Vertices")
                histos_top[ihisto].GetYaxis().SetTitleSize(histos_top[ihisto].GetYaxis().GetTitleSize()*0.6)
                histos_top[ihisto].GetYaxis().SetTitleOffset(histos_top[ihisto].GetYaxis().GetTitleOffset()*1.5)

            else:
                histos_top[ihisto].Draw("P SAME")

        for ihisto in range(len(histos_bot)):
            self.set_histo_style(histos_bot[ihisto], ihisto)
            histos_bot[ihisto].Rebin(1)
            histos_bot[ihisto].Draw("P SAME")

        leg = self.do_legend(histos, self.legend_names, 4)
        if (leg is not None):
            leg.Draw()
        c.SaveAs(self.outdir + "MultiEventVtx_z_tb" + self.oFext)

        print("--- multi vtx for top/bottom X-Y ---")

        histos2d_top = []
        names = [leg+"_x_y_top" for leg in self.legend_names]
        for infile in self.input_files:
            histos2d_top.append(infile.Get(f_path + "/vtx_x_y_top"))
            # names.append("MultiEventVtx_x_y_top" + iF.GetName().strip(".root"))

        utils.Make2DPlots(names, self.outdir, histos2d_top, legends=self.legend_names, xtitle="MultiEvt Vtx V_{x} [mm]", ytitle="MultiEvt Vtx V_{y} [mm]", colors2d=self.colors)

        histos2d_bot = []
        names = [leg+"_x_y_bot" for leg in self.legend_names]
        for infile in self.input_files:
            histos2d_bot.append(infile.Get(f_path + "/vtx_x_y_bottom"))
        utils.Make2DPlots(names, self.outdir, histos2d_bot, legends=self.legend_names, xtitle="Multi Vtx FEE V_{x} [mm]", ytitle="Multi Vtx FEE V_{y} [mm]", colors2d=self.colors)

        histos2d = []
        names = [leg+"_x_y_top_bot" for leg in self.legend_names]
        for infile in self.input_files:
            histos1 = infile.Get(f_path + "/vtx_x_y_top")
            histos2 = infile.Get(f_path + "/vtx_x_y_bottom")
            histos1.Add(histos2)
            histos2d.append(histos1)

        utils.Make2DPlots(names, self.outdir, histos2d, legends=self.legend_names, xtitle="MultiEvt Vtx V_{x} [mm]", ytitle="MultiEvt Vtx V_{y} [mm]", colors2d=self.colors)

        histos2d = []
        names = [leg+"_x_y_combined" for leg in self.legend_names]
        for infile in self.input_files:
            histo = infile.Get(f_path + "/vtx_x_y")
            histos2d.append(histo)
        utils.Make2DPlots(names, self.outdir, histos2d, legends=self.legend_names, xtitle="MultiEvt Vtx V_{x} [mm]", ytitle="MultiEvt Vtx V_{y} [mm]", colors2d=self.colors)

        if self.do_HTML:
            hw = htmlWriter(self.outdir)
            hw.add_images(self.outdir)
            hw.close_html()
