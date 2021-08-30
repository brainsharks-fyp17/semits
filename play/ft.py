from easse.sari import corpus_sari, get_corpus_sari_operation_scores
from easse.bleu import corpus_bleu
from easse.cli import report

original = open("ori.txt").readlines()
syst = open("pre.txt").readlines()
ref = open("ref.txt").readlines()

print("SARI Score using ref: ", corpus_sari(orig_sents=original,
                                            sys_sents=syst,
                                            refs_sents=[ref]))

print("SARI components: add, keep ,del ", get_corpus_sari_operation_scores(orig_sents=original,
                                                                           sys_sents=syst,
                                                                           refs_sents=[ref]))
print("BLEU: ", corpus_bleu(sys_sents=syst, refs_sents=[ref]))

report(
    "custom",
    sys_sents_path="pre.txt",
    orig_sents_path="ori.txt",
    refs_sents_paths="ref.txt",
    lowercase=False
)
