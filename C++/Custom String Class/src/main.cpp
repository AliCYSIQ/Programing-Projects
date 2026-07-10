#include <iostream>
#include <string>

class MyString {
   private:
    char* data;
    size_t len = 0;

   public:
    MyString() {
        len = 0;
        data = new char[1];
        data[0] = '\0';
    }
    void work(const std::string& d) {
        len = 0;
        while (d[len] != '\0') {
            len++;
        }
        data = new char[len + 1];
        size_t i = 0;
        while (d[i] != '\0') {
            data[i] = d[i];

            i++;
        }
        data[i] = '\0';
    }
    MyString(const std::string& d) { work(d); }
    ~MyString() {
        delete[] data;
        data = nullptr;
    }
    MyString(const MyString& s) {
        len = s.len;
        data = new char[len + 1];
        for (size_t i = 0; i <= len; i++) {
            data[i] = s.c_str()[i];
        }
    }
    MyString& operator=(const MyString& s) {
        if (this == &s)
            return *this;
        delete[] data;
        len = s.len;
        data = new char[len + 1];
        for (size_t i = 0; i <= len; i++) {
            data[i] = s.c_str()[i];
        }
        return *this;
    }
    MyString(MyString&& s) {
        len = s.len;
        data = s.data;

        s.data = nullptr;
        s.len = 0;
    }
    MyString& operator=(MyString&& s) {
        if (this == &s)
            return *this;
        delete[] data;
        data = s.data;
        len = s.len;
        s.data = nullptr;
        s.len = 0;
        return *this;
    }

    std::string c_str() const { return data; }
    size_t length() const { return len; }

    bool operator==(const MyString& s) {
        if (this == &s)
            return true;
        if (len != s.len)
            return false;
        for (size_t i = 0; i < len; ++i) {
            if (data[i] != s.data[i]) {
                return false;
            }
        }
        return true;
    }
    // *thinking if i should make this operator type a string or MyString? i think both work so
    // *i will go with the easer one which is string (which one is more opmized for performence)
    std::string operator+(const MyString& s) { return std::string(data) + s.data; }
    MyString& operator=(const std::string s) {
        // ! Important
        // * here i should use char* in both d and s and check the length of s and alocate on d
        // * then use in *work function

        delete[] data;
        work(s);
        return *this;
    }
    std::string operator[](size_t i) {
        if (i >= len)
            return "ERR";

        return std::string(1, data[i]);
    }
};

int main() {
    MyString a("hello");
    MyString b("world");

    std::cout << a.c_str() << " " << a.length();  // hello 5
    std::cout << a[0];                            // h
    std::cout << (a == b);                        // 0

    MyString c = a + b;
    std::cout << c.c_str() << " " << c.length();  // helloworld 10

    MyString d = a;             // copy ctor
    d = b;                      // copy assign
    MyString e = std::move(a);  // move ctor — don't touch a again after this
    b = std::move(d);           // move assign
    a = "ali";
    std::cout << std::endl << a.c_str();

    return 0;
}
