#ifndef GOST_GOST28147_HPP
#define GOST_GOST28147_HPP

#include <array>
#include <cstdint>

#include "gost/substitution_table.hpp"

namespace gost {

// 64-битовый блок данных как 8 байт.
using Block = std::array<std::uint8_t, 8>;
// 256-битовый ключ как 32 байта.
using Key = std::array<std::uint8_t, 32>;

// Ядро ГОСТ 28147-89: основной шаг криптопреобразования и базовые циклы
// (32-З зашифрования, 32-Р расшифрования, 16-З выработки имитовставки).
//
// Объект инкапсулирует ключевую информацию: 256-битовый ключ (восемь
// 32-битовых элементов K0..K7) и таблицу замен.
class Gost28147 {
public:
    Gost28147(const Key& key, const SubstitutionTable& sbox);

    // Простая замена одного 64-битового блока (цикл 32-З).
    Block encrypt_block(const Block& in) const;
    // Простая замена одного 64-битового блока (цикл 32-Р).
    Block decrypt_block(const Block& in) const;

    // Один проход цикла 16-З над 64-битовым блоком. Используется при
    // выработке имитовставки; в отличие от шифрования, перестановка половин
    // в конце не выполняется.
    Block mac_transform(const Block& in) const;

    const SubstitutionTable& sbox() const { return sbox_; }

private:
    // Пара 32-битовых половин блока: n1 — младшая, n2 — старшая.
    struct Halves {
        std::uint32_t n1;
        std::uint32_t n2;
    };

    // Основной шаг криптопреобразования (раздел 3.2 методички) с использованием
    // элемента ключа round_key. Включает "сдвиг по цепочке": новая младшая
    // половина — результат шага, новая старшая — прежняя младшая.
    Halves main_step(Halves state, std::uint32_t round_key) const;

    static Halves split(const Block& in);
    static Block join(Halves state);

    std::array<std::uint32_t, 8> key_{};  // K0..K7
    SubstitutionTable sbox_;
};

}  // namespace gost

#endif  // GOST_GOST28147_HPP
