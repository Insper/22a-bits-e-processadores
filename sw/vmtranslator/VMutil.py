#!/usr/bin/env python3

import os
import sys
from VM import VM


def clearbin(outPath):
    try:
        shutil.rmtree(outPath)
    except:
        pass


def ExecFromDir(inPath, outPath, inputExtension, outExtension):
    inPath = os.path.abspath(inPath)
    outPath = os.path.abspath(outPath)

    print(" 1/2 Removendo arquivos antigos .outPath")
    print("  - {}".format(outPath))
    clearbin(outPath)

    print(" 2/2 Gerando novos arquivos .outPath")
    print(" Destine: {}".format(outPath))

    if os.path.exists(outPath) == False:
        os.makedirs(outPath)

    if os.path.isdir(inPath) and os.path.isdir(outPath):
        for filename in os.listdir(inPath):
            if filename.strip().find(inputExtension) > 0:
                nOut = os.path.join(outPath, filename[:-5] + outExtension)
                nIn= os.path.join(inPath, filename)
                fOut = open(nOut, "w")
                fIn = open(nIn, "r")
                if not os.path.basename(nIn).startswith("."):
                    print("\t" + filename[:-5] + outExtension)
                    yield fIn, fOut
    else:
        print("output must be folder")
