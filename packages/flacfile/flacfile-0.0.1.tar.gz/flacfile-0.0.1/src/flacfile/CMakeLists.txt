# src folder name is used as the target name 
get_filename_component(TARGET ${CMAKE_CURRENT_SOURCE_DIR} NAME)

# copy all the py module files to dist folder
file(RELATIVE_PATH DST_DIR ${SRC_DIR} ${CMAKE_CURRENT_SOURCE_DIR})
file(GLOB_RECURSE PYFILES LIST_DIRECTORIES false RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "*.py")
foreach(FILE ${PYFILES})
    get_filename_component(PYDIR ${FILE} DIRECTORY)
    install(FILES ${FILE} DESTINATION "${DST_DIR}/${PYDIR}" COMPONENT "PY") # copy all the py-files in dir
endforeach(FILE ${PYFILES})

add_subdirectory("__native__")
