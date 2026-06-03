#include "gost/gost28147.hpp"

namespace gost {

namespace {

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

// Циклический сдвиг влево на 11 бит (шаг 3 основного шага).
std::uint32_t rotl11(std::uint32_t x) {
    return (x << 11) | (x >> (32 - 11));
}

}  // namespace

Gost28147::Gost28147(const Key& key, const SubstitutionTable& sbox)
    : sbox_(sbox) {
    for (int i = 0; i < 8; ++i) {
        key_[i] = load_le32(key.data() + 4 * i);
    }
}

Gost28147::Halves Gost28147::split(const Block& in) {
    return Halves{load_le32(in.data()), load_le32(in.data() + 4)};
}

Block Gost28147::join(Halves state) {
    Block out{};
    store_le32(out.data(), state.n1);
    store_le32(out.data() + 4, state.n2);
    return out;
}

Gost28147::Halves Gost28147::main_step(Halves state, std::uint32_t round_key) const {
    // Шаг 1. Сложение младшей половины с элементом ключа по модулю 2^32.
    std::uint32_t s = state.n1 + round_key;
    // Шаг 2. Поблочная замена по таблице замен.
    s = sbox_.substitute(s);
    // Шаг 3. Циклический сдвиг на 11 бит влево.
    s = rotl11(s);
    // Шаг 4. Побитовое сложение со старшей половиной.
    s ^= state.n2;
    // Шаг 5. Сдвиг по цепочке.
    return Halves{s, state.n1};
}

Block Gost28147::encrypt_block(const Block& in) const {
    Halves st = split(in);
    // Цикл 32-З: K0..K7 трижды, затем K7..K0.
    for (int rep = 0; rep < 3; ++rep) {
        for (int i = 0; i < 8; ++i) {
            st = main_step(st, key_[i]);
        }
    }
    for (int i = 7; i >= 0; --i) {
        st = main_step(st, key_[i]);
    }
    // На последнем шаге цикла перестановка половин не производится: эквивалентно
    // одной обратной перестановке после 32 шагов со сдвигом по цепочке.
    return join(Halves{st.n2, st.n1});
}

Block Gost28147::decrypt_block(const Block& in) const {
    Halves st = split(in);
    // Цикл 32-Р: K0..K7 один раз, затем K7..K0 трижды.
    for (int i = 0; i < 8; ++i) {
        st = main_step(st, key_[i]);
    }
    for (int rep = 0; rep < 3; ++rep) {
        for (int i = 7; i >= 0; --i) {
            st = main_step(st, key_[i]);
        }
    }
    return join(Halves{st.n2, st.n1});
}

Block Gost28147::mac_transform(const Block& in) const {
    Halves st = split(in);
    // Цикл 16-З: K0..K7 дважды. Финальная перестановка половин не выполняется.
    for (int rep = 0; rep < 2; ++rep) {
        for (int i = 0; i < 8; ++i) {
            st = main_step(st, key_[i]);
        }
    }
    return join(st);
}

}  // namespace gost
