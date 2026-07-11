#include <iostream>
#include <string>

// TODO: add struct that take any number of vars and push back to the DynArray in one line
template <typename T>
class DynArray {
   private:
    T* data;
    size_t size = 0;
    size_t capacity = 0;

   public:
    DynArray() {
        data = nullptr;
        size = 0;
        capacity = 0;
    }

    ~DynArray() {
        delete[] data;
        data = nullptr;
        size = 0;
        capacity = 0;
    }
    size_t Size() { return size; }
    size_t Capacity() { return capacity; }
    void PushBack(T value) {
        if (size == capacity) {
            if (size == 0) {
                capacity = 3;
                data = new T[capacity];

                data[size] = value;
                size++;
                return;
            }
            capacity = (capacity * 2) - 1;
            T* oldData = data;
            data = nullptr;
            data = new T[capacity];

            for (size_t i = 0; i < size; ++i) {
                data[i] = oldData[i];
            }
            delete[] oldData;
            oldData = nullptr;
        }

        data[size] = value;
        size++;
    }
    T GetLast() { return data[size - 1]; }
    T operator[](int i) {
        if (i < 0)
            i = size + i;

        if (i >= size || i < 0)
            return -1;  // need a way to make it show as error becuase return -1 could be a number
                        // that's already exists
        return data[i];
    }
};

int main() {
    DynArray<int> a;
    a.PushBack(5);
    a.PushBack(3);
    a.PushBack(10);
    a.PushBack(8);
    a.PushBack(9);
    a.PushBack(7);
    a.PushBack(6);
    std::cout << a.GetLast() << std::endl;
    std::cout << a.Size() << std::endl;
    std::cout << a[-5] << std::endl;
    std::cout << a.Capacity();

    return 0;
}
