#include <iostream>
#include <string>

char board[9] = {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '};
bool still = true;
void PrintBoard() {
    std::cout << " " << board[0] << " | " << board[1] << " | " << board[2] << " " << std::endl;
    std::cout << "---+---+---" << std::endl;
    std::cout << " " << board[3] << " | " << board[4] << " | " << board[5] << " " << std::endl;
    std::cout << "---+---+---" << std::endl;
    std::cout << " " << board[6] << " | " << board[7] << " | " << board[8] << " " << std::endl;
}

char checkWinner() {
    // 1. Check Rows
    for (int i = 0; i < 9; i++) {
        if (i % 3 == 0) {
            if (board[i] == board[i + 1] && board[i + 1] == board[i + 2] && board[i] != ' ') {
                return board[i];
            }
        }
        if (i / 3 == 0) {
            if (board[i] == board[i + 3] && board[i + 6] == board[i + 3] && board[i] != ' ')
                return board[i];
        }
        if (i == 0) {  // main diagonal 0,4,6 -> 0,4,8
            if (board[0] == board[4] && board[4] == board[8] && board[0] != ' ')
                return board[i];
        }
        if (i == 2) {  // anti-diagonal 2,4,6
            if (board[2] == board[4] && board[4] == board[6] && board[2] != ' ')
                return board[i];
        }
    }

    for (int i = 0; i < 9; i++) {
        if (board[i] == ' ')
            return ' ';
    }
    return 'D';
}

int Minimax(int depth, bool isMax) {
    char check = checkWinner();
    if (check == 'X')
        return -10 + depth;  // O loses -> prefer a LATER loss
    if (check == 'O')
        return 10 - depth;  // O wins  -> prefer a SOONER win
    if (check == 'D')
        return 0;
    if (isMax) {
        int best = -100;
        for (int i = 0; i < 9; i++) {
            if (board[i] == ' ') {
                board[i] = 'O';
                best = std::max(best, Minimax(depth + 1, !isMax));
                board[i] = ' ';
            }
        }
        return best;
    } else {
        int best = 100;
        for (int i = 0; i < 9; i++) {
            if (board[i] == ' ') {
                board[i] = 'X';
                best = std::min(best, Minimax(depth + 1, !isMax));
                board[i] = ' ';
            }
        }
        return best;
    }
}
void FindBestMove() {
    int bestVal = -100;
    int moveVal;
    int cordinit = -1;
    for (int i = 0; i < 9; i++) {
        if (board[i] == ' ') {
            board[i] = 'O';
            moveVal = Minimax(0, false);
            board[i] = ' ';
            if (moveVal > bestVal) {
                cordinit = i;
                bestVal = moveVal;
            }
        }
    }
    if (checkWinner() == ' ')
        board[cordinit] = 'O';
}

int main() {
    while (still) {
        PrintBoard();
        switch (checkWinner()) {
            case 'X':
                still = false;
                std::cout << "the winner is the humen" << std::endl;
                break;
            case 'O':
                still = false;
                std::cout << "the winner is the AI" << std::endl;
                break;
            case 'D':
                still = false;
                std::cout << "It's Draw" << std::endl;
                break;
        }
        while (still) {
            std::cout << std::endl << "enter index [1-9]: " << std::endl;
            int index = 0;
            std::cin >> index;
            index--;
            if ((index < 9 && index >= 0) && board[index] == ' ') {
                board[index] = 'X';

                break;
            }
            std::cout << "Please Enter vaild number!" << std::endl;
            PrintBoard();
        }

        FindBestMove();
    }
    return 0;
}
