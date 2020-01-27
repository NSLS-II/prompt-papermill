import sys

from event_model import RunRouter
from bluesky.callbacks.zmq import RemoteDispatcher
import papermill


def factory(name, start_doc):
    plan_name = start_doc.get('plan_name')
    uid = start_doc['uid']
    callbacks = []
    if plan_name == 'reflection_scan':
        def callback(name, doc):
            if name == 'stop':
                papermill.execute_notebook(
                    '/opt/papermill/templates/reflection_scan.ipynb',
                    f"/opt/papermill/results/reflection_scan_{uid}.ipynb",
                    dict(uid=uid))
        callbacks.append(callback)
    else:
        print("Nothing to do for Run with uid={uid!r} "
              "and plan_name={plan_name!r}", file=sys.stderr)

    # Give the RunRouter two lists, List[Callbacks], List[SubFactories].
    return callbacks, []


def main():
    rr = RunRouter([factory])
    dispatcher = RemoteDispatcher('localhost:5578')
    dispatcher.subscribe(rr)
    dispatcher.start()


if __name__ == '__main__':
    main()
