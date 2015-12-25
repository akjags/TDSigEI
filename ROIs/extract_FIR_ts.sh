#!/bin/bash
# extract FIR timecourse for each condition from fROIs

WD='/home/despoB/kaihwang/TRSE/TDSigEI'
cd $WD


for s in $(ls -d 5*); do
	cd ${WD}/${s}

	for ROI in PPA FFA LH RH; do
		for condition in FH Fo Fp HF Ho Hp; do
			3dmaskave -mask ${ROI}_indiv_ROI.nii.gz -q ${condition}_FIR+tlrc > ${WD}/FIR_1Ds/${s}_${ROI}_${condition}.1D
			#3dmaskSVD -mask ${ROI}masked.nii.gz \
			#-input ${condition}_FIR+tlrc > ${WD}/FIR_1Ds/${s}_${ROI}_${condition}.1D 
		done
	done	


done
#${ROI}_indiv_ROI+tlrc
