import os
import sys

from postFitPlot import draw_plots

class CombinePlots:
    def __init__(self, args):
        self.args    = args
        self.ws_path = args["workspace"]
        self.points  = args["points"]
        self.poi     = args["poi"]
        self.mode    = args["mode"]
        
        direc, ws_file  = os.path.split(args["workspace"])
        self.observable = direc.split("/")[-1]
        self.name       = "{}_asimov_{}_ZXZT{}".format(self.observable, args["poi"], args["name"])

        self.fstates = ["fs_4e", "fs_4mu", "fs_2e2mu"]

    def scan(self):
        fitfile = "higgsCombine.{}.MultiDimFit.mH120.root".format(self.name)

        scan_comm = "combineTool.py -M MultiDimFit {} -t -1 --setParameters r=1,f_LL=0.0579 --X-rtd FAST_VERTICAL_MORPH --algo=grid --points={} -P {} -n .{}".format(self.ws_path, self.points, self.poi, self.name)
        #scan_comm = "combineTool.py -M MultiDimFit {} -t -1 --setParameters r=1,f_L=0.2406 --X-rtd FAST_VERTICAL_MORPH --algo=grid --points={} -P {} -n .{}".format(self.ws_path, self.points, self.poi, self.name)
        plot_comm = "python3 scripts/plot1DScan.py {} -o {} --POI {}".format(fitfile, self.name, self.poi)

        for comm in [scan_comm, plot_comm]:
            os.system(comm)

    def impacts(self):
        init_fit    = "combineTool.py -M Impacts -d {} -m 120 -t -1 --robustFit 1 --doInitialFit --X-rtd FAST_VERTICAL_MORPH --setParameters r=1,f_LL=0.0579".format(self.ws_path)
        do_fits     = "combineTool.py -M Impacts -d {} -m 120 -t -1 --robustFit 1 --doFits --X-rtd FAST_VERTICAL_MORPH --setParameters r=1,f_LL=0.0579".format(self.ws_path)
        #init_fit    = "combineTool.py -M Impacts -d {} -m 120 -t -1 --robustFit 1 --doInitialFit --X-rtd FAST_VERTICAL_MORPH --setParameters r=1,f_L=0.2406".format(self.ws_path)
        #do_fits     = "combineTool.py -M Impacts -d {} -m 120 -t -1 --robustFit 1 --doFits --X-rtd FAST_VERTICAL_MORPH --setParameters r=1,f_L=0.2406".format(self.ws_path)
        write_json  = "combineTool.py -M Impacts -d {} -m 120 --output {}_impacts{}.json".format(self.ws_path, self.observable, self.args["name"])
        plot_impact = "plotImpacts.py -i {}_impacts{}.json -o {}_impacts{} --POI {}".format(self.observable, self.args["name"], self.observable, self.args["name"], self.poi)

        for comm in [init_fit, do_fits, write_json, plot_impact]:
            os.system(comm)
    
    def postfit_shapes(self):
        asimov_set = "combine -M GenerateOnly {} -t -1 --setParameters r=1,f_LL=0.0579 --saveToys".format(self.ws_path)
        #asimov_set = "combine -M GenerateOnly {} -t -1 --setParameters r=1,f_L=0.2406 --saveToys".format(self.ws_path)
        merge      = "combineTool.py -M ModifyDataSet {}:w {}_asimov.root:w:data_asimov -d higgsCombineTest.GenerateOnly.mH120.123456.root:toys/toy_asimov".format(self.ws_path, self.ws_path)
        fit        = "combine -M MultiDimFit {}_asimov.root -D data_asimov --saveFitResult".format(self.ws_path)
        hists      = "PostFitShapesFromWorkspace -w {}_asimov.root --dataset data_asimov --output {}_shapes{}.root -m 120 --postfit --sampling -f multidimfitTest.root:fit_mdf".format(self.ws_path, self.observable, self.args["name"])

        for comm in [asimov_set, merge, fit, hists]:
            os.system(comm)

        shape_file = "{}_shapes{}.root".format(self.observable, self.args["name"])
        for fit in ["prefit", "postfit"]:
            for fs in self.fstates:
                fs_dir = fs+"_"+fit
                draw_plots(shape_file, fs_dir, self.args["name"])

    def main(self):
        if self.mode == "scan":
            self.scan()
        elif self.mode == "impacts":
            self.impacts()
        elif self.mode == "postfit_shapes":
            self.postfit_shapes()
        elif self.mode == "all":
            self.scan()
            self.impacts()
            self.postfit_shapes()

if __name__=="__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(description="arguments")
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--points", default=500)
    parser.add_argument("--poi", default="f_LL")
    parser.add_argument("--name", default="")
    parser.add_argument("--mode", choices=("scan", "impacts", "postfit_shapes", "all"), default="all")
    args = vars(parser.parse_args())

    combinePlots = CombinePlots(args)
    combinePlots.main()



