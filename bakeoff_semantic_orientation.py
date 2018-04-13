__author__ = "Morgan Bryant"
__version__ = "CS224u, Stanford, Spring 2018 term"

from collections import defaultdict
import csv
import numpy as np
import os, sys
import pandas as pd
from scipy.stats import pearsonr, spearmanr
import vsm
import sys
data_home = 'vsmdata'

def bootstrap(seedset, DF, var, dist_factor, laplace, nsteps, nadditions):
    print('orig set:', seedset)
    ssd = defaultdict(lambda:laplace)
    ssd.update({s:laplace for s in seedset[0]})
    #for s in seedset: 
    #    ssd[s]=[laplace,var]
    print('orig ssd:', ssd)

    for stp in range(nsteps):
        ssnext = []
        ssprev = list(ssd.keys())
        if len(ssprev)>100:
            ssprev = ssprev.sorted(ssprev.values())[-100:]

        print('depth',stp,'on',ssprev,':')
        for seed in set(ssprev):
            if seed not in DF.index: continue
            for newseed in vsm.neighbors(seed, DF).head(
                        nadditions).keys().tolist():
                ssd[newseed] += dist_factor(stp) # <- factor in value?
                if not newseed in ssnext:
                    ssnext += [newseed]
        print('current set size:',var,stp, len(ssd.keys()))
    return ssd, ssd.keys()


#
#
#
#
#
#def semantic_orientation(
#        df,        
#        seeds1=('bad', 'nasty', 'poor', 'negative', 'unfortunate', 'wrong', 'inferior'),
#        seeds2=('good', 'nice', 'excellent', 'positive', 'fortunate', 'correct', 'superior'),
#        distfunc=vsm.cosine):    
#    """No frills implementation of the semantic Orientation (SO) method of 
#    Turney and Littman. `seeds1` and `seeds2` should be representative members 
#    of two intutively opposing semantic classes. The method will then try 
#    to rank the vocabulary by its relative association with each seed set.
#        
#    Parameters
#    ----------
#    df : pd.DataFrame
#        The matrix used to derive the SO ranking.           
#    seeds1 : tuple of str
#        The default is the negative seed set of Turney and Littman.        
#    seeds2 : tuple of str
#        The default is the positive seed set of Turney and Littman.        
#    distfunc : function mapping vector pairs to floats (default: `cosine`)
#        The measure of distance between vectors. Can also be `euclidean`, 
#        `matching`, `jaccard`, as well as any other distance measure 
#        between 1d vectors. 
#    
#    Returns
#    -------    
#    pd.Series
#        The vocabulary ranked according to the SO method, with words 
#        closest to `seeds1` at the top and words closest to `seeds2` at the 
#        bottom.
#    
#    """
#    rownames = set(df.index)
#    # Check that the seed sets are in the vocabulary, filtering
#    # where necessary, and warn the user about exclusions:
#    seeds1 = _value_check(seeds1, "seeds1", rownames)
#    seeds2 = _value_check(seeds2, "seeds2", rownames)
#    
#    # Subframes for the two seeds-sets
#    sm1 = df.loc[seeds1]
#    sm2 = df.loc[seeds2]
#    
#    # Core semantic orientation calculation:
#    def row_func(row):
#        val1 = sm1.apply(lambda x: distfunc(row, x), axis=1).sum()
#        val2 = sm2.apply(lambda x: distfunc(row, x), axis=1).sum()
#        return val1 - val2
#    
#    scores = df.apply(row_func, axis=1)
#    return scores.sort_values(ascending=False)
#
#def _value_check(ss, name, rownames):
#    new = set()
#    for w in ss:
#        if w not in rownames:
#            print("Warning: {} not in {}".format(w, name))
#        else:
#            new.add(w)
#    return new
#
#def load_warriner_lexicon(src_filename, df=None):
#    """Read in 'Ratings_Warriner_et_al.csv' and optionally restrict its 
#    vocabulary to items in `df`.
#    
#    Parameters
#    ----------
#    src_filename : str
#        Full path to 'Ratings_Warriner_et_al.csv'
#    df : pd.DataFrame or None
#        If this is given, then its index is intersected with the 
#        vocabulary from the lexicon, and we return a lexicon 
#        containing only values in both vocabularies.
#        
#    Returns
#    -------
#    pd.DataFrame
#    
#    """
#    lexicon = pd.read_csv(src_filename, index_col=0)
#    lexicon = lexicon[['Word', 'V.Mean.Sum', 'A.Mean.Sum', 'D.Mean.Sum']]
#    lexicon = lexicon.set_index('Word').rename(
#        columns={'V.Mean.Sum': 'Valence', 
#                 'A.Mean.Sum': 'Arousal', 
#                 'D.Mean.Sum': 'Dominance'})
#    if df is not None:
#        shared_vocab = sorted(set(lexicon.index) & set(df.index))
#        lexicon = lexicon.loc[shared_vocab]
#    return lexicon
#
#def read_options_file(argv):
#    with open(argv[1]) as f:
#        s1 = f.readline().split()
#        s2 = f.readline().split()
#        dfile = f.readline().strip()
#        return s1, s2, dfile
#
#
#def run_trial(inputs=None):
#    if inputs==None:
#        seeds1, seeds2, datamat_name = read_options_file(sys.argv)
#    else:
#        seeds1, seeds2, datamat_name = inputs
#    print(seeds1, seeds2, datamat_name)
#    if datamat_name == 'imdb20':
#        data_file_name = 'imdb_window20-flat.csv.gz'
#    elif datamat_name == 'imdb5':
#        data_file_name = 'imdb_window5-scaled.csv.gz'
#    datamat = pd.read_csv(
#        os.path.join(data_home, data_file_name), index_col=0)
#    datamat_ppmi = vsm.pmi(datamat)
#    datamat_ppmi_so = semantic_orientation(datamat_ppmi, seeds1, seeds2)
#    lexicon = load_warriner_lexicon(
#        os.path.join(data_home, 'Ratings_Warriner_et_al.csv'),
#        datamat_ppmi)
#    def evaluation(lexicon, so, colname='Valence', metric=pearsonr):
#        lexicon['so'] = so
#        rho, pvalue = metric(lexicon['so'], lexicon[colname])
#        print("{0:}'s r: {1:0.3f}".format(metric.__name__, rho))
#        rho_str = "{0:}'s r: {1:0.3f}".format(metric.__name__, rho)
#        return rho, rho_str
#
#    _,rho0str = evaluation(lexicon, datamat_ppmi_so, colname='Valence')
#    _,rho1str = evaluation(lexicon, datamat_ppmi_so, colname='Arousal')
#    _,rho2str = evaluation(lexicon, datamat_ppmi_so, colname='Dominance')
#    
#    with open(sys.argv[1], 'a+') as f:
#        f.write('Valence: '+rho0str+' \t')
#        f.write('Arousal: '+rho1str+' \t')
#        f.write('Dominance: '+rho2str+'\n')
#        f.write(input("Describe what you changed in this iteration: "))
#
#
#if __name__=='__main__':
#    run_trial()
#
#
#
#
#
