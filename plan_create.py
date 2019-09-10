from pydent import AqSession, planner
from pydent.utils import make_async
from resources import resources


def set_primer(*, canvas, field_value, sample):
    canvas.set_field_value(field_value, sample=sample)
    items = [item for item in sample.items if item.location != 'deleted']
    primer_stocks = [
        item for item in items if item.object_type.name == "Primer Stock"]
    primer_aliquots = [
        item for item in items if item.object_type.name == "Primer Aliquot"]

    if len(primer_aliquots) > 0:
        # set item
        canvas.set_field_value(field_value, sample=sample,
                               item=primer_aliquots[-1])
        return

    print("No primer aliquots found for {}".format(sample.name))
    if len(primer_stocks) > 0:
        # create Make Primer Aliquot from Stock
        op = canvas.create_operation_by_name(
            "Make Primer Aliquot from Stock")
        canvas.add_wire(op.outputs[0], field_value)
        canvas.set_field_value(
            ops[0].inputs[0], sample=sample, item=primer_stocks[-1])
        return

    print("No primer stocks found for {}".format(sample.name))
    # create Order Primer and Rehydrate Primer
    op = canvas.create_operation_by_name("Order Primer")

    canvas.set_field_value(op.inputs[0], value="yes")
    canvas.set_field_value(op.outputs[0], sample=field_value.sample)
    ops = canvas.quick_create_chain(op, "Rehydrate Primer")
    canvas.add_wire(ops[1].outputs[0], field_value)


def submit_pcr(*, canvas, sample):
    op = canvas.create_operation_by_name("Make PCR Fragment")
    canvas.set_field_value(op.output("Fragment"), sample=sample)

    fwd = sample.properties['Forward Primer']
    rev = sample.properties['Reverse Primer']
    template = sample.properties['Template']

    set_primer(
        canvas=canvas,
        field_value=op.input("Forward Primer"),
        sample=fwd
    )
    set_primer(
        canvas=canvas,
        field_value=op.input("Reverse Primer"),
        sample=rev
    )

    canvas.set_field_value(op.input("Template"), sample=template)

    new_ops = canvas.quick_create_chain(
        op, "Run Gel", "Extract Gel Slice", "Purify Gel Slice")
    run_gel = new_ops[1]
    canvas.quick_create_chain("Pour Gel", run_gel)


def submit_pcrs(*, sample_range, session, canvas):
    for sample_id in sample_range:
        submit_pcr(
            canvas=canvas,
            sample=session.Sample.find(sample_id)
        )
    return []


def main():
    session = AqSession(
        resources['aquarium']['login'],
        resources['aquarium']['password'],
        resources['aquarium']['aquarium_url']
    )

    canvas = planner.Planner(session)
    submit_pcrs(
        sample_range=list(range(25589, 25591)),
        session=session,
        canvas=canvas
    )
    print(canvas.plan)

    # canvas.layout.topo_sort() # layout the plan for display in Aquarium
    # canvas.create() # push the plan to Aquarium
    # canvas.plan.submit(user, budget) # run plan on Aquarium


if __name__ == "__main__":
    main()
