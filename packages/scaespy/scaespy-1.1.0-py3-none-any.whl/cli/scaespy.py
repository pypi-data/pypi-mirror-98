"""
 * Copyright (C) 2021 - Andrea Tangherloni
 * Distributed under the terms of the GNU General Public License (GPL)
 * This file is part of scAEspy.

 * scAEspy is a free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License v3.0 as published by
 * the Free Software Foundation.
  
 * scAEspy is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU General Public License for more details.
"""


import warnings
warnings.simplefilter(action='ignore')

import argparse, os
import numpy as np
import pandas as pd
from pandas.api.types import is_string_dtype, is_numeric_dtype
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from scaespy import scAEspy
from _version import __version__

def getArgs():

    parser = argparse.ArgumentParser(add_help=False)
    
    # The required setting
    parser.add_argument('--matrices',      help='Gene expression matrices (each row must be a cell)', nargs='+', required=True)

    # Optional settings
    parser.add_argument('--delimiter',   help='String used to separate values', nargs='?', default="\t", type=str)
    parser.add_argument('--output',      help='Output folder', nargs='?', default="output", type=str)
    parser.add_argument('--latent',      help='Dimensions of the latent space', nargs='?', default=16, type=int)
    parser.add_argument('--hidden',      help='Dimensions of the hidden layers (list)', nargs='+', default=[64], type=int)
    parser.add_argument('--loss',        help='Loss function', nargs='?', default="Poisson", type=str)
    parser.add_argument('--activation',  help='Activation fuction', nargs='?', default="sigmoid", type=str)
    parser.add_argument('--epochs',      help='Number of epochs', nargs='?', default=100, type=int)
    parser.add_argument('--batch',       help='Batch size', nargs='?', default=100, type=int)
    parser.add_argument('--gaussian',    help='Number of Gaussian distribution(s)', nargs='?', default=1, type=int)
    parser.add_argument('--alpha',       help='alpha setting used to balance between KL and MMD', nargs='?', default=0,  type=int)
    parser.add_argument('--lambda',      help='lambda setting used to balance between KL and MMD', nargs='?', default=1, type=int)
    parser.add_argument('--patience',    help='Max patience', nargs='?', default=None, type=int)
    parser.add_argument('--seed',        help='Seed value used for reproducibility', nargs='?', default=None, type=int)
    parser.add_argument('--synthetic',   help='Number of synthetic cells to generate', nargs='?', default=None, type=int)

    # Settings without a parameter value
    parser.add_argument('--constrained', help='Enable the constrained version of the loss fuction', action='store_true')
    parser.add_argument('--clipping',    help='Clip the value when NB loss fuctions are used', action='store_true')
    parser.add_argument('--prior',       help='Enable the learnable prior distribution', action='store_true')
    parser.add_argument('--split',       help='Split the provided matrix into train and test sets', action='store_true')
    parser.add_argument('--plot',        help='Plot the term of the ELBO function', action='store_true')
    parser.add_argument('--verbose',     help='Enable the verbose modality of scAEspy', action='store_true')
    parser.add_argument('--help',        action='help')

    args = vars(parser.parse_args())

    return args

def prefixAE(args):
    if args["alpha"] == 0 and args["lambda"] == 1:
        if args["gaussian"] == 1:
            value =  "VAE"
        elif args["gaussian"] > 1:
            value =  "GMVAE"

    elif args["alpha"] == 1 and args["lambda"] == 1:
        if args["gaussian"] == 1:
            value =  "MMDAE"
        elif args["gaussian"] > 1:
            value =  "GMMMD"

    elif args["alpha"] == 0 and args["lambda"] == 2:
        if args["gaussian"] == 1:
            value =  "MMDVAE"
        elif args["gaussian"] > 1:    
            value =  "GMMMDVAE"

    else:
        value = "AE_alpha=%d_lambda=%d"%(args["alpha"], args["lambda"])

    return value

def saveCells(args, cells_ids, genes_ids, prefix, synthetic_cells, reconstructed_cells, latent_cells):
    
    if args["synthetic"] is not None:
        synthetic_cells = pd.DataFrame(index=["Cell %d"%(d+1) for d in range(args["synthetic"])], columns=genes_ids, data=synthetic_cells)
        synthetic_cells.to_csv(args["output"]+os.sep+"%s_synthetic_cells.tsv"%prefix, sep="\t")
    
    latent_cells = pd.DataFrame(index=cells_ids, columns=["Latent_%d"%(d+1) for d in range(args["latent"])], data=latent_cells)
    latent_cells.to_csv(args["output"]+os.sep+"%s_latent_representation.tsv"%prefix, sep="\t")

    reconstructed_cells = pd.DataFrame(index=cells_ids, columns=genes_ids, data=reconstructed_cells)
    reconstructed_cells.to_csv(args["output"]+os.sep+"%s_reconstructed_cells.tsv"%prefix, sep="\t")
    
def saveLosses(args, prefix, history):

    train_losses = pd.DataFrame(columns=["Total loss",
                                         "Reconstruction loss",
                                         "KLy loss",
                                         "KLz loss",
                                         "MMD loss"],
                                data=np.transpose([history["train_loss"],
                                                   history["train_rec"],
                                                   history["train_kly"],
                                                   history["train_klz"],
                                                   history["train_mmd"]])) 

    test_losses = pd.DataFrame(columns=["Total loss",
                                        "Reconstruction loss",
                                        "KLy loss",
                                        "KLz loss",
                                        "MMD loss"],
                               data=np.transpose([history["test_loss"],
                                                  history["test_rec"],
                                                  history["test_kly"],
                                                  history["test_klz"],
                                                  history["test_mmd"]])) 

    train_losses.to_csv(args["output"]+os.sep+"%s_train_losses.tsv"%prefix, sep="\t")
    test_losses.to_csv(args["output"]+os.sep+"%s_test_losses.tsv"%prefix, sep="\t")

    
def readMatrices(matrices, delimiter):
    
    dataframes = []
    for matrix in matrices:
        try:
            df = np.loadtxt(matrix, delimiter=delimiter)
            df = pd.DataFrame(df)
            if df.shape[1] < 2:
                exit(-100)

            dataframes.append(df)
            continue
        except:
            pass
        try:
            df = pd.read_csv(matrix, sep=delimiter)
            if df.shape[1] < 2:
                exit(-100)
            
            if is_string_dtype(df[df.columns[0]]):
                df.set_index(df.columns[0], drop=True, inplace=True)
                df.index.name = None
            dataframes.append(df)
            continue
        except:
            print("Error, unable to load the gene expression matrix %s using the provided delimiter"%matrix)
            print("Consider using another delimiter for .%s files"%matrix.split(".")[-1])
            exit(-100)
    
    ignore_index = False
    if len(dataframes) > 1:
        toExit = False
        for idx,dataframe in enumerate(dataframes):
            try:
                names = list(map(int, dataframe.columns.tolist()))
                print(names)
                print("The gene names of matrix %s are numeric"%matrices[idx])
                toExit = True
            except:
                continue
        
        if toExit:
            print("Consider using standard gene names or strings")
            exit(-200)

        names = set(dataframes[0].index.tolist())
        for dataframe in dataframes[1:]:
            names = names.intersection(set(dataframe.index.tolist()))
        
        if len(names) > 0:
            print("* Warning! There are some cells with the same IDs")
            print("* Cells have been concatenated with new IDs")
            ignore_index = True


    merged = pd.concat(dataframes, join="outer", axis=0, ignore_index=ignore_index)
    merged = merged.fillna(0)
                    
    return merged.index.tolist(), merged.columns.tolist(), merged.values

def main():

    print("#"*200)
    print("* scAEspy (v.%s): a unifying tool based on autoencoders for the analysis of single-cell RNA sequencing data"%__version__)
    print()

    args = getArgs()

    if args["verbose"]:
        print("* Loading the gene expression matrices using the provided delimiter")

    cells_ids, genes_ids, merged_matrix = readMatrices(args["matrices"], args["delimiter"]) 

    prefix = prefixAE(args)

    if args["verbose"]:
        print("* Initialising scAEspy ...")
        print("\t* alpha = %2d; lambda = %2d -> %s"%(args["alpha"], args["lambda"], prefix))
        print("\t* Loss                    -> %s"%args["loss"])
        print("\t* Constrained             -> %s"%args["constrained"])
        print("\t* Number of Gaussian(s)   -> %s"%args["gaussian"])
        print("\t* Learnable prior         -> %s"%args["prior"])
        print("\t* Number of epochs        -> %s"%args["epochs"])
        print("\t* Batch size              -> %s"%args["batch"])
        print("\t* Max patience (epochs)   -> %s"%args["patience"])
        print()
        print()


    scaespy = scAEspy(merged_matrix.shape[1],
                      hidden_layers   = args["hidden"],
                      latent_layer    = args["latent"],
                      activation      = args["activation"],
                      rec_loss        = args["loss"],
                      num_gaussians   = args["gaussian"],
                      learnable_prior = args["prior"],
                      alpha           = args["alpha"],
                      lambd           = args["lambda"],
                      constrained     = args["constrained"],
                      clipping        = args["clipping"],
                      verbose         = args["verbose"],
                      seed            = args["seed"])

    if args["verbose"]:
        print()
        print("#"*200)
        print("* Building %s ..."%prefix)
    
    scaespy.build()

    if args["split"]:
        if args["verbose"]:
            print()
            print("* Splitting in training and validation sets shuffling the data ...")
            print()
            print("* Analysing %d cells across %d genes"%merged_matrix.shape)
            print()
            print()
    
        x_train, x_test = train_test_split(merged_matrix, test_size=0.1, random_state=42, shuffle=True)
        scaespy.train(x_train, x_test, epochs=args["epochs"], batch_size=args["batch"], max_patience=args["patience"])
    
    else:
        if args["verbose"]:
            print()
            print("* Shuffling the data ...")
            print()
            print("* Analysing %d cells across %d genes"%merged_matrix.shape)
            print()
            print()
        
        matrix_shuffled = shuffle(merged_matrix, random_state=42)
        scaespy.train(matrix_shuffled, matrix_shuffled, epochs=args["epochs"], batch_size=args["batch"], max_patience=args["patience"])

    if not os.path.isdir(args["output"]):
        os.mkdir(args["output"])

    history = scaespy.getHistory()
    if args["verbose"]:
        print("#"*200)
        print("*  Saving the values of the terms of the ELBO function ...")
        print()
    saveLosses(args, prefix, history)

    if args["plot"]:
        if args["verbose"]:
            print("*  Plotting the terms of the ELBO function ...")
        scaespy.plotLosses(show=False, folder=args["output"], name=prefix)

    synthetic_cells     = None
    if args["verbose"]:
        print("*  Generating the reconstructed cells ...")
        print()
    reconstructed_cells = scaespy.reconstructedRepresentation(merged_matrix)

    if args["verbose"]:
        print("*  Generating the latent representation of the cells ...")
        print()
    latent_cells        = scaespy.latentRepresentation(merged_matrix)

    if args["synthetic"] is not None:
        if args["verbose"]:
            print("*  Generating %d synthetic cells ..."%args["synthetic"])
        synthetic_cells = scaespy.sampling(args["synthetic"])

    if args["verbose"]:
        print("*  Saving the generated data ...")
    saveCells(args, cells_ids, genes_ids, prefix, synthetic_cells, reconstructed_cells, latent_cells)
    
    print("#"*200)
    print()

if __name__ == '__main__':

    main()