import os, numpy as np, nibabel as nib
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy.stats.stats import pearsonr
import pandas as pd

dataPath = '/home/despoB/kaihwang/TRSE/TDSigEI/'
dataPath2 = '/home/despoB/akshayj/TDSigEI/SpatialCorr/'
subjects = ['503', '505', '508', '509', '510', '512', '513', '516', '517', '518', '519', '523', '527', '528', '529', '530', '531', '532', '534', '536', '537', '539', '540', '542', '546', '547', '549', '550']
#subjects = ['503']
# blocks_to_keep = range(1,20) + range(28,47) + range(55,74) + range(82,101) \
# + range(1+102,20+102) + range(28+102,47+102) + range(55+102,74+102) + range(82+102,101+102) \
# + range(1+204,20+204) + range(28+204,47+204) + range(55+204,74+204) + range(82+204,101+204) \
# + range(1+306,20+306) + range(28+306,47+306) + range(55+306,74+306) + range(82+306,101+306) 

repEnhanceArrFFA = np.zeros((len(subjects), 21))
repSuppArrFFA = np.zeros((len(subjects), 21))
repEnhanceArrPPA = np.zeros((len(subjects), 21))
repSuppArrPPA = np.zeros((len(subjects), 21))

SpatialCorrDF = pd.DataFrame()
corrFunc2 = lambda a, c, d: np.array(pearsonr(a, d)) - np.array(pearsonr(c, d))
subjNum = 0
for i, subj in enumerate(subjects):

    print '*******************{1}. SUBJECT {0}*******************'.format(subj, i)
    SpatialCorrDF.set_value(i, 'Subject', subj)
    os.chdir(dataPath+subj)
    #convert to nifti
    files = os.listdir('.')
    if 'FIR_Hp.nii.gz' not in files:
        os.system("3dAFNItoNIFTI -prefix FIR_FH.nii.gz FH_FIR+tlrc")
        os.system("3dAFNItoNIFTI -prefix FIR_HF.nii.gz HF_FIR+tlrc")
        os.system("3dAFNItoNIFTI -prefix FIR_Fo.nii.gz Fo_FIR+tlrc")
        os.system("3dAFNItoNIFTI -prefix FIR_Ho.nii.gz Ho_FIR+tlrc")
        os.system("3dAFNItoNIFTI -prefix FIR_Fp.nii.gz Fp_FIR+tlrc")
        os.system("3dAFNItoNIFTI -prefix FIR_Hp.nii.gz Hp_FIR+tlrc")
    else:
        print('Skipping afni to nifti file conversion...')
    fn = 'FIR_FH.nii.gz'
    FH_beta = nib.load(fn).get_data()
    fn = 'FIR_HF.nii.gz'
    HF_beta = nib.load(fn).get_data()
    fn = 'FIR_Fo.nii.gz'
    Fo_beta = nib.load(fn).get_data()
    fn = 'FIR_Ho.nii.gz'
    Ho_beta = nib.load(fn).get_data()
    fn = 'FIR_Fp.nii.gz'
    Fp_beta = nib.load(fn).get_data()
    fn = 'FIR_Hp.nii.gz'
    Hp_beta = nib.load(fn).get_data()

    #FH_beta = nib.load(dataPath + subj + '/FIR_FH.nii.gz')
    #HF_beta = nib.load(dataPath + subj + '/FIR_HF.nii.gz')
    #Fo_beta = nib.load(dataPath + subj + '/FIR_Fo.nii.gz')
    #Ho_beta = nib.load(dataPath + subj + '/FIR_Ho.nii.gz')
    #Fp_beta = nib.load(dataPath + subj + '/FIR_Fp.nii.gz')
    #Hp_beta = nib.load(dataPath + subj + '/FIR_Fp.nii.gz')

    ffa = nib.load(dataPath + subj + '/FFA_indiv_ROI.nii.gz').get_data()
    ppa = nib.load(dataPath + subj + '/PPA_indiv_ROI.nii.gz').get_data()
    
    Ho_ffa = Ho_beta[ffa!=0].mean(1)
    Fo_ffa = Fo_beta[ffa!=0].mean(1)
    FH_ffa = FH_beta[ffa!=0].mean(1)
    Fp_ffa = Fp_beta[ffa!=0].mean(1)
    HF_ffa = HF_beta[ffa!=0].mean(1)
    Hp_ffa = Hp_beta[ffa!=0].mean(1)
    Ho_ppa = Ho_beta[ppa!=0].mean(1)
    Fo_ppa = Fo_beta[ppa!=0].mean(1)
    FH_ppa = FH_beta[ppa!=0].mean(1)
    Fp_ppa = Fp_beta[ppa!=0].mean(1)
    HF_ppa = HF_beta[ppa!=0].mean(1)
    Hp_ppa = Hp_beta[ppa!=0].mean(1)

    #FH_ffaT = FH_beta[ffa!=0]
    #HF_ffaT = HF_beta[ffa!=0]
    #FH_ppaT = FH_beta[ppa!=0]
    #HF_ppaT = HF_beta[ppa!=0]

    #Measure 2b: Compared to target only condition as template for FFA
    repEnhancementB = corrFunc2(FH_ffa, Fp_ffa, Fo_ffa)
    repSuppressionB = corrFunc2(HF_ffa, Fp_ffa, Fo_ffa)
    print('Measure 2b: FFA Representation Similarity compared to attention only')
    print('\tRepresentation Enhancement: {0}'.format(repEnhancementB[0]))
    print('\tRepresentation Suppression: {0}'.format(repSuppressionB[0]))
    SpatialCorrDF.set_value(i, 'FFARepEnhancement', repEnhancementB[0])
    SpatialCorrDF.set_value(i, 'FFARepSuppression', repSuppressionB[0])

    #Measure 3b: Compared to target only condition as template for PPA
    repEnhancementB = corrFunc2(HF_ppa, Hp_ppa, Ho_ppa)
    repSuppressionB = corrFunc2(FH_ppa, Hp_ppa, Ho_ppa)
    print('Measure 3b: PPA Representation Similarity compared to attention only')
    print('\tRepresentation Enhancement: {0}'.format(repEnhancementB[0]))
    print('\tRepresentation Suppression: {0}'.format(repSuppressionB[0]))
    SpatialCorrDF.set_value(i, 'PPARepEnhancement', repEnhancementB[0])
    SpatialCorrDF.set_value(i, 'PPARepSuppression', repSuppressionB[0])

    # # Measure 4a: Time series correlation coefficient for FFA
    # repEnhanceArr1 = np.zeros(FH_ffaT.shape[1])
    # repSuppArr1 = np.zeros(FH_ffaT.shape[1])
    # for i in range(FH_ffaT.shape[1]):
    #     repEnhanceArr1[i] = corrFunc2(FH_ffaT[:,i], Fp_ffa, Fo_ffa)[0]
    #     repSuppArr1[i] = corrFunc2(HF_ffaT[:, i], Fp_ffa, Fo_ffa)[0]
    # repEnhanceArrFFA[subjNum, :] = repEnhanceArr1
    # repSuppArrFFA[subjNum, :] = repSuppArr1
    # print('Measure 4a: Time series pattern enhancement/suppression for FFA')

    # # Measure 4b: Time series correlation coefficient for PPA
    # repEnhanceArr2 = np.zeros(FH_ppaT.shape[1])
    # repSuppArr2 = np.zeros(FH_ppaT.shape[1])
    # for i in range(FH_ppaT.shape[1]):
    #     repEnhanceArr2[i] = corrFunc2(HF_ppaT[:,i], Hp_ppa, Ho_ppa)[0]
    #     repSuppArr2[i] = corrFunc2(FH_ppaT[:, i], Hp_ppa, Ho_ppa)[0]
    # repEnhanceArrPPA[subjNum, :] = repEnhanceArr2
    # repSuppArrPPA[subjNum, :] = repSuppArr2
    # print('Measure 4b: Time series pattern enhancement/suppression for PPA')
    # print('FFA Shape', FH_ffaT.shape)
    # print('PPA Shape', FH_ppaT.shape)

    subjNum += 1
    #end for loop

SpatialCorrDF.to_csv('/home/despoB/akshayj/TDSigEI/SpatialCorr/SpatialCorr_df.csv')
# Average across subjects for PPA
# enhanceMeanPPA = repEnhanceArrPPA.mean(0)
# enhanceErrorPPA = repEnhanceArrPPA.std(0) / np.sqrt(len(subjects))
# suppMeanPPA = repSuppArrPPA.mean(0)
# suppErrorPPA = repSuppArrPPA.std(0) / np.sqrt(len(subjects))

# # Average across subjects for FFA
# enhanceMean = repEnhanceArrFFA.mean(0)
# enhanceError = repEnhanceArrFFA.std(0)/np.sqrt(len(subjects))
# suppressMean = repSuppArrFFA.mean(0)
# suppressError = repSuppArrFFA.std(0)/np.sqrt(len(subjects))

# x = np.linspace(1, len(repSuppArr1), len(repSuppArr1))
# plt.subplot(1, 2, 1)
# plt.plot(x, enhanceMean, ':bo', label='Enhancement')
# plt.plot(x, suppressMean, '-ro', label='Suppression')
# plt.fill_between(x, enhanceMean - 0.75*enhanceError, enhanceMean + 0.75*enhanceError, alpha=0.2, edgecolor='c', facecolor='c')
# plt.fill_between(x, suppressMean - 0.75*suppressError, suppressMean + 0.75*suppressError, alpha = 0.2, edgecolor='m', facecolor='m')
# plt.title('Representation Similarity across time for faces in FFA')
# plt.xlabel('Time')
# plt.ylabel('Correlation Coefficient')
# plt.legend()

# plt.subplot(1, 2, 2)
# plt.plot(x, enhanceMeanPPA, ':bo', label='Enhancement')
# plt.plot(x, suppMeanPPA, '-ro', label='Suppression')
# plt.fill_between(x, enhanceMeanPPA - 0.75*enhanceErrorPPA, enhanceMeanPPA + 0.75*enhanceErrorPPA, alpha=0.2, edgecolor='c', facecolor='c')
# plt.fill_between(x, suppMeanPPA - 0.75*suppErrorPPA, suppMeanPPA + 0.75*suppErrorPPA, alpha=0.2, edgecolor='m', facecolor='m')
# plt.title('Representation Similarity across time for houses in PPA')
# plt.xlabel('Time')
# plt.ylabel('Correlation Coefficient')
# plt.legend()
# plt.show()
