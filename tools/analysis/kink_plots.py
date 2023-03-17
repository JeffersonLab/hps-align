from base_plotter import BasePlotter
import ROOT as r
import alignment_utils as alignUtils


class KinkPlots(BasePlotter):

    def __init__(self):
        super().__init__()

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

    def plot_lambda_kinks(self):
        histos = []
        for infile in self.input_files:
            histos.append(infile.Get("gbl_kinks/lambda_kink_mod_p"))

        c = r.TCanvas("c1", "c1", 2200, 2000)
        c.SetGridx()
        c.SetGridy()

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
        c.SaveAs(self.outdir + "/" + "lambda_kinks" + self.oFext)

    def plot_phi_kinks(self):
        histos = []
        for infile in self.input_files:
            histos.append(infile.Get("gbl_kinks/phi_kink_mod_p"))

        c = r.TCanvas("c1", "c1", 2200, 2000)
        c.SetGridx()
        c.SetGridy()

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
                histos[ihisto].GetYaxis().SetRangeUser(-0.001, 0.001)
                histos[ihisto].Draw("P")
            else:
                histos[ihisto].Draw("P SAME")

        leg = self.do_legend(histos, self.legend_names, 2)
        if (leg is not None):
            leg.Draw()
        c.SaveAs(self.outdir + "/" + "phi_kinks" + self.oFext)

        # Profile with gaussian

        histos = []
        histos_mu = []
        for infile in self.input_files:
            histos.append(infile.Get("gbl_kinks/phi_kink_mod"))

        for ihisto in range(len(histos)):
            histos_mu.append(r.TH1F(histos[ihisto].GetName()+"_mu"+str(ihisto), histos[ihisto].GetName()+"_mu"+str(ihisto), histos[ihisto].GetXaxis().GetNbins(), histos[ihisto].GetXaxis().GetXmin(), histos[ihisto].GetXaxis().GetXmax()))
            sigma_graph = r.TH1F(histos[ihisto].GetName()+"_sigma"+str(ihisto), histos[ihisto].GetName()+"_sigma"+str(ihisto), histos[ihisto].GetXaxis().GetNbins(), histos[ihisto].GetXaxis().GetXmin(), histos[ihisto].GetXaxis().GetXmax())
            alignUtils.profile_y_with_iterative_gauss_fit(histos[ihisto], histos_mu[ihisto], sigma_graph, 1)

            self.set_histo_style(histos_mu[ihisto], ihisto)

            if (ihisto == 0):
                for ibin in range(0, histos[ihisto].GetXaxis().GetNbins()):
                    histos_mu[ihisto].GetXaxis().SetBinLabel(ibin+1, self.binLabels[ibin])
                    histos_mu[ihisto].GetXaxis().SetLabelSize(0.04)
                    histos_mu[ihisto].GetXaxis().ChangeLabel(ibin+1, 270)
                histos_mu[ihisto].GetYaxis().SetLabelSize(0.05)
                histos_mu[ihisto].GetYaxis().SetTitle("<#phi kink>")
                histos_mu[ihisto].GetYaxis().SetTitleSize(histos[ihisto].GetYaxis().GetTitleSize()*0.7)
                histos_mu[ihisto].GetYaxis().SetTitleOffset(histos[ihisto].GetYaxis().GetTitleOffset()*1.35)
                histos_mu[ihisto].GetYaxis().SetRangeUser(-0.002, 0.002)
                histos_mu[ihisto].Draw("P")
            else:
                histos_mu[ihisto].Draw("P SAME")

        leg = self.do_legend(histos_mu, self.legend_names, 2)
        if (leg is not None):
            leg.Draw()
        c.SaveAs(self.outdir + "/" + "phi_kinks_gaus" + self.oFext)
