// Thin-target validation of ParticleHP final states, reduced from Hadr03.
//
// Each primary is tracked to its first inelastic interaction on a single isotope, with no EM or
// elastic physics, so that its energy at the interaction is the gun energy. The products are written
// with full precision and the event is aborted, so only final-state sampling is compared.
//
//   HadrPHPValidation <macro> <output prefix>  ->  <prefix>_events.csv, <prefix>_products.csv
//
// The macro must not depend on code under test: the correlated sampling flag is only set by macros
// that are run with builds that have it.

#include "G4Box.hh"
#include "G4BaryonConstructor.hh"
#include "G4BosonConstructor.hh"
#include "G4Element.hh"
#include "G4Event.hh"
#include "G4EventManager.hh"
#include "G4HadronicParameters.hh"
#include "G4IonConstructor.hh"
#include "G4IonPhysicsPHP.hh"
#include "G4Ions.hh"
#include "G4Isotope.hh"
#include "G4LeptonConstructor.hh"
#include "G4LogicalVolume.hh"
#include "G4Material.hh"
#include "G4MesonConstructor.hh"
#include "G4NucleiProperties.hh"
#include "G4NuclideTable.hh"
#include "G4ParticleGun.hh"
#include "G4ParticleHPManager.hh"
#include "G4ParticleTable.hh"
#include "G4PVPlacement.hh"
#include "G4RunManager.hh"
#include "G4ShortLivedConstructor.hh"
#include "G4Step.hh"
#include "G4SystemOfUnits.hh"
#include "G4UImanager.hh"
#include "G4UserSteppingAction.hh"
#include "G4VModularPhysicsList.hh"
#include "G4VUserActionInitialization.hh"
#include "G4VUserDetectorConstruction.hh"
#include "G4VUserPrimaryGeneratorAction.hh"

#include <cstdio>

namespace
{
constexpr G4int targetZ = 18;
constexpr G4int targetA = 40;
}  // namespace

class DetectorConstruction : public G4VUserDetectorConstruction
{
  public:

    G4VPhysicalVolume* Construct() override
    {
      auto isotope = new G4Isotope("Ar40", targetZ, targetA);
      auto element = new G4Element("Argon40", "Ar40", 1);
      element->AddIsotope(isotope, 100. * perCent);
      // Unphysical density: every primary interacts within the box, even at low cross sections.
      auto material = new G4Material("Ar40Target", 1000. * g / cm3, 1);
      material->AddElement(element, 1);
      const G4double half = 500. * m;
      auto box = new G4Box("Target", half, half, half);
      auto logical = new G4LogicalVolume(box, material, "Target");
      return new G4PVPlacement(nullptr, G4ThreeVector(), logical, "Target", nullptr, false, 0);
    }
};

class PhysicsList : public G4VModularPhysicsList
{
  public:

    PhysicsList()
    {
      SetVerboseLevel(0);
      G4NuclideTable::GetInstance()->SetMeanLifeThreshold(1. * nanosecond);
      RegisterPhysics(new G4IonPhysicsPHP(0));
    }

    void ConstructParticle() override
    {
      G4BosonConstructor::ConstructParticle();
      G4LeptonConstructor::ConstructParticle();
      G4MesonConstructor::ConstructParticle();
      G4BaryonConstructor::ConstructParticle();
      G4IonConstructor::ConstructParticle();
      G4ShortLivedConstructor::ConstructParticle();
    }
};

class PrimaryGenerator : public G4VUserPrimaryGeneratorAction
{
  public:

    PrimaryGenerator()
    {
      fGun.SetParticleDefinition(G4ParticleTable::GetParticleTable()->FindParticle("alpha"));
      fGun.SetParticleEnergy(10. * MeV);
      fGun.SetParticlePosition(G4ThreeVector());
      fGun.SetParticleMomentumDirection(G4ThreeVector(0., 0., 1.));
    }

    void GeneratePrimaries(G4Event* event) override { fGun.GeneratePrimaryVertex(event); }

  private:

    G4ParticleGun fGun;
};

class SteppingAction : public G4UserSteppingAction
{
  public:

    SteppingAction(std::FILE* events, std::FILE* products) : fEvents(events), fProducts(products) {}

    void UserSteppingAction(const G4Step* step) override
    {
      const G4Track* track = step->GetTrack();
      if (track->GetTrackID() != 1 || track->GetCurrentStepNumber() != 1) return;

      const G4int event = G4EventManager::GetEventManager()->GetConstCurrentEvent()->GetEventID();
      const G4StepPoint* post = step->GetPostStepPoint();
      const G4VProcess* process = post->GetProcessDefinedStep();
      const G4double kinetic = step->GetPreStepPoint()->GetKineticEnergy();
      const auto* secondaries = step->GetSecondaryInCurrentStep();
      const G4bool alive = track->GetTrackStatus() == fAlive;
      std::fprintf(fEvents, "%d,%s,%.17g,%.17g,%.17g,%d\n", event,
                   process != nullptr ? process->GetProcessName().c_str() : "none", kinetic,
                   track->GetDefinition()->GetPDGMass(),
                   G4NucleiProperties::GetNuclearMass(targetA, targetZ),
                   (G4int)secondaries->size() + (alive ? 1 : 0));
      if (alive)
      {
        Write(event, track->GetDefinition(), post->GetKineticEnergy(), post->GetMomentum());
      }
      for (const G4Track* secondary : *secondaries)
      {
        Write(event, secondary->GetDefinition(), secondary->GetKineticEnergy(),
              secondary->GetMomentum());
      }
      G4EventManager::GetEventManager()->AbortCurrentEvent();
    }

  private:

    void Write(G4int event, const G4ParticleDefinition* def, G4double kinetic,
               const G4ThreeVector& p)
    {
      const auto* ion = dynamic_cast<const G4Ions*>(def);
      std::fprintf(fProducts, "%d,%d,%d,%d,%.17g,%.17g,%.17g,%.17g,%.17g,%.17g\n", event,
                   def->GetPDGEncoding(), G4lrint(def->GetPDGCharge() / eplus),
                   def->GetBaryonNumber(), ion != nullptr ? ion->GetExcitationEnergy() : 0., kinetic,
                   p.x(), p.y(), p.z(), def->GetPDGMass());
    }

    std::FILE* fEvents;
    std::FILE* fProducts;
};

class ActionInitialization : public G4VUserActionInitialization
{
  public:

    ActionInitialization(std::FILE* events, std::FILE* products)
      : fEvents(events), fProducts(products)
    {}

    void Build() const override
    {
      SetUserAction(new PrimaryGenerator);
      SetUserAction(new SteppingAction(fEvents, fProducts));
    }

  private:

    std::FILE* fEvents;
    std::FILE* fProducts;
};

int main(int argc, char** argv)
{
  if (argc != 3)
  {
    G4cerr << "usage: " << argv[0] << " <macro> <output prefix>" << G4endl;
    return 1;
  }
  const G4String prefix = argv[2];
  std::FILE* events = std::fopen((prefix + "_events.csv").c_str(), "w");
  std::FILE* products = std::fopen((prefix + "_products.csv").c_str(), "w");
  if (events == nullptr || products == nullptr)
  {
    G4cerr << "cannot open output files for " << prefix << G4endl;
    return 1;
  }
  std::fprintf(events, "event,process,kinetic,proj_mass,targ_mass,n\n");
  std::fprintf(products, "event,pdg,Z,A,excitation,kinetic,px,py,pz,mass\n");

  G4HadronicParameters::Instance();  // constructs the messenger for the macro
  // Sequential, so that a seed fixes the whole sequence of events.
  auto runManager = new G4RunManager;
  runManager->SetUserInitialization(new DetectorConstruction);
  runManager->SetUserInitialization(new PhysicsList);
  runManager->SetUserInitialization(new ActionInitialization(events, products));

  G4UImanager::GetUIpointer()->ApplyCommand(G4String("/control/execute ") + argv[1]);
  // The method that was really used, in the log of the run.
  G4cout << "VALIDATION multiplicity method: "
         << (G4ParticleHPManager::GetInstance()->GetPHCUsePoisson() ? "Poisson" : "BetweenInts")
         << G4endl;

  delete runManager;
  std::fclose(events);
  std::fclose(products);
  return 0;
}
