#include <iostream>
#include <string>

template <typename T>
class DynArray {
   private:
    T* data;
    size_t size = 0;
    size_t capacity = 0;

   public:
    void ReAlocate() {
        T* oldData = data;
        data = nullptr;
        data = new T[capacity];

        for (size_t i = 0; i < size; ++i) {
            data[i] = oldData[i];
        }
        delete[] oldData;
        oldData = nullptr;
    }
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
            ReAlocate();
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
    DynArray& operator=(std::initializer_list<T> list) {
        delete[] data;
        size = capacity = list.size();
        data = new T[capacity];
        for (size_t i = 0; i < size; i++) {
            data[i] = *(list.begin() + i);
        }
        return *this;
    }
    bool IsEmpty() { return size == 0; }
    void Reserve(size_t cap) {
        if (cap <= capacity)
            return;
        capacity = cap;
        ReAlocate();
    }
    T Front() { return data[0]; }
    T Back() { return data[size - 1]; }
    T PopBack() {
        if (size > 0)
            size--;
        return data[size];
    }
    void Print() {
        std::cout << std::endl;
        for (size_t i = 0; i < size; i++) {
            std::cout << data[i] << " ";
        }
        std::cout << std::endl;
    }
    void Print(size_t index) {
        if (index >= size) {
            index = size;
        }
        std::cout << std::endl;
        for (size_t i = 0; i < index; i++) {
            std::cout << data[i] << " ";
        }
        std::cout << std::endl;
    }
    void Insert(size_t index, const T& value) {
        if (index > size || index < 0)
            return;
        size++;
        if (size >= capacity) {
            capacity = capacity * 2 - 1;
            ReAlocate();
        }

        for (size_t i = size - 1; i > index; i--) {
            data[i] = data[i - 1];
        }
        data[index] = value;
    }
    void Erase(size_t index) {
        if (index > size || index < 0)
            return;

        size--;
        for (size_t i = index; i < size; i++) {
            data[i] = data[i + 1];
        }
    }
    void Clear() { size = 0; }
    T* Begin() { return data; }
    T* End() { return data + size; }
};

int main() {
    DynArray<int> a;
    a.PushBack(5);
    a = {5, 10, 20, 32, 453, 543};
    a.Print();
    std::cout << a.Size() << std::endl;
    a.Erase(1);
    a.Print();
    std::cout << a.Size() << std::endl;
    std::cout << a.Capacity() << std::endl;
    a.Clear();
    std::cout << a.Size() << std::endl;
    std::cout << a.Capacity() << std::endl;

    return 0;
}
