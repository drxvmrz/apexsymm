cmake_minimum_required(VERSION 3.10)

project(apexcore)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS YES)

#[[ ============== Common =============== ]]
set(CMAKE_BUILD_TYPE Release)

include_directories("../inc")

file(GLOB SRCS_C "*.c") # [[ collect or .c-files in ./src ]]
file(GLOB SRCS_CPP "*.cpp") # [[ collect or .cpp-files ./src ]]

#[[ =========== WINDOWS (MSVC) ========== ]]
if(WIN32)
include_directories("YOUR FULL PATH TO EIGEN LIB includes")
include_directories("YOUR FULL PATH TO FFTW/FFTW3 includes")

link_directories("YOUR FULL PATH TO FFTW DIR")

if(CMAKE_BUILD_TYPE STREQUAL "Debug")
message("Compiling as Debug for Win32/Win64")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} /openmp")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /openmp")
else()
message("Compiling as Release for Win32/Win64")
set(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE} /O2 /DNDEBUG /sdl /openmp")
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /O2 /DNDEBUG /sdl /openmp")
set(CMAKE_EXE_LINKER_FLAGS_RELEASE "${CMAKE_EXE_LINKER_FLAGS_RELEASE} /DEBUG:NONE")
endif()

add_executable(apexcore_win ${SRCS_C} ${SRCS_CPP})
target_link_libraries(apexcore_win libfftw3-3)
endif()

#[[ =========== MACOSX (brew) =========== ]]
if(APPLE)

# It used a HOMEBREW lipomp and llvm by default
set(LLVM_PATH "/opt/homebrew/opt/llvm")
set(OPENMP_PATH "/opt/homebrew/opt/libomp")
set(CMAKE_C_COMPILER "${LLVM_PATH}/bin/clang")
set(CMAKE_CXX_COMPILER "${LLVM_PATH}/bin/clang++")

# flags
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
message("Compiling as Debug for MacOS X")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fopenmp")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fopenmp")
else()
message("Compiling as Release for MacOS X")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O2 -DNDEBUG -fopenmp")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O2 -DNDEBUG -fopenmp")
endif()

include_directories("/opt/homebrew/include")
include_directories("/opt/homebrew/include/eigen3")
include_directories("${OPENMP_PATH}/include")

link_directories("/opt/homebrew/lib")
link_directories("${OPENMP_PATH}/lib")

add_executable(apexcore_mac ${SRCS_C} ${SRCS_CPP})
target_link_libraries(apexcore_mac PRIVATE libfftw3.a libomp.a)
endif(APPLE)

#[[ ================ LINUX ============== ]]
if(UNIX AND NOT APPLE)

include_directories("YOUR FULL PATH TO EIGEN LIBS includes")

if(CMAKE_BUILD_TYPE STREQUAL "Debug")
message("Compiling as Debug for Linux")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fopenmp")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fopenmp")
else()
message("Compiling as Release for Linux")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O2 -DNDEBUG -fopenmp")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O2 -DNDEBUG -fopenmp")
endif()

add_executable(apexcore_lnx ${SRCS_C} ${SRCS_CPP})
target_link_libraries(apexcore_lnx fftw3)
endif(UNIX AND NOT APPLE)