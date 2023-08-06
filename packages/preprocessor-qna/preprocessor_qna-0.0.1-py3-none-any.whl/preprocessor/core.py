from base_processor.core import Processor


class SquadDatasetTransformer(Processor):

    def process(self, dataset):
        paragraphs = []
        questions = []

        topic = dataset["data"][0]
        # for topic in dataset["data"]:
        for pgraph in topic["paragraphs"]:
            paragraphs.append(pgraph["context"])
            for qa in pgraph["qas"]:
                if not qa["is_impossible"]:
                    questions.append(qa["question"])

        return paragraphs, questions
