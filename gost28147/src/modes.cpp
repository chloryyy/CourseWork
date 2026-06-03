#include "gost/modes.hpp"

#include <algorithm>
#include <stdexcept>

namespace gost {

namespace {

constexpr std::uint32_t kGammaConstLow = 0x01010101;   // C2: к младшей половине
constexpr std::uint32_t kGammaConstHigh = 0x01010104;  // C1: к старшей половине

std::uint32_t load_le32(const std::uint8_t* p) {
    return static_cast<std::uint32_t>(p[0]) |
           (static_cast<std::uint32_t>(p[1]) << 8) |
           (static_cast<std::uint32_t>(p[2]) << 16) |
           (static_cast<std::uint32_t>(p[3]) << 24);
}

void store_le32(std::uint8_t* p, std::uint32_t v) {
    p[0] = static_cast<std::uint8_t>(v & 0xFF);
    p[1] = static_cast<std::uint8_t>((v >> 8) & 0xFF);
    p[2] = static_cast<std::uint8_t>((v >> 16) & 0xFF);
    p[3] = static_cast<std::uint8_t>((v >> 24) & 0xFF);
}

// Один шаг рекуррентного генератора псевдослучайных чисел (РГПЧ).
// Младшая половина: (N1 + C2) mod 2^32.
// Старшая половина: (N2 + C1) mod (2^32 - 1) с учётом особого правила ГОСТ
// (значение 2^32-1 не заменяется на 0), что эквивалентно прибавлению 1 при
// переполнении.
void gamma_next(Block& state) {
    std::uint32_t lo = load_le32(state.data());
    lo += kGammaConstLow;
    store_le32(state.data(), lo);

    std::uint32_t hi = load_le32(state.data() + 4);
    std::uint32_t prev = hi;
    hi += kGammaConstHigh;
    if (prev > hi) {  // переполнение -> модуль (2^32 - 1)
        ++hi;
    }
    store_le32(state.data() + 4, hi);
}

}  // namespace

Bytes SimpleReplacement::encrypt(const Bytes& plaintext) const {
    if (plaintext.size() % 8 != 0) {
        throw std::invalid_argument(
            "simple replacement: data size must be a multiple of 8 bytes");
    }
    Bytes out(plaintext.size());
    for (std::size_t i = 0; i < plaintext.size(); i += 8) {
        Block in{};
        for (int j = 0; j < 8; ++j) in[j] = plaintext[i + j];
        Block enc = cipher_.encrypt_block(in);
        for (int j = 0; j < 8; ++j) out[i + j] = enc[j];
    }
    return out;
}

Bytes SimpleReplacement::decrypt(const Bytes& ciphertext) const {
    if (ciphertext.size() % 8 != 0) {
        throw std::invalid_argument(
            "simple replacement: data size must be a multiple of 8 bytes");
    }
    Bytes out(ciphertext.size());
    for (std::size_t i = 0; i < ciphertext.size(); i += 8) {
        Block in{};
        for (int j = 0; j < 8; ++j) in[j] = ciphertext[i + j];
        Block dec = cipher_.decrypt_block(in);
        for (int j = 0; j < 8; ++j) out[i + j] = dec[j];
    }
    return out;
}

Bytes Gamma::process(const Bytes& data, const Sync& sync) const {
    // Начальное заполнение РГПЧ: Ω0 = Ц32-З(S).
    Block state = cipher_.encrypt_block(sync);
    Bytes out(data.size());
    for (std::size_t i = 0; i < data.size(); i += 8) {
        gamma_next(state);
        Block gamma = cipher_.encrypt_block(state);
        const std::size_t n = std::min<std::size_t>(8, data.size() - i);
        for (std::size_t j = 0; j < n; ++j) {
            out[i + j] = data[i + j] ^ gamma[j];
        }
    }
    return out;
}

Bytes GammaFeedback::encrypt(const Bytes& plaintext, const Sync& sync) const {
    Block cur = sync;
    Bytes out(plaintext.size());
    for (std::size_t i = 0; i < plaintext.size(); i += 8) {
        Block gamma = cipher_.encrypt_block(cur);
        const std::size_t n = std::min<std::size_t>(8, plaintext.size() - i);
        for (std::size_t j = 0; j < n; ++j) {
            out[i + j] = plaintext[i + j] ^ gamma[j];
        }
        // Обратная связь: очередной блок шифртекста становится входом для
        // следующего элемента гаммы (для полного блока).
        if (n == 8) {
            for (std::size_t j = 0; j < 8; ++j) cur[j] = out[i + j];
        }
    }
    return out;
}

Bytes GammaFeedback::decrypt(const Bytes& ciphertext, const Sync& sync) const {
    Block cur = sync;
    Bytes out(ciphertext.size());
    for (std::size_t i = 0; i < ciphertext.size(); i += 8) {
        Block gamma = cipher_.encrypt_block(cur);
        const std::size_t n = std::min<std::size_t>(8, ciphertext.size() - i);
        for (std::size_t j = 0; j < n; ++j) {
            out[i + j] = ciphertext[i + j] ^ gamma[j];
        }
        if (n == 8) {
            for (std::size_t j = 0; j < 8; ++j) cur[j] = ciphertext[i + j];
        }
    }
    return out;
}

Bytes Mac::compute(const Bytes& data, std::size_t mac_size) const {
    if (mac_size < 1 || mac_size > 8) {
        throw std::invalid_argument("mac size must be in range 1..8 bytes");
    }
    Block buffer{};  // нулевое начальное заполнение
    std::size_t i = 0;
    const std::size_t n = data.size();
    // Каждый блок (последний неполный дополняется нулями) складывается по
    // модулю 2 с накопителем и пропускается через цикл 16-З.
    do {
        Block block{};
        for (std::size_t j = 0; j < 8 && i + j < n; ++j) {
            block[j] = data[i + j];
        }
        for (int j = 0; j < 8; ++j) buffer[j] ^= block[j];
        buffer = cipher_.mac_transform(buffer);
        i += 8;
    } while (i < n);

    Bytes out(mac_size);
    for (std::size_t j = 0; j < mac_size; ++j) out[j] = buffer[j];
    return out;
}

}  // namespace gost
