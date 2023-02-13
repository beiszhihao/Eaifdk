cmake_minimum_required(VERSION 3.20)

project(efdk)

include_directories(${CMAKE_BINARY_DIR}/tools/efdk/lib/gflags/include)

link_directories(${CMAKE_BINARY_DIR}/tools/efdk/lib/gflags)

link_libraries(libgflags_nothreads.a)


add_executable(efdk func/main.cpp)

SET(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/../../../bin)
