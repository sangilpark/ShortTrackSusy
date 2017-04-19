#! /usr/bin/env python

from ROOT import *
import sys
from DataFormats.FWLite import Events, Handle

# Make VarParsing object
# https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideAboutPythonConfigFile#VarParsing_Example
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')
options.parseArguments()

# Events takes either
# - single file name
# - list of file names
# - VarParsing options
# use Varparsing object
#events = Events (options)

events = Events('root://cmsxrootd.fnal.gov//store/user/sbein/LongLiveTheChi/pMSSM12_MCMC1_27_200970_step2_AODSIM_15of100.root')

handle_muons  = Handle ("std::vector<reco::Muon>")
label_muons = ('muons')

handle_tracks  = Handle ("vector<reco::Track>")
label_tracks = ('generalTracks')

handle_genparticles  = Handle ("vector<reco::GenParticle>")
label_genparticles = ('genParticlePlusGeant')

# Create histograms, etc.
gROOT.SetBatch()        # don't pop up canvases
gROOT.SetStyle('Plain') # white background
hDrChiTrack = TH1F("hDrChiTrack", "hDrChiTrack", 50, 0, .2)
hDrRandomTrackTrack = TH1F("hDrRandomTrackTrack", "hDrRandomTrackTrack", 50, 0, .2)

# loop over events
for event in events:
    # use getByLabel, just like in cmsRun
    event.getByLabel (label_muons, handle_muons)
    event.getByLabel (label_tracks, handle_tracks)
    event.getByLabel (label_genparticles, handle_genparticles)
    # get the product
    muons = handle_muons.product()
    tracks = handle_tracks.product()
    genparticles = handle_genparticles.product()
    charginos = []
    print '='*10
    for gp in genparticles:
        if abs(gp.pdgId())==1000024 and gp.status()==1:
            print 'found chargino!, pt=', gp.pt()
            chiTlv = TLorentzVector()
            chiTlv.SetPxPyPzE(gp.px(),gp.py(),gp.pz(),gp.energy())
            charginos.append(chiTlv)
            drsmall = 10
            for track in tracks:
                trkTlv = TLorentzVector()
                trkTlv.SetPxPyPzE(track.px(), track.py(), track.pz(), track.pt())
                dr = trkTlv.DeltaR(chiTlv)
                if dr<drsmall:
                    drsmall = dr
            hDrChiTrack.Fill(drsmall)

    randomtrack = TLorentzVector()
    irandom=5
    randomtrack.SetPxPyPzE(tracks[irandom].px(),tracks[irandom].py(),tracks[irandom].pz(),tracks[irandom].pt())
    drsmall = 10
    for itrack, track in enumerate(tracks):
        if itrack==irandom: continue
        trkTlv = TLorentzVector()
        trkTlv.SetPxPyPzE(track.px(), track.py(), track.pz(), track.pt())
        dr = trkTlv.DeltaR(randomtrack)
        if dr<drsmall:
            drsmall = dr
    print 'drsmall', drsmall
    hDrRandomTrackTrack.Fill(drsmall)            

            
            #if dr<0.3: print hitpattern.numberOfValidPixelHits()
    
# make a canvas, draw, and save it
c1 = TCanvas()
hDrChiTrack.Draw()
c1.Print ("dr_track_chargino.png")

hDrRandomTrackTrack.Draw()
c1.Print ("dr_track_randomtrack.png")

#print dir(track)
#hitpattern = track.hitPattern()
#print dir(hitpattern)
#exit(0)
