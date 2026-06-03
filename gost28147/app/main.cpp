// Демонстрация всех режимов шифрования ГОСТ 28147-89.
//
// Программа не требует аргументов командной строки: она прогоняет фиксированный
// пример через все четыре режима (простая замена, гаммирование, гаммирование с
// обратной связью, выработка имитовставки) и печатает результаты в hex.

#include <iostream>
#include <string>

#include "gost/gost28147.hpp"
#include "gost/hex.hpp"
#include "gost/modes.hpp"
#include "gost/substitution_table.hpp"

namespace {

gost::Key make_key(const std::string& hex) {
    auto bytes = gost::from_hex(hex);
    gost::Key key{};
    for (std::size_t i = 0; i < key.size() && i < bytes.size(); ++i) {
        key[i] = bytes[i];
    }
    return key;
}

gost::Block make_block(const std::string& hex) {
    auto bytes = gost::from_hex(hex);
    gost::Block b{};
    for (std::size_t i = 0; i < b.size() && i < bytes.size(); ++i) {
        b[i] = bytes[i];
    }
    return b;
}

gost::Bytes to_bytes(const std::string& text) {
    return gost::Bytes(text.begin(), text.end());
}

void line() { std::cout << std::string(60, '-') << "\n"; }

}  // namespace

int main() {
    const std::string key_hex =
        "00112233445566778899aabbccddeeff"
        "fedcba98765432101032547698badcfe";
    const gost::Key key = make_key(key_hex);
    const gost::SubstitutionTable sbox =
        gost::SubstitutionTable::gost28147_CryptoProParamSetA();
    const gost::Sync sync = make_block("1234567890abcdef");

    gost::Gost28147 cipher(key, sbox);

    std::cout << "ГОСТ 28147-89 — демонстрация режимов\n";
    line();
    std::cout << "Ключ (256 бит): " << key_hex << "\n";
    std::cout << "Таблица замен : Gost28147_CryptoProParamSetA\n";
    std::cout << "Синхропосылка : " << gost::to_hex(sync) << "\n";
    line();

    // 1. Простая замена (данные кратны 8 байтам).
    {
        gost::Bytes pt = gost::from_hex("112233445566778899aabbccddeeff00");
        gost::SimpleReplacement mode(cipher);
        gost::Bytes ct = mode.encrypt(pt);
        gost::Bytes back = mode.decrypt(ct);
        std::cout << "1) Простая замена\n";
        std::cout << "   открытый  : " << gost::to_hex(pt) << "\n";
        std::cout << "   шифр      : " << gost::to_hex(ct) << "\n";
        std::cout << "   расшифр.  : " << gost::to_hex(back) << "\n";
    }
    line();

    const std::string message = "ГОСТ 28147-89: gamma mode demo!";

    // 2. Гаммирование (произвольная длина).
    {
        gost::Bytes pt = to_bytes(message);
        gost::Gamma mode(cipher);
        gost::Bytes ct = mode.encrypt(pt, sync);
        gost::Bytes back = mode.decrypt(ct, sync);
        std::cout << "2) Гаммирование\n";
        std::cout << "   открытый  : " << gost::to_hex(pt) << "\n";
        std::cout << "   шифр      : " << gost::to_hex(ct) << "\n";
        std::cout << "   расшифр.  : " << gost::to_hex(back) << "\n";
        std::cout << "   текст     : "
                  << std::string(back.begin(), back.end()) << "\n";
    }
    line();

    // 3. Гаммирование с обратной связью.
    {
        gost::Bytes pt = to_bytes(message);
        gost::GammaFeedback mode(cipher);
        gost::Bytes ct = mode.encrypt(pt, sync);
        gost::Bytes back = mode.decrypt(ct, sync);
        std::cout << "3) Гаммирование с обратной связью\n";
        std::cout << "   открытый  : " << gost::to_hex(pt) << "\n";
        std::cout << "   шифр      : " << gost::to_hex(ct) << "\n";
        std::cout << "   расшифр.  : " << gost::to_hex(back) << "\n";
        std::cout << "   текст     : "
                  << std::string(back.begin(), back.end()) << "\n";
    }
    line();

    // 4. Выработка имитовставки.
    {
        gost::Bytes data = to_bytes(message);
        gost::Mac mode(cipher);
        gost::Bytes mac = mode.compute(data, 4);
        std::cout << "4) Имитовставка (32 бита)\n";
        std::cout << "   данные    : " << gost::to_hex(data) << "\n";
        std::cout << "   имитовст. : " << gost::to_hex(mac) << "\n";
    }
    line();

    return 0;
}
