# minimum cmake version
cmake_minimum_required(VERSION 3.18)

project(hps-align)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_C_STANDARD 14)
set(CMAKE_C_STANDARD_REQUIRED ON)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()
set(CMAKE_CXX_FLAGS_RELEASE "-O3")

# enable in source build since default is not writable from a non-root account
if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    set(CMAKE_INSTALL_PREFIX "${CMAKE_SOURCE_DIR}/install" CACHE PATH "..." FORCE)
endif()

# add dir with extra CMake modules
list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake/Modules/)

# find Python 3
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
message(STATUS "Python executable found at: ${Python3_EXECUTABLE}")
message(STATUS "Python lib found at: ${Python3_LIBRARIES}")
message(STATUS "Python include dir found at: ${Python3_INCLUDE_DIRS}")

# find ROOT installation
find_package(ROOT REQUIRED COMPONENTS Core RIO Geom Eve Gui)
message(STATUS "ROOT found at: ${ROOT_DIR}")

# option to print extra module information during CMake config
option(MODULE_DEBUG "Print extra module information during CMake config" OFF)

# add dir with extra CMake modules
list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake/Modules/)

# import macro for declaring modules
include(MacroModule)

# import macro for declaring external dependencies
include(MacroExtDeps)

# configure and install setup script
configure_file(hps-align-env.sh.in ${CMAKE_INSTALL_PREFIX}/bin/hps-align-env.sh)

# install python files
install(DIRECTORY tools/analysis DESTINATION lib/python/tools)

# info message about install prefix
message(STATUS "hpstr will be installed to: ${CMAKE_INSTALL_PREFIX}")