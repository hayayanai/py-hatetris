def main():
    with open("tmp6.txt", mode="r") as f:
        ls = [s.strip() for s in f.readlines()]
    split_row = []

    for line in ls:
        split_row.append((line.split(" ")[0], float(line.split(" ")[1])))
    dic = {}
    for l in split_row:
        if l[0] in dic:
            dic[l[0]] += l[1]
        else:
            dic[l[0]] = l[1]

    for k, v in dic.items():
        print(f"{k} {v}")


if __name__ == "__main__":
    main()
