##  Copyright 2020 Regents of the University of Minnesota.
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
from typing import Dict, Any

import stanza
from mtap import Document, processor, run_processor
from mtap.processing import DocumentProcessor
from mtap.processing.descriptions import labels, label_property

from biomedicus.dependencies.stanza_parser import stanza_deps_and_upos_tags


@processor('biomedicus-selective-dependencies',
           human_name="BioMedICUS Stanza Selective Dependency Parser",
           entry_point=__name__,
           description="Calls out to the Stanford Stanza framework for dependency parsing"
                       "on a appropriate subset of sentences.",
           inputs=[
               labels(name='sentences', reference='biomedicus-sentences/sentences'),
               labels(
                   name='umls_terms',
                   reference='biomedicus-concepts/umls_terms',
                   name_from_parameter='terms_index'
               ),
               labels(
                   "negation_triggers",
                   reference='biomedicus-negex-triggers'
               )
           ],
           outputs=[
               labels(
                   name='dependencies',
                   description="The dependent words.",
                   properties=[
                       label_property(
                           'deprel',
                           description="The dependency relation",
                           data_type='str'
                       ),
                       label_property(
                           'head',
                           description="The head of this label or null if its the root.",
                           nullable=True,
                           data_type='ref:dependencies'
                       ),
                       label_property(
                           'dependents',
                           description="The dependents of ths dependent.",
                           data_type='list[ref:dependencies]'
                       )
                   ]
               ),
               labels(
                   name='upos_tags',
                   description="Universal Part-of-speech tags",
                   properties=[
                       label_property(
                           'tag',
                           description="The Universal Part-of-Speech tag",
                           data_type='str'
                       )
                   ]
               )
           ])
class StanzaSelectiveParser(DocumentProcessor):
    def __init__(self):
        stanza.download('en')
        self.tokenize = stanza.Pipeline('en', processors='tokenize')
        self.nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse',
                                   tokenize_no_ssplit=True)

    def process_document(self,
                         document: Document,
                         params: Dict[str, Any]):
        terms_index_name = params.get('terms_index', 'umls_terms')
        terms = document.labels[terms_index_name]
        negation_triggers = document.labels['negation_triggers']

        all_deps = []
        all_upos_tags = []
        sentences = []
        sentence_texts = []
        for sentence in document.labels['sentences']:
            if len(terms.inside(sentence)) == 0 or len(negation_triggers.inside(sentence)) == 0:
                continue
            sentences.append(sentence)
            sentence_texts.append(sentence.text)

        stanza_doc = self.nlp(sentence_texts)
        for (sentence, stanza_sentence) in zip(sentences, stanza_doc.sentences):
            sentence_deps, sentence_upos_tags = stanza_deps_and_upos_tags(sentence, stanza_sentence)
            all_deps.extend(sentence_deps)
            all_upos_tags.extend(sentence_upos_tags)

        document.add_labels('dependencies', all_deps)
        document.add_labels('upos_tags', all_upos_tags)


def main(args=None):
    run_processor(StanzaSelectiveParser(), args=args)


if __name__ == '__main__':
    main()
