from array import array
from math import floor
import ROOT as r


def find_max(histos):
    """!
    Find the maximum entry in a list of histograms

    @param histos  list of histograms
    @return maximum entry
    """

    maximum = -1

    for histo in histos:
        if (histo.GetMaximum() > maximum):
            maximum = histo.GetMaximum()
    return maximum


def make_fit(histoGram, fitType, range=[], color=None):
    """Make a fit to a histogram

    Parameters
    ----------
    h : r.TH1
        ROOT histogram to fit
    fitType : str
        type of fit to perform
    range : 2-tuple or length-2 list
        end-points of fit to include
    color : int, optional
        ROOT color to align with histogram style
    """

    # no Fit
    if fitType == "noFit":
        return None
    elif fitType == "singleGausIterative":
        fit = single_gauss_iterative(histoGram, 2, range, color)

    return fit


def profile_y_with_iterative_gauss_fit(hist, mu_graph, sigma_graph, num_bins, fitrange=[-2e5, 2e5], color=None):
    """!
    Profile a histogram in y with an iterative Gaussian fit

    @param hist  histogram to profile
    @param mu_graph  graph to store the mean values
    @param sigma_graph  graph to store the sigma values
    @param num_bins  number of bins to use for the profile
    @param fitrange  range of the fit
    @param color  color of the fit graph
    """

    if (num_bins < 1):
        return

    minEntries = 50
    fDebug = False

    num_bins_x = hist.GetXaxis().GetNbins()
    mu_graph.Rebin(num_bins)
    sigma_graph.Rebin(num_bins)

    errs_mu = [0. for x in range(floor(num_bins_x / num_bins) + 2)]
    errs_sigma = [0. for x in range(floor(num_bins_x / num_bins) + 2)]

    min_sigma = 0.
    max_sigma = 0.
    min_mu = 0.
    max_mu = 0.

    num_skipped = 0

    current_proj = None

    for i in range(1, num_bins_x+1, num_bins):
        index = int(i / num_bins)
        if (num_bins == 1):
            index -= 1

        current_proj = hist.ProjectionY(
            hist.GetName() + "_" + str(index), i, i+num_bins-1)

        mu = 0.
        mu_err = 0.
        sigma = 0.
        sigma_err = 0.
        fit = None

        if (current_proj.GetEntries() < minEntries):
            continue
        else:
            fit = single_gauss_iterative(current_proj, 2, fitrange, color)

        mu = fit.GetParameter(1)
        mu_err = fit.GetParError(1)

        sigma = fit.GetParameter(2)
        sigma_err = fit.GetParError(2)

        if (sigma > max_sigma or max_sigma == 0):
            max_sigma = sigma
        if (sigma < min_sigma or min_sigma == 0):
            min_sigma = sigma

        if (mu > max_mu or max_mu == 0):
            max_mu = mu
        if (mu < min_mu or min_mu == 0):
            min_mu = mu

        value_x = (hist.GetXaxis().GetBinLowEdge(i) +
                   hist.GetXaxis().GetBinUpEdge(i+num_bins-1))/2.

        # Important!! Use Fill to increment the graph with each iteration, or SetBinContent to replace contents...
        if (sigma_graph is not None):
            sigma_graph.Fill(value_x, sigma)

        if (mu_graph is not None):
            mu_graph.Fill(value_x, mu)

        errs_mu[index+1] = mu_err
        errs_sigma[index+1] = sigma_err

    a_errs_mu = array("d", errs_mu)
    a_errs_sigma = array("d", errs_sigma)
    if (sigma_graph is not None):
        sigma_graph.SetError(a_errs_sigma)
        sigma_graph.GetYaxis().SetTitleOffset(1.5)
        sigma_graph.GetYaxis().SetTitle(hist.GetYaxis().GetTitle())
        sigma_graph.GetXaxis().SetTitle(hist.GetXaxis().GetTitle())
        sigma_graph.SetTitle("")

    if (mu_graph is not None):
        mu_graph.SetError(a_errs_mu)
        mu_graph.GetYaxis().SetTitleOffset(1.5)
        mu_graph.GetYaxis().SetTitle(hist.GetYaxis().GetTitle())
        mu_graph.GetXaxis().SetTitle(hist.GetXaxis().GetTitle())
        mu_graph.SetTitle("")

    if (fDebug and num_skipped):
        print("Number of skipped bins: ", num_skipped)


def single_gauss_iterative(hist, sigmaRange, range=[], color=None):
    """!
    Perform a single Gaussian fit to a histogram

    @param hist  histogram to fit
    @param sigmaRange  range of the fit
    @param range  range of the fit
    @param color  color of the fit graph
    """

    debug = False
    # first perform a single Gaus fit across full range of histogram or in a specified range

    min = hist.GetBinLowEdge(1)
    max = hist.GetBinLowEdge(hist.GetNbinsX()) + \
        hist.GetBinWidth(hist.GetNbinsX())

    # if range:
    if (len(range) != 0):
        min = range[0]
        max = range[1]

    fitA = r.TF1("fitA", "gaus", min, max)
    hist.Fit("fitA", "ORQN", "same")
    fitAMean = fitA.GetParameter(1)
    fitASig = fitA.GetParameter(2)

    # performs a second fit with range determined by first fit
    max = fitAMean + (fitASig*sigmaRange)
    min = fitAMean - (fitASig*sigmaRange)
    fitB = r.TF1("fitB", "gaus", min, max)
    hist.Fit("fitB", "ORQN", "same")
    fitMean = fitB.GetParameter(1)
    fitSig = fitB.GetParameter(2)

    newFitSig = 99999
    newFitMean = 99999
    i = 0
    max = fitMean + (fitSig*sigmaRange)
    min = fitMean - (fitSig*sigmaRange)
    fit = r.TF1("fit", "gaus", min, max)

    while abs(fitSig - newFitSig) > 0.0005 or abs(fitMean - newFitMean) > 0.0005:

        if (i > 0):
            fitMean = newFitMean
            fitSig = newFitSig
        if debug:
            print("i = ", i, " fitMean = ", fitMean, " fitSig = ", fitSig)

        max = fitMean + (fitSig*sigmaRange)
        min = fitMean - (fitSig*sigmaRange)
        fit.SetRange(min, max)
        hist.Fit("fit", "ORQN", "same")
        newFitMean = fit.GetParameter(1)
        newFitSig = fit.GetParameter(2)
        if debug:  # \todo logging analogously to Jeremy's hps-mc PR
            print("i = ", i, " newFitMean = ",
                  newFitMean, " newFitSig = ", newFitSig)
        if (i > 50):
            print(
                "WARNING terminate iterative gaus fit because of convergence problems")
            print("final mean =  ", newFitMean,
                  ", previous iter mean = ", fitMean)
            print("final sigma =  ", newFitSig,
                  ", previous iter sigma = ", fitSig)
            break

        i += 1

    if debug:
        print("Final i = ", i, " finalFitMean = ", fit.GetParameter(
            1), " finalFitSig = ", fit.GetParameter(2))

    fit.SetLineWidth(2)
    if color:
        fit.SetLineColor(color)

    return fit


def set_style():
    """!
    Set the style of the plots"""

    r.gROOT.SetBatch(1)

    # put tick marks on top and RHS of plots
    r.gStyle.SetPadTickX(1)
    r.gStyle.SetPadTickY(1)

    # do not display any of the standard histogram decorations
    r.gStyle.SetOptTitle(0)
    r.gStyle.SetOptStat(0)
    r.gStyle.SetOptFit(0)

    # use bold lines and markers
    r.gStyle.SetMarkerSize(1.0)
    r.gStyle.SetHistLineWidth(3)
    r.gStyle.SetLineStyleString(2, "[12 12]")  # postscript dashes

    # set the paper & margin sizes
    r.gStyle.SetPaperSize(20, 26)
    r.gStyle.SetPadLeftMargin(0.14)
    r.gStyle.SetPadRightMargin(0.06)
    r.gStyle.SetPadBottomMargin(0.15)
    r.gStyle.SetPadTopMargin(0.08)
    r.gStyle.SetFrameFillColor(0)

    # use large fonts
    r.gStyle.SetTextFont(62)
    r.gStyle.SetLegendFont(62)
    r.gStyle.SetLabelFont(42, "xyz")
    r.gStyle.SetTitleSize(0.04, "xyz")
    r.gStyle.SetLabelSize(0.04, "xyz")
    r.gStyle.SetTitleFont(42, "xyz")
    r.gStyle.SetLabelFont(42, "xyz")

    # get rid of X error bars and y error bar caps
    r.gStyle.SetErrorX(0.001)

    # use plain black on white colors
    r.gStyle.SetFrameBorderMode(0)
    r.gStyle.SetCanvasBorderMode(0)
    r.gStyle.SetPadBorderMode(0)
    r.gStyle.SetPadColor(0)
    r.gStyle.SetCanvasColor(0)
    r.gStyle.SetStatColor(0)

    NRGBs = 5
    NCont = 255

    stops = array("d", [0.00, 0.34, 0.61, 0.84, 1.00])
    red = array("d", [0.00, 0.00, 0.87, 1.00, 0.51])
    green = array("d", [0.00, 0.81, 1.00, 0.20, 0.00])
    blue = array("d", [0.51, 1.00, 0.12, 0.00, 0.00])
    r.TColor.CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont)
    r.gStyle.SetNumberContours(NCont)

    r.gROOT.ForceStyle()
