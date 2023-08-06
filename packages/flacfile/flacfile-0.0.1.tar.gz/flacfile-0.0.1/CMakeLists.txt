cmake_minimum_required(VERSION 3.5)

# when installing directly in CMake, redirect its intall root to dist dir
# if (CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    set (CMAKE_INSTALL_PREFIX "${CMAKE_SOURCE_DIR}/dist" CACHE PATH "default install path" FORCE )
    set (CMAKE_INSTALL_BINDIR "${CMAKE_SOURCE_DIR}/dist/bin" CACHE PATH "default bin install path" FORCE )
    set (CMAKE_INSTALL_LIBDIR "${CMAKE_SOURCE_DIR}/dist/lib" CACHE PATH "default lib install path" FORCE )
    set (CMAKE_INSTALL_INCLUDEDIR "${CMAKE_SOURCE_DIR}/dist/include" CACHE PATH "default include install path" FORCE )
# endif()

project(python-flac)

# add_subdirectory(extern)
option(BUILD_CXXLIBS "Build libFLAC++" OFF)
option(BUILD_PROGRAMS "Build and install programs" OFF)
option(BUILD_EXAMPLES "Build and install examples" OFF)
option(BUILD_DOCS "Build and install doxygen documents" OFF)
option(WITH_STACK_PROTECTOR "Enable GNU GCC stack smash protection" OFF)
option(INSTALL_MANPAGES "Install MAN pages" OFF)
option(INSTALL_PKGCONFIG_MODULES "Install PkgConfig modules" OFF)
option(INSTALL_CMAKE_CONFIG_MODULE "Install CMake package-config module" OFF)
option(WITH_OGG "ogg support (default: test for libogg)" OFF)
add_subdirectory(extern/flac)

if(UNIX AND NOT APPLE)
    target_compile_options(FLAC PRIVATE -fPIC)
endif()

install(TARGETS FLAC EXCLUDE_FROM_ALL)

add_subdirectory(extern/pybind11)

option(FMT_DOC "Generate the doc target." OFF)
option(FMT_INSTALL "Generate the install target." OFF)
option(FMT_TEST "Generate the test target." OFF)
option(FMT_FUZZ "Generate the fuzz target." OFF)
option(FMT_CUDA_TEST "Generate the cuda-test target." OFF)
option(FMT_OS "Include core requiring OS (Windows/Posix) " OFF)
add_subdirectory(extern/fmt)

add_subdirectory(src)
