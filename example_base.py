from pydent import AqSession
from resources import resources


def main():
    session = AqSession(
        resources['aquarium']['login'],
        resources['aquarium']['password'],
        resources['aquarium']['aquarium_url']
    )


if __name__ == "__main__":
    main()