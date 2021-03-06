# - G4geomtext module build definition

# Define the Geant4 Module.
geant4_add_module(G4geomtext
  PUBLIC_HEADERS
    G4tgbDetectorBuilder.hh
    G4tgbDetectorConstruction.hh
    G4tgbElement.hh
    G4tgbGeometryDumper.hh
    G4tgbIsotope.hh
    G4tgbMaterial.hh
    G4tgbMaterialMgr.hh
    G4tgbMaterialMixture.hh
    G4tgbMaterialMixtureByNoAtoms.hh
    G4tgbMaterialMixtureByVolume.hh
    G4tgbMaterialMixtureByWeight.hh
    G4tgbMaterialSimple.hh
    G4tgbPlaceParamCircle.hh
    G4tgbPlaceParamLinear.hh
    G4tgbPlaceParamSquare.hh
    G4tgbPlaceParameterisation.hh
    G4tgbRotationMatrix.hh
    G4tgbRotationMatrixMgr.hh
    G4tgbVolume.hh
    G4tgbVolumeMgr.hh
    G4tgrElement.hh
    G4tgrElementFromIsotopes.hh
    G4tgrElementSimple.hh
    G4tgrEvaluator.hh
    G4tgrFileIn.hh
    G4tgrFileReader.hh
    G4tgrIsotope.hh
    G4tgrLineProcessor.hh
    G4tgrMaterial.hh
    G4tgrMaterialFactory.hh
    G4tgrMaterialMixture.hh
    G4tgrMaterialSimple.hh
    G4tgrMessenger.hh
    G4tgrParameterMgr.hh
    G4tgrPlace.hh
    G4tgrPlaceDivRep.hh
    G4tgrPlaceParameterisation.hh
    G4tgrPlaceSimple.hh
    G4tgrRotationMatrix.hh
    G4tgrRotationMatrixFactory.hh
    G4tgrSolid.hh
    G4tgrSolidBoolean.hh
    G4tgrUtils.hh
    G4tgrVolume.hh
    G4tgrVolumeAssembly.hh
    G4tgrVolumeDivision.hh
    G4tgrVolumeMgr.hh
    G4tgrSolidMultiUnion.hh
    G4tgrSolidScaled.hh
  SOURCES
    G4tgbDetectorBuilder.cc
    G4tgbDetectorConstruction.cc
    G4tgbElement.cc
    G4tgbGeometryDumper.cc
    G4tgbIsotope.cc
    G4tgbMaterial.cc
    G4tgbMaterialMgr.cc
    G4tgbMaterialMixture.cc
    G4tgbMaterialMixtureByNoAtoms.cc
    G4tgbMaterialMixtureByVolume.cc
    G4tgbMaterialMixtureByWeight.cc
    G4tgbMaterialSimple.cc
    G4tgbPlaceParamCircle.cc
    G4tgbPlaceParamLinear.cc
    G4tgbPlaceParamSquare.cc
    G4tgbPlaceParameterisation.cc
    G4tgbRotationMatrix.cc
    G4tgbRotationMatrixMgr.cc
    G4tgbVolume.cc
    G4tgbVolumeMgr.cc
    G4tgrElement.cc
    G4tgrElementFromIsotopes.cc
    G4tgrElementSimple.cc
    G4tgrEvaluator.cc
    G4tgrFileIn.cc
    G4tgrFileReader.cc
    G4tgrIsotope.cc
    G4tgrLineProcessor.cc
    G4tgrMaterial.cc
    G4tgrMaterialFactory.cc
    G4tgrMaterialMixture.cc
    G4tgrMaterialSimple.cc
    G4tgrMessenger.cc
    G4tgrParameterMgr.cc
    G4tgrPlace.cc
    G4tgrPlaceDivRep.cc
    G4tgrPlaceParameterisation.cc
    G4tgrPlaceSimple.cc
    G4tgrRotationMatrix.cc
    G4tgrRotationMatrixFactory.cc
    G4tgrSolid.cc
    G4tgrSolidBoolean.cc
    G4tgrUtils.cc
    G4tgrVolume.cc
    G4tgrVolumeAssembly.cc
    G4tgrVolumeDivision.cc
    G4tgrVolumeMgr.cc
    G4tgrSolidMultiUnion.cc
    G4tgrSolidScaled.cc)

geant4_module_link_libraries(G4geomtext
  PUBLIC
    G4geometrymng
    G4materials
    G4intercoms
    G4globman
    G4hepgeometry
  PRIVATE
    G4volumes
    G4geomBoolean
    G4csg
    G4specsolids
    G4geomdivision
    G4graphics_reps)
