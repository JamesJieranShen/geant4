#!/bin/bash
# Samples for investigate.py, with the Poisson method.
#
#   run_investigation.sh <pr exe> <output dir> [jobs]
#
# A 20 MeV sample of the tabulated draws (flag off, no relabelling), and an energy scan.
set -euo pipefail
EXE=$1
OUT=$2
JOBS=${3:-12}
N_DRAWS=${N_DRAWS:-1000000}
N_SCAN=${N_SCAN:-200000}
SCAN=${SCAN:-"8 10 12 14 16 18 20 22 25"}

D=${G4DATA_ROOT:-/cvmfs/geant4.cern.ch/share/data}
export G4NEUTRONHPDATA=$D/G4NDL4.7.1 G4LEDATA=$D/G4EMLOW9.0 G4LEVELGAMMADATA=$D/PhotonEvaporation6.1.2
export G4RADIOACTIVEDATA=$D/RadioactiveDecay6.1.2 G4PARTICLEXSDATA=$D/G4PARTICLEXS4.2
export G4ENSDFSTATEDATA=$D/G4ENSDFSTATE3.0 G4INCLDATA=$D/G4INCL1.3 G4ABLADATA=$D/G4ABLA3.3
export G4PARTICLEHPDATA=${G4PARTICLEHPDATA:-/home/jierans/work/dune/solar/G4TENDL1.4}
export G4PHP_MULTIPLICITY_METHOD=Poisson
mkdir -p "$OUT"
macro() {  # name flag energy n
  { echo "/process/had/enableParticleHPCorrelatedSampling $2"; echo "/run/initialize"
    echo "/random/setSeeds 3003 7"; echo "/gun/energy $3 MeV"; echo "/run/beamOn $4"; } > "$OUT/$1.mac"
}
run() { "$EXE" "$OUT/$1.mac" "$OUT/$1" > "$OUT/$1.log" 2>&1 || { echo "FAILED $1"; return 1; }; }
export -f run
export OUT EXE
macro draws_20 false 20 "$N_DRAWS"
HADRPHP_DO_NOT_ADJUST=1 run draws_20
for e in $SCAN; do
  macro "scan_off_$e" false "$e" "$N_SCAN"; macro "scan_on_$e" true "$e" "$N_SCAN"
  echo "scan_off_$e"; echo "scan_on_$e"
done | xargs -P "$JOBS" -I{} bash -c 'run {}'
