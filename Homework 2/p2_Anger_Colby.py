def main() -> None:
    part_a = [
        (a, b, c, d)
        for a in range(1, 11)
        for b in range(1, 11)
        for c in range(1, 11)
        for d in range(1, 11)
        if len({a, b, c, d}) == 4
        and a ** 2 + b ** 2 == c ** 2 + d ** 2
    ]

    print("Part A:")
    print(part_a)

    strings = ["One", "SEVEN", "three", "two", "Ten"]

    part_b = [
        (word.lower(), len(word))
        for word in strings
        if len(word) < 5
    ]

    print("\nPart B:")
    print(part_b)

    names = [
        "Christopher Ashton Kutcher",
        "Elizabeth Stamatina Fey"
    ]

    part_c = [
        f"{parts[0]} {parts[1][0]}. {parts[2]}"
        for parts in (name.split() for name in names)
    ]

    print("\nPart C:")
    print(part_c)

    lst1 = ["Spam", "Trams", "Elbows", "Tops", "Astral"]
    lst2 = ["Bowels", "Sample", "Altars", "Stop", "Course", "Smart"]

    part_d = [
        (w1, w2)
        for w1 in lst1
        for w2 in lst2
        if sorted(w1.lower()) == sorted(w2.lower())
    ]

    print("\nPart D:")
    print(part_d)

    s = ["one", "two", "three"]

    part_e = {
        word: len(word)
        for word in s
    }

    print("\nPart E:")
    print(part_e)

    text = "Hello world"

    part_f = {
        index: character
        for index, character in enumerate(text)
        if character.lower() in "aeiou"
    }

    print("\nPart F:")
    print(part_f)


if __name__ == "__main__":
    main()
