import glob
import os
import sys

from event_model import RunRouter
from bluesky.callbacks.zmq import RemoteDispatcher
import papermill


BASE_PATH = '/opt/papermill/'
TEMPLATE_PATH = os.path.join(BASE_PATH, 'templates')
OUTPUT_PATH = os.path.join(BASE_PATH, 'results')


def factory(name, start_doc):
    plan_name = start_doc.get('plan_name')
    uid = start_doc['uid']
    callbacks = []
    input_directory = os.path.join(TEMPLATE_PATH, plan_name)
    if os.path.isdir(input_directory):
        for input_path in glob.glob(os.path.join(input_directory, '*.ipynb')):
            basename = os.path.basename(input_path)
            filename, ext = os.path.splitext(basename)
            output_path = os.path.join(
                OUTPUT_PATH,
                plan_name,
                f'{filename}_{uid}{ext}')

            def callback(name, doc):
                if name == 'stop':
                    papermill.execute_notebook(
                        input_path,
                        output_path,
                        dict(uid=uid))

        callbacks.append(callback)
    if not callbacks:
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
