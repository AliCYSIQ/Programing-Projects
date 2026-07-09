#include <cstdlib>
#include <iostream>
#include <string>

using namespace std;

struct Item {
    string name, type;
    int attackBonus, defenseBonus;

    Item() : name(), type(), attackBonus(0), defenseBonus(0) {}
    Item(string n, string ty, int attB, int defB)
        : name(n), type(ty), attackBonus(attB), defenseBonus(defB) {}
};
struct Stats {
    int hp, maxHp, attack, defense, speed;
    Stats() : hp(100), maxHp(150), attack(10), defense(25), speed(5) {}
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

    // copy consturcter
    Fighter(const Fighter& f) : name(f.name), stat(f.stat), inventorySize(f.inventorySize) {
        inventory = new Item[inventorySize];
        inventoryCount = f.inventoryCount;
        totalCreated++;
        id = totalCreated;
        for (int i = 0; i < inventoryCount; i++) {
            inventory[i] = f.inventory[i];
        }
    }
    // copy assignment
    Fighter& operator=(const Fighter& f) {
        if (this == &f)
            return *this;
        delete[] inventory;
        inventory = new Item[f.inventorySize];
        name = f.name;
        stat = f.stat;
        inventorySize = f.inventorySize;
        inventoryCount = f.inventoryCount;

        for (int i = 0; i < inventoryCount; i++) {
            inventory[i] = f.inventory[i];
        }
        return *this;
    }
    // move consturcter
    Fighter(Fighter&& f)
        : name(std::move(f.name)),
          stat(std::move(f.stat)),
          inventorySize(std::move(f.inventorySize)) {
        inventoryCount = f.inventoryCount;
        totalCreated++;
        id = totalCreated;

        inventory = f.inventory;

        f.inventory = nullptr;
        f.inventorySize = 0;
        f.inventoryCount = 0;
    }
    // move assigment
    Fighter& operator=(Fighter&& f) {
        if (this == &f)
            return *this;
        delete[] inventory;
        name = std::move(f.name);
        stat = f.stat;
        inventorySize = f.inventorySize;
        inventoryCount = f.inventoryCount;

        inventory = f.inventory;

        f.inventory = nullptr;
        f.inventorySize = 0;
        f.inventoryCount = 0;
        return *this;
    }
    bool isAlive() const { return stat.hp > 0; }
    ~Fighter() {
        delete[] inventory;
        inventory = nullptr;
    }
};
int Fighter::totalCreated = 0;
void PrintFighter(const Fighter& f) {
    cout << "your name is : " << f.name << endl;
    cout << "your id is: " << f.id << endl;
    cout << "your hp is: " << f.stat.hp << endl;
}

bool AddItem(Fighter& f, const Item& t) {
    if (f.inventoryCount < f.inventorySize) {
        f.inventory[f.inventoryCount] = t;
        f.inventoryCount++;
        return true;
    }
    return false;
}
int rollDamage(const Fighter& attacker) {
    return attacker.stat.attack + rand() % 6 + 1;
}
void applyDamage(Fighter& f, int dmg) {
    f.stat.hp -= dmg;
    if (f.stat.hp < 0)
        f.stat.hp = 0;
}

void combatRound(Fighter& a, Fighter& b, bool rest = false) {
    static int round = 0;
    if (rest) {
        round = 0;
        return;
    }

    round++;
    int aDmg = rollDamage(a);
    int bDmg = rollDamage(b);
    cout << "in round " << round << ": \n";
    applyDamage(b, aDmg);
    cout << "\t" << a.name << " deal " << aDmg << " damage to " << b.name;
    cout << ", " << b.name << " health now is " << b.stat.hp << "!\n";
    if (!b.isAlive())
        return;
    applyDamage(a, bDmg);
    cout << "\t" << b.name << " deal " << bDmg << " damage to " << a.name;
    cout << ", " << a.name << " health now is " << a.stat.hp << "!\n";
}
// True for player win , Flase to his lose
bool runCombat(Fighter& player, Fighter* enemy) {
    if (enemy == nullptr)
        return false;

    combatRound(player, *enemy, true);
    while (player.isAlive() && enemy->isAlive()) {
        combatRound(player, *enemy);
    }
    if (player.isAlive()) {
        cout << "\nPlayer is the winner\nHis health now is " << player.stat.hp;
        player.stat.attack += 50;
        player.stat.maxHp += 100;
        return true;
    } else {
        cout << "\nPlayer lose to " << enemy->name << "!\nHis health now is " << enemy->stat.hp;
        return false;
    }
}
int main() {
    Stats s1;
    Stats s2(100, 200, 5, 15, 5);
    Fighter f1("ilent0", s2, 10);
    Fighter f2("ahmed", s1, 10);
    Fighter f3("ali", s1, 10);

    runCombat(f1, &f3);
}
