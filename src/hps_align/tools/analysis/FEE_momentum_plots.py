import ROOT as r
import tools.analysis.alignment_utils as alignUtils
from tools.analysis.base_plotter import BasePlotter
from tools.analysis.index_page import htmlWriter


class FeeMomentumPlots(BasePlotter):
    """!
    Class for plotting the FEE track parameters"""

    def __init__(self, legend_names=[], infile_names=[], outdir="", do_HTML=False, oFext=".png", config_file="", indir=""):
        super().__init__(legend_names=legend_names, infile_names=infile_names, outdir=outdir, do_HTML=do_HTML, oFext=oFext, config_file=config_file, indir=indir)

    def plot_histos(self, histopath, do_fit=True, xtitle="", ytitle="", scale_histos=False):
        """!
        Plot the FEE track parameters histograms

        @param histopath     path to the histogram in the root file
        @param do_fit        do a fit to the histogram
        @param xtitle        x-axis title
        @param ytitle        y-axis title
        @param scale_histos  scale the histograms to unity
        """

        canv = r.TCanvas("c", "c", 2200, 2000)

        histos = []
        for infile in self.input_files:
            histos.append(infile.Get(histopath))

        fitList = []
        plotProperties = []

        for ihisto in range(len(histos)):
            self.set_histo_style(histos[ihisto], ihisto, line_width=3)

            # Scale the histogram to unity
            if scale_histos:
                histos[ihisto].Scale(1./histos[ihisto].Integral())
            histos[ihisto].SetLineWidth(3)

            if do_fit:
                fitList.append(alignUtils.make_fit(histos[ihisto], "singleGausIterative", color=self.colors[ihisto]))

            if (ihisto == 0):
                histos[ihisto].Draw("h")
                histos[ihisto].GetXaxis().SetTitle(xtitle)
                histos[ihisto].GetXaxis().SetTitleSize(0.05)
                histos[ihisto].GetXaxis().SetTitleOffset(1.)
                histos[ihisto].GetXaxis().SetLabelSize(0.06)

                histos[ihisto].GetYaxis().SetTitle(ytitle)
                histos[ihisto].GetYaxis().SetLabelSize(0.06)
                histos[ihisto].GetYaxis().SetTitleSize(0.05)
                histos[ihisto].GetYaxis().SetTitleOffset(1.4)

            else:
                histos[ihisto].Draw("hsame")

            if len(fitList) > 0:
                fitList[ihisto].Draw("same")
                mu = fitList[ihisto].GetParameter(1)
                mu_err = fitList[ihisto].GetParError(1)
                sigma = fitList[ihisto].GetParameter(2)
                sigma_err = fitList[ihisto].GetParError(2)

                plotProperties.append((" #mu=%.3f" % round(mu, 3)) + ("+/- %.3f" % round(mu_err, 3))
                                      + (" #sigma=%.3f" % round(sigma, 3)) + ("+/- %.3f" % round(sigma_err, 3)))

        leg = self.do_legend(histos, self.legend_names, 3, plotProperties, leg_location=[0.6, 0.80])

        leg.Draw("same")

        text = r.TLatex()
        text.SetNDC()
        text.SetTextFont(42)
        text.SetTextSize(0.04)
        text.SetTextColor(r.kBlack)
        text.DrawLatex(0.62, 0.82, '#bf{#it{HPS}} Work In Progress')

        saveName = self.outdir + "/" + histopath.split("/")[-1] + self.oFext

        canv.SaveAs(saveName)

        if self.do_HTML:
            img_type = self.oFext.strip(".")
            hw = htmlWriter(self.outdir, img_type=img_type)
            hw.add_images(self.outdir)
            hw.close_html()
