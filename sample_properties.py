from pydent import AqSession
from resources import resources


def main():
    session = AqSession(
        resources['aquarium']['login'],
        resources['aquarium']['password'],
        resources['aquarium']['aquarium_url']
    )
    sample = session.Sample.find_by_name('IAA1-Nat-F')
    print("Name: {}\nProject: {}\nDescription: {}\nSample Type: {}\nProperties: {}".format(
        sample.name,
        sample.project,
        sample.description,
        sample.sample_type.name,
        sample.properties)
    )


if __name__ == "__main__":
    main()
