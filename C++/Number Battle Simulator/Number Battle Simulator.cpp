#include <iostream>
using namespace std;

struct Address {
    string city;
    string street;
};

struct Person {
    string name;
    int age;
    Address address;

    Person(string n, int a, string c, string s) {
        name = n;
        age = a;
        address.city = c;
        address.street = s;
    }

    void print() const {
        cout << "Name: " << name << endl;
        cout << "Age: " << age << endl;
        cout << "City: " << address.city << endl;
        cout << "Street: " << address.street << endl;
    }
};

int main() {
    Person p1("Ali", 21, "Amarah", "Street 1");

    p1.print();

    Person* ptr = &p1;
    cout << "\nAccess via pointer: " << ptr->name << endl;

    return 0;
}