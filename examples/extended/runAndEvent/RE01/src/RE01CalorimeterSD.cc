//
// ********************************************************************
// * DISCLAIMER                                                       *
// *                                                                  *
// * The following disclaimer summarizes all the specific disclaimers *
// * of contributors to this software. The specific disclaimers,which *
// * govern, are listed with their locations in:                      *
// *   http://cern.ch/geant4/license                                  *
// *                                                                  *
// * Neither the authors of this software system, nor their employing *
// * institutes,nor the agencies providing financial support for this *
// * work  make  any representation or  warranty, express or implied, *
// * regarding  this  software system or assume any liability for its *
// * use.                                                             *
// *                                                                  *
// * This  code  implementation is the  intellectual property  of the *
// * GEANT4 collaboration.                                            *
// * By copying,  distributing  or modifying the Program (or any work *
// * based  on  the Program)  you indicate  your  acceptance of  this *
// * statement, and all its terms.                                    *
// ********************************************************************
//
// $Id: RE01CalorimeterSD.cc,v 1.1 2004/11/26 07:37:41 asaim Exp $
// GEANT4 tag $Name: geant4-07-00-cand-01 $
//


#include "RE01CalorimeterSD.hh"
#include "RE01CalorimeterHit.hh"
#include "G4VPhysicalVolume.hh"
#include "G4LogicalVolume.hh"
#include "G4Track.hh"
#include "G4Step.hh"
#include "G4ParticleDefinition.hh"
#include "G4VTouchable.hh"
#include "G4TouchableHistory.hh"
#include "G4ios.hh"

RE01CalorimeterSD::RE01CalorimeterSD(G4String name)
:G4VSensitiveDetector(name),
 numberOfCellsInZ(20),numberOfCellsInPhi(48)
{
  G4String HCname;
  collectionName.insert(HCname="calCollection");
}

RE01CalorimeterSD::~RE01CalorimeterSD()
{;}

void RE01CalorimeterSD::Initialize(G4HCofThisEvent* HCE)
{
  CalCollection = new RE01CalorimeterHitsCollection
                      (SensitiveDetectorName,collectionName[0]); 
  for(G4int j=0;j<numberOfCellsInZ;j++)
  for(G4int k=0;k<numberOfCellsInPhi;k++)
  {
    CellID[j][k] = -1;
  }

  static G4int HCID = -1;
  if(HCID<0)
  { HCID = GetCollectionID(0); }
  HCE->AddHitsCollection( HCID, CalCollection );
}

G4bool RE01CalorimeterSD::ProcessHits(G4Step*aStep,G4TouchableHistory*ROhist)
{
  if(!ROhist) return false;
  G4double edep = aStep->GetTotalEnergyDeposit();
  if(edep==0.) return false;

  G4VPhysicalVolume* physVol = ROhist->GetVolume();
  //ROhist->MoveUpHistory();
  //G4VPhysicalVolume* mothVol = ROhist->GetVolume(1);
  G4int copyIDinZ = ROhist->GetReplicaNumber();
  G4int copyIDinPhi = ROhist->GetReplicaNumber(1);

  if(CellID[copyIDinZ][copyIDinPhi]==-1)
  {
    RE01CalorimeterHit* calHit
      = new RE01CalorimeterHit
            (physVol->GetLogicalVolume(),copyIDinZ,copyIDinPhi);
    G4RotationMatrix rotM;
    if(physVol->GetObjectRotation()) rotM = *(physVol->GetObjectRotation());
    calHit->SetEdep( edep );
    calHit->SetPos( physVol->GetTranslation() );
    calHit->SetRot( rotM );
    calHit->SetTrackInformation(aStep->GetTrack());
    G4int icell = CalCollection->insert( calHit );
    CellID[copyIDinZ][copyIDinPhi] = icell - 1;
    if(verboseLevel>0)
    { G4cout << " New Calorimeter Hit on CellID " 
           << copyIDinZ << " " << copyIDinPhi << G4endl; }
  }
  else
  { 
    (*CalCollection)[CellID[copyIDinZ][copyIDinPhi]]->AddEdep(edep);
    (*CalCollection)[CellID[copyIDinZ][copyIDinPhi]]->SetTrackInformation(aStep->GetTrack());
    if(verboseLevel>0)
    { G4cout << " Energy added to CellID " 
           << copyIDinZ << " " << copyIDinPhi << G4endl; }
  }

  return true;
}

void RE01CalorimeterSD::EndOfEvent(G4HCofThisEvent*)
{
}

void RE01CalorimeterSD::clear()
{
} 

void RE01CalorimeterSD::DrawAll()
{
} 

void RE01CalorimeterSD::PrintAll()
{
} 
