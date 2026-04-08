#include <iostream>
#include <string>
using namespace std;

struct Item {
    string name, type;
    int attackBonus, defenseBonus;

    Item() : name(), type(), attackBonus(0), defenseBonus(0) {}
    Item(string n, string y, int aB, int dB)
        : name(n), type(y), attackBonus(aB), defenseBonus(dB) {}
};
struct Stats {
    int hp, maxHp, attack, defense, speed;
    Stats() : hp(0), maxHp(0), attack(0), defense(0), speed(0) {}
    Stats(int h, int mH, int a, int d, int s) : hp(h), maxHp(mH), attack(a), defense(d), speed(s) {}
};

struct Fighter {
    string name;
    Stats stat;
    Item* inventory;
    int inventorySize = 0, inventoryCount = 0, id;
    static int totalCreated;

    Fighter(string n, Stats S, int invS) : name(n), stat(S), inventorySize(invS) {
        inventory = new Item[inventorySize];
        totalCreated++;
        id = totalCreated;
    }

    void PrintFighter(const Fighter& f) {
        cout << "your name is : " << f.name << endl;
        cout << "your id is: " << f.id << endl;
        cout << "your hp is: " << f.stat.hp << endl;
    }

    ~Fighter() {
        delete[] inventory;
        inventory = nullptr;
    }
};
int Fighter::totalCreated = 0;
int main() {
    Stats s1;
    Fighter f1("ali", s1, 10);
    Fighter* f2 = new Fighter("ali2", s1, 10);

    f1.PrintFighter(f1);
    f2->PrintFighter(*f2);

    delete f2;
    return 0;
}
