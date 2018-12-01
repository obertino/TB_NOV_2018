import ROOT as R

c=R.TCanvas("c","c",800,600)
c.Divide(2,1)

f=R.TFile("plots.root")
c.cd(1)
f.Get("marghe").Draw("COLZ")
c.cd(2)
f.Get("amp_21").Draw("COLZ")

c.SaveAs("c.png")
