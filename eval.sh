ROOT=$(pwd)
DATA_DIR="${ROOT}/data"

PARA_DIR="${DATA_DIR}/parallel"
DEV_DATASET="si-cc"
PARA_DEV_PATH="${PARA_DIR}/${DEV_DATASET}/newsela-eval.txt"
PARA_TEST_PATH="${PARA_DIR}/${DEV_DATASET}/test.txt"
SUPERVISED_RATE=1
RL_FINETUNE=1

TEST_OUTPUT_PARH="${ROOT}/test_result"
NAME="${DEV_DATASET}_SUPERVISED_RATE_${SUPERVISED_RATE}_RL_FINETUNE_${RL_FINETUNE}"
OUTPUT_NAME="${TEST_OUTPUT_PARH}/${NAME}"


if [ ${DEV_DATASET} = "si-cc" ]
then
	python extract.py ${PARA_TEST_PATH} ${TEST_OUTPUT_PARH}
	echo "Extraction done"
	python get_courpus_sari.py ${OUTPUT_NAME} ${TEST_OUTPUT_PARH}/ref.txt ${TEST_OUTPUT_PARH}/comp.txt 1
elif [ ${DEV_DATASET} = "wiki_large" ]
then
	python get_courpus_sari.py ${OUTPUT_NAME} ${DATA_DIR}/turkcorpus/test.8turkers.tok.turk ${DATA_DIR}/turkcorpus/test.8turkers.tok.norm
fi

