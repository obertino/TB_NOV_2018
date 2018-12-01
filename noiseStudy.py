import ROOT as R

ch5=R.TChain("pulse")
ch5.Add("/eos/cms/store/group/dpg_mtd/comm_mtd/TB/MTDTB_FNAL_Nov2018/reco/v5/DataVMETiming_Run1032.root")
ch5.Add("/eos/cms/store/group/dpg_mtd/comm_mtd/TB/MTDTB_FNAL_Nov2018/reco/v5/DataVMETiming_Run1034.root")
ch5.Add("/eos/cms/store/group/dpg_mtd/comm_mtd/TB/MTDTB_FNAL_Nov2018/reco/v5/DataVMETiming_Run1035.root")
ch5.Add("/eos/cms/store/group/dpg_mtd/comm_mtd/TB/MTDTB_FNAL_Nov2018/reco/v5/DataVMETiming_Run1036.root")
ch5.Add("/eos/cms/store/group/dpg_mtd/comm_mtd/TB/MTDTB_FNAL_Nov2018/reco/v5/DataVMETiming_Run1039.root")
ch5.Add("/eos/cms/store/group/dpg_mtd/comm_mtd/TB/MTDTB_FNAL_Nov2018/reco/v5/DataVMETiming_Run1040.root")
ch5.Add("/eos/cms/store/group/dpg_mtd/comm_mtd/TB/MTDTB_FNAL_Nov2018/reco/v5/DataVMETiming_Run1041.root")
ch5.Add("/eos/cms/store/group/dpg_mtd/comm_mtd/TB/MTDTB_FNAL_Nov2018/reco/v5/DataVMETiming_Run1042.root")
ch5.Add("/eos/cms/store/group/dpg_mtd/comm_mtd/TB/MTDTB_FNAL_Nov2018/reco/v5/DataVMETiming_Run1043.root")
ch5.Add("/eos/cms/store/group/dpg_mtd/comm_mtd/TB/MTDTB_FNAL_Nov2018/reco/v5/DataVMETiming_Run1046.root")
ch5.Add("/eos/cms/store/group/dpg_mtd/comm_mtd/TB/MTDTB_FNAL_Nov2018/reco/v5/DataVMETiming_Run1047.root")
ch5.Add("/eos/cms/store/group/dpg_mtd/comm_mtd/TB/MTDTB_FNAL_Nov2018/reco/v5/DataVMETiming_Run1049.root")
ch5.Add("/eos/cms/store/group/dpg_mtd/comm_mtd/TB/MTDTB_FNAL_Nov2018/reco/v5/DataVMETiming_Run1050.root")
ch5.Add("/eos/cms/store/group/dpg_mtd/comm_mtd/TB/MTDTB_FNAL_Nov2018/reco/v5/DataVMETiming_Run1052.root")
ch5.Add("/eos/cms/store/group/dpg_mtd/comm_mtd/TB/MTDTB_FNAL_Nov2018/reco/v5/DataVMETiming_Run1053.root")
ch5.Add("/eos/cms/store/group/dpg_mtd/comm_mtd/TB/MTDTB_FNAL_Nov2018/reco/v5/DataVMETiming_Run1056.root")
ch5.Add("/eos/cms/store/group/dpg_mtd/comm_mtd/TB/MTDTB_FNAL_Nov2018/reco/v5/DataVMETiming_Run1057.root")

channels  = [ 18, 21, 22 ]
variables = ["t_peak","gaus_mean","amp","LP2_20","LP2_50"]

vars = []
for ch in channels:
    for var in variables:
        vars.append("%s[%d]"%(var,ch))

values = {}

variables_str = ""
for str in vars:
    variables_str = variables_str+str+":"
variables_str = variables_str[:-1] #remove last :
 
print variables_str

cut = "amp[18]>30"

histo = {}
#
hrange = {}
hrange["t_peak"]=[0,200]
hrange["gaus_mean"]=[0,200]
hrange["amp"]=[0,1000]
hrange["LP2_20"]=[0,200]
hrange["LP2_50"]=[0,200]
#
hbins = {}
hbins["t_peak"]=50
hbins["gaus_mean"]=50
hbins["amp"]=200
hbins["LP2_20"]=50
hbins["LP2_50"]=50
#
for ch in channels:
    for var in variables:
        name="%s_%d"%(var,ch)
        histo[name]=R.TH1F(name,name,hbins[var],hrange[var][0],hrange[var][1])

histo["marghe"] = R.TH2F("marghe","marghe",100,0,100,200,0,200)

hcut = "amp[18]>30 && amp[18]<300"         
for i in range(0,min(5000,ch5.GetEntriesFast())):
    ch5.Draw(variables_str,hcut,"goff",1,i)
    for idx,str in enumerate(vars):
        values[str]=ch5.GetVal(idx)[0]

#Fill 1D PLOT
    for ch in channels:
        for var in variables:
            name="%s_%d"%(var,ch)  
            varSt="%s[%d]"%(var,ch)
            histo[name].Fill(values[varSt])

    if (values['amp[21]']>0 and values['LP2_20[21]']!=0 ):
        histo["marghe"].Fill(values['amp[21]'],values['t_peak[21]'])
            
fOut=R.TFile("plots.root","RECREATE")
for h in histo.keys():
    histo[h].Write()
fOut.Close()

