from __future__ import absolute_import

import HiggsAnalysis.CombinedLimit.util.plotting as plot
import ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

plot.ModTDRStyle()

def draw_plots(shape_file, fs_dir, name=""):
    titles = {
    f"cosTheta1_shapes{name}.root": "cos(#theta_{1})",
    f"cosTheta3_shapes{name}.root": "cos(#theta_{3})",
    f"cosThetaStar_shapes{name}.root": "cos(#theta *)"
    }

    canvas = ROOT.TCanvas()

    fin = ROOT.TFile(shape_file)

    h_bkg = fin.Get(fs_dir + "/TotalBkg")
    h_sig = fin.Get(fs_dir + "/TotalSig")
    h_dat = fin.Get(fs_dir + "/data_obs")  # This is a TGraphAsymmErrors, not a TH1F

    #h_xt  = fin.Get(fs_dir + "/ZXZT_qq")
    h_lt  = fin.Get(fs_dir + "/ZLZT_qq")
    h_tt  = fin.Get(fs_dir + "/ZTZT_qq")

    h_xt  = h_lt.Clone("ZXZT")
    h_xt.Add(h_tt)

    h_bkg.SetFillColor(ROOT.TColor.GetColor(100, 192, 232))
    h_bkg.Draw("HIST")

    h_err = h_bkg.Clone()
    h_err.SetFillColorAlpha(12, 0.3)  # Set grey colour (12) and alpha (0.3)
    h_err.SetMarkerSize(0)
    h_err.Draw("E2SAME")

    h_sig.SetLineColor(ROOT.kRed)
    h_sig.Draw("HISTSAME")

    h_xt.SetLineColor(ROOT.kGreen)
    h_xt.Draw("HISTSAME")

    h_dat.Draw("PSAME")

    h_bkg.SetMinimum(0.)
    h_bkg.SetMaximum(h_bkg.GetMaximum() * 1.4)

    title = titles[shape_file]
    h_bkg.GetXaxis().SetTitle(title)
    h_bkg.GetYaxis().SetTitle("Events")

    legend = ROOT.TLegend(0.60, 0.70, 0.90, 0.91, "", "NBNDC")
    legend.AddEntry(h_bkg, "XT + Other Bkg", "F")
    legend.AddEntry(h_sig, "LL", "L")
    legend.AddEntry(h_xt, "XT", "L")
    legend.AddEntry(h_err, "Background uncertainty", "F")
    legend.Draw()

    outfile = "{}_{}{}_LLandXT.png".format(shape_file.replace("_shapes.root", ""), fs_dir.replace("fs_", ""), name)

    canvas.SaveAs(outfile)

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(description="")
    parser.add_argument("--shape_file")
    parser.add_argument("--fs_dir", choices=("fs_4e_prefit", "fs_4mu_prefit", "fs_2e2mu_prefit", "fs_4e_postfit", "fs_4mu_postfit", "fs_2e2mu_postfit"))
    args = vars(parser.parse_args())

    draw_plots(args["shape_file"], args["fs_dir"])
