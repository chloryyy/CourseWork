// Точка входа для модульных тестов: прогон встроенных тест-векторов.
// Вся логика проверок вынесена в gost::run_selftests (src/selftest.cpp),
// чтобы её можно было запускать и из демонстрационной программы.

#include <cstdlib>
#include <iostream>

#include "gost/selftest.hpp"

int main() {
    return gost::run_selftests(std::cout) == 0 ? EXIT_SUCCESS : EXIT_FAILURE;
}
