#include <vector>
#include <string>
#include "json.hpp"

using json = nlohmann::json;

class Piece
{
public:
    const std::string NAME[7] = {"I", "J", "L", "O", "S", "T", "Z"};
    const json UNMODIFIED = {{"I", {{"....", "####", "....", "...."}, {"..#.", "..#.", "..#.", "..#."}, {"....", "....", "####", "...."}, {".#..", ".#..", ".#..", ".#.."}}}, {"J", {{"....", ".##.", ".#..", ".#.."}, {"....", "###.", "..#.", "...."}, {"..#.", "..#.", ".##.", "...."}, {"....", ".#..", ".###", "...."}}}, {"L", {{"....", ".###", ".#..", "...."}, {"....", ".##.", "..#.", "..#."}, {"....", "..#.", "###.", "...."}, {".#..", ".#..", ".##.", "...."}}}, {"O", {{"....", ".##.", ".##.", "...."}, {"....", ".##.", ".##.", "...."}, {"....", ".##.", ".##.", "...."}, {"....", ".##.", ".##.", "...."}}}, {"S", {{"....", "..##", ".##.", "...."}, {"....", ".#..", ".##.", "..#."}, {"....", ".##.", "##..", "...."}, {".#..", ".##.", "..#.", "...."}}}, {"T", {{"....", ".###", "..#.", "...."}, {"....", "..#.", ".##.", "..#."}, {"....", ".#..", "###.", "...."}, {".#..", ".##.", ".#..", "...."}}}, {"Z", {{"....", ".##.", "..##", "...."}, {"....", "..#.", ".##.", ".#.."}, {"....", "##..", ".##.", "...."}, {"..#.", ".##.", ".#..", "...."}}}};

    int x;
    int y;
    int id;
    int rot;
    int age;

    Piece()
    {
        x = 3;
        y = 19;
        id = 0;
        rot = 0;
        age = 0;
    }
    Piece(int id) : id(id)
    {
        x = 3;
        y = 19;
        rot = 0;
        age = 0;
    }

    std::string getName();
    char getChar(int x, int y);

    void print();
};

class Hatetris
{
private:
    const int WORST_PIECES[7] = {4, 6, 3, 0, 2, 1, 5};
    const std::vector<std::string> ACTIONS = {
        "LLLLH",
        "LLLH",
        "LLH",
        "LH",
        "H",
        "RH",
        "RRH",
        "RRRH",
        "RRRRH",
        "ULLLLLH",
        "ULLLLH",
        "ULLLH",
        "ULLH",
        "ULH",
        "UH",
        "URH",
        "URRH",
        "URRRH",
        "URRRRH",
        "URRRRRH",
        "UULLLLH",
        "UULLLH",
        "UULLH",
        "UULH",
        "UUH",
        "UURH",
        "UURRH",
        "UURRRH",
        "UURRRRH",
        "UUULLLLLH",
        "UUULLLLH",
        "UUULLLH",
        "UUULLH",
        "UUULH",
        "UUUH",
        "UUURH",
        "UUURRH",
        "UUURRRH",
        "UUURRRRH",
        "UUURRRRRH"};

    const int DEPTH = 23;
    const int WIDTH = 10;
    const std::vector<std::vector<int>> field;
    std::vector<std::vector<int>> future_field;
    int filledLine(std::vector<std::vector<int>> &field);
    void cutLine(int y, std::vector<std::vector<int>> &field);
    // bool field[23][10];

protected:
    void putBlock(std::vector<std::vector<int>> &field, std::string action, int pid);
    void handleInput(std::vector<std::vector<int>> &field, std::string action, Piece &piece);
    bool canMovePiece(std::vector<std::vector<int>> &field, Piece &piece);
    void lockPiece(std::vector<std::vector<int>> &field, Piece &piece);
    int deleteLines(std::vector<std::vector<int>> &field);
    int evaluate(std::vector<std::vector<int>> &field);

public:
    // std::vector<std::vector<int>> field;
    Hatetris(std::vector<std::vector<int>> field) : field(field)
    {
        future_field = field;
    }
    int getFirstPiece()
    {
        return WORST_PIECES[0];
    }
    // int getNextPiece();
    int getHatetris();
    void print();
};
