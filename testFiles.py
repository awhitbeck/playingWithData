from inputFiles import *
from ROOT import *

gROOT.ProcessLine(".L ~/tdrstyle.C")
gROOT.ProcessLine("setTDRStyle()")

histo = {} 

leg = TLegend(.7,.7,.9,.9)
leg.SetBorderSize(0)
leg.SetFillColor(0)

for s in samples :

    s.tree.Draw("HT>>{0}_HT(20,0,4000)".format(s.tag),"MHT>200.&&NJets>3&&DeltaPhi1>0.5&&DeltaPhi2>0.5&&DeltaPhi3>0.3&&Leptons==0")
    if s.legendLabel in histo : 
        temp = gDirectory.Get("{0}_HT".format(s.tag)) 
        if s.legendLabel == "QCD" : 
            histo[s.legendLabel].Scale(s.weight/1000.)
        else : 
            histo[s.legendLabel].Scale(s.weight)
        
        histo[s.legendLabel].Add( temp )

    else : 
        histo[s.legendLabel] = gDirectory.Get("{0}_HT".format(s.tag))
        histo[s.legendLabel].Sumw2()
        if s.legendLabel == "QCD" : 
            histo[s.legendLabel].Scale(s.weight/1000.)
        else : 
            histo[s.legendLabel].Scale(s.weight)
        histo[s.legendLabel].SetFillColor( s.color )
        histo[s.legendLabel].SetLineColor( 1 )
        histo[s.legendLabel].SetLineWidth( 2 )
        leg.AddEntry( histo[s.legendLabel] , s.legendLabel , "f" )

stack = THStack("stack","stack")

for h in histo:

    stack.Add(histo[h])

can = TCanvas("can","can",500,500)
stack.Draw("histo")

gStyle.SetLogy()

leg.Draw()

can.SaveAs("testHTdistribution.png")
