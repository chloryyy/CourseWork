cmake_minimum_required(VERSION 3.15)
project(gost28147 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(MSVC)
    add_compile_options(/W4 /utf-8)
else()
    add_compile_options(-Wall -Wextra)
endif()

# Ядро библиотеки: основной шаг, базовые циклы, таблицы замен, режимы.
add_library(gost_core
    src/substitution_table.cpp
    src/gost28147.cpp
    src/modes.cpp
    src/selftest.cpp
)
target_include_directories(gost_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)

# Демонстрационная программа.
add_executable(gost_demo app/main.cpp)
target_link_libraries(gost_demo PRIVATE gost_core)

# Тесты.
enable_testing()
add_executable(gost_tests tests/test_gost.cpp)
target_link_libraries(gost_tests PRIVATE gost_core)
add_test(NAME gost_tests COMMAND gost_tests)
