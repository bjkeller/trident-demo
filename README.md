# Aquarium Python Scripting Demo

This is a demo for Python scripting to accessing Aquarium using [Trident](klavinslab.org/trident).

This demo uses pydent 0.0.35.
Version 0.1.5a6 is also available.

Note: The use of Docker is technically not necessary, but it is used here to manage the Python environment.

## Getting started

The example scripts assume a file `resources.py` that defines the values `login`, `password` and `url`.
This file can be constructed by first running the command

```bash
cp resources.py-temp resources.py
```

and then changing the values to match your Aquarium account.

The import

```python
from resources import resources
```

should be included at the top of each script.

The command

```python
session = AqSession(
        resources['aquarium']['login'],
        resources['aquarium']['password'],
        resources['aquarium']['aquarium_url']
    )
```

creates the session object to make queries to Aquarium.

Note that `resources.py` contains secrets that should not be checked into your version control.

## Samples

To get a sample, the best strategy is to query by the sample name.
For instance, using the BIOFAB production system, the query

```python
sample = session.Sample.find_by_name('IAA1-Nat-F')
```

returns the sample with the name `IAA1-Nat-F`.
We can inspect the type of the sample with

```python
print(sample.sample_type.name)
```

which shows this sample is a primer.
Running

```python
print(sample.properties)
```

will show the properties that define this sample as a case of the sample type (a primer should have an overhang and anneal sequence, and an annealing temperature).

Each sample has a `name`, `project`, `description`, `properties` and `sample_type` properties.

To create a sample linked to the database, use the `Sample.new` function:

```python
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
```

To save this sample object to Aquarium, it is necessary to run the command

```python
sample.save()
```

(Don't do save this demo object to a production system!)

## Plans

Using Trident makes it possible to create complex plans that are tedious to create with the graphical planner in Aquarium.

*This section shows creating plans in pydent 0.0.35
The next release includes simplified planning.*


## Provenance

For getting information about previous runs, we are going to demo the [aquarium-provenance](https://github.com/klavinslab/aquarium-provenance) package based on Trident.



