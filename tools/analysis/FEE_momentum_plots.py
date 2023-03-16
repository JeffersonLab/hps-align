from ROOT import *
from alignmentUtils import *
import utilities as utils


def conditionHistos(histos):
    for ihisto in range(len(histos)):
        print(ihisto, histos[ihisto])
        histos[ihisto].SetMarkerStyle(20)
        histos[ihisto].SetMarkerColor(utils.colors[ihisto])
        histos[ihisto].SetLineColor(utils.colors[ihisto])
        histos[ihisto].SetLineWidth(3)


def feeMomentumPlot(inputF, legends, histopath, outputF="", oFext=".png", doFit=True, xtitle="", ytitle=""):

    c = TCanvas("c", "c", 2400, 2000)
    # c.SetGridx()
    # c.SetGridy()

    histos = []
    for iF in inputF:
        histos.append(iF.Get(histopath))

    conditionHistos(histos)

    fitList = []
    plotProperties = []

    for ihisto in range(len(histos)):

        # Scale the histogram to unity
        # histos[ihisto].Scale(1./histos[ihisto].Integral())
        histos[ihisto].SetLineWidth(3)

        if doFit:
            fitList.append(MakeFit(histos[ihisto], "singleGausIterative", utils.colors[ihisto]))

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

    leg = doLegend(histos, legends, 3, plotProperties, legLocation=[0.6, 0.80])

    leg.Draw("same")

    text = TLatex()
    text.SetNDC()
    text.SetTextFont(42)
    text.SetTextSize(0.04)
    text.SetTextColor(kBlack)
    text.DrawLatex(0.62, 0.82, '#bf{#it{HPS}} Work In Progress')

    saveName = "./" + outputF + "/" + histopath.split("/")[-1] + oFext

    c.SaveAs(saveName)


def doLegend(histos, legends, location=1, plotProperties=[], legLocation=[]):
    if len(legends) < len(histos):
        print("WARNING:: size of legends doesn't match the size of histos")
        return None
    leg = None
    xshift = 0.3
    yshift = 0.65
    if (location == 1):
        leg = TLegend(0.6, 0.35, 0.90, 0.15)
    if (location == 2):
        leg = TLegend(0.40, 0.3, 0.65, 0.15)
    if (location == 3):
        leg = TLegend(0.15, 0.90, 0.15+xshift, 0.90-yshift)
    if (location == 4):
        xmin = 0.6
        leg = TLegend(xmin, 0.90, xmin+xshift, 0.90-yshift)

    if len(legLocation) == 2:
        leg = TLegend(legLocation[0], legLocation[1], legLocation[0]+xshift, legLocation[1]-yshift*0.6)

    for l in range(len(histos)):
        if (len(plotProperties) != len(histos)):
            leg.AddEntry(histos[l], legends[l], 'lpf')
        else:
            # splitline{The Data }{slope something }
            entry = "#splitline{" + legends[l] + "}{" + plotProperties[l] + "}"
            leg.AddEntry(histos[l], entry, 'lpf')
    leg.SetBorderSize(0)

    return leg
