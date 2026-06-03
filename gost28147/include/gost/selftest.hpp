#ifndef GOST_SELFTEST_HPP
#define GOST_SELFTEST_HPP

#include <ostream>

namespace gost {

// Прогон встроенных тест-векторов ГОСТ 28147-89. Печатает результат каждой
// проверки в поток os и возвращает число непройденных проверок (0 — успех).
int run_selftests(std::ostream& os);

}  // namespace gost

#endif  // GOST_SELFTEST_HPP
