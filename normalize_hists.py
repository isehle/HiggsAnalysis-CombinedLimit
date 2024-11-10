import ROOT

def scale_hists(path, i):
    fstates = ["fs_4e", "fs_4mu", "fs_2e2mu"]

    pol_hists = ["ZLZL", "ZLZT", "ZTZT"]
    hists = pol_hists + ["ZZ_LO", "ZZ_NLO", "ZpX", "H", "VVV"]

    hists += [proc+"_pdfUp" for proc in hists] + [proc_"pdfDown" for proc in hists]

    with ROOT.TFile.Open(path) as infile:    
        new_hists = {}
        for fs in fstates:
            new_hists[fs] = {}

            zz_lo  = infile.Get(fs+"/ZZ_LO").Integral()
            zz_nlo = infile.Get(fs+"/ZZ_NLO").Integral()

            if i==0:
                print(f"ZZ_LO_{fs}: {zz_lo}")
                print(f"ZZ_NLO_{fs}: {zz_nlo}")
                print("=="*15)

            zxzt = infile.Get(fs+"/ZLZT").Clone("ZXZT")
            ztzt = infile.Get(fs+"/ZTZT").Clone()
            zxzt.Add(ztzt)
            zxzt.SetDirectory(0)
            zxzt_norm = zxzt.Integral()
            zxzt.Scale(1/zxzt_norm)

            new_hists[fs]["ZXZT"] = zxzt

            for hist in hists:
                new_hist = infile.Get(fs+"/"+hist).Clone()
                new_hist.SetDirectory(0)
                if hist in pol_hists + ["ZZ_LO"]:
                    norm = new_hist.Integral()
                    new_hist.Scale(1/norm)

                new_hists[fs][hist] = new_hist

    return new_hists

def write_tfile(path, new_hists):
    outpath = path.replace(".root", "_normedZZLO.root")
    with ROOT.TFile.Open(outpath, "recreate") as infile:
        for fs in new_hists.keys():
            infile.mkdir(fs)
            infile.cd(fs)
            for hist in new_hists[fs].values():
                hist.Write()
            infile.cd("../")

if __name__=="__main__":
    ct1_path = "data/zzPolFractions/all_cosTheta1_hists_v2.root"
    ct3_path = "data/zzPolFractions/cosTheta3/all_cosTheta3_hists_filledZeros.root"
    cts_path = "data/zzPolFractions/cosThetaStar/all_cosThetaStar_hists_filledZeros.root"

    for i, path in enumerate([ct1_path, ct3_path, cts_path]):
        new_hists = scale_hists(path, i)
        write_tfile(path, new_hists)