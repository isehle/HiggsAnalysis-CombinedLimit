import ROOT

def copy_hists(path):
    fstates = ["fs_4e", "fs_4mu", "fs_2e2mu"]

    pol_hists = ["ZLZL", "ZXZT"]
    hists = pol_hists + ["ZZ_LO", "ZZ_NLO", "ggZZ", "ZpX", "H", "VVV"]

    with ROOT.TFile.Open(path) as infile:    
        new_hists = {}
        for fs in fstates:
            new_hists[fs] = {}

            for hist in hists:
                if hist in pol_hists :
                    new_hist_qq = infile.Get(fs+"/"+hist).Clone(hist+"_qq")
                    new_hist_gg = infile.Get(fs+"/"+hist).Clone(hist+"_gg")
                    new_hist_qq.SetDirectory(0)
                    new_hist_gg.SetDirectory(0)
                    new_hists[fs][hist+"_qq"] = new_hist_qq
                    new_hists[fs][hist+"_gg"] = new_hist_gg
                else:
                    new_hist = infile.Get(fs+"/"+hist).Clone()
                    new_hist.SetDirectory(0)
                    new_hists[fs][hist] = new_hist

    return new_hists

def write_tfile(path, new_hists):
    outpath = path.replace("v2.root", "_normed.root")
    with ROOT.TFile.Open(outpath, "recreate") as infile:
        for fs in new_hists.keys():
            infile.mkdir(fs)
            infile.cd(fs)
            for hist in new_hists[fs].values():
                hist.Write()
            infile.cd("../")

if __name__=="__main__":
    #ct1_path = "data/zzPolFractions/cosTheta1/all_cosTheta1_hists_ggZZBkg_v2.root"
    ct3_path = "data/zzPolFractions/cosTheta3/all_cosTheta3_hists_ggZZBkg_v2.root"
    cts_path = "data/zzPolFractions/cosThetaStar/all_cosThetaStar_hists_ggZZBkg_v2.root"

    ct1_path = "/afs/cern.ch/user/i/iehle/polZZTo4l_New/CMSSW_13_0_16/src/ZZAnalysis/all_cosThetaStar_hists_qqAndggPols_v2.root"

    for i, path in enumerate([ct1_path, ct3_path, cts_path]):
        new_hists = copy_hists(path)
        write_tfile(path, new_hists)