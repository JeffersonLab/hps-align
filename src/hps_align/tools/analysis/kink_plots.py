import ROOT as r
from .base_plotter import BasePlotter
from . import alignment_utils
from .index_page import htmlWriter


class KinkPlots(BasePlotter):

    def __init__(self, legend_names=[], infile_names=[], outdir="", do_HTML=False, oFext=".png", config_file="", indir=""):
        super().__init__(legend_names=legend_names, infile_names=infile_names, outdir=outdir, do_HTML=do_HTML, oFext=oFext, config_file=config_file, indir=indir)

    def plot_lambda_kinks(self):
        """! Create and save the lambda kink summary plots"""

        histos = []
        for infile in self.input_files:
            histos.append(infile.Get("gbl_kinks/lambda_kink_mod_p"))

        canv = r.TCanvas("c1", "c1", 2200, 2000)
        canv.SetGridx()
        canv.SetGridy()

        for ihisto in range(len(histos)):
            self.set_histo_style(histos[ihisto], ihisto)

            if (ihisto == 0):

                for ibin in range(0, histos[ihisto].GetXaxis().GetNbins()):
                    histos[ihisto].GetXaxis().SetBinLabel(ibin+1, self.binLabels[ibin])
                    histos[ihisto].GetXaxis().SetLabelSize(0.04)
                    histos[ihisto].GetXaxis().ChangeLabel(ibin+1, 270)

                histos[ihisto].GetYaxis().SetRangeUser(-0.0006, 0.0006)
                histos[ihisto].GetYaxis().SetTitle("<#lambda kink>")
                histos[ihisto].GetYaxis().SetLabelSize(0.05)
                histos[ihisto].GetYaxis().SetTitleSize(histos[ihisto].GetYaxis().GetTitleSize()*0.7)
                histos[ihisto].GetYaxis().SetTitleOffset(histos[ihisto].GetYaxis().GetTitleOffset()*1.35)
                histos[ihisto].Draw("P")
            else:
                histos[ihisto].Draw("P SAME")

        leg = self.do_legend(histos, self.legend_names, 2)
        if (leg is not None):
            leg.Draw()
        canv.SaveAs(self.outdir + "/" + "lambda_kinks" + self.oFext)

        # Put plots in a webpage
        if self.do_HTML:
            hw = htmlWriter(self.outdir)
            hw.add_images(self.outdir)
            hw.close_html()

    def plot_phi_kinks(self):
        """! Create and save the phi kink summary plots"""

        histos = []
        for infile in self.input_files:
            histos.append(infile.Get("gbl_kinks/phi_kink_mod_p"))

        canv = r.TCanvas("c1", "c1", 2200, 2000)
        canv.SetGridx()
        canv.SetGridy()

        for ihisto in range(len(histos)):
            self.set_histo_style(histos[ihisto], ihisto)

            if (ihisto == 0):
                for ibin in range(0, histos[ihisto].GetXaxis().GetNbins()):
                    histos[ihisto].GetXaxis().SetBinLabel(ibin+1, self.binLabels[ibin])
                    histos[ihisto].GetXaxis().SetLabelSize(0.04)
                    histos[ihisto].GetXaxis().ChangeLabel(ibin+1, 270)
                histos[ihisto].GetYaxis().SetLabelSize(0.05)
                histos[ihisto].GetYaxis().SetTitle("<#phi kink>")
                histos[ihisto].GetYaxis().SetTitleSize(histos[ihisto].GetYaxis().GetTitleSize()*0.7)
                histos[ihisto].GetYaxis().SetTitleOffset(histos[ihisto].GetYaxis().GetTitleOffset()*1.35)
                histos[ihisto].GetYaxis().SetRangeUser(-0.00099, 0.00099)
                histos[ihisto].Draw("P")
            else:
                histos[ihisto].Draw("P SAME")

        leg = self.do_legend(histos, self.legend_names, 2)
        if (leg is not None):
            leg.Draw()
        canv.SaveAs(self.outdir + "/" + "phi_kinks" + self.oFext)

        # Profile with gaussian
        histos = []
        histos_mu = []
        for infile in self.input_files:
            histos.append(infile.Get("gbl_kinks/phi_kink_mod"))

        for ihisto in range(len(histos)):
            histos_mu.append(r.TH1F(histos[ihisto].GetName() + "_mu" + str(ihisto), histos[ihisto].GetName() + "_mu" + str(ihisto), histos[ihisto].GetXaxis().GetNbins(), histos[ihisto].GetXaxis().GetXmin(), histos[ihisto].GetXaxis().GetXmax()))
            sigma_graph = r.TH1F(histos[ihisto].GetName() + "_sigma" + str(ihisto), histos[ihisto].GetName() + "_sigma" + str(ihisto), histos[ihisto].GetXaxis().GetNbins(), histos[ihisto].GetXaxis().GetXmin(), histos[ihisto].GetXaxis().GetXmax())
            alignment_utils.profile_y_with_iterative_gauss_fit(histos[ihisto], histos_mu[ihisto], sigma_graph, 1)

            self.set_histo_style(histos_mu[ihisto], ihisto)

            if (ihisto == 0):
                for ibin in range(0, histos[ihisto].GetXaxis().GetNbins()):
                    histos_mu[ihisto].GetXaxis().SetBinLabel(ibin+1, self.binLabels[ibin])
                    histos_mu[ihisto].GetXaxis().SetLabelSize(0.04)
                    histos_mu[ihisto].GetXaxis().ChangeLabel(ibin+1, 270)
                histos_mu[ihisto].GetYaxis().SetLabelSize(0.05)
                histos_mu[ihisto].GetYaxis().SetTitle("<#phi kink> gauss")
                histos_mu[ihisto].GetYaxis().SetTitleSize(histos[ihisto].GetYaxis().GetTitleSize()*0.7)
                histos_mu[ihisto].GetYaxis().SetTitleOffset(histos[ihisto].GetYaxis().GetTitleOffset()*1.35)
                histos_mu[ihisto].GetYaxis().SetRangeUser(-0.00099, 0.00099)
                histos_mu[ihisto].Draw("P")
            else:
                histos_mu[ihisto].Draw("P SAME")

        leg = self.do_legend(histos_mu, self.legend_names, 2)
        if (leg is not None):
            leg.Draw()
        canv.SaveAs(self.outdir + "/" + "phi_kinks_gaus" + self.oFext)

        if self.do_HTML:
            img_type = self.oFext.strip(".")
            hw = htmlWriter(self.outdir, img_type=img_type)
            hw.add_images(self.outdir)
            hw.close_html()
