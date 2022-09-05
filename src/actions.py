ACTIONS = [
    "LLLLLH",
    "LLLLH",
    "LLLH",
    "LLH",
    "LH",
    "H",
    "RH",
    "RRH",
    "RRRH",
    "RRRRH",
    "RRRRRH",
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
    "ULLLLLH",
    "ULLLLH",
    "ULLH",
    "ULH",
    "UH",
    "URH",
    "URRH",
    "URRRH",
    "URRRRH",
    "URRRRRH",
    "ULULLLLH",
    "ULULLLH",
    "ULULLH",
    "ULULH",
    "ULUH",
    "UUH",
    "URUH",
    "URURH",
    "URURRH",
    "URURRRH",
    "URURRRRH",
]

if __name__ == "__main__":
    def hoge(act):
        print(act)
        if (len(act) == 1):
            print("final", act)
        else:
            hoge(act[0])
            hoge(act[1:])

    act = ACTIONS[0]
    hoge(act)
