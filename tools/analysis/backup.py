def plotPhiKinks(inputF, legends=[], outFolder="./"):
    histos = []
    for iF in inputF:
        histos.append(iF.Get("gbl_kinks/phi_kink_mod_p"))

    c = r.TCanvas("c1", "c1", 2200, 2000)
    c.SetGridx()
    c.SetGridy()

    for ihisto in range(len(histos)):
        print(ihisto, histos[ihisto])
        histos[ihisto].SetMarkerStyle(config.markers[ihisto])
        histos[ihisto].SetMarkerColor(config.colors[ihisto])
        histos[ihisto].SetMarkerSize(4)
        histos[ihisto].SetLineColor(config.colors[ihisto])
        histos[ihisto].SetLineWidth(5)

        if (ihisto == 0):
            for ibin in range(0, histos[ihisto].GetXaxis().GetNbins()):
                histos[ihisto].GetXaxis().SetBinLabel(ibin+1, config.binLabels[ibin])
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

    leg = doLegend(histos, legends, 2)
    if (leg is not None):
        leg.Draw()
    c.SaveAs(outFolder + "/" + "phi_kinks" + config.args.oFext)

    # Profile with gaussian

    histos = []
    histos_mu = []
    for iF in inputF:
        histos.append(iF.Get("gbl_kinks/phi_kink_mod"))

    for ihisto in range(len(histos)):
        histos_mu.append(r.TH1F(histos[ihisto].GetName()+"_mu"+str(ihisto), histos[ihisto].GetName()+"_mu"+str(ihisto), histos[ihisto].GetXaxis().GetNbins(), histos[ihisto].GetXaxis().GetXmin(), histos[ihisto].GetXaxis().GetXmax()))
        sigma_graph = r.TH1F(histos[ihisto].GetName()+"_sigma"+str(ihisto), histos[ihisto].GetName()+"_sigma"+str(ihisto), histos[ihisto].GetXaxis().GetNbins(), histos[ihisto].GetXaxis().GetXmin(), histos[ihisto].GetXaxis().GetXmax())
        alignUtils.profile_y_with_iterative_gauss_fit(histos[ihisto], histos_mu[ihisto], sigma_graph, 1)

        histos_mu[ihisto].SetMarkerStyle(config.markers[ihisto])
        histos_mu[ihisto].SetMarkerColor(config.colors[ihisto])
        histos_mu[ihisto].SetMarkerSize(4)
        histos_mu[ihisto].SetLineColor(config.colors[ihisto])
        histos_mu[ihisto].SetLineWidth(5)

        if (ihisto == 0):
            for ibin in range(0, histos[ihisto].GetXaxis().GetNbins()):
                histos_mu[ihisto].GetXaxis().SetBinLabel(ibin+1, config.binLabels[ibin])
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

    leg = doLegend(histos_mu, legends, 2)
    if (leg is not None):
        leg.Draw()
    c.SaveAs(outFolder + "/" + "phi_kinks_gaus" + config.args.oFext)

    def plotLambdaKinks(inputF, legends=[], outFolder=""):
    histos = []
    for iF in inputF:
        histos.append(iF.Get("gbl_kinks/lambda_kink_mod_p"))

    c = r.TCanvas("c1", "c1", 2200, 2000)
    c.SetGridx()
    c.SetGridy()

    for ihisto in range(len(histos)):
        print(ihisto, histos[ihisto])
        histos[ihisto].SetMarkerStyle(config.markers[ihisto])
        histos[ihisto].SetMarkerColor(config.colors[ihisto])
        histos[ihisto].SetMarkerSize(4)
        histos[ihisto].SetLineColor(config.colors[ihisto])
        histos[ihisto].SetLineWidth(5)

        if (ihisto == 0):

            for ibin in range(0, histos[ihisto].GetXaxis().GetNbins()):
                histos[ihisto].GetXaxis().SetBinLabel(ibin+1, config.binLabels[ibin])
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

    leg = doLegend(histos, legends, 2)
    if (leg is not None):
        leg.Draw()
    c.SaveAs(outFolder + "/" + "lambda_kinks" + config.args.oFext)


def plotRes(inputF, legends=[], outputF="./"):

    histos = []
    for iF in inputF:
        histos.append(iF.Get("res/uresidual_GBL_mod_p"))

    c = r.TCanvas("c1", "c1", 2200, 2000)
    c.SetGridx()
    # c.SetGridy()

    for ihisto in range(len(histos)):
        print(ihisto, histos[ihisto])
        histos[ihisto].SetMarkerStyle(config.markers[ihisto])
        histos[ihisto].SetMarkerColor(config.colors[ihisto])
        histos[ihisto].SetMarkerSize(4)
        histos[ihisto].SetLineColor(config.colors[ihisto])
        histos[ihisto].SetLineWidth(5)

        if (ihisto == 0):

            for ibin in range(0, histos[ihisto].GetXaxis().GetNbins()):
                histos[ihisto].GetXaxis().SetBinLabel(ibin+1, config.binLabels[ibin])
                histos[ihisto].GetXaxis().SetLabelSize(0.04)
                histos[ihisto].GetXaxis().ChangeLabel(ibin+1, 270)
            histos[ihisto].GetYaxis().SetRangeUser(-0.2, 0.2)
            histos[ihisto].GetYaxis().SetLabelSize(0.05)
            histos[ihisto].GetYaxis().SetTitle("<unbiased local X residual> [mm]")
            histos[ihisto].GetYaxis().SetTitleSize(histos[ihisto].GetYaxis().GetTitleSize()*0.7)
            histos[ihisto].GetYaxis().SetTitleOffset(histos[ihisto].GetYaxis().GetTitleOffset()*1.65)

            histos[ihisto].Draw("P")
        else:
            histos[ihisto].Draw("P SAME")

    leg = doLegend(histos, legends, legLocation=[0.5, 0.85])
    if (leg is not None):
        leg.Draw()

    text = r.TLatex()
    text.SetNDC()
    text.SetTextFont(42)
    text.SetTextSize(0.04)
    text.SetTextColor(r.kBlack)
    text.DrawLatex(0.52, 0.87, '#bf{#it{HPS} Work In Progress}')

    c.SaveAs(outputF + "/uresiduals" + config.args.oFext)


def plot1DResiduals(inputF, name, legends=[], outFolder="./", inFolder="res/", titleName=""):

    histos = []
    for iF in inputF:
        histos.append(iF.Get(inFolder+name))

    c = r.TCanvas("c1", "c1", 2200, 2000)
    # c.SetGridx()
    # c.SetGridy()
    if (titleName == ""):
        titleName = name.split("_")[3] + "_" + name.split("_")[5]

    maximum = -1.

    fitList = []
    plotProperties = []

    # Normalise and get maximum after normalisation
    for histo in histos:

        # Normalise the histogram

        if abs(histo.Integral()) > 1e-8:
            histo.Scale(1./histo.Integral())

        # Get the maximum
        if (histo.GetMaximum() > maximum):
            maximum = histo.GetMaximum()

    if ("slot") in name:
        titleName += "_slot"
    elif "hole" in name:
        titleName += "_hole"

    for ihisto in range(len(histos)):
        histos[ihisto].SetMarkerStyle(config.markers[ihisto])
        histos[ihisto].SetMarkerColor(config.colors[ihisto])
        histos[ihisto].SetMarkerSize(4)
        histos[ihisto].SetLineColor(config.colors[ihisto])
        histos[ihisto].GetXaxis().SetLabelSize(0.05)
        histos[ihisto].GetYaxis().SetLabelSize(0.05)
        histos[ihisto].SetLineWidth(5)

        # Fitting
        fitList.append(alignUtils.make_fit(histos[ihisto], "singleGausIterative", [], config.colors[ihisto]))

        if (ihisto == 0):
            # histos[ihisto].GetXaxis().SetTitle(titleName + " local X residual [mm]")
            histos[ihisto].GetXaxis().SetTitle(titleName)
            histos[ihisto].GetXaxis().SetTitleSize(0.05)
            histos[ihisto].GetXaxis().SetTitleOffset(1.25)
            histos[ihisto].SetMaximum(maximum*1.5)
            histos[ihisto].GetYaxis().SetRangeUser(0.0, maximum*1.5)
            histos[ihisto].Draw("P")
        else:
            histos[ihisto].Draw("P SAME")

        fitList[ihisto].Draw("SAME")
        # Save fit properties

        mu = fitList[ihisto].GetParameter(1)
        mu_err = fitList[ihisto].GetParError(1)
        sigma = fitList[ihisto].GetParameter(2)
        sigma_err = fitList[ihisto].GetParError(2)

        # plotProperties.append((" #mu=%.3f"%round(mu,3))+("+/- %.3f"%round(mu_err,3))
        #                       +(" #sigma=%.3f"%round(sigma,3)) +("+/- %.3f"%round(sigma_err,3) ))

        plotProperties.append((" #mu=%.3f" % round(mu, 3))
                              + (" #sigma=%.3f" % round(sigma, 3)))

    leg = doLegend(histos, legends, 3, plotProperties)

    if (leg is not None):
        leg.Draw()

    text = r.TLatex()
    text.SetNDC()
    text.SetTextFont(42)
    text.SetTextSize(0.04)
    text.SetTextColor(r.kBlack)
    text.DrawLatex(0.16, 0.89, '#bf{#it{HPS}} Work In Progress')

    c.SaveAs(outFolder + "/" + name + config.args.oFext)


# 1: bottom right
# 2: bottom center
# 3: top right and bigger

def doLegend(histos, legends, location=1, plotProperties=[], legLocation=[]):
    if len(legends) < len(histos):
        print("WARNING:: size of legends doesn't match the size of histos")
        return None
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

    if len(legLocation) == 2:
        leg = r.TLegend(legLocation[0], legLocation[1], legLocation[0]+xshift, legLocation[1]-yshift*0.6)

    for l in range(len(histos)):
        if (len(plotProperties) != len(histos)):
            leg.AddEntry(histos[l], legends[l], 'lpf')
        else:
            # splitline{The Data }{slope something }
            # entry = "#splitline{"+legends[l]+"}{"+plotProperties[l]+"}"
            entry = (legends[l] + " " + plotProperties[l])
            leg.AddEntry(histos[l], entry, 'lpf')
    leg.SetBorderSize(0)

    return leg


def plotProfileY(inputF, name, legends=[],
                 outFolder="./",
                 inFolder="res/",
                 xtitle="hit position [mm]",
                 ytitle="<ures> [mm]",
                 rangeX=[], rangeY=[], fitrange=[-2e5, 2e5],
                 outFile=None,
                 fit="[0]*x + [1]", num_bins=1, rebin=1):

    histos = []
    histos_mu = []
    histos_sigma = []

    for iF in inputF:
        if not iF.Get(inFolder+name):
            print(inFolder+name + "   NOT FOUND")
            return

        histos.append(iF.Get(inFolder+name))

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

        histos_mu[ihisto].SetMarkerStyle(config.markers[ihisto])
        histos_mu[ihisto].SetMarkerColor(config.colors[ihisto])
        histos_mu[ihisto].SetMarkerSize(4)
        histos_mu[ihisto].SetLineColor(config.colors[ihisto])
        histos_mu[ihisto].SetLineWidth(5)

        histos_sigma[ihisto].SetMarkerStyle(config.markers[ihisto])
        histos_sigma[ihisto].SetMarkerColor(config.colors[ihisto])
        histos_sigma[ihisto].SetMarkerSize(4)
        histos_sigma[ihisto].SetLineColor(config.colors[ihisto])
        histos_sigma[ihisto].SetLineWidth(5)

        hist = histos_mu[ihisto]
        hmin = hist.GetBinLowEdge(1)
        hmax = (hist.GetBinLowEdge(hist.GetNbinsX()))+hist.GetBinWidth(hist.GetNbinsX())

        fitPars = []

        fitF = r.TF1("fit"+str(ihisto), fit, hmin, hmax)
        histos_mu[ihisto].Fit("fit"+str(ihisto), "QNR")

        string = ""
        for i in range(fitF.GetNpar()):
            fitPars.append(fitF.GetParameter(i))
            string += str(round(fitPars[i], 4)) + ","

        # plotProperties.append((" %.4f"%round(fit_par1,4))+"x + " +(" %.4f"%round(fit_par0,4)) )
        plotProperties.append(string)
        fits.append(fitF)

        if (ihisto == 0):
            histos_mu[ihisto].GetXaxis().SetTitle(xtitle)
            histos_mu[ihisto].GetYaxis().SetTitle(ytitle)
            histos_mu[ihisto].GetYaxis().SetTitleSize(histos[ihisto].GetYaxis().GetTitleSize()*0.7)
            histos_mu[ihisto].GetYaxis().SetTitleOffset(histos[ihisto].GetYaxis().GetTitleOffset()*1.35)
            # histos_mu[ihisto].GetYaxis().SetRangeUser(-0.0002,0.0002)
            histos_mu[ihisto].GetYaxis().SetRangeUser(-0.2, 0.2)
            if len(rangeY) > 1:
                histos_mu[ihisto].GetYaxis().SetRangeUser(rangeY[0], rangeY[1])
            histos_mu[ihisto].Draw("P")
            if len(rangeX) > 1:
                histos_mu[ihisto].GetXaxis().SetRangeUser(rangeX[0], rangeX[1])
        else:
            histos_mu[ihisto].Draw("P SAME")

        fitF.SetLineColor(config.colors[ihisto])
        # fitF.Draw("SAME")

    leg = doLegend(histos_mu, legends, 2, plotProperties)

    if (leg is not None):
        leg.Draw()

    text = r.TLatex()
    text.SetNDC()
    text.SetTextFont(42)
    text.SetTextSize(0.04)
    text.SetTextColor(r.kBlack)
    text.DrawLatex(0.66, 0.89, '#bf{#it{HPS}} Work In Progress')

    c.SaveAs(outFolder + "/" + name + "_profiled" + config.args.oFext)

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

        fitF.SetLineColor(config.colors[ihisto])
        # fitF.Draw("SAME")

    leg = doLegend(histos_sigma, legends, 2, plotProperties)

    if (leg is not None):
        leg.Draw()

    c1.SaveAs(outFolder + "/" + name + "_sigma_profiled" + config.args.oFext)


def doMultVtxPlots(inputF, legends=[], outDir="./MultiVtx_plots/"):

    print("--- MultiVtxPlots --- ")
    histos_top = []
    histos_bot = []
    histos = []
    f_path = "MultiEventVtx/"

    for iF in inputF:
        histos_top.append(iF.Get("MultiEventVtx/vtx_z_top"))
        histos_bot.append(iF.Get("MultiEventVtx/vtx_z_bottom"))
        histos.append(iF.Get("MultiEventVtx/vtx_z"))

    c = r.TCanvas("c1", "c1", 2200, 2000)
    c.SetGridx()
    c.SetGridy()

    if (not os.path.exists(outDir)):
        os.mkdir(outDir)

    maximum = 150

    for ihisto in range(len(histos)):
        histos[ihisto].SetMarkerStyle(config.markers[ihisto])
        histos[ihisto].SetMarkerColor(config.colors[ihisto])
        histos[ihisto].SetMarkerSize(4)
        histos[ihisto].SetLineColor(config.colors[ihisto])
        histos[ihisto].SetLineWidth(5)
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

    leg = doLegend(histos, legends, 4)
    if (leg is not None):
        leg.Draw()
    c.SaveAs(outDir + "MultiEventVtx_z" + config.args.oFext)

    c = r.TCanvas("c1", "c1", 2200, 2000)
    c.SetGridx()
    c.SetGridy()

    for ihisto in range(len(histos_top)):
        histos_top[ihisto].SetMarkerStyle(config.markers[ihisto])
        histos_top[ihisto].SetMarkerColor(config.colors[ihisto])
        histos_top[ihisto].SetMarkerSize(4)
        histos_top[ihisto].SetLineColor(config.colors[ihisto])
        histos_top[ihisto].SetLineStyle(2)
        histos_top[ihisto].SetLineWidth(5)
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
        histos_bot[ihisto].SetMarkerStyle(config.markers[ihisto])
        histos_bot[ihisto].SetMarkerColor(config.colors[ihisto])
        histos_bot[ihisto].SetMarkerSize(4)
        histos_bot[ihisto].SetLineColor(config.colors[ihisto])
        histos_bot[ihisto].SetLineWidth(5)
        histos_bot[ihisto].Rebin(1)
        histos_bot[ihisto].Draw("P SAME")

    leg = doLegend(histos, legends, 4)
    if (leg is not None):
        leg.Draw()
    c.SaveAs(outDir + "MultiEventVtx_z_tb" + config.args.oFext)

    print("--- multi vtx for top/bottom X-Y ---")

    histos2d_top = []
    names = [leg+"_x_y_top" for leg in legends]
    for iF in inputF:
        histos2d_top.append(iF.Get(f_path + "/vtx_x_y_top"))
        # names.append("MultiEventVtx_x_y_top" + iF.GetName().strip(".root"))

    utils.Make2DPlots(names, outDir, histos2d_top, legends=legends, xtitle="MultiEvt Vtx V_{x} [mm]", ytitle="MultiEvt Vtx V_{y} [mm]", colors2d=config.colors)

    histos2d_bot = []
    names = [leg+"_x_y_bot" for leg in legends]
    for iF in inputF:
        histos2d_bot.append(iF.Get(f_path + "/vtx_x_y_bottom"))
    utils.Make2DPlots(names, outDir, histos2d_bot, legends=legends, xtitle="Multi Vtx FEE V_{x} [mm]", ytitle="Multi Vtx FEE V_{y} [mm]", colors2d=config.colors)

    histos2d = []
    names = [leg+"_x_y_top_bot" for leg in legends]
    for iF in inputF:
        histos1 = iF.Get(f_path + "/vtx_x_y_top")
        histos2 = iF.Get(f_path + "/vtx_x_y_bottom")
        histos1.Add(histos2)
        histos2d.append(histos1)

    utils.Make2DPlots(names, outDir, histos2d, legends=legends, xtitle="MultiEvt Vtx V_{x} [mm]", ytitle="MultiEvt Vtx V_{y} [mm]", colors2d=config.colors)

    histos2d = []
    names = [leg+"_x_y_combined" for leg in legends]
    for iF in inputF:
        histo = iF.Get(f_path + "/vtx_x_y")
        histos2d.append(histo)
    utils.Make2DPlots(names, outDir, histos2d, legends=legends, xtitle="MultiEvt Vtx V_{x} [mm]", ytitle="MultiEvt Vtx V_{y} [mm]", colors2d=config.colors)


def doDerPlots(inputF, name, legends=[]):
    outDir = "./derivatives"

    if (not os.path.exists(outDir)):
        os.mkdir(outDir)

    histos = []

    for iF in inputF:
        histos.append(iF.Get("gbl_derivatives/"+name))

    c = r.TCanvas("c1", "c1", 2200, 2000)
    c.SetGridx()
    c.SetGridy()

    titleName = name
    maximum = -1.

    for histo in histos:
        if abs(histo.Integral()) > 1e-8:
            histo.Scale(1./histo.Integral())

        # Get the maximum
        if (histo.GetMaximum() > maximum):
            maximum = histo.GetMaximum()

    for ihisto in range(len(histos)):
        histos[ihisto].SetMarkerStyle(config.markers[ihisto])
        histos[ihisto].SetMarkerColor(config.colors[ihisto])
        histos[ihisto].SetMarkerSize(4)
        histos[ihisto].SetLineColor(config.colors[ihisto])
        histos[ihisto].GetXaxis().SetLabelSize(0.05)
        histos[ihisto].GetYaxis().SetLabelSize(0.05)
        histos[ihisto].SetLineWidth(5)

        if (ihisto == 0):
            histos[ihisto].GetXaxis().SetTitle(titleName + " global derivative")
            histos[ihisto].GetXaxis().SetTitleSize(0.05)
            histos[ihisto].GetXaxis().SetTitleOffset(0.9)
            histos[ihisto].SetMaximum(maximum*1.5)
            histos[ihisto].Draw("P")

            if "223" in name or "123" in name:
                if int(name[-2:]) < 4:
                    histos[ihisto].GetXaxis().SetRangeUser(-25, 25)
                else:
                    histos[ihisto].GetXaxis().SetRangeUser(-100, 100)
            else:
                histos[ihisto].GetXaxis().SetRangeUser(-5, 5)
        else:
            histos[ihisto].Draw("P SAME")

    leg = doLegend(histos, legends, 3)

    if (leg is not None):
        leg.Draw()

    c.SaveAs(outDir + "/" + name + config.args.oFext)


def z0VsTanLambdaFitPlot(inputF, name, legends=[], outFolder="./"):

    histos = []
    # grab the histos
    for iF in inputF:
        histos.append(iF.Get("trk_params/"+name))

    print("Histograms to fit:", len(histos))
    c = r.TCanvas("c1", "c1", 2200, 2000)
    c.SetGridx()
    c.SetGridy()

    fitList = []
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

        histos_mu[ihisto].Fit("fit"+str(ihisto), "QNR")
        fit_par0 = fitF.GetParameter(0)
        fit_par1 = fitF.GetParameter(1)
        plotProperties.append((" z_tgt=%.3f" % round(fit_par1, 3)))

        histos_mu[ihisto].SetMarkerStyle(config.markers[ihisto])
        histos_mu[ihisto].SetMarkerColor(config.colors[ihisto])
        histos_mu[ihisto].SetMarkerSize(4)
        histos_mu[ihisto].SetLineColor(config.colors[ihisto])
        histos_mu[ihisto].GetXaxis().SetLabelSize(0.05)
        histos_mu[ihisto].GetYaxis().SetLabelSize(0.05)
        histos_mu[ihisto].SetLineWidth(5)
        histos_mu[ihisto].GetYaxis().SetTitle("<z0> [mm]")
        histos_mu[ihisto].GetXaxis().SetTitle("tan(#lambda)")
        histos_mu[ihisto].GetYaxis().SetTitleSize(histos[ihisto].GetYaxis().GetTitleSize()*0.7)
        histos_mu[ihisto].GetYaxis().SetTitleOffset(histos[ihisto].GetYaxis().GetTitleOffset()*1.35)

        histos_mu[ihisto].GetYaxis().SetRangeUser(-2, 2)
        histos_mu[ihisto].GetXaxis().SetRangeUser(-2, 2)

        if (ihisto == 0):
            print("Drawing")
            histos_mu[ihisto].Draw("P")
        else:
            print("Drawing same")
            histos_mu[ihisto].Draw("P SAME")

        fitF.SetLineColor(config.colors[ihisto])
        fitF.DrawClone("SAME")

    leg = doLegend(histos_mu, legends, 2, plotProperties)
    if (leg is not None):
        leg.Draw()

    c.SaveAs(outFolder + "/" + name + config.args.oFext)
