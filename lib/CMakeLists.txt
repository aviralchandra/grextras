########################################################################
# Setup library
########################################################################
include_directories(${GREXTRAS_SOURCE_DIR}/include)
include_directories(${CMAKE_CURRENT_SOURCE_DIR})
list(APPEND GREXTRAS_SOURCES
    add.cpp
    add_const.cpp
    add_const_v.cpp
    multiply.cpp
    multiply_const.cpp
    multiply_const_v.cpp
    subtract.cpp
    divide.cpp

    noise_source.cpp
    signal_source.cpp

    datagram_to_stream.cpp
    stream_to_datagram.cpp
    socket_message.cpp
    tuntap.cpp

    delay.cpp
    time_align.cpp
    burst_tagger.cpp
    stream_selector.cpp

    opencl_block.cpp
    orc_block.cpp
    clang_block.cpp

    uhd_status_port.cpp
    uhd_control_port.cpp

    serializer.cpp
    deserializer.cpp

    scrambler.cpp
    descrambler.cpp
)

########################################################################
# Setup PMC
########################################################################
include_directories(${PMC_INCLUDE_DIRS})
link_directories(${PMC_LIBRARY_DIRS})
list(APPEND GREXTRAS_LIBRARIES ${PMC_LIBRARIES})

########################################################################
# Setup GRAS
########################################################################
include_directories(${GRAS_INCLUDE_DIRS})
link_directories(${GRAS_LIBRARY_DIRS})
list(APPEND GREXTRAS_LIBRARIES ${GRAS_LIBRARIES})

########################################################################
# Setup Volk
########################################################################
if(VOLK_FOUND)
    include_directories(${VOLK_INCLUDE_DIRS})
    link_directories(${VOLK_LIBRARY_DIRS})
    list(APPEND GREXTRAS_LIBRARIES ${VOLK_LIBRARIES})
    add_definitions(-DHAVE_VOLK)
endif()

########################################################################
# Setup Boost
########################################################################
find_package(Boost COMPONENTS thread serialization)
include_directories(${Boost_INCLUDE_DIRS})
link_directories(${Boost_LIBRARY_DIRS})
list(APPEND GREXTRAS_LIBRARIES ${Boost_LIBRARIES})

########################################################################
# Optional UHD
########################################################################
if(UHD_FOUND)
    include_directories(${UHD_INCLUDE_DIRS})
    link_directories(${UHD_LIBRARY_DIRS})
    list(APPEND GREXTRAS_LIBRARIES ${UHD_LIBRARIES})
    add_definitions(-DHAVE_UHD)
endif()

########################################################################
# Optional OpenCL
########################################################################
if(OPENCL_FOUND)
    include_directories(${OPENCL_INCLUDE_DIRS})
    list(APPEND GREXTRAS_LIBRARIES ${OPENCL_LIBRARIES})
    add_definitions(-DHAVE_OPENCL)
    #the following definition is supposed to be a harmless fix
    #http://www.khronos.org/message_boards/showthread.php/7931
    add_definitions(-DCL_USE_DEPRECATED_OPENCL_1_1_APIS)
endif()

########################################################################
# Optional ORC
########################################################################
if(ORC_FOUND)
    include_directories(${ORC_INCLUDE_DIRS})
    list(APPEND GREXTRAS_LIBRARIES ${ORC_LIBRARIES})
    add_definitions(-DHAVE_ORC)
endif()

########################################################################
# Optional Clang
########################################################################
if(CLANG_FOUND)
    add_definitions(${LLVM_CFLAGS})
    link_directories(${LLVM_LIBRARY_DIRS})
    include_directories(${LLVM_INCLUDE_DIRS})
    list(APPEND GREXTRAS_LIBRARIES ${LLVM_MODULE_LIBS})
    list(APPEND GREXTRAS_LIBRARIES ${LLVM_LDFLAGS})
    SET_SOURCE_FILES_PROPERTIES(
        ${CMAKE_CURRENT_SOURCE_DIR}/clang_block.cpp
        PROPERTIES COMPILE_DEFINITIONS "CLANG_EXECUTABLE=${CLANG_EXECUTABLE}"
    )
    add_definitions(-DHAVE_CLANG)
endif()

########################################################################
# Build library
########################################################################
add_library(grextras SHARED ${GREXTRAS_SOURCES})
target_link_libraries(grextras ${GREXTRAS_LIBRARIES})
set_target_properties(grextras PROPERTIES VERSION ${GREXTRAS_VERSION})
set_target_properties(grextras PROPERTIES DEFINE_SYMBOL "GREXTRAS_DLL_EXPORTS")

########################################################################
# Install library
########################################################################
install(TARGETS grextras
    LIBRARY DESTINATION lib${LIB_SUFFIX} COMPONENT "extras_runtime" # .so file
    ARCHIVE DESTINATION lib${LIB_SUFFIX} COMPONENT "extras_devel"   # .lib file
    RUNTIME DESTINATION bin              COMPONENT "extras_runtime" # .dll file
)

########################################################################
# Build pkg config file
########################################################################
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/grextras.pc.in
    ${CMAKE_CURRENT_BINARY_DIR}/grextras.pc
@ONLY)

install(
    FILES ${CMAKE_CURRENT_BINARY_DIR}/grextras.pc
    DESTINATION lib${LIB_SUFFIX}/pkgconfig
    COMPONENT "extras_devel"
)
