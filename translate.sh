#/bin/bash

SUBWORDTools=NMTScripts/subword-nmt

export ENGINEDIR=$1
export DATADIR=$ENGINEDIR/data
export MODELDIR=$ENGINEDIR/model

$SUBWORDTools/apply_bpe.py -c $DATADIR/bpe.src-trg < $DATADIR/WinoBias+.test > $DATADIR/WinoBias+.sw.test
$SUBWORDTools/apply_bpe.py -c $DATADIR/bpe.src-trg < $DATADIR/OpenSubsReddit.test > $DATADIR/OpenSubsReddit.sw.test
$SUBWORDTools/apply_bpe.py -c $DATADIR/bpe.src-trg < $DATADIR/WinoBias+.references > $DATADIR/WinoBias+.sw.references
$SUBWORDTools/apply_bpe.py -c $DATADIR/bpe.src-trg < $DATADIR/OpenSubsReddit.references > $DATADIR/OpenSubsReddit.sw.references
$SUBWORDTools/apply_bpe.py -c $DATADIR/bpe.src-trg < $DATADIR/Reddit.test > $DATADIR/Reddit.sw.test
$SUBWORDTools/apply_bpe.py -c $DATADIR/bpe.src-trg < $DATADIR/Reddit.references > $DATADIR/Reddit.sw.references


SRC=test
TRG=references

for FILE in Reddit WinoBias+ OpenSubsReddit
do
	rm $DATADIR/ready_to_translate -rf

	fairseq-preprocess --source-lang $SRC --target-lang $TRG \
        	--testpref $DATADIR/$FILE.sw \
		--srcdict $DATADIR/ready_to_train/dict.src.txt \
		--tgtdict $DATADIR/ready_to_train/dict.trg.txt \
        	--destdir $DATADIR/ready_to_translate

	echo "Done preprocessing"

	fairseq-generate $DATADIR/ready_to_translate \
		--path $MODELDIR/checkpoint_best.pt \
		--batch-size 1 --remove-bpe > $FILE.translation

done


