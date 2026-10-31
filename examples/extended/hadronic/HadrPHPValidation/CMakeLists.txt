cmake_minimum_required(VERSION 3.16...3.27)
project(HadrPHPValidation)

find_package(Geant4 REQUIRED)
include(${Geant4_USE_FILE})

add_executable(HadrPHPValidation HadrPHPValidation.cc)
target_link_libraries(HadrPHPValidation ${Geant4_LIBRARIES})
