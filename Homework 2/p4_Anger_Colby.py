import csv


def load_rated_movies(filename: str) -> dict:
    """Load the top-rated movies into a dictionary."""
    movies = {}

    with open(filename, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            movies[(row["Title"], row["Year"])] = float(
                row["IMDb Rating"]
                )

    return movies


def load_grossing_movies(filename: str) -> dict:
    """Load the top-grossing movies into a dictionary."""
    movies = {}

    with open(filename, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            money = row["USA Box Office"]
            money = money.replace("$", "").replace(",", "").strip()

            movies[(row["Title"], row["Year"])] = float(money)

    return movies


def load_casts(filename: str) -> dict:
    """Load movie directors and casts into a dictionary."""
    movies = {}

    with open(filename, "r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)

        for row in reader:
            if len(row) >= 3:
                title = row[0]
                year = row[1]
                director = row[2]

                actors = [
                    actor
                    for actor in row[3:8]
                    if actor.strip()
                ]

                movies[(title, year)] = (director, actors)

    return movies


def display_ranking(ranking: list, limit: int | None = None) -> None:
    """Display a ranking with an optional maximum number of entries."""
    if limit is not None:
        ranking = ranking[:limit]

    for position, item in enumerate(ranking, start=1):
        print(position, item)


def display_top_collaborations(
    rated_filename: str,
    casts_filename: str,
    limit: int | None = None
) -> None:
    """Display director/actor pairs ranked by number of top-rated movies."""
    rated_movies = load_rated_movies(rated_filename)
    casts = load_casts(casts_filename)

    collaborations = {}

    for movie in rated_movies:
        if movie in casts:
            director, actors = casts[movie]

            for actor in actors:
                pair = (director, actor)
                collaborations[pair] = collaborations.get(pair, 0) + 1

    ranking = [
        (director, actor, count)
        for (director, actor), count in collaborations.items()
    ]

    ranking.sort(key=lambda item: item[2], reverse=True)

    display_ranking(ranking, limit)


def display_top_actors(
    grossing_filename: str,
    casts_filename: str,
    limit: int | None = None
) -> None:
    """Display actors ranked by total box-office money."""
    grossing_movies = load_grossing_movies(grossing_filename)
    casts = load_casts(casts_filename)

    totals = {}

    for movie, box_office in grossing_movies.items():
        if movie in casts:
            _, actors = casts[movie]

            for actor in actors:
                totals[actor] = totals.get(actor, 0) + box_office

    ranking = list(totals.items())
    ranking.sort(key=lambda item: item[1], reverse=True)

    display_ranking(ranking, limit)


def main() -> None:
    """Display the top ten results for both rankings."""
    rated_file = "imdb-top-rated.csv"
    grossing_file = "imdb-top-grossing.csv"
    casts_file = "imdb-top-casts.csv"

    print("Top 10 Director/Actor Collaborations")
    print("------------------------------------")

    display_top_collaborations(rated_file, casts_file, 10)

    print("\nTop 10 Actors by Total Box Office")
    print("---------------------------------")

    display_top_actors(grossing_file, casts_file, 10)


if __name__ == "__main__":
    main()
