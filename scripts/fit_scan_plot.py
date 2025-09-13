import os
import sys

from postFitPlot import draw_plots

class CombinePlots:
    def __init__(self, args):
        self.args    = args

        # NLO EW x QCD values from Denner and Pelliccioli: https://inspirehep.net/literature/1884197
        self.model_info = dict(
            single = dict(
                model       = "HiggsAnalysis.CombinedLimit.PolZZModel:singlePolRateParams",
                init_params = "r=1,f_L=0.2408",
            ),
            diboson = dict(
                model       = "HiggsAnalysis.CombinedLimit.PolZZModel:diBosonRateParams",
                init_params = "r=1,f_LL=0.058",
            ),
        )

        self.datacard = args["datacard"]
        self.model    = args["model"]
        self.points   = args["points"]
        self.poi      = args["poi"]
        self.mode     = args["mode"]
        self.asimov   = not args["data"]
        self.write_ws = args["write_ws"]
        self.floatOtherPOIs = args["floatOtherPOIs"]

        self.scan_label = " --logo-sub"
        if args["year"] == 2022:
            self.scan_label += r" 'Private Work, 35 fb^{-1}'"
        elif args["year"] == 2023:
            self.scan_label += r" 'Private Work, 27 fb^{-1}'"
        else:
            self.scan_label += r" 'Private Work, 62 fb^{-1}'"

        self.ws_file = self.datacard.replace("txt", "root")

        # Params from LO MG w/ noTau
        #self.init_params = "r=1,f_LL=0.0601" if self.poi == "f_LL" else "r=1,f_L=0.2452"
        #self.init_params = "r=1,f_LL=0.0601" if ("diBoson" in self.model) else "r=1,f_L=0.2452"

        self.init_params = self.model_info[self.model]["init_params"]

        self.freeze = ""
        if not self.floatOtherPOIs:
            if self.model == "single":
                self.freeze = " --freezeParameters r" if self.poi == "f_L" else " --freezeParameters f_L"

            elif self.model == "diboson":
                self.freeze = " --freezeParameters r" if self.poi == "f_LL" else " --freezeParameters f_LL"
        
        direc, _  = os.path.split(args["datacard"])
        self.observable = direc.split("/")[-1]
        
        tag       = "asimov" if self.asimov else "data"
        self.name = "{}_{}_{}_{}_{}".format(self.observable, tag, args["poi"], args["name"], self.model)

        self.asimov_file = f"higgsCombine.{self.name}.GenerateOnly.mH120.123456.root"

        #self.fstates = ["fs_4e", "fs_4mu", "fs_2e2mu"]
        self.fstates = ["fs_4e", "fs_4mu", "fs_2e2mu", "fs_2mu2e"]

        self.files   = FileHandler()

    def _track_params(self):
        params = dict(
            r                            = True,
            f_L                          = True,
            LHEPdfWeight                 = False,
            LHEScaleWeight               = True,
            trig_2e2mu                   = False,
            trig_4e                      = False,
            trig_4mu                     = False,
            lepIDRec                     = False,
            kfactor_ggzz                 = False,
            kfactor_qqzz                 = False,
            lumi                         = False,
            puWeight                     = False,
            rateScale_2022_Full_fs_2x2mu = False,
            rateScale_2022_Full_fs_2x2e  = False,
            rateScale_2023_Full_fs_2x2mu = False,
            rateScale_2023_Full_fs_2x2e  = False,
        )
        if self.model == "single":
            params["f_L"] = True
        else:
            params["f_LL"] = True
        if True in params.values():
            tracked_params = [param for param, val in params.items() if val]
            return " --trackParameters " + ",".join(tracked_params)
        else:
            return ""
            
    def write_workspace(self):
        #comm = f"text2workspace.py {self.datacard} -P {self.model} --channel-masks"
        #comm = f"text2workspace.py {self.datacard} -P {self.model_info[self.model]["model"]}"
        comm = "text2workspace.py {} -P {}".format(self.datacard, self.model_info[self.model]["model"])
        os.system(comm)

    def gen_asimov(self):
        comm = f"combine -M GenerateOnly {self.ws_file} -n .{self.name} --setParameters {self.init_params},mask_SR_fs_4e=1,mask_SR_fs_4mu=1,mask_SR_fs_2e2mu=1,mask_SR_fs_2mu2e=1 --saveToys --toysFrequentist" + self._track_params()
        os.system(comm)

    def scan(self):
        tracked_params = self._track_params()

        fitfile = "higgsCombine.{}.MultiDimFit.mH120.root".format(self.name)

        #init_fit_comm   = "combine -M MultiDimFit {} --setParameters {} -n .{} -P {} --saveWorkspace{} --saveFitResult --cminDefaultMinimizerStrategy 0 --robustHesse 1{}".format(self.ws_file, self.init_params, self.name, self.poi, tracked_params, self.freeze)
        #total_scan_comm = "combine -M MultiDimFit {} -n .{}Total --algo=grid --points=500 --setParameters {} --X-rtd FAST_VERTICAL_MORPH -P {} --snapshotName MultiDimFit{} --saveFitResult --cminDefaultMinimizerStrategy 0 --robustHesse 1".format(fitfile, self.name, self.init_params, self.poi, tracked_params)
        #no_mcStat_comm  = "combine -M MultiDimFit {} -n .{}FreezeSystNotMCStat --setParameters {}  --X-rtd FAST_VERTICAL_MORPH --algo=grid --points=500 -P {} --snapshotName MultiDimFit --freezeNuisanceGroups syst_no_mcStat --X-rtd MINIMIZER_no_analytic{} --saveFitResult --cminDefaultMinimizerStrategy 0 --robustHesse 1".format(fitfile, self.name, self.init_params, self.poi, tracked_params)
        #no_syst_comm    = "combine -M MultiDimFit {} -n .{}DataStatOnly --setParameters {}  --X-rtd FAST_VERTICAL_MORPH --algo=grid --points=500 -P {} --snapshotName MultiDimFit --freezeParameters allConstrainedNuisances{} --saveFitResult --cminDefaultMinimizerStrategy 0 --robustHesse 1".format(fitfile, self.name, self.init_params, self.poi, tracked_params)

        init_fit_comm   = "combine -M MultiDimFit {} --setParameters {} -n .{} -P {} --saveWorkspace{} --saveFitResult --cminDefaultMinimizerStrategy 0 --robustHesse 1 {}".format(self.ws_file, self.init_params, self.name, self.poi, tracked_params, self.freeze)
        total_scan_comm = "combine -M MultiDimFit {} -n .{}Total --algo=grid --points=500 --setParameters {} -P {} --snapshotName MultiDimFit{} --saveFitResult --cminDefaultMinimizerStrategy 0 --robustHesse 1".format(fitfile, self.name, self.init_params, self.poi, tracked_params)
        no_mcStat_comm  = "combine -M MultiDimFit {} -n .{}FreezeSystNotMCStat --setParameters {} --algo=grid --points=500 -P {} --snapshotName MultiDimFit --freezeNuisanceGroups syst_no_mcStat --X-rtd MINIMIZER_no_analytic{} --saveFitResult --cminDefaultMinimizerStrategy 0 --robustHesse 1".format(fitfile, self.name, self.init_params, self.poi, tracked_params)
        no_syst_comm    = "combine -M MultiDimFit {} -n .{}DataStatOnly --setParameters {} --algo=grid --points=500 -P {} --snapshotName MultiDimFit --freezeParameters allConstrainedNuisances{} --saveFitResult --cminDefaultMinimizerStrategy 0 --robustHesse 1".format(fitfile, self.name, self.init_params, self.poi, tracked_params)

        plot_comm       = 'python3 scripts/plot1DScan.py higgsCombine.{}Total.MultiDimFit.mH120.root --main-label "Total Uncert." --others higgsCombine.{}FreezeSystNotMCStat.MultiDimFit.mH120.root:"Data+MCStat Only":2 higgsCombine.{}DataStatOnly.MultiDimFit.mH120.root:"Data Stat Only":3 -o {}_fullBreakdown --breakdown OtherSyst,MCStat,DataStat --POI {} --translate poi_labels.json {}'.format(self.name, self.name, self.name, self.name, self.poi, self.scan_label)

        for comm in [init_fit_comm, total_scan_comm, no_mcStat_comm, no_syst_comm]:
            if self.asimov: comm += " -t -1"
            
            if self.floatOtherPOIs:
                comm += " --floatOtherPOIs=1 --saveInactivePOI=1"
            
            comm += " --robustFit 1 --toysNoSystematics"

            os.system(comm)

        os.system(plot_comm)
        
        #self.files.move_files(mode="scans", sub_dir = self.observable)

    def impacts(self):
        #init_fit    = "combineTool.py -M Impacts -d {} -m 120 --robustFit 1 --doInitialFit --X-rtd FAST_VERTICAL_MORPH --setParameters {} --cminDefaultMinimizerStrategy 0 --robustHesse 1 --toysNoSystematics".format(self.ws_file, self.init_params)
        #do_fits     = "combineTool.py -M Impacts -d {} -m 120 --robustFit 1 --doFits --X-rtd FAST_VERTICAL_MORPH --setParameters {} --parallel 20 --cminDefaultMinimizerStrategy 0 --robustHesse 1 --toysNoSystematics --saveSpecifiedNuis=all".format(self.ws_file, self.init_params)

        #write_json  = "combineTool.py -M Impacts -d {} -m 120 --output {}_impacts.json".format(self.ws_file, self.name)

        #init_fit    = "combineTool.py -M Impacts -d {} -m 120 --robustFit 1 --doInitialFit --X-rtd FAST_VERTICAL_MORPH --setParameters {} --cminDefaultMinimizerStrategy 0 --toysNoSystematics --robustHesse 1".format(self.ws_file, self.init_params)
        #do_fits     = "combineTool.py -M Impacts -d {} -m 120 --robustFit 1 --doFits --X-rtd FAST_VERTICAL_MORPH --setParameters {} --parallel 20 --cminDefaultMinimizerStrategy 0 --toysNoSystematics --saveSpecifiedNuis=all --robustHesse 1".format(self.ws_file, self.init_params)

        init_fit    = "combineTool.py -M Impacts -d {} -m 120 --robustFit 1 --doInitialFit --setParameters {} --cminDefaultMinimizerStrategy 0 --toysNoSystematics --robustHesse 1".format(self.ws_file, self.init_params)
        do_fits     = "combineTool.py -M Impacts -d {} -m 120 --robustFit 1 --doFits --setParameters {} --parallel 20 --cminDefaultMinimizerStrategy 0 --toysNoSystematics --saveSpecifiedNuis=all --robustHesse 1".format(self.ws_file, self.init_params)

        write_json  = "combineTool.py -M Impacts -d {} -m 120 --output {}_impacts.json".format(self.ws_file, self.name)

        plot_impact = "plotImpacts.py -i {}_impacts.json -o {}_impacts --POI {} --summary".format(self.name, self.name, self.poi)

        for comm in [init_fit, do_fits, write_json]:
            if self.asimov: comm += " -t -1"
            #if self.asimov: comm += " -t 100"
            os.system(comm)

        os.system(write_json)
        os.system(plot_impact)

        #self.files.move_files(mode="impacts", sub_dir = self.poi)

    def postfit_shapes(self):
        asimov_set = "combine -M GenerateOnly {} -t -1 --setParameters {} --saveToys".format(self.ws_file, self.init_params)
        merge      = "combineTool.py -M ModifyDataSet {}:w {}_asimov.root:w:data_asimov -d higgsCombineTest.GenerateOnly.mH120.123456.root:toys/toy_asimov".format(self.ws_file, self.ws_file) # DATACARD NAME IS WRONG NO WONDER WE GET BULLSHIT
        fit        = "combine -M MultiDimFit {}_asimov.root -D data_asimov --saveFitResult".format(self.ws_file)
        hists      = "PostFitShapesFromWorkspace -w {}_asimov.root --dataset data_asimov --output {}_shapes{}.root -m 120 --postfit --sampling -f multidimfitTest.root:fit_mdf".format(self.ws_file, self.observable, self.args["name"])

        for comm in [asimov_set, merge, fit, hists]:
            os.system(comm)

        shape_file = "{}_shapes{}.root".format(self.observable, self.args["name"])
        for fit in ["prefit", "postfit"]:
            for fs in self.fstates:
                fs_dir = fs+"_"+fit
                draw_plots(shape_file, fs_dir, self.args["name"])

    def postfit_shapes(self):
        asimov_set = "combine -M GenerateOnly higgsCombine.cosTheta1_asimov_f_L_fullModel_nZpXCRFit_Testing.MultiDimFit.mH120.root --snapshotName MultiDimFit --saveToys --saveWorkspace"
        
    def main(self):
        if self.write_ws:
            self.write_workspace()
        elif not self.write_ws and not os.path.exists(self.ws_file):
            print(f"Workspace {self.ws_file} does not exist: writing... ")
            self.write_workspace()
        
        self.gen_asimov()
        if self.mode == "scan":
            self.scan()
        elif self.mode == "impacts":
            self.impacts()
        elif self.mode == "postfit_shapes":
            self.postfit_shapes()
        elif self.mode == "all":
            self.scan()
            self.impacts()
            #self.postfit_shapes()

class FileHandler:
    def __init__(self):
        self.dir = os.getcwd()

        self.root_files = self._files_by_type("root")
        self.json_files = self._files_by_type("json")
        self.pdf_files  = self._files_by_type("pdf")
        self.png_files  = self._files_by_type("png")

        self.eos_dir = "/eos/user/i/iehle/"
        self.plots_out_base = os.path.join(self.eos_dir, "php-plots/PolZZTo4l/")

        self.year = "2022"
        self.era  = "EFG"
        self.root_out_base = os.path.join(self.eos_dir, "Analysis/rootFiles", self.year, self.era, "combine")

    def _files_by_type(self, ftype):
        files = os.listdir()
        files_by_type = lambda ftype: [os.path.join(self.dir, file) for file in files if file.endswith(f".{ftype}")]

        return files_by_type(ftype)

    def _get_outdir(self, mode, sub_dir):
        """<sub_dir> depends on whether you're getting the outdir for scans,
        where it should correspond to obversables i.e. cosTheta1,3 etc, or
        for impacts, where it should correspond to which poi you're considering,
        i.e. f_L, r, f_LL etc."""
        return dict(
            root = self.root_out_base,
            pdf  = os.path.join(self.plots_out_base, mode, sub_dir),
            png  = os.path.join(self.plots_out_base, mode, sub_dir)
        )

    def get_new(self, ftype):
        old = self.__dict__[f"{ftype}_files"]
        new = self._files_by_type(ftype)
        return list(set(new) - set(old))

    def move_files(self, mode, sub_dir):
        outdirs = self._get_outdir(mode, sub_dir)
        for ftype, outdir in outdirs.items():
            for new_file in self.get_new(ftype):
                comm = "mv {} {}".format(new_file, outdir)
                os.system(comm)

if __name__=="__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(description="arguments")
    parser.add_argument("--datacard", default="data/zzPolFractions/ggBkg/cosTheta1/datacard_ZpXFromCR_wKFactors_wAsimov_channelMasking_v2.txt"),
    parser.add_argument("--model", choices = ("single", "diboson"), default="single"),
    parser.add_argument("--points", default=500)
    parser.add_argument("--poi", choices = ("f_LL", "f_L", "r", "both"), default="f_L")
    parser.add_argument("--name", default="")
    parser.add_argument("--mode", choices=("scan", "impacts", "postfit_shapes", "all"), default="all")
    parser.add_argument("--year", choices=(2022, 2023, -1), default=-1, type=int)
    parser.add_argument("--data", action='store_true')
    parser.add_argument("--floatOtherPOIs", action="store_true")
    parser.add_argument("--write_ws", action="store_true")
    args = vars(parser.parse_args())

    combinePlots = CombinePlots(args)
    combinePlots.main()



