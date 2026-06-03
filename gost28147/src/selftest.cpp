// Встроенные тест-векторы ГОСТ 28147-89.
//
// Источники:
//  * Официальные векторы простой замены из примеров ГОСТ Р 34.11-94
//    (RFC 5831 / OpenSSL ccgost) — проверяют ядро шифра.
//  * Векторы для режимов гаммирования, гаммирования с обратной связью и
//    выработки имитовставки получены независимой эталонной реализацией,
//    сверенной с OpenSSL/CryptoPro.

#include "gost/selftest.hpp"

#include <cstddef>
#include <ostream>
#include <stdexcept>
#include <string>

#include "gost/gost28147.hpp"
#include "gost/hex.hpp"
#include "gost/modes.hpp"
#include "gost/substitution_table.hpp"

namespace gost {

namespace {

struct Counters {
    int checks = 0;
    int failures = 0;
};

void check_eq(std::ostream& os, Counters& c, const std::string& name,
              const std::string& got, const std::string& expected) {
    ++c.checks;
    if (got == expected) {
        os << "[ OK ] " << name << "\n";
    } else {
        ++c.failures;
        os << "[FAIL] " << name << "\n        got: " << got
           << "\n        exp: " << expected << "\n";
    }
}

void check_true(std::ostream& os, Counters& c, const std::string& name, bool cond) {
    ++c.checks;
    if (cond) {
        os << "[ OK ] " << name << "\n";
    } else {
        ++c.failures;
        os << "[FAIL] " << name << "\n";
    }
}

Key key_from_hex(const std::string& hex) {
    auto bytes = from_hex(hex);
    Key key{};
    for (std::size_t i = 0; i < key.size(); ++i) key[i] = bytes[i];
    return key;
}

Block block_from_hex(const std::string& hex) {
    auto bytes = from_hex(hex);
    Block b{};
    for (std::size_t i = 0; i < b.size(); ++i) b[i] = bytes[i];
    return b;
}

Bytes bytes_from_hex(const std::string& hex) {
    auto v = from_hex(hex);
    return Bytes(v.begin(), v.end());
}

std::string ecb_block(const SubstitutionTable& sbox, const std::string& key_hex,
                      const std::string& pt_hex) {
    Gost28147 cipher(key_from_hex(key_hex), sbox);
    return to_hex(cipher.encrypt_block(block_from_hex(pt_hex)));
}

struct ModeVectors {
    const char* sbox_name;
    SubstitutionTable sbox;
    const char* ecb_ct;
    const char* gamma_ct;
    const char* cfb_ct;
    const char* mac;
};

}  // namespace

int run_selftests(std::ostream& os) {
    Counters c;

    check_true(os, c, "sbox GostR3411_94_TestParamSet valid",
               SubstitutionTable::gostR3411_94_TestParamSet().is_valid());
    check_true(os, c, "sbox Gost28147_TestParamSet valid",
               SubstitutionTable::gost28147_TestParamSet().is_valid());
    check_true(os, c, "sbox Gost28147_CryptoProParamSetA valid",
               SubstitutionTable::gost28147_CryptoProParamSetA().is_valid());

    // Официальные одно-блочные векторы простой замены (ГОСТ Р 34.11-94).
    const auto sbox411 = SubstitutionTable::gostR3411_94_TestParamSet();
    check_eq(os, c, "official ECB #1",
             ecb_block(sbox411,
                       "546d203368656c3269736520"
                       "73736e622061677969677474"
                       "73656865202c3d73",
                       "0000000000000000"),
             "1b0bbc32cebcab42");
    check_eq(os, c, "official ECB #2",
             ecb_block(sbox411,
                       "ec0a8ba15ec004a8bac50cac"
                       "0c621deee1c7b8e7007ae2ecf2731bff4e80e2a0",
                       "0000000000000000"),
             "2d562a0d190486e7");
    check_eq(os, c, "official ECB #3",
             ecb_block(sbox411,
                       "348724a4c1a6766715"
                       "3dde5933884250e3248c657d413b8c1c9ca09a56d968cf",
                       "34c01533e37d1c56"),
             "863e78dd2d60d13c");

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
         SubstitutionTable::gostR3411_94_TestParamSet(),
         "f798ce8acd160f09789738dd0343bd7a",
         "5524c55f96f38de0d6acbd89f95eebba5f1cf677",
         "2d0fb00ddd131b44ebf87df4ef83e8e291454335",
         "82e06877"},
        {"Gost28147_TestParamSet",
         SubstitutionTable::gost28147_TestParamSet(),
         "d2f582d4bd16097e9c32401427bcf681",
         "dfd7bef81212d5aa6421015317a45b28b63ebb5d",
         "f1eda97a782d2205d9191fbeaee91e8df99fa42e",
         "eaff3c1c"},
    };

    for (const auto& v : vectors) {
        const std::string tag = std::string("[") + v.sbox_name + "] ";
        Gost28147 cipher(key_from_hex(KEY), v.sbox);

        SimpleReplacement ecb(cipher);
        Bytes ecb_ct = ecb.encrypt(bytes_from_hex(ECB_PT));
        check_eq(os, c, tag + "simple replacement encrypt", to_hex(ecb_ct), v.ecb_ct);
        check_eq(os, c, tag + "simple replacement round-trip",
                 to_hex(ecb.decrypt(ecb_ct)), ECB_PT);

        Gamma gamma(cipher);
        Sync sync = block_from_hex(IV);
        Bytes gamma_ct = gamma.encrypt(bytes_from_hex(MSG), sync);
        check_eq(os, c, tag + "gamma encrypt", to_hex(gamma_ct), v.gamma_ct);
        check_eq(os, c, tag + "gamma round-trip",
                 to_hex(gamma.decrypt(gamma_ct, sync)), MSG);

        GammaFeedback cfb(cipher);
        Bytes cfb_ct = cfb.encrypt(bytes_from_hex(MSG), sync);
        check_eq(os, c, tag + "gamma feedback encrypt", to_hex(cfb_ct), v.cfb_ct);
        check_eq(os, c, tag + "gamma feedback round-trip",
                 to_hex(cfb.decrypt(cfb_ct, sync)), MSG);

        Mac mac(cipher);
        check_eq(os, c, tag + "mac (32 bit)",
                 to_hex(mac.compute(bytes_from_hex(MAC_MSG), 4)), v.mac);
    }

    // Проверка обработки ошибок: простая замена требует размер, кратный 8.
    {
        Gost28147 cipher(Key{}, SubstitutionTable::gost28147_TestParamSet());
        SimpleReplacement ecb(cipher);
        bool threw = false;
        try {
            ecb.encrypt(Bytes(5, 0));
        } catch (const std::invalid_argument&) {
            threw = true;
        }
        check_true(os, c, "simple replacement rejects non-multiple-of-8 size", threw);
    }

    os << "\n" << (c.checks - c.failures) << "/" << c.checks << " checks passed.\n";
    if (c.failures != 0) {
        os << c.failures << " FAILED\n";
    } else {
        os << "All tests passed.\n";
    }
    return c.failures;
}

}  // namespace gost
