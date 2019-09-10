from pydent import AqSession
from resources import resources


def main():
    session = AqSession(
        resources['aquarium']['login'],
        resources['aquarium']['password'],
        resources['aquarium']['aquarium_url']
    )
    primer_type = session.SampleType.find_by_name('Primer')
    sample = session.Sample.new(
        name="Example Primer",
        project="trident-demo",
        description="primer created with trident",
        sample_type_id=primer_type.id,
        properties={
            'Overhang Sequence': 'AAAAA',
            'Anneal Sequence': 'GGGGGGGG',
            'T Anneal': 70
        }
    )

    print("Name: {}\nProject: {}\nDescription: {}\nSample Type: {}\nProperties: {}".format(
        sample.name,
        sample.project,
        sample.description,
        sample.sample_type.name,
        sample.properties)
    )

    # DO NOT SAVE THIS Sample OBJECT TO AQUARIUM

if __name__ == "__main__":
    main()
