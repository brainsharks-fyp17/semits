ROOT="/home/rumesh/Desktop/semits2/1/"
MODEL_OUT="si-cc_SUPERVISED_RATE_0_RL_FINETUNE_0"
echo "(keep, del, add, SARI)"
python get_courpus_sari.py ${ROOT}/${MODEL_OUT} ${ROOT}/ref.txt ${ROOT}/comp.txt 1


