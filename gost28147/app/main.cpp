// Интерактивная демонстрация ГОСТ 28147-89.
//
// Программа выводит меню и не закрывается, пока пользователь не выберет выход.
// Поддерживаются:
//   * ручной ввод (шифрование/дешифрование текста);
//   * шифрование/дешифрование файлов;
//   * прогон встроенных тест-векторов.
//
// Для корректного отображения кириллицы под Windows консоль переключается в
// кодировку UTF-8.

#include <fstream>
#include <iostream>
#include <string>

#include "gost/gost28147.hpp"
#include "gost/hex.hpp"
#include "gost/modes.hpp"
#include "gost/selftest.hpp"
#include "gost/substitution_table.hpp"

#if defined(_WIN32)
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#endif

namespace {

const std::string kDefaultKey =
    "00112233445566778899aabbccddeeff"
    "fedcba98765432101032547698badcfe";
const std::string kDefaultSync = "1234567890abcdef";

void enable_utf8_console() {
#if defined(_WIN32)
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
#endif
}

// Чтение строки целиком (с учётом пробелов).
std::string read_line() {
    std::string s;
    std::getline(std::cin, s);
    return s;
}

// Чтение целого числа в диапазоне [lo, hi]. При неверном вводе повторяет запрос.
int read_choice(int lo, int hi) {
    for (;;) {
        std::cout << "> ";
        std::string line = read_line();
        if (!std::cin) {
            return lo;  // EOF: выходим по нижней границе
        }
        try {
            std::size_t pos = 0;
            int value = std::stoi(line, &pos);
            if (pos == line.size() && value >= lo && value <= hi) {
                return value;
            }
        } catch (...) {
        }
        std::cout << "Введите число от " << lo << " до " << hi << ".\n";
    }
}

gost::Key read_key() {
    for (;;) {
        std::cout << "Ключ (64 hex-символа, Enter — демо-ключ):\n";
        std::string line = read_line();
        if (line.empty()) {
            line = kDefaultKey;
            std::cout << "Используется демо-ключ: " << kDefaultKey << "\n";
        }
        try {
            auto bytes = gost::from_hex(line);
            if (bytes.size() != 32) {
                std::cout << "Нужно ровно 32 байта (64 hex-символа), получено "
                          << bytes.size() << ".\n";
                continue;
            }
            gost::Key key{};
            for (std::size_t i = 0; i < 32; ++i) key[i] = bytes[i];
            return key;
        } catch (const std::exception&) {
            std::cout << "Ошибка: некорректная hex-строка.\n";
        }
    }
}

gost::Sync read_sync() {
    for (;;) {
        std::cout << "Синхропосылка (16 hex-символов, Enter — демо):\n";
        std::string line = read_line();
        if (line.empty()) {
            line = kDefaultSync;
            std::cout << "Используется демо-синхропосылка: " << kDefaultSync << "\n";
        }
        try {
            auto bytes = gost::from_hex(line);
            if (bytes.size() != 8) {
                std::cout << "Нужно ровно 8 байт (16 hex-символов), получено "
                          << bytes.size() << ".\n";
                continue;
            }
            gost::Sync sync{};
            for (std::size_t i = 0; i < 8; ++i) sync[i] = bytes[i];
            return sync;
        } catch (const std::exception&) {
            std::cout << "Ошибка: некорректная hex-строка.\n";
        }
    }
}

gost::SubstitutionTable read_sbox() {
    std::cout << "Таблица замен:\n"
              << "  1) Gost28147_CryptoProParamSetA (по умолчанию)\n"
              << "  2) Gost28147_TestParamSet\n"
              << "  3) GostR3411_94_TestParamSet\n";
    std::cout << "> ";
    std::string line = read_line();
    if (line == "2") return gost::SubstitutionTable::gost28147_TestParamSet();
    if (line == "3") return gost::SubstitutionTable::gostR3411_94_TestParamSet();
    return gost::SubstitutionTable::gost28147_CryptoProParamSetA();
}

gost::Bytes to_bytes(const std::string& s) {
    return gost::Bytes(s.begin(), s.end());
}

// Дополнение нулями до кратности 8 (для простой замены).
gost::Bytes pad8(const gost::Bytes& in) {
    gost::Bytes out = in;
    while (out.size() % 8 != 0) out.push_back(0);
    return out;
}

int select_mode(bool with_mac) {
    std::cout << "Режим:\n"
              << "  1) Простая замена\n"
              << "  2) Гаммирование\n"
              << "  3) Гаммирование с обратной связью\n";
    if (with_mac) {
        std::cout << "  4) Выработка имитовставки\n";
    }
    return read_choice(1, with_mac ? 4 : 3);
}

void manual_text() {
    std::cout << "\n--- Ручной ввод ---\n";
    std::cout << "Действие:\n  1) Зашифровать\n  2) Расшифровать\n";
    int action = read_choice(1, 2);
    const bool encrypt = (action == 1);

    int mode = select_mode(/*with_mac=*/encrypt);
    gost::SubstitutionTable sbox = read_sbox();
    gost::Key key = read_key();
    gost::Gost28147 cipher(key, sbox);

    gost::Sync sync{};
    if (mode == 2 || mode == 3) {
        sync = read_sync();
    }

    if (encrypt) {
        std::cout << "Введите текст:\n";
        gost::Bytes data = to_bytes(read_line());
        gost::Bytes out;
        switch (mode) {
            case 1: {
                gost::Bytes padded = pad8(data);
                if (padded.size() != data.size()) {
                    std::cout << "(текст дополнен нулями до " << padded.size()
                              << " байт)\n";
                }
                out = gost::SimpleReplacement(cipher).encrypt(padded);
                break;
            }
            case 2:
                out = gost::Gamma(cipher).encrypt(data, sync);
                break;
            case 3:
                out = gost::GammaFeedback(cipher).encrypt(data, sync);
                break;
            case 4: {
                gost::Bytes mac = gost::Mac(cipher).compute(data, 4);
                std::cout << "Имитовставка (32 бита): " << gost::to_hex(mac) << "\n";
                return;
            }
        }
        std::cout << "Результат (hex): " << gost::to_hex(out) << "\n";
    } else {
        std::cout << "Введите шифртекст (hex):\n";
        gost::Bytes data;
        try {
            auto v = gost::from_hex(read_line());
            data.assign(v.begin(), v.end());
        } catch (const std::exception&) {
            std::cout << "Ошибка: некорректная hex-строка.\n";
            return;
        }
        gost::Bytes out;
        try {
            switch (mode) {
                case 1:
                    out = gost::SimpleReplacement(cipher).decrypt(data);
                    break;
                case 2:
                    out = gost::Gamma(cipher).decrypt(data, sync);
                    break;
                case 3:
                    out = gost::GammaFeedback(cipher).decrypt(data, sync);
                    break;
            }
        } catch (const std::exception& e) {
            std::cout << "Ошибка: " << e.what() << "\n";
            return;
        }
        std::cout << "Результат (hex):  " << gost::to_hex(out) << "\n";
        std::cout << "Результат (текст): " << std::string(out.begin(), out.end())
                  << "\n";
    }
}

bool read_file(const std::string& path, gost::Bytes& out) {
    std::ifstream f(path, std::ios::binary);
    if (!f) {
        std::cout << "Не удалось открыть файл: " << path << "\n";
        return false;
    }
    out.assign(std::istreambuf_iterator<char>(f), std::istreambuf_iterator<char>());
    return true;
}

bool write_file(const std::string& path, const gost::Bytes& data) {
    std::ofstream f(path, std::ios::binary);
    if (!f) {
        std::cout << "Не удалось создать файл: " << path << "\n";
        return false;
    }
    f.write(reinterpret_cast<const char*>(data.data()),
            static_cast<std::streamsize>(data.size()));
    return static_cast<bool>(f);
}

void file_mode() {
    std::cout << "\n--- Работа с файлом ---\n";
    std::cout << "Действие:\n  1) Зашифровать\n  2) Расшифровать\n";
    int action = read_choice(1, 2);
    const bool encrypt = (action == 1);

    int mode = select_mode(/*with_mac=*/encrypt);
    gost::SubstitutionTable sbox = read_sbox();
    gost::Key key = read_key();
    gost::Gost28147 cipher(key, sbox);

    gost::Sync sync{};
    if (mode == 2 || mode == 3) {
        sync = read_sync();
    }

    std::cout << "Путь к входному файлу:\n";
    std::string in_path = read_line();
    gost::Bytes data;
    if (!read_file(in_path, data)) return;

    if (mode == 4) {
        gost::Bytes mac = gost::Mac(cipher).compute(data, 4);
        std::cout << "Имитовставка файла (32 бита): " << gost::to_hex(mac) << "\n";
        return;
    }

    std::cout << "Путь к выходному файлу:\n";
    std::string out_path = read_line();

    gost::Bytes out;
    try {
        switch (mode) {
            case 1: {
                if (encrypt) {
                    gost::Bytes padded = pad8(data);
                    if (padded.size() != data.size()) {
                        std::cout << "(данные дополнены нулями до " << padded.size()
                                  << " байт)\n";
                    }
                    out = gost::SimpleReplacement(cipher).encrypt(padded);
                } else {
                    out = gost::SimpleReplacement(cipher).decrypt(data);
                }
                break;
            }
            case 2:
                out = gost::Gamma(cipher).process(data, sync);
                break;
            case 3:
                out = encrypt ? gost::GammaFeedback(cipher).encrypt(data, sync)
                              : gost::GammaFeedback(cipher).decrypt(data, sync);
                break;
        }
    } catch (const std::exception& e) {
        std::cout << "Ошибка: " << e.what() << "\n";
        return;
    }

    if (write_file(out_path, out)) {
        std::cout << "Готово: записано " << out.size() << " байт в " << out_path
                  << "\n";
    }
}

void print_menu() {
    std::cout << "\n==================== ГОСТ 28147-89 ====================\n"
              << "  1) Ручной ввод (шифрование/дешифрование текста)\n"
              << "  2) Работа с файлом (шифрование/дешифрование)\n"
              << "  3) Прогнать встроенные тесты\n"
              << "  0) Выход\n"
              << "=======================================================\n";
}

}  // namespace

int main() {
    enable_utf8_console();

    for (;;) {
        print_menu();
        int choice = read_choice(0, 3);
        switch (choice) {
            case 1:
                manual_text();
                break;
            case 2:
                file_mode();
                break;
            case 3:
                std::cout << "\n--- Встроенные тесты ---\n";
                gost::run_selftests(std::cout);
                break;
            case 0:
                std::cout << "Выход.\n";
                return 0;
        }
        if (!std::cin) {  // EOF (например, ввод из пайпа закончился)
            return 0;
        }
    }
}
