# HadrPHPValidation

Thin-target check of the ParticleHP inclusive (MT5) correlated sampling, reduced from Hadr03.
Alpha on pure 40Ar with only `G4IonPhysicsPHP` registered and no EM or elastic physics, so each
primary interacts at the gun energy. The products of the first inelastic interaction are written
with full precision and the event is aborted.

## Running

Two Geant4 builds with identical flags are needed: the commit before the PR (`f3d5293d38`) and this
branch. Both need the Poisson fix in `G4ParticleHPManager.cc` (commit "let G4PHP_MULTIPLICITY_METHOD=Poisson
select the Poisson method" on this branch): without it, Poisson cannot be selected in 11.3 or later.

    cmake <this dir> -DGeant4_DIR=<build>   # once for each Geant4 build
    ./run_tests.sh <baseline exe> <pr exe> <output dir> [jobs]
    ./analyze.py <output dir> $G4PARTICLEHPDATA/Alpha/Inelastic
    ./extra_stats.py <this dir> <output dir>

The data default to /cvmfs/geant4.cern.ch/share/data and the 2021 G4TENDL 1.4; set `G4DATA_ROOT` and
`G4PARTICLEHPDATA` to change them.

- Test 1 compares event records byte by byte, before the PR against the PR with the flag off and unset,
  with both multiplicity methods. A repeat of the baseline, another seed and the flag on are controls.
- Test 2 compares the flag on and off with Poisson, and both against the tabulated yields.

`results/` has the output of one run (5, 10, 20 MeV; 100k primaries for test 1, 1M for test 2).

## Investigation of the spectra and the residual loss

    ./run_investigation.sh <pr exe> <investigation dir>
    ./investigate.py <investigation dir> <run_tests output dir> $G4PARTICLEHPDATA/Alpha/Inelastic <output dir>

`HADRPHP_DO_NOT_ADJUST=1` turns off the relabelling in `BaseApply`, which leaves the tabulated draws.
`investigate.py` rebuilds the correlated spectra from those draws, and scans the alpha energy. The output
of one run is in `results/investigation/`.
