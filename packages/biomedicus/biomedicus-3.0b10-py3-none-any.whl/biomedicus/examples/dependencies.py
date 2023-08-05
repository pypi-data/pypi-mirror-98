#  Copyright 2020 Regents of the University of Minnesota.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from argparse import ArgumentParser
from pathlib import Path

from mtap import EventsClient, Pipeline, RemoteProcessor, Event


def main(args=None):
    parser = ArgumentParser()
    parser.add_argument('--events-service')
    parser.add_argument('--sentences-service')
    parser.add_argument('--dependencies-service')
    parser.add_argument('input_file')
    conf = parser.parse_args(args)

    with EventsClient(address=conf.events_service) as client, \
            Pipeline(
                RemoteProcessor('biomedicus-sentences', address=conf.sentences_service),
                RemoteProcessor('biomedicus-dependencies', address=conf.dependencies_service)
            ) as pipeline:
        with open(conf.input_file, 'r') as in_f:
            txt = in_f.read()
        with Event(event_id=Path(conf.input_file).name, client=client) as event:
            document = event.create_document('plaintext', txt)
            pipeline.run(document)
            for sentence in document.labels['sentences']:
                print(sentence.text)
                print('\n')
                for dependency in document.labels['dependencies'].inside(sentence):
                    print((dependency.text, dependency.deprel, dependency.head.text if dependency.head is not None else 'ROOT'))
                print('\n')


if __name__ == '__main__':
    main()
