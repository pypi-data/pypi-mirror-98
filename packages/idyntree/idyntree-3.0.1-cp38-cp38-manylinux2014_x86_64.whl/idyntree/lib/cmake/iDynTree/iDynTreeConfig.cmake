set(iDynTree_VERSION 3.0.1)


####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was iDynTreeConfig.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

####################################################################################

#### Expanded from @PACKAGE_DEPENDENCIES@ by install_basic_package_files() ####

include(CMakeFindDependencyMacro)
find_dependency(LibXml2)
find_dependency(assimp)

###############################################################################


include("${CMAKE_CURRENT_LIST_DIR}/iDynTreeTargets.cmake")

# Compatibility
set(iDynTree_LIBRARIES iDynTree::idyntree-core iDynTree::idyntree-model iDynTree::idyntree-sensors iDynTree::idyntree-modelio-xml iDynTree::idyntree-modelio-urdf iDynTree::idyntree-estimation iDynTree::idyntree-solid-shapes iDynTree::idyntree-high-level iDynTree::idyntree-inverse-kinematics iDynTree::idyntree-optimalcontrol iDynTree::idyntree-yarp iDynTree::idyntree-icub iDynTree::idyntree-visualization)
set(iDynTree_INCLUDE_DIRS $<TARGET_PROPERTY:iDynTree::idyntree-core,INTERFACE_INCLUDE_DIRECTORIES> $<TARGET_PROPERTY:iDynTree::idyntree-model,INTERFACE_INCLUDE_DIRECTORIES> $<TARGET_PROPERTY:iDynTree::idyntree-sensors,INTERFACE_INCLUDE_DIRECTORIES> $<TARGET_PROPERTY:iDynTree::idyntree-modelio-xml,INTERFACE_INCLUDE_DIRECTORIES> $<TARGET_PROPERTY:iDynTree::idyntree-modelio-urdf,INTERFACE_INCLUDE_DIRECTORIES> $<TARGET_PROPERTY:iDynTree::idyntree-estimation,INTERFACE_INCLUDE_DIRECTORIES> $<TARGET_PROPERTY:iDynTree::idyntree-solid-shapes,INTERFACE_INCLUDE_DIRECTORIES> $<TARGET_PROPERTY:iDynTree::idyntree-high-level,INTERFACE_INCLUDE_DIRECTORIES> $<TARGET_PROPERTY:iDynTree::idyntree-inverse-kinematics,INTERFACE_INCLUDE_DIRECTORIES> $<TARGET_PROPERTY:iDynTree::idyntree-optimalcontrol,INTERFACE_INCLUDE_DIRECTORIES> $<TARGET_PROPERTY:iDynTree::idyntree-yarp,INTERFACE_INCLUDE_DIRECTORIES> $<TARGET_PROPERTY:iDynTree::idyntree-icub,INTERFACE_INCLUDE_DIRECTORIES> $<TARGET_PROPERTY:iDynTree::idyntree-visualization,INTERFACE_INCLUDE_DIRECTORIES>)
if(NOT "${iDynTree_INCLUDE_DIRS}" STREQUAL "")
  list(REMOVE_DUPLICATES iDynTree_INCLUDE_DIRS)
endif()



