from easse.sari import corpus_sari, get_corpus_sari_operation_scores
from easse.bleu import corpus_bleu
from easse.cli import report

base = "/home/rumesh/Desktop/semits2/5/new2/"
original =base+"comp.txt"
sys_out = base + "si-cc_SUPERVISED_RATE_1_RL_FINETUNE_0"
refr = base+"ref.txt"
original = open(original).readlines()
syst = open(sys_out).readlines()
ref = open(refr).readlines()

print("SARI Score using ref: ", corpus_sari(orig_sents=original,
                                            sys_sents=syst,
                                            refs_sents=[ref]))

print("SARI components: add, keep ,del ", get_corpus_sari_operation_scores(orig_sents=original,
                                                                           sys_sents=syst,
                                                                           refs_sents=[ref]))
print("BLEU: ", corpus_bleu(sys_sents=syst, refs_sents=[ref]))

# report(
#     "custom",
#     sys_sents_path=sys_out,
#     orig_sents_path=original,
#     refs_sents_paths=refr,
#     lowercase=False
# )
