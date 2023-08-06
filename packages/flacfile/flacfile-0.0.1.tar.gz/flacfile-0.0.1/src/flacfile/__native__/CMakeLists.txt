# src folder name is used as the target name 
get_filename_component(TARGET ${CMAKE_CURRENT_SOURCE_DIR} NAME)

# create the target
pybind11_add_module(${TARGET} "__native__.cpp" "read.cpp" "write.cpp")

target_link_libraries(${TARGET} PRIVATE FLAC)
target_link_libraries(${TARGET} PRIVATE fmt::fmt-header-only)

set_target_properties(${TARGET} PROPERTIES
	CXX_STANDARD 17
	CXX_STANDARD_REQUIRED TRUE
	CXX_EXTENSIONS FALSE
)
# set_target_properties(praat fmt PROPERTIES
# 	POSITION_INDEPENDENT_CODE TRUE
# 	# Fixing "ld: warning: direct access in function '...' from file '...' to global weak symbol '...' from file '...' means the weak symbol cannot
# 	# be overridden at runtime. This was likely caused by different translation units being compiled with different visibility settings."
# 	C_VISIBILITY_PRESET hidden
# 	CXX_VISIBILITY_PRESET hidden
# )

# install pyd files one directory structure UP in the destination as 
# CMAKE_CURRENT_SOURCE_DIR is holding the source files of the MODULE
# which matches the name of CMAKE_CURRENT_SOURCE_DIR
get_filename_component(CURRENT_SRC_DIR ${CMAKE_CURRENT_SOURCE_DIR} DIRECTORY)
if(${SRC_DIR} STREQUAL ${CURRENT_SRC_DIR}) 
    set(DST_DIR ".") # if parent is the base folder
else()
    file(RELATIVE_PATH DST_DIR ${SRC_DIR} ${CURRENT_SRC_DIR})
endif()
install(TARGETS ${TARGET} DESTINATION ${DST_DIR} COMPONENT "EXT")
