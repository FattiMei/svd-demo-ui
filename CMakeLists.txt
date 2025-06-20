cmake_minimum_required(VERSION 3.10)
project(svd-demo-ui VERSION 1.0)


set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)


add_compile_options(-Wall -Wextra -Wpedantic)


find_package(glfw3 3.3 REQUIRED)
find_package(OpenGL REQUIRED)


set(EXE_NAME "demo")
set(INCLUDE_DIR "${CMAKE_SOURCE_DIR}/include")
file(GLOB SRC "${CMAKE_SOURCE_DIR}/src/*.cpp")

add_executable(${EXE_NAME}
	src/main.cpp
	src/window.cpp
)
target_include_directories(${EXE_NAME} PRIVATE ${INCLUDE_DIR})
target_link_libraries(${EXE_NAME} PRIVATE glfw)
target_link_libraries(${EXE_NAME} PRIVATE OpenGL::GL)
