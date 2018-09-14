INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_REIBLOCKS reiblocks)

FIND_PATH(
    REIBLOCKS_INCLUDE_DIRS
    NAMES reiblocks/api.h
    HINTS $ENV{REIBLOCKS_DIR}/include
        ${PC_REIBLOCKS_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    REIBLOCKS_LIBRARIES
    NAMES gnuradio-reiblocks
    HINTS $ENV{REIBLOCKS_DIR}/lib
        ${PC_REIBLOCKS_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(REIBLOCKS DEFAULT_MSG REIBLOCKS_LIBRARIES REIBLOCKS_INCLUDE_DIRS)
MARK_AS_ADVANCED(REIBLOCKS_LIBRARIES REIBLOCKS_INCLUDE_DIRS)

