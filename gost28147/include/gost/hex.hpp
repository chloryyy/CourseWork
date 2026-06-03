#ifndef GOST_HEX_HPP
#define GOST_HEX_HPP

#include <cstdint>
#include <stdexcept>
#include <string>
#include <vector>

namespace gost {

// Преобразование массива байт в шестнадцатеричную строку.
inline std::string to_hex(const std::uint8_t* data, std::size_t len) {
    static const char* digits = "0123456789abcdef";
    std::string out;
    out.reserve(len * 2);
    for (std::size_t i = 0; i < len; ++i) {
        out.push_back(digits[data[i] >> 4]);
        out.push_back(digits[data[i] & 0xF]);
    }
    return out;
}

template <typename Container>
std::string to_hex(const Container& c) {
    return to_hex(c.data(), c.size());
}

// Разбор шестнадцатеричной строки в массив байт. Пробелы игнорируются.
inline std::vector<std::uint8_t> from_hex(const std::string& hex) {
    auto nibble = [](char ch) -> int {
        if (ch >= '0' && ch <= '9') return ch - '0';
        if (ch >= 'a' && ch <= 'f') return ch - 'a' + 10;
        if (ch >= 'A' && ch <= 'F') return ch - 'A' + 10;
        return -1;
    };
    std::vector<std::uint8_t> out;
    int hi = -1;
    for (char ch : hex) {
        if (ch == ' ' || ch == '\t' || ch == '\n' || ch == '\r') {
            continue;
        }
        int v = nibble(ch);
        if (v < 0) {
            throw std::invalid_argument("invalid hex character");
        }
        if (hi < 0) {
            hi = v;
        } else {
            out.push_back(static_cast<std::uint8_t>((hi << 4) | v));
            hi = -1;
        }
    }
    if (hi >= 0) {
        throw std::invalid_argument("hex string has odd number of digits");
    }
    return out;
}

}  // namespace gost

#endif  // GOST_HEX_HPP
