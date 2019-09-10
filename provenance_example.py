import json
from pydent import AqSession
from resources import resources
from aquarium.provenance import (CollectionEntity, PartEntity, ProvenanceTrace)
from aquarium.trace.factory import TraceFactory
from aquarium.trace.visitor import ProvenanceVisitor


def main():
    session = AqSession(
        resources['aquarium']['login'],
        resources['aquarium']['password'],
        resources['aquarium']['aquarium_url']
    )

    plan = session.Plan.find(35448)
    trace = TraceFactory.create_from(session=session,
                                     plans=[plan],
                                     experiment_id="dummy")
    print(json.dumps(trace.as_dict(), indent=4))


if __name__ == "__main__":
    main()
