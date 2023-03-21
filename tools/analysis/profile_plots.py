from base_plotter import BasePlotter
import ROOT as r
import alignment_utils as alignUtils
from index_page import htmlWriter


class ProfilePlots(BasePlotter):

    def __init__(self, indir="res/"):
        super().__init__()
        self.indir = indir

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
        for l in range(len(histos)):
            if (len(plot_properties) != len(histos)):
                leg.AddEntry(histos[l], legend_names[l], 'lpf')
            else:
                # splitline{The Data }{slope something }
                entry = "#splitline{" + legend_names[l] + "}{" + plot_properties[l] + "}"
                leg.AddEntry(histos[l], entry, 'lpf')
        leg.SetBorderSize(0)

        return leg

    def plot_profileY(self, name,
                      xtitle="hit position [mm]",
                      ytitle="<ures> [mm]",
                      rangeX=[], rangeY=[], fitrange=[-2e5, 2e5],
                      fit="[0]*x + [1]", num_bins=1, rebin=1):

        histos = []
        histos_mu = []
        histos_sigma = []

        for infile in self.input_files:
            if not infile.Get(self.indir+name):
                raise Exception(self.indir + name + "   NOT FOUND")

            histos.append(infile.Get(self.indir+name))

        c = r.TCanvas("c1", "c1", 2200, 2000)
        c.SetGridx()
        c.SetGridy()

        plotProperties = []
        fits = []
        for ihisto in range(0, len(histos)):

            histos[ihisto].Rebin(rebin)

            histos_mu.append(r.TH1F(histos[ihisto].GetName()+"_mu"+str(ihisto), histos[ihisto].GetName()+"_mu"+str(ihisto), histos[ihisto].GetXaxis().GetNbins(), histos[ihisto].GetXaxis().GetXmin(), histos[ihisto].GetXaxis().GetXmax()))
            histos_sigma.append(r.TH1F(histos[ihisto].GetName()+"_sigma"+str(ihisto), histos[ihisto].GetName()+"_sigma"+str(ihisto), histos[ihisto].GetXaxis().GetNbins(), histos[ihisto].GetXaxis().GetXmin(), histos[ihisto].GetXaxis().GetXmax()))
            alignUtils.profile_y_with_iterative_gauss_fit(histos[ihisto], histos_mu[ihisto], histos_sigma[ihisto], num_bins, fitrange=fitrange)
            # alignUtils.profile_y_with_iterative_gauss_fit(histos[ihisto],histos_sigma[ihisto] ,histos_mu[ihisto], num_bins,fitrange=fitrange)

            self.set_histo_style(histos_mu[ihisto], ihisto)
            self.set_histo_style(histos_sigma[ihisto], ihisto)

            hist = histos_mu[ihisto]
            hmin = hist.GetBinLowEdge(1)
            hmax = (hist.GetBinLowEdge(hist.GetNbinsX())) + hist.GetBinWidth(hist.GetNbinsX())

            fitPars = []

            fitF = r.TF1("fit"+str(ihisto), fit, hmin, hmax)
            histos_mu[ihisto].Fit("fit"+str(ihisto), "QNR")

            string = ""
            for i in range(fitF.GetNpar()):
                fitPars.append(fitF.GetParameter(i))
                string += str(round(fitPars[i], 4)) + ","

            plotProperties.append(string)
            fits.append(fitF)

            if (ihisto == 0):
                histos_mu[ihisto].GetXaxis().SetTitle(xtitle)
                histos_mu[ihisto].GetYaxis().SetTitle(ytitle)
                histos_mu[ihisto].GetYaxis().SetTitleSize(histos[ihisto].GetYaxis().GetTitleSize()*0.7)
                histos_mu[ihisto].GetYaxis().SetTitleOffset(histos[ihisto].GetYaxis().GetTitleOffset()*1.35)

                histos_mu[ihisto].GetYaxis().SetRangeUser(-0.2, 0.2)
                if len(rangeY) > 1:
                    histos_mu[ihisto].GetYaxis().SetRangeUser(rangeY[0], rangeY[1])
                histos_mu[ihisto].Draw("P")
                if len(rangeX) > 1:
                    histos_mu[ihisto].GetXaxis().SetRangeUser(rangeX[0], rangeX[1])
            else:
                histos_mu[ihisto].Draw("P SAME")

            fitF.SetLineColor(self.colors[ihisto])
            # fitF.Draw("SAME")

        leg = self.do_legend(histos_mu, self.legend_names, 2, plotProperties)

        if (leg is not None):
            leg.Draw()

        text = r.TLatex()
        text.SetNDC()
        text.SetTextFont(42)
        text.SetTextSize(0.04)
        text.SetTextColor(r.kBlack)
        text.DrawLatex(0.66, 0.89, '#bf{#it{HPS}} Work In Progress')

        c.SaveAs(self.outdir + "/" + name + "_profiled" + self.oFext)

        c1 = r.TCanvas("c1", "c1", 2200, 2000)
        c1.SetGridx()
        c1.SetGridy()
        c1.cd()

        if (ihisto == 0):
            histos_sigma[ihisto].GetXaxis().SetTitle(xtitle)
            histos_sigma[ihisto].GetYaxis().SetTitle(ytitle)
            histos_sigma[ihisto].GetYaxis().SetTitleSize(histos[ihisto].GetYaxis().GetTitleSize()*0.7)
            histos_sigma[ihisto].GetYaxis().SetTitleOffset(histos[ihisto].GetYaxis().GetTitleOffset()*1.35)
            histos_sigma[ihisto].GetYaxis().SetRangeUser(-0.2, 0.2)
            if len(rangeY) > 1:
                histos_sigma[ihisto].GetYaxis().SetRangeUser(rangeY[0], rangeY[1])
            histos_sigma[ihisto].Draw("P")
            if len(rangeX) > 1:
                histos_sigma[ihisto].GetXaxis().SetRangeUser(rangeX[0], rangeX[1])
            else:
                histos_sigma[ihisto].Draw("P SAME")
                pass

            fitF.SetLineColor(self.colors[ihisto])
            # fitF.Draw("SAME")

        leg = self.do_legend(histos_sigma, self.legend_names, 2, plotProperties)

        if (leg is not None):
            leg.Draw()

        c1.SaveAs(self.outdir + "/" + name + "_sigma_profiled" + self.oFext)

        if self.do_HTML:
            hw = htmlWriter(self.outdir)
            hw.add_images(self.outdir)
            hw.close_html()
