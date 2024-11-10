from HiggsAnalysis.CombinedLimit.PhysicsModel import PhysicsModel
    
class PolZZModel(PhysicsModel):

    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""
        #self.modelBuilder.doVar("N_ZZ_4e[72.31]") # LO qqZZ yields
        #self.modelBuilder.doVar("N_ZZ_4mu[123.45]")
        #self.modelBuilder.doVar("N_ZZ_2e2mu[191.92]")
        self.modelBuilder.doVar("N_ZZ_4e[102.64]") # NLO qqZZ+ggZZ yields
        self.modelBuilder.doVar("N_ZZ_4mu[169.55]")
        self.modelBuilder.doVar("N_ZZ_2e2mu[255.67]")
        self.modelBuilder.doVar("f_LL[0.0579, 0, 0.4]")
        self.modelBuilder.doVar("r[1,-5,5]")
        self.modelBuilder.factory_('expr::f_LL_4e("@0*@1*@2", r, f_LL, N_ZZ_4e)')
        self.modelBuilder.factory_('expr::f_LL_4mu("@0*@1*@2", r, f_LL, N_ZZ_4mu)')
        self.modelBuilder.factory_('expr::f_LL_2e2mu("@0*@1*@2", r, f_LL, N_ZZ_2e2mu)')
        self.modelBuilder.factory_('expr::f_XT_4e("@0*(1-@1)*@2", r, f_LL, N_ZZ_4e)')
        self.modelBuilder.factory_('expr::f_XT_4mu("@0*(1-@1)*@2", r, f_LL, N_ZZ_4mu)')
        self.modelBuilder.factory_('expr::f_XT_2e2mu("@0*(1-@1)*@2", r, f_LL, N_ZZ_2e2mu)')
        self.modelBuilder.doSet("POI", ",".join(["r", "f_LL"]))

    def getYieldScale(self, bin, process):
        "Return the name of a RooAbsReal to scale this yield by or the two special values 1 and 0 (don't scale, and set to zero)"
        if self.DC.isSignal[process]:
            print("Scaling %s/%s by r*f_LL*N_%s" % (bin, process, bin))
            if bin=="fs_4e":
                return "f_LL_4e"
            elif bin == "fs_4mu":
                return "f_LL_4mu"
            elif bin == "fs_2e2mu":
                return "f_LL_2e2mu"
            else:
                raise Exception("Bin options are fs_4e, fs_4mu, fs_2e2mu")
        elif process == "ZXZT":
            print("Scaling %s/%s by r*(1-f_LL)*N_%s" % (bin, process, bin))
            if bin=="fs_4e":
                return "f_XT_4e"
            elif bin == "fs_4mu":
                return "f_XT_4mu"
            elif bin == "fs_2e2mu":
                return "f_XT_2e2mu"
            else:
                raise Exception("Bin options are fs_4e, fs_4mu, fs_2e2mu")
        return 1

class PolZZSepQQModel(PhysicsModel):

    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""
        self.modelBuilder.doVar("N_ZZ_4e_qq[97.39]")
        self.modelBuilder.doVar("N_ZZ_4mu_qq[160.91]")
        self.modelBuilder.doVar("N_ZZ_2e2mu_qq[248.32]")
        self.modelBuilder.doVar("N_ZZ_4e_gg[5.25]")
        self.modelBuilder.doVar("N_ZZ_4mu_gg[8.64]")
        self.modelBuilder.doVar("N_ZZ_2e2mu_gg[7.35]")
        self.modelBuilder.doVar("f_LL[0.0579, 0, 0.4]")
        self.modelBuilder.doVar("r[1,-5,5]")
        self.modelBuilder.factory_('expr::f_LL_4e_qq("@0*@1*@2", r, f_LL, N_ZZ_4e_qq)')
        self.modelBuilder.factory_('expr::f_LL_4mu_qq("@0*@1*@2", r, f_LL, N_ZZ_4mu_qq)')
        self.modelBuilder.factory_('expr::f_LL_2e2mu_qq("@0*@1*@2", r, f_LL, N_ZZ_2e2mu_qq)')
        self.modelBuilder.factory_('expr::f_XT_4e_qq("@0*(1-@1)*@2", r, f_LL, N_ZZ_4e_qq)')
        self.modelBuilder.factory_('expr::f_XT_4mu_qq("@0*(1-@1)*@2", r, f_LL, N_ZZ_4mu_qq)')
        self.modelBuilder.factory_('expr::f_XT_2e2mu_qq("@0*(1-@1)*@2", r, f_LL, N_ZZ_2e2mu_qq)')
        self.modelBuilder.factory_('expr::f_LL_4e_gg("@0*@1*@2", r, f_LL, N_ZZ_4e_gg)')
        self.modelBuilder.factory_('expr::f_LL_4mu_gg("@0*@1*@2", r, f_LL, N_ZZ_4mu_gg)')
        self.modelBuilder.factory_('expr::f_LL_2e2mu_gg("@0*@1*@2", r, f_LL, N_ZZ_2e2mu_gg)')
        self.modelBuilder.factory_('expr::f_XT_4e_gg("@0*(1-@1)*@2", r, f_LL, N_ZZ_4e_gg)')
        self.modelBuilder.factory_('expr::f_XT_4mu_gg("@0*(1-@1)*@2", r, f_LL, N_ZZ_4mu_gg)')
        self.modelBuilder.factory_('expr::f_XT_2e2mu_gg("@0*(1-@1)*@2", r, f_LL, N_ZZ_2e2mu_gg)')
        self.modelBuilder.doSet("POI", ",".join(["r", "f_LL"]))

    def getYieldScale(self, bin, process):
        "Return the name of a RooAbsReal to scale this yield by or the two special values 1 and 0 (don't scale, and set to zero)"
        if self.DC.isSignal[process]:
            print("Scaling %s/%s by r*f_LL*N_%s" % (bin, process, bin))
            if bin=="fs_4e":
                if "qq" in process:
                    return "f_LL_4e_qq"
                else:
                    return "f_LL_4e_gg"
            elif bin == "fs_4mu":
                if "qq" in process:
                    return "f_LL_4mu_qq"
                else:
                    return "f_LL_4mu_gg"
            elif bin == "fs_2e2mu":
                if "qq" in process:
                    return "f_LL_2e2mu_qq"
                else:
                    return "f_LL_2e2mu_gg"
            else:
                raise Exception("Bin options are fs_4e, fs_4mu, fs_2e2mu")
        elif "ZXZT" in process:
            print("Scaling %s/%s by r*(1-f_LL)*N_%s" % (bin, process, bin))
            if bin=="fs_4e":
                if "qq" in process:
                    return "f_XT_4e_qq"
                else:
                    return "f_XT_4e_gg"
            elif bin == "fs_4mu":
                if "qq" in process:
                    return "f_XT_4mu_qq"
                else:
                    return "f_XT_4mu_gg"
            elif bin == "fs_2e2mu":
                if "qq" in process:
                    return "f_XT_2e2mu_qq"
                else:
                    return "f_XT_2e2mu_gg"
            else:
                raise Exception("Bin options are fs_4e, fs_4mu, fs_2e2mu")
        return 1

class SinglePolModel(PhysicsModel):

    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""
        self.modelBuilder.doVar("N_ZZ_4e_qq[97.39]")
        self.modelBuilder.doVar("N_ZZ_4mu_qq[160.91]")
        self.modelBuilder.doVar("N_ZZ_2e2mu_qq[248.32]")
        self.modelBuilder.doVar("N_ZZ_4e_gg[5.25]")
        self.modelBuilder.doVar("N_ZZ_4mu_gg[8.64]")
        self.modelBuilder.doVar("N_ZZ_2e2mu_gg[7.35]")
        self.modelBuilder.doVar("f_L[0.2406, 0, 1]") # Single boson polarization!
        self.modelBuilder.doVar("r[1,-5,5]")
        self.modelBuilder.factory_('expr::f_LL_4e_qq("@0*@1*@1*@2", r, f_L, N_ZZ_4e_qq)')
        self.modelBuilder.factory_('expr::f_LL_4mu_qq("@0*@1*@1*@2", r, f_L, N_ZZ_4mu_qq)')
        self.modelBuilder.factory_('expr::f_LL_2e2mu_qq("@0*@1*@1*@2", r, f_L, N_ZZ_2e2mu_qq)')
        self.modelBuilder.factory_('expr::f_LL_4e_gg("@0*@1*@1*@2", r, f_L, N_ZZ_4e_gg)')
        self.modelBuilder.factory_('expr::f_LL_4mu_gg("@0*@1*@1*@2", r, f_L, N_ZZ_4mu_gg)')
        self.modelBuilder.factory_('expr::f_LL_2e2mu_gg("@0*@1*@1*@2", r, f_L, N_ZZ_2e2mu_gg)')
        self.modelBuilder.factory_('expr::f_LT_4e_qq("2*@0*@1*(1-@1)*@2", r, f_L, N_ZZ_4e_qq)')
        self.modelBuilder.factory_('expr::f_LT_4mu_qq("2*@0*@1*(1-@1)*@2", r, f_L, N_ZZ_4mu_qq)')
        self.modelBuilder.factory_('expr::f_LT_2e2mu_qq("2*@0*@1*(1-@1)*@2", r, f_L, N_ZZ_2e2mu_qq)')
        self.modelBuilder.factory_('expr::f_LT_4e_gg("2*@0*@1*(1-@1)*@2", r, f_L, N_ZZ_4e_gg)')
        self.modelBuilder.factory_('expr::f_LT_4mu_gg("2*@0*@1*(1-@1)*@2", r, f_L, N_ZZ_4mu_gg)')
        self.modelBuilder.factory_('expr::f_LT_2e2mu_gg("2*@0*@1*(1-@1)*@2", r, f_L, N_ZZ_2e2mu_gg)')
        self.modelBuilder.factory_('expr::f_TT_4e_qq("@0*(1-@1)*(1-@1)*@2", r, f_L, N_ZZ_4e_qq)')
        self.modelBuilder.factory_('expr::f_TT_4mu_qq("@0*(1-@1)*(1-@1)*@2", r, f_L, N_ZZ_4mu_qq)')
        self.modelBuilder.factory_('expr::f_TT_2e2mu_qq("@0*(1-@1)*(1-@1)*@2", r, f_L, N_ZZ_2e2mu_qq)')
        self.modelBuilder.factory_('expr::f_TT_4e_gg("@0*(1-@1)*(1-@1)*@2", r, f_L, N_ZZ_4e_gg)')
        self.modelBuilder.factory_('expr::f_TT_4mu_gg("@0*(1-@1)*(1-@1)*@2", r, f_L, N_ZZ_4mu_gg)')
        self.modelBuilder.factory_('expr::f_TT_2e2mu_gg("@0*(1-@1)*(1-@1)*@2", r, f_L, N_ZZ_2e2mu_gg)')
        self.modelBuilder.doSet("POI", ",".join(["r", "f_L"]))

    def getYieldScale(self, bin, process):
        "Return the name of a RooAbsReal to scale this yield by or the two special values 1 and 0 (don't scale, and set to zero)"
        if self.DC.isSignal[process]:
            print("Scaling %s/%s by r*f_L^2*N_%s" % (bin, process, bin))
            if bin=="fs_4e":
                if "qq" in process:
                    return "f_LL_4e_qq"
                else:
                    return "f_LL_4e_gg"
            elif bin == "fs_4mu":
                if "qq" in process:
                    return "f_LL_4mu_qq"
                else:
                    return "f_LL_4mu_gg"
            elif bin == "fs_2e2mu":
                if "qq" in process:
                    return "f_LL_2e2mu_qq"
                else:
                    return "f_LL_2e2mu_gg"
            else:
                raise Exception("Bin options are fs_4e, fs_4mu, fs_2e2mu")
        elif "ZLZT" in process:
            print("Scaling %s/%s by r*f_L*(1-f_L)*N_%s" % (bin, process, bin))
            if bin=="fs_4e":
                if "qq" in process:
                    return "f_LT_4e_qq"
                else:
                    return "f_LT_4e_gg"
            elif bin == "fs_4mu":
                if "qq" in process:
                    return "f_LT_4mu_qq"
                else:
                    return "f_LT_4mu_gg"
            elif bin == "fs_2e2mu":
                if "qq" in process:
                    return "f_LT_2e2mu_qq"
                else:
                    return "f_LT_2e2mu_gg"
            else:
                raise Exception("Bin options are fs_4e, fs_4mu, fs_2e2mu")
        elif "ZTZT" in process:
            print("Scaling %s/%s by r*(1-f_L)^2*N_%s" % (bin, process, bin))
            if bin=="fs_4e":
                if "qq" in process:
                    return "f_TT_4e_qq"
                else:
                    return "f_TT_4e_gg"
            elif bin == "fs_4mu":
                if "qq" in process:
                    return "f_TT_4mu_qq"
                else:
                    return "f_TT_4mu_gg"
            elif bin == "fs_2e2mu":
                if "qq" in process:
                    return "f_TT_2e2mu_qq"
                else:
                    return "f_TT_2e2mu_gg"
            else:
                raise Exception("Bin options are fs_4e, fs_4mu, fs_2e2mu")
        return 1


class LOtoNLOZZ(PhysicsModel):

    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""
        self.modelBuilder.doVar("N_ZZ_4e[92.596706]") #NLO Yields
        self.modelBuilder.doVar("N_ZZ_4mu[152.99069]")
        self.modelBuilder.doVar("N_ZZ_2e2mu[235.79314]")
        self.modelBuilder.doVar("r[1,-5,5]")
        self.modelBuilder.factory_('expr::norm_4e("@0*@1", r, N_ZZ_4e)')
        self.modelBuilder.factory_('expr::norm_4mu("@0*@1", r, N_ZZ_4mu)')
        self.modelBuilder.factory_('expr::norm_2e2mu("@0*@1", r, N_ZZ_2e2mu)')
        self.modelBuilder.doSet("POI", ",".join(["r"]))

    def getYieldScale(self, bin, process):
        "Return the name of a RooAbsReal to scale this yield by or the two special values 1 and 0 (don't scale, and set to zero)"
        if self.DC.isSignal[process]:
            print("Scaling %s/%s by r*N_%s_NLO" % (bin, process, bin))
            if bin=="fs_4e":
                return "norm_4e"
            elif bin == "fs_4mu":
                return "norm_4mu"
            elif bin == "fs_2e2mu":
                return "norm_2e2mu"
            else:
                raise Exception("Bin options are fs_4e, fs_4mu, fs_2e2mu")
        return 1

polZZModel     = PolZZModel()
singlePolModel = SinglePolModel()
polZZSepQQ     = PolZZSepQQModel()
loToNLO        = LOtoNLOZZ()