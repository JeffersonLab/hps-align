import ROOT as r
import json
import os
from tools.analysis.base_plotter import BasePlotter
import tools.analysis.alignment_utils as alignUtils
from tools.analysis.index_page import htmlWriter


class ResidualPlots2D():
    """! Class for 2D residual plots"""

    def __init__(self, config_file=""):
        self.config_file = config_file
        self.read_config()

        ## input TFiles 2D
        self.input_files = []
        for inFile in self.infile_names:
            self.input_files.append(r.TFile(inFile))

        for outdir in self.outdirs:
            if (not os.path.exists(outdir)):
                os.makedirs(outdir)

    def read_config(self):
        """! Read configuration file

        Possible options:
        - inputFiles: input files
        - outdir: output directory
        - do_HTML: create html page
        - oFext: extension of output files; default .png
        - legend: names displayed in legend
        """

        f = open(self.config_file, 'r')
        config = json.load(f)

        if config['inputFiles']:
            self.infile_names = config['inputFiles']
        if config['outdirs']:
            self.outdirs = config['outdirs']
        if config['oFext']:
            self.oFext = config['oFext']

    def plot_2D_residuals(self, histo_name):
        histos = []
        for infile in self.input_files:
            print(infile)
            histos.append(infile.Get(histo_name))

        for ihist in range(len(histos)):
            print(str(ihist) + " " + self.outdirs[ihist] + " " + histo_name)
            self.profileZ_with_custom_fit(histos[ihist], 1, self.outdirs[ihist], histo_name)

    def profileZ_with_custom_fit(self, hist, num_bins, outdir, name, fitrange=[-2e5, 2e5], fittype="gaus", transform=0, get_simple_mean=True):
        """!
        2D profile of a histogram in Z with a custom fit

        @param hist  histogram to profile
        @param num_bins  number of bins to use for the profile
        @param fitrange  range of the fit
        @param fittype  type of fit to use
        @param transform  transform to apply to mu graph when filling output histograms
        """

        if (not hist):
            print("profileZ_with_custom_fit(): No histogram supplied!")
            return

        num_bins_x = hist.GetXaxis().GetNbins()
        num_bins_y = hist.GetYaxis().GetNbins()
        xmin = hist.GetXaxis().GetXmin()
        xmax = hist.GetXaxis().GetXmax()
        ymin = hist.GetYaxis().GetXmin()
        ymax = hist.GetYaxis().GetXmax()

        mu_name = hist.GetName() + "_mu_profiled_" + fittype
        mu_graph = r.TH2D(mu_name, mu_name, num_bins_x, xmin, xmax, num_bins_y, ymin, ymax)
        sigma_name = hist.GetName() + "_sigma_profiled_" + fittype
        sigma_graph = r.TH2D(sigma_name, sigma_name, num_bins_x, xmin, xmax, num_bins_y, ymin, ymax)
        mu_err_name = hist.GetName() + "_mu_err_profiled_" + fittype
        mu_err_graph = r.TH2D(mu_err_name, mu_err_name, num_bins_x, xmin, xmax, num_bins_y, ymin, ymax)
        sigma_err_name = hist.GetName() + "_sigma_err_profiled_" + fittype
        sigma_err_graph = r.TH2D(sigma_err_name, sigma_err_name, num_bins_x, xmin, xmax, num_bins_y, ymin, ymax)

        minEntries = 100
        fDebug = 0

        num_skipped = 0  # number of bins skipped due to too few entries

        max_sigma = 0  # maximum sigma value
        min_sigma = 0

        max_mu = 0
        min_mu = 0

        current_proj = None

        for i in range(1, num_bins_x+(num_bins == 1), num_bins):
            for j in range(1, num_bins_y+(num_bins == 1), num_bins):
                index = i/num_bins
                index_y = j/num_bins

                current_proj = hist.ProjectionZ(hist.GetName() + "_" + str(index) + "_" + str(index_y), i, i+num_bins-1, j, j+num_bins-1)
                current_proj.SetTitle(hist.GetName() + "_" + str(index) + "_" + str(index_y))

                current_mu = -999
                current_err_mu = -999
                current_sigma = -999
                current_err_sigma = -999

                if current_proj.GetEntries() < minEntries:
                    current_mu = 0
                    current_sigma = 0
                    if (get_simple_mean):
                        current_mu = current_proj.GetMean()
                        current_sigma = current_proj.GetStdDev()
                    current_err_mu = 1
                    current_err_sigma = 1

                    if (fDebug):
                        print("WARNING: Only " + current_proj.GetEntries() + " entries in bin " + index + "," + index_y + " in histogram " + hist.GetName())
                        num_skipped += 1

                else:
                    fit = alignUtils.single_gauss_iterative(current_proj, 2, fitrange)
                    current_norm = fit.GetParameter(0)
                    current_mu = fit.GetParameter(1)
                    current_err_mu = fit.GetParError(1)
                    current_sigma = fit.GetParameter(2)
                    current_err_sigma = fit.GetParError(2)

                    if fittype == "cb":
                        crystalFit = r.CrystalBallFit(current_proj,
                                                      [current_norm, current_mu, current_sigma],
                                                      fitrange=[current_mu - 5*current_sigma, current_mu + 5*current_sigma])

                        current_mu = crystalFit.GetParameter(4)
                        current_err_mu = crystalFit.GetParError(4)
                        current_sigma = crystalFit.GetParameter(3)
                        current_err_sigma = crystalFit.GetParError(3)

                if (current_sigma > max_sigma or max_sigma == 0):
                    max_sigma = current_sigma
                if (current_sigma < min_sigma or min_sigma == 0):
                    min_sigma = current_sigma
                if (current_mu > max_mu or max_mu == 0):
                    max_mu = current_mu
                if (current_mu < min_mu or min_mu == 0):
                    min_mu = current_mu

                x_coord = (hist.GetXaxis().GetBinLowEdge(i) + hist.GetXaxis().GetBinUpEdge(i+num_bins-1))/2
                y_coord = (hist.GetYaxis().GetBinLowEdge(j) + hist.GetYaxis().GetBinUpEdge(j+num_bins-1))/2

                if (sigma_graph):
                    sigma_graph.Fill(x_coord, y_coord, current_sigma)
                if (mu_graph):
                    if transform == 0:
                        mu_graph.Fill(x_coord, y_coord, current_mu)
                    elif transform == 1:
                        mu_graph.Fill(-x_coord, y_coord, current_mu)
                    elif transform == 2:
                        mu_graph.Fill(x_coord, -y_coord, current_mu)
                    elif transform == 3:
                        mu_graph.Fill(x_coord, -y_coord, -current_mu)
                    elif transform == 4:
                        mu_graph.Fill(-x_coord, -y_coord, -current_mu)

                # should probably be replace bin content, not fill?
                if (sigma_err_graph):
                    sigma_err_graph.Fill(x_coord, y_coord, current_err_sigma)
                if (mu_err_graph):
                    mu_err_graph.Fill(x_coord, y_coord, current_err_mu)

        if (mu_graph):
            mu_graph.GetXaxis().SetTitle(hist.GetXaxis().GetTitle())
            mu_graph.GetYaxis().SetTitle(hist.GetYaxis().GetTitle())
            mu_graph.GetYaxis().SetTitleOffset(1)
            mu_graph.GetZaxis().SetTitle(hist.GetZaxis().GetTitle())
            mu_graph.GetZaxis().SetTitleOffset(1.2)
            mu_graph.SetTitle("")

        if (sigma_graph):
            sigma_graph.GetXaxis().SetTitle(hist.GetXaxis().GetTitle())
            sigma_graph.GetYaxis().SetTitle(hist.GetYaxis().GetTitle())
            sigma_graph.GetYaxis().SetTitleOffset(1)
            sigma_graph.GetZaxis().SetTitle(hist.GetZaxis().GetTitle())
            sigma_graph.GetZaxis().SetTitleOffset(1.2)
            sigma_graph.SetTitle("")

        if (mu_err_graph):
            mu_err_graph.GetXaxis().SetTitle(hist.GetXaxis().GetTitle())
            mu_err_graph.GetYaxis().SetTitle(hist.GetYaxis().GetTitle())
            mu_err_graph.GetYaxis().SetTitleOffset(1)
            mu_err_graph.GetZaxis().SetTitle("Error of fit #mu:" + hist.GetZaxis().GetTitle())
            mu_err_graph.GetZaxis().SetTitleOffset(1.2)
            mu_err_graph.SetTitle(hist.GetTitle())

        if (sigma_err_graph):
            sigma_err_graph.GetXaxis().SetTitle(hist.GetXaxis().GetTitle())
            sigma_err_graph.GetYaxis().SetTitle(hist.GetYaxis().GetTitle())
            sigma_err_graph.GetYaxis().SetTitleOffset(1)
            sigma_err_graph.GetZaxis().SetTitle("Error of fit #sigma: " + hist.GetZaxis().GetTitle())
            sigma_err_graph.GetZaxis().SetTitleOffset(1.2)
            sigma_err_graph.SetTitle(hist.GetTitle())

        canv = r.TCanvas("c1", "c1", 2200, 2000)
        mu_graph.GetZaxis().SetRangeUser(-0.1, 0.1)
        mu_graph.Draw("COLZ")
        canv.SaveAs(outdir + "/" + name + ".png")
