import csv


def add_user(
    sn: dict[str, tuple[str, list[str]]],
    username: str,
    fullname: str
) -> bool:
    """Add a new user to the social network."""
    try:
        if username in sn:
            return False

        sn[username] = (fullname, [])
        return True

    except Exception as error:
        print(f"Error adding user: {error}")
        raise


def add_friend(
    sn: dict[str, tuple[str, list[str]]],
    user1: str,
    user2: str
) -> bool:
    """Add a mutual friendship between two users."""
    try:
        if user1 not in sn or user2 not in sn:
            return False

        if user1 == user2:
            return False

        if user2 not in sn[user1][1]:
            sn[user1][1].append(user2)

        if user1 not in sn[user2][1]:
            sn[user2][1].append(user1)

        return True

    except Exception as error:
        print(f"Error adding friendship: {error}")
        raise


def get_friends(
    sn: dict[str, tuple[str, list[str]]],
    user1: str,
    distance: int
) -> list[str]:
    """Return all friends within the specified link distance."""
    try:
        if user1 not in sn or distance <= 0:
            return []

        visited = {user1}
        current_level = [user1]
        result = []

        for _ in range(distance):
            next_level = []

            for user in current_level:
                for friend in sn[user][1]:
                    if friend not in visited:
                        visited.add(friend)
                        result.append(friend)
                        next_level.append(friend)

            current_level = next_level

            if not current_level:
                break

        return result

    except Exception as error:
        print(f"Error getting friends: {error}")
        raise


def save_network(
    filename: str,
    sn: dict[str, tuple[str, list[str]]]
) -> None:
    """Save a social network dictionary to a CSV file."""
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            for username, data in sn.items():
                fullname, friends = data
                writer.writerow([username, fullname] + friends)

    except Exception as error:
        print(f"Error saving network: {error}")
        raise


def load_network(
    filename: str
) -> dict[str, tuple[str, list[str]]]:
    """Load a social network dictionary from a CSV file."""
    try:
        sn = {}

        with open(filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)

            for row in reader:
                if len(row) >= 2:
                    username = row[0]
                    fullname = row[1]
                    friends = row[2:]
                    sn[username] = (fullname, friends)

        return sn

    except Exception as error:
        print(f"Error loading network: {error}")
        raise


def main() -> None:
    """Test the social network functions."""
    sn = {
        "alice": ("Alice Smith", ["maria"]),
        "maria": ("Maria Cortez", ["alice", "joe", "david"]),
        "joe": ("Joseph Adams", ["maria", "eve"]),
        "eve": ("Evelyn Cooper", ["joe"]),
        "david": ("David Benson", ["maria"])
    }

    print("Original network:")
    print(sn)

    print("\nAdd user:")
    print(add_user(sn, "bob", "Bob Johnson"))

    print("\nAdd friendship:")
    print(add_friend(sn, "bob", "alice"))

    print("\nAlice - distance 1:")
    print(get_friends(sn, "alice", 1))

    print("\nAlice - distance 2:")
    print(get_friends(sn, "alice", 2))

    print("\nAlice - distance 3:")
    print(get_friends(sn, "alice", 3))

    filename = "social_network.csv"

    save_network(filename, sn)

    print("\nLoaded network:")
    print(load_network(filename))


if __name__ == "__main__":
    main()
