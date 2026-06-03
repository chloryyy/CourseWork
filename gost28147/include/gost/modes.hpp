#ifndef GOST_MODES_HPP
#define GOST_MODES_HPP

#include <cstdint>
#include <vector>

#include "gost/gost28147.hpp"

namespace gost {

using Bytes = std::vector<std::uint8_t>;
// Синхропосылка для режимов гаммирования — 64-битовый элемент данных.
using Sync = Block;

// Режим простой замены (ECB). Размер данных должен быть кратен 8 байтам.
class SimpleReplacement {
public:
    explicit SimpleReplacement(const Gost28147& cipher) : cipher_(cipher) {}

    Bytes encrypt(const Bytes& plaintext) const;
    Bytes decrypt(const Bytes& ciphertext) const;

private:
    const Gost28147& cipher_;
};

// Режим гаммирования. Зашифрование и расшифрование выполняются одной и той же
// операцией. Поддерживается неполный последний блок (данные произвольной длины).
class Gamma {
public:
    explicit Gamma(const Gost28147& cipher) : cipher_(cipher) {}

    // Наложение/снятие гаммы. process(process(x)) == x при той же синхропосылке.
    Bytes process(const Bytes& data, const Sync& sync) const;

    Bytes encrypt(const Bytes& data, const Sync& sync) const { return process(data, sync); }
    Bytes decrypt(const Bytes& data, const Sync& sync) const { return process(data, sync); }

private:
    const Gost28147& cipher_;
};

// Режим гаммирования с обратной связью (CFB). Поддерживается неполный
// последний блок.
class GammaFeedback {
public:
    explicit GammaFeedback(const Gost28147& cipher) : cipher_(cipher) {}

    Bytes encrypt(const Bytes& plaintext, const Sync& sync) const;
    Bytes decrypt(const Bytes& ciphertext, const Sync& sync) const;

private:
    const Gost28147& cipher_;
};

// Режим выработки имитовставки (MAC). Длина имитовставки задаётся в байтах
// (1..8, обычно 4 — 32 бита).
class Mac {
public:
    explicit Mac(const Gost28147& cipher) : cipher_(cipher) {}

    Bytes compute(const Bytes& data, std::size_t mac_size = 4) const;

private:
    const Gost28147& cipher_;
};

}  // namespace gost

#endif  // GOST_MODES_HPP
