// Модульные тесты для реализации ГОСТ 28147-89.
//
// Источники тест-векторов:
//  * Официальные векторы простой замены из примеров ГОСТ Р 34.11-94
//    (RFC 5831 / OpenSSL ccgost) — проверяют ядро шифра.
//  * Векторы для режимов гаммирования, гаммирования с обратной связью и
//    выработки имитовставки получены независимой эталонной реализацией,
//    сверенной с OpenSSL/CryptoPro, и зафиксированы здесь.

#include <cstdlib>
#include <iostream>
#include <string>

#include "gost/gost28147.hpp"
#include "gost/hex.hpp"
#include "gost/modes.hpp"
#include "gost/substitution_table.hpp"

namespace {

int g_failures = 0;
int g_checks = 0;

void check_eq(const std::string& name, const std::string& got,
              const std::string& expected) {
    ++g_checks;
    if (got == expected) {
        std::cout << "[ OK ] " << name << "\n";
    } else {
        ++g_failures;
        std::cout << "[FAIL] " << name << "\n        got: " << got
                  << "\n        exp: " << expected << "\n";
    }
}

void check_true(const std::string& name, bool cond) {
    ++g_checks;
    if (cond) {
        std::cout << "[ OK ] " << name << "\n";
    } else {
        ++g_failures;
        std::cout << "[FAIL] " << name << "\n";
    }
}

gost::Key key_from_hex(const std::string& hex) {
    auto bytes = gost::from_hex(hex);
    gost::Key key{};
    for (std::size_t i = 0; i < key.size(); ++i) key[i] = bytes[i];
    return key;
}

gost::Block block_from_hex(const std::string& hex) {
    auto bytes = gost::from_hex(hex);
    gost::Block b{};
    for (std::size_t i = 0; i < b.size(); ++i) b[i] = bytes[i];
    return b;
}

gost::Bytes bytes_from_hex(const std::string& hex) {
    auto v = gost::from_hex(hex);
    return gost::Bytes(v.begin(), v.end());
}

// Один блок простой замены, hex -> hex.
std::string ecb_block(const gost::SubstitutionTable& sbox, const std::string& key_hex,
                      const std::string& pt_hex) {
    gost::Gost28147 cipher(key_from_hex(key_hex), sbox);
    return gost::to_hex(cipher.encrypt_block(block_from_hex(pt_hex)));
}

void test_substitution_tables() {
    check_true("sbox GostR3411_94_TestParamSet valid",
               gost::SubstitutionTable::gostR3411_94_TestParamSet().is_valid());
    check_true("sbox Gost28147_TestParamSet valid",
               gost::SubstitutionTable::gost28147_TestParamSet().is_valid());
    check_true("sbox Gost28147_CryptoProParamSetA valid",
               gost::SubstitutionTable::gost28147_CryptoProParamSetA().is_valid());
}

// Официальные одно-блочные векторы простой замены (ГОСТ Р 34.11-94).
void test_official_ecb_vectors() {
    const auto sbox = gost::SubstitutionTable::gostR3411_94_TestParamSet();
    check_eq("official ECB #1",
             ecb_block(sbox,
                       "546d203368656c3269736520"
                       "73736e622061677969677474"
                       "73656865202c3d73",
                       "0000000000000000"),
             "1b0bbc32cebcab42");
    check_eq("official ECB #2",
             ecb_block(sbox,
                       "ec0a8ba15ec004a8bac50cac"
                       "0c621deee1c7b8e7007ae2ecf2731bff4e80e2a0",
                       "0000000000000000"),
             "2d562a0d190486e7");
    check_eq("official ECB #3",
             ecb_block(sbox,
                       "348724a4c1a6766715"
                       "3dde5933884250e3248c657d413b8c1c9ca09a56d968cf",
                       "34c01533e37d1c56"),
             "863e78dd2d60d13c");
}

struct ModeVectors {
    const char* sbox_name;
    gost::SubstitutionTable sbox;
    const char* ecb_ct;
    const char* gamma_ct;
    const char* cfb_ct;
    const char* mac;
};

void test_modes() {
    const std::string KEY =
        "00112233445566778899aabbccddeeff"
        "fedcba98765432101032547698badcfe";
    const std::string IV = "1234567890abcdef";
    const std::string ECB_PT = "112233445566778899aabbccddeeff00";
    const std::string MSG = "54686520717569636b2062726f776e20666f7821";  // 20 байт
    const std::string MAC_MSG =
        "474f53542032383134372d383920696d69746f76"
        "737461766b612074657374206d6573736167652e";

    const ModeVectors vectors[] = {
        {"GostR3411_94_TestParamSet",
         gost::SubstitutionTable::gostR3411_94_TestParamSet(),
         "f798ce8acd160f09789738dd0343bd7a",
         "5524c55f96f38de0d6acbd89f95eebba5f1cf677",
         "2d0fb00ddd131b44ebf87df4ef83e8e291454335",
         "82e06877"},
        {"Gost28147_TestParamSet",
         gost::SubstitutionTable::gost28147_TestParamSet(),
         "d2f582d4bd16097e9c32401427bcf681",
         "dfd7bef81212d5aa6421015317a45b28b63ebb5d",
         "f1eda97a782d2205d9191fbeaee91e8df99fa42e",
         "eaff3c1c"},
    };

    for (const auto& v : vectors) {
        const std::string tag = std::string("[") + v.sbox_name + "] ";
        gost::Gost28147 cipher(key_from_hex(KEY), v.sbox);

        // Простая замена.
        gost::SimpleReplacement ecb(cipher);
        gost::Bytes ecb_ct = ecb.encrypt(bytes_from_hex(ECB_PT));
        check_eq(tag + "simple replacement encrypt", gost::to_hex(ecb_ct), v.ecb_ct);
        check_eq(tag + "simple replacement round-trip",
                 gost::to_hex(ecb.decrypt(ecb_ct)), ECB_PT);

        // Гаммирование.
        gost::Gamma gamma(cipher);
        gost::Sync sync = block_from_hex(IV);
        gost::Bytes gamma_ct = gamma.encrypt(bytes_from_hex(MSG), sync);
        check_eq(tag + "gamma encrypt", gost::to_hex(gamma_ct), v.gamma_ct);
        check_eq(tag + "gamma round-trip",
                 gost::to_hex(gamma.decrypt(gamma_ct, sync)), MSG);

        // Гаммирование с обратной связью.
        gost::GammaFeedback cfb(cipher);
        gost::Bytes cfb_ct = cfb.encrypt(bytes_from_hex(MSG), sync);
        check_eq(tag + "gamma feedback encrypt", gost::to_hex(cfb_ct), v.cfb_ct);
        check_eq(tag + "gamma feedback round-trip",
                 gost::to_hex(cfb.decrypt(cfb_ct, sync)), MSG);

        // Имитовставка.
        gost::Mac mac(cipher);
        check_eq(tag + "mac (32 bit)",
                 gost::to_hex(mac.compute(bytes_from_hex(MAC_MSG), 4)), v.mac);
    }
}

void test_error_handling() {
    gost::Gost28147 cipher(gost::Key{},
                           gost::SubstitutionTable::gost28147_TestParamSet());
    gost::SimpleReplacement ecb(cipher);
    bool threw = false;
    try {
        ecb.encrypt(gost::Bytes(5, 0));  // не кратно 8
    } catch (const std::invalid_argument&) {
        threw = true;
    }
    check_true("simple replacement rejects non-multiple-of-8 size", threw);
}

}  // namespace

int main() {
    test_substitution_tables();
    test_official_ecb_vectors();
    test_modes();
    test_error_handling();

    std::cout << "\n" << (g_checks - g_failures) << "/" << g_checks
              << " checks passed.\n";
    if (g_failures != 0) {
        std::cout << g_failures << " FAILED\n";
        return EXIT_FAILURE;
    }
    std::cout << "All tests passed.\n";
    return EXIT_SUCCESS;
}
