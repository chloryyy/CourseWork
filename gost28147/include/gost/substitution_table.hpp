#ifndef GOST_SUBSTITUTION_TABLE_HPP
#define GOST_SUBSTITUTION_TABLE_HPP

#include <array>
#include <cstdint>

namespace gost {

// Таблица замен (H) ГОСТ 28147-89.
//
// Это матрица 8x16 из 4-битовых значений. Строка таблицы называется "узлом
// замен"; узел с номером i применяется к i-му (нумерация с нуля) 4-битовому
// блоку 32-битового слова, где блок 0 — это младшие 4 бита.
//
// Хранение в "узловом" порядке: rows_[0] — узел 0 (младший нибл),
// rows_[7] — узел 7 (старший нибл). Каждый узел обязан содержать перестановку
// чисел 0..15.
class SubstitutionTable {
public:
    using Node = std::array<std::uint8_t, 16>;
    using Rows = std::array<Node, 8>;

    SubstitutionTable() = default;
    explicit SubstitutionTable(const Rows& rows) : rows_(rows) {}

    // Применение таблицы замен к 32-битовому значению (шаг 2 основного шага).
    std::uint32_t substitute(std::uint32_t value) const {
        std::uint32_t result = 0;
        for (int i = 0; i < 8; ++i) {
            const std::uint32_t nibble = (value >> (4 * i)) & 0xF;
            result |= static_cast<std::uint32_t>(rows_[i][nibble]) << (4 * i);
        }
        return result;
    }

    const Rows& rows() const { return rows_; }

    // Проверка, что каждый узел является перестановкой 0..15.
    bool is_valid() const;

    // Стандартные наборы узлов замен.
    // Тестовый набор из примеров ГОСТ Р 34.11-94 (используется в официальных
    // тест-векторах простой замены).
    static SubstitutionTable gostR3411_94_TestParamSet();
    // Тестовый набор из ГОСТ 28147-89.
    static SubstitutionTable gost28147_TestParamSet();
    // Набор узлов CryptoPro A (id 1.2.643.2.2.31.1).
    static SubstitutionTable gost28147_CryptoProParamSetA();

private:
    Rows rows_{};
};

}  // namespace gost

#endif  // GOST_SUBSTITUTION_TABLE_HPP
