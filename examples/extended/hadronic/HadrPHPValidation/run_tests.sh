#!/bin/bash
# Run the identity and correlated-sampling tests.
#
#   run_tests.sh <baseline exe> <pr exe> <output dir> [jobs]
#
# Identity test: the build before the PR and the PR with the flag off, same seeds, Poisson and the
# default method. Correlated test: the PR with the flag on and off, Poisson.
set -euo pipefail

BASE_EXE=$1
PR_EXE=$2
OUT=$3
JOBS=${4:-12}
ENERGIES=${ENERGIES:-"5 10 20"}
N_IDENTITY=${N_IDENTITY:-100000}
N_CORRELATED=${N_CORRELATED:-1000000}

D=${G4DATA_ROOT:-/cvmfs/geant4.cern.ch/share/data}
export G4NEUTRONHPDATA=$D/G4NDL4.7.1
export G4LEDATA=$D/G4EMLOW9.0
export G4LEVELGAMMADATA=$D/PhotonEvaporation6.1.2
export G4RADIOACTIVEDATA=$D/RadioactiveDecay6.1.2
export G4PARTICLEXSDATA=$D/G4PARTICLEXS4.2
export G4ENSDFSTATEDATA=$D/G4ENSDFSTATE3.0
export G4INCLDATA=$D/G4INCL1.3
export G4ABLADATA=$D/G4ABLA3.3
export G4PARTICLEHPDATA=${G4PARTICLEHPDATA:-/home/jierans/work/dune/solar/G4TENDL1.4}

mkdir -p "$OUT/macros" "$OUT/data" "$OUT/logs"

# job: name exe method(Poisson|default) flag(on|off|none) energy seed nevents
job() {
  local name=$1 exe=$2 method=$3 flag=$4 energy=$5 seed=$6 n=$7
  local mac="$OUT/macros/$name.mac"
  {
    [ "$flag" = none ] || echo "/process/had/enableParticleHPCorrelatedSampling $([ "$flag" = on ] && echo true || echo false)"
    echo "/run/initialize"
    echo "/random/setSeeds $seed 7"
    echo "/gun/energy $energy MeV"
    echo "/run/beamOn $n"
  } > "$mac"
  echo "$name $exe $method $mac"
}

run_one() {
  local name=$1 exe=$2 method=$3 mac=$4
  if [ "$method" = default ]; then unset G4PHP_MULTIPLICITY_METHOD
  else export G4PHP_MULTIPLICITY_METHOD=$method; fi
  "$exe" "$mac" "$OUT/data/$name" > "$OUT/logs/$name.log" 2>&1 || { echo "FAILED $name"; return 1; }
}
export -f run_one
export OUT

{
  for e in $ENERGIES; do
    for m in Poisson default; do
      job "id_base_${m}_${e}" "$BASE_EXE" "$m" none "$e" 1001 "$N_IDENTITY"
      job "id_base2_${m}_${e}" "$BASE_EXE" "$m" none "$e" 1001 "$N_IDENTITY"  # reproducibility
      job "id_off_${m}_${e}" "$PR_EXE" "$m" off "$e" 1001 "$N_IDENTITY"
      job "id_unset_${m}_${e}" "$PR_EXE" "$m" none "$e" 1001 "$N_IDENTITY"  # the default of the flag
      job "id_otherseed_${m}_${e}" "$PR_EXE" "$m" off "$e" 2002 "$N_IDENTITY"  # the test can fail
      job "id_on_${m}_${e}" "$PR_EXE" "$m" on "$e" 1001 "$N_IDENTITY"  # the test can fail
    done
    job "corr_off_${e}" "$PR_EXE" Poisson off "$e" 3003 "$N_CORRELATED"
    job "corr_on_${e}" "$PR_EXE" Poisson on "$e" 3003 "$N_CORRELATED"
  done
} > "$OUT/jobs.txt"

xargs -P "$JOBS" -L 1 bash -c 'run_one "$@"' _ < "$OUT/jobs.txt"
