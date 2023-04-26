import ROOT as r
from .base_plotter import BasePlotter
from . import alignment_utils
from .index_page import htmlWriter


class ProfilePlots(BasePlotter):

    def __init__(self, **kwargs):
        if 'indir' not in kwargs or kwargs['indir'] is None:
            kwargs['indir'] = 'res/'
        super().__init__(**kwargs)

    def plot_profileY(self, name,
                      xtitle="hit position [mm]",
                      ytitle="<ures> [mm]",
                      rangeX=[], rangeY=[], do_fit=False,
                      fitrange=[-2e5, 2e5], fit="[0]*x + [1]",
                      num_bins=1, rebin=1, do_sigma_profile=False):
        """!
        Plot y profile of distribution

        @param name              name of the histogram
        @param xtitle            x axis title
        @param ytitle            y axis title
        @param rangeX            x axis range
        @param rangeY            y axis range
        @param do_fit            if true, fit is performed
        @param fitrange          range for fit
        @param fit               fit function
        @param num_bins          number of bins for profile
        @param rebin             rebinning factor
        @param do_sigma_profile  if true, sigma profile plots are added
        """

        histos = []
        histos_mu = []
        histos_sigma = []

        for infile in self.input_files:
            if not infile.Get(self.indir+name):
                raise Exception(self.indir + name + "   NOT FOUND")

            histos.append(infile.Get(self.indir+name))

        canv = r.TCanvas("c1", "c1", 2200, 2000)
        canv.SetGridx()
        canv.SetGridy()

        plotProperties = []

        for ihisto in range(0, len(histos)):
            histos[ihisto].Rebin(rebin)

            histos_mu.append(r.TH1F(histos[ihisto].GetName() + "_mu" + str(ihisto), histos[ihisto].GetName() + "_mu" + str(
                ihisto), histos[ihisto].GetXaxis().GetNbins(), histos[ihisto].GetXaxis().GetXmin(), histos[ihisto].GetXaxis().GetXmax()))
            histos_sigma.append(r.TH1F(histos[ihisto].GetName() + "_sigma" + str(ihisto), histos[ihisto].GetName() + "_sigma" + str(
                ihisto), histos[ihisto].GetXaxis().GetNbins(), histos[ihisto].GetXaxis().GetXmin(), histos[ihisto].GetXaxis().GetXmax()))
            alignment_utils.profile_y_with_iterative_gauss_fit(
                histos[ihisto], histos_mu[ihisto], histos_sigma[ihisto], num_bins, fitrange=fitrange)

            self.set_histo_style(histos_mu[ihisto], ihisto)

            hist = histos_mu[ihisto]
            hmin = hist.GetBinLowEdge(1)
            hmax = (hist.GetBinLowEdge(hist.GetNbinsX())) + \
                hist.GetBinWidth(hist.GetNbinsX())

            fitPars = []

            if do_fit:
                fitF = r.TF1("fit" + str(ihisto), fit, hmin, hmax)
                string = ""
                for i in range(fitF.GetNpar()):
                    fitPars.append(fitF.GetParameter(i))
                    string += str(round(fitPars[i], 4)) + ","
                plotProperties.append(string)

            histos_mu[ihisto].Fit("fit" + str(ihisto), "QNR")

            if (ihisto == 0):
                histos_mu[ihisto].GetXaxis().SetTitle(xtitle)
                histos_mu[ihisto].GetYaxis().SetTitle(ytitle)
                histos_mu[ihisto].GetYaxis().SetTitleSize(
                    histos[ihisto].GetYaxis().GetTitleSize()*0.7)
                histos_mu[ihisto].GetYaxis().SetTitleOffset(
                    histos[ihisto].GetYaxis().GetTitleOffset()*1.35)

                histos_mu[ihisto].GetYaxis().SetRangeUser(-0.2, 0.2)
                if len(rangeY) > 1:
                    histos_mu[ihisto].GetYaxis().SetRangeUser(
                        rangeY[0], rangeY[1])
                histos_mu[ihisto].Draw("P")
                if len(rangeX) > 1:
                    histos_mu[ihisto].GetXaxis().SetRangeUser(
                        rangeX[0], rangeX[1])
            else:
                histos_mu[ihisto].Draw("P SAME")

            if do_fit:
                fitF.SetLineColor(self.colors[ihisto])
                fitF.Draw("SAME")

        leg = self.do_legend(histos_mu, self.legend_names, 2, plotProperties)

        if (leg is not None):
            leg.Draw()

        text = r.TLatex()
        text.SetNDC()
        text.SetTextFont(42)
        text.SetTextSize(0.04)
        text.SetTextColor(r.kBlack)
        text.DrawLatex(0.66, 0.89, '#bf{#it{HPS}} Work In Progress')

        canv.SaveAs(self.outdir + "/" + name + "_profiled" + self.oFext)

        if do_sigma_profile:
            canv_sigma = r.TCanvas("c1", "c1", 2200, 2000)
            canv_sigma.SetGridx()
            canv_sigma.SetGridy()
            canv_sigma.cd()

            for ihisto in range(0, len(histos_sigma)):
                self.set_histo_style(histos_sigma[ihisto], ihisto)
                if (ihisto == 0):
                    histos_sigma[ihisto].GetXaxis().SetTitle(xtitle)
                    histos_sigma[ihisto].GetYaxis().SetTitle(ytitle)
                    histos_sigma[ihisto].GetYaxis().SetTitleSize(
                        histos[ihisto].GetYaxis().GetTitleSize()*0.7)
                    histos_sigma[ihisto].GetYaxis().SetTitleOffset(
                        histos[ihisto].GetYaxis().GetTitleOffset()*1.35)
                    histos_sigma[ihisto].GetYaxis().SetRangeUser(-0.2, 0.2)
                    if len(rangeY) > 1:
                        histos_sigma[ihisto].GetYaxis().SetRangeUser(
                            rangeY[0], rangeY[1])
                    histos_sigma[ihisto].Draw("P")
                    if len(rangeX) > 1:
                        histos_sigma[ihisto].GetXaxis().SetRangeUser(
                            rangeX[0], rangeX[1])
                else:
                    histos_sigma[ihisto].Draw("P SAME")

            leg = self.do_legend(
                histos_sigma, self.legend_names, 2, plotProperties)

            if (leg is not None):
                leg.Draw()

            canv_sigma.SaveAs(self.outdir + "/" + name +
                              "_sigma_profiled" + self.oFext)

        if self.do_HTML:
            img_type = self.oFext.strip(".")
            hw = htmlWriter(self.outdir, img_type=img_type)
            hw.add_images(self.outdir)
            hw.close_html()
