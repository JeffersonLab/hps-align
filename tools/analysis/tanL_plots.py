import ROOT as r
from tools.analysis.base_plotter import BasePlotter
import tools.analysis.alignment_utils as alignUtils
from tools.analysis.index_page import htmlWriter


class TanLambdaPlots(BasePlotter):

    def __init__(self):
        super().__init__()

    def do_legend(self, histos, legend_names, location=1, plot_properties=[], leg_location=[]):
        """!
        Create legend

        @param histos  list of histograms
        @param legend_names  list of names for legend entries
        @param location  location of the legend
        @param plot_properties  list of properties for legend entries
        @param leg_location  more precise location of the legend overwriting simple location

        @return legend
        """
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

    def plot_z0_vs_tanL_fit(self, name):
        """!
        Plot z0 vs tanL and fit it

        root file has to contain directory "trk_params/"

        @param name  name of the histogram
        """

        histos = []
        # grab the histos
        for infile in self.input_files:
            histos.append(infile.Get("trk_params/" + name))

        print("Histograms to fit:", len(histos))
        canv = r.TCanvas("c1", "c1", 2200, 2000)
        canv.SetGridx()
        canv.SetGridy()

        plotProperties = []

        histos_mu = []
        histos_sigma = []

        for ihisto in range(0, len(histos)):
            # Profile it
            histos_mu.append(r.TH1F(histos[ihisto].GetName()+"_mu"+str(ihisto), histos[ihisto].GetName()+"_mu"+str(ihisto), histos[ihisto].GetXaxis().GetNbins(), histos[ihisto].GetXaxis().GetXmin(), histos[ihisto].GetXaxis().GetXmax()))

            histos_sigma.append(r.TH1F(histos[ihisto].GetName()+"_sigma"+str(ihisto), histos[ihisto].GetName()+"_sigma"+str(ihisto), histos[ihisto].GetXaxis().GetNbins(), histos[ihisto].GetXaxis().GetXmin(), histos[ihisto].GetXaxis().GetXmax()))
            alignUtils.profile_y_with_iterative_gauss_fit(histos[ihisto], histos_mu[ihisto], histos_sigma[ihisto], 1)

            hist = histos_mu[ihisto]
            hmin = hist.GetBinLowEdge(1)
            hmax = (hist.GetBinLowEdge(hist.GetNbinsX()))+hist.GetBinWidth(hist.GetNbinsX())

            fitF = r.TF1("fit"+str(ihisto), "[1]*x + [0]", hmin, hmax)
            histos_mu[ihisto].Fit("fit" + str(ihisto), "QNR")
            string = ""
            for i in range(fitF.GetNpar()):
                if i < range(fitF.GetNpar())[-1]:
                    string += str(round(fitF.GetParameter(i), 3)) + ","
                else:
                    string += str(round(fitF.GetParameter(i), 3))
            plotProperties.append(string)

            self.set_histo_style(histos_mu[ihisto], ihisto)
            histos_mu[ihisto].GetYaxis().SetTitle("<z0> [mm]")
            histos_mu[ihisto].GetXaxis().SetTitle("tan(#lambda)")
            histos_mu[ihisto].GetYaxis().SetTitleSize(histos[ihisto].GetYaxis().GetTitleSize()*0.7)
            histos_mu[ihisto].GetYaxis().SetTitleOffset(histos[ihisto].GetYaxis().GetTitleOffset()*1.35)

            histos_mu[ihisto].GetYaxis().SetRangeUser(-2, 2)
            histos_mu[ihisto].GetXaxis().SetRangeUser(-2, 2)

            if (ihisto == 0):
                histos_mu[ihisto].Draw("P")
            else:
                histos_mu[ihisto].Draw("P SAME")

            fitF.SetLineColor(self.colors[ihisto])
            fitF.DrawClone("SAME")

        leg = self.do_legend(histos_mu, self.legend_names, 2, plotProperties)
        if (leg is not None):
            leg.Draw()

        canv.SaveAs(self.outdir + "/" + name + self.oFext)

        if self.do_HTML:
            img_type = self.oFext.strip(".")
            hw = htmlWriter(self.outdir, img_type=img_type)
            hw.add_images(self.outdir)
            hw.close_html()
