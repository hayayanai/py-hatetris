
#include "hate.hpp"
#include <iostream>
#include <map>
#include <string>
#include <algorithm>

std::string Piece::getName()
{
    if (id == -1)
    {
        return NAME[0];
    }
    return NAME[id];
}

char Piece::getChar(int x, int y)
{
    std::string str = std::string(UNMODIFIED[getName()][rot][y]);
    return str[x];
}

void Piece::print()
{
    // std::string s = unmodified.dump();
    // std::cout << s << std::endl;
    // std::cout << UNMODIFIED["J"][0][0] << std::endl;                    // json String
    // std::cout << std::string(UNMODIFIED["J"][0][0]).at(0) << std::endl; // cast to std::string and use at() or []
}

int Hatetris::getHatetris()
{
    std::map<int, int> ratings;
    for (int pid = 0; pid < 7; pid++)
    {
        ratings[pid] = 25;
    }

    for (int pid = 0; pid < 7; pid++)
    {
        for (std::string action : ACTIONS)
        {
            // std::vector<std::vector<int>> future_field(field);

            // std::copy(field.begin(), field.end(), std::back_inserter(future_field));
            // future_field = field;

            putBlock(future_field, action, pid);
            // for (int i = DEPTH - 1; i >= 0; i--)
            // {
            //     for (int j = 0; j < WIDTH; j++)
            //     {
            //         if (future_field.at(i).at(j)) {
            //             std::cout << "#";
            //         }else {
            //             std::cout << ".";
            //         }
            //     }
            //     std::cout << "\n";
            // }
            // std::cout << "---\n" << std::endl;
            const int rating = evaluate(future_field);
            future_field = field;
            if (ratings[pid] > rating)
            {
                ratings[pid] = rating;
            }
        }
    }
    std::vector<int> pids;
    int mx_v = -1;
    for (const auto &item : ratings)
    {
        // std::cout << "[" << item.first << "," << item.second << "]\n";
        if (item.second > mx_v)
        {
            mx_v = item.second;
            pids.clear();
            pids.push_back(item.first);
        }
        else if (item.second == mx_v)
        {
            pids.push_back(item.first);
        }
    }
    // for (int pid: pids) { std::cout << pid << std::endl;}
    for (int p : WORST_PIECES)
    {
        for (int pid : pids)
        {
            if (p == pid)
            {
                return p;
            }
        }
    }
    return -1;
}

void Hatetris::putBlock(std::vector<std::vector<int>> &field, std::string action, int pid)
{
    Piece piece(pid);
    Hatetris::handleInput(field, action, piece);
}

int Hatetris::evaluate(std::vector<std::vector<int>> &field)
{
    std::vector<int> res(10, 0);
    for (int x = 0; x < WIDTH; x++)
    {
        for (int y = DEPTH - 1; y >= 0; y--)
        {
            if (field.at(y).at(x) == 1)
            {
                res.at(x) = y + 1;
                break;
            }
        }
    }
    int mx = *std::max_element(res.begin(), res.end());
    return mx;
}

void Hatetris::handleInput(std::vector<std::vector<int>> &field, std::string action, Piece &piece)
{
    int pre_x = piece.x;
    int pre_y = piece.y;
    int pre_rot = piece.rot;

    if (action.size() == 1 && piece.id != -1)
    {
        if (action == "D")
        {
            piece.y -= 1;
        }
        else if (action == "L")
        {
            piece.x -= 1;
        }
        else if (action == "R")
        {
            piece.x += 1;
        }
        else if (action == "U")
        {
            piece.rot = (piece.rot + 1) % 4;
        }
        else if (action == "H")
        {
            while (piece.id != -1)
            {
                handleInput(field, "D", piece);
            }
        }

        if (!canMovePiece(field, piece))
        {
            piece.x = pre_x;
            piece.rot = pre_rot;
            if (piece.y != pre_y && piece.id != -1)
            {
                piece.y = pre_y;
                lockPiece(field, piece);
            }
        }
    }
    else if (action.size() > 1)
    {
        std::string str(1, action.at(0));
        handleInput(field, str, piece);
        handleInput(field, action.substr(1), piece);
    }
}

bool Hatetris::canMovePiece(std::vector<std::vector<int>> &field, Piece &piece)
{
    for (int y = 0; y < 4; y++)
    {
        for (int x = 0; x < 4; x++)
        {
            if (piece.getChar(x, y) == '#')
            {
                try
                {
                    if (field.at(3 - y + piece.y).at(x + piece.x) == 1)
                    {
                        return false;
                    }
                }
                catch (std::exception &e)
                {
                    return false;
                }
            }
        }
    }
    return true;
}

void Hatetris::lockPiece(std::vector<std::vector<int>> &field, Piece &piece)
{
    for (int y = 0; y < 4; y++)
    {
        for (int x = 0; x < 4; x++)
        {
            if (piece.getChar(x, y) == '#')
            {
                try
                {
                    field.at(3 - y + piece.y).at(x + piece.x) = 1;
                }
                catch (std::exception &e)
                {
                }
            }
        }
    }
    // int l = deleteLines(field);
    deleteLines(field);
    piece.id = -1;
}

int Hatetris::deleteLines(std::vector<std::vector<int>> &field)
{
    int count = 0;
    while (filledLine(field) != -1)
    {
        cutLine(filledLine(field), field);
        count++;
    }
    return count;
}

int Hatetris::filledLine(std::vector<std::vector<int>> &field)
{
    for (int y = 0; y < DEPTH; y++)
    {
        bool is_filled = true;
        for (int x = 0; x < WIDTH; x++)
        {
            if (!field[y][x])
            {
                is_filled = false;
                break;
            }
        }
        if (is_filled)
        {
            return y;
        }
    }
    return -1;
}

void Hatetris::cutLine(int y, std::vector<std::vector<int>> &field)
{
    if (y > -1)
    {
        auto elem_to_remove = field.begin() + y;
        if (elem_to_remove != field.end())
        {
            field.erase(elem_to_remove);
        }
        std::vector<int> vec = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
        field.push_back(vec);
    }
}

// int Hatetris::getNextPiece()
// {
//     return getHatetris();
// }

void Hatetris::print()
{
    for (int i = DEPTH - 1; i >= 0; i--)
    {
        for (int j = 0; j < WIDTH; j++)
        {
            std::cout << field.at(i).at(j);
        }
        std::cout << std::endl;
    }
}

int main()
{
    // Hatetris h({{0, 1, 1, 1, 1, 1, 1, 1, 1, 1}, {0, 1, 1, 1, 1, 1, 1, 1, 1, 1}, {0, 1, 1, 1, 1, 1, 1, 1, 1, 1}, {0, 1, 1, 1, 1, 0, 0, 0, 1, 1}, {1, 1, 1, 1, 0, 1, 1, 1, 1, 1}, {1, 0, 1, 1, 1, 1, 1, 1, 1, 0}, {1, 0, 1, 1, 1, 1, 1, 1, 1, 1}, {1, 0, 1, 1, 1, 0, 1, 0, 1, 1}, {1, 0, 1, 1, 1, 1, 1, 0, 1, 1}, {0, 0, 0, 1, 1, 1, 0, 0, 0, 1}, {0, 0, 0, 1, 1, 0, 0, 0, 0, 1}, {0, 0, 0, 1, 1, 0, 0, 0, 0, 1}, {0, 0, 0, 1, 1, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}});
    Hatetris h({{0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0}});

    // h.print();
    std::cout << h.getHatetris() << std::endl;
    // h.deleteLines(h.field);
    // std::cout << h.getNextPiece() << std::endl;
}
