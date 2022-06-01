#!/usr/bin/env python3

import click
import yaml
from tabulate import tabulate
from myhdl import *
import sys
import os.path

# TODO usar __init__ !
sys.path.insert(0, "./hw")
sys.path.insert(0, "./sw/assembler")
from z01 import z01_sim
from simulation import *
from assembler import Assembler
from test_assembler import clearbin, assemblerFromDir


class helpers:
    def createDir(d):
        if os.path.exists(d) == False:
            os.makedirs(d)


class configFile:
    def __init__(self, configFile):
        self.config = ""
        self.tests = ""
        self.name = ""
        self.inDir = ""
        self.outDir = ""
        self.workDir = ""
        self.open(configFile)

    def open(self, configFile):
        try:
            with open(configFile, "r") as file:
                self.config = yaml.load(file, Loader=yaml.FullLoader)
                self.tests = self.config["test_files"]
                self.name = self.config["config"]["name"]
                self.workDir = os.path.dirname(os.path.abspath(configFile))
                inDir = self.config["config"]["inDir"]
                outDir = self.config["config"]["outDir"]
                self.inDir = path.join(self.workDir, inDir)
                self.outDir = path.join(self.workDir, outDir)
        except FileNotFoundError:
            print("%s: file not found" % self.confFileName)
            return False

    def getTests(self):
        return self.tests


class cpuTest:
    def __init__(self, folderPath):
        self.confFileName = "config.yml"
        self.folderPath = folderPath
        self.tests = []
        self.testsConfig = []

        self.readTestsFromConf()
        for i in self.tests:
            self.getTestFilesFromTestName(i)

    def lstHeader(self):
        h = []
        h.append("ps")
        h.append("clock")
        h.append("instruction")
        h.append("pcout")
        h.append("s_regDout")
        h.append("s_regSout")
        h.append("s_regAout")
        h.append("c_muxALUI_A")
        h.append("c_muxSD_ALU")
        h.append("outM")
        h.append("writeM")
        h.append("inM")
        return h

    def lstWrite(self, data, lstFile):
        f = open(lstFile, "w")
        f.write(tabulate(data, headers=self.lstHeader(), tablefmt="plain"))
        f.close()

    def run_cpu_test(self, tstFolder, name, inRamMif, inRomHack, testFile, time):
        print("--- %s ---" % name)
        mem = [Signal(intbv(0)) for i in range(2**15 - 1)]
        lst_data = []
        tb = z01_sim(mem, inRamMif, inRomHack, lst_data)
        tb.config_sim(trace=True, tracebackup=False)
        tb.run_sim(time)
        mem_dump_file(mem, path.join(tstFolder, name + "_ram_dump.txt"))
        if ram_test(mem, testFile) == 0:
            print("ok")
        self.lstWrite(lst_data, path.join(tstFolder, name + ".lst"))
        tb.quit_sim()
        mem = []

    def configPaths(self, name):
        romFile = path.join(self.folderPath, "hack", name + ".hack")
        if path.exists(romFile) == False:
            print("%s: file not found" % romFile)
            return False

        tstFolder = path.join(self.folderPath, "tests", name + "/")
        if path.exists(tstFolder) == False:
            print("%s: dir not found" % tstFolder)
            return False

        return romFile, tstFolder

    def readTestsFromConf(self):
        try:
            with open(path.join(self.folderPath, self.confFileName), "r") as file:
                conf = yaml.load(file, Loader=yaml.FullLoader)
                self.tests = conf["test_files"]
                return
        except FileNotFoundError:
            print("%s: file not found" % self.confFileName)
            return False

    def getTestFilesFromTestName(self, name):

        romFile, tstFolder = self.configPaths(name)

        for file in listdir(tstFolder):
            if "_in.mif" in file:
                tstName = file[:-7]
                mif = path.join(tstFolder, file)
                tst = path.join(tstFolder, tstName + "_tst.mif")
                self.testsConfig.append(
                    {
                        "tstFolder": tstFolder,
                        "name": tstName,
                        "romFile": romFile,
                        "ramFile": mif,
                        "tstFile": tst,
                    }
                )

    def run(self):
        for t in self.testsConfig:
            self.run_cpu_test(
                t["tstFolder"],
                t["name"],
                t["ramFile"],
                t["romFile"],
                t["tstFile"],
                50000,
            )


@click.group()
def assembler():
    pass


@click.group()
def hw():
    pass


@click.argument("hack", type=click.Path("w"))
@click.argument("nasm", type=click.Path("r"))
@assembler.command()
def from_nasm(nasm, hack):
    assembler = Assembler(nasm, hack)


@click.argument("hackPath")
@click.argument("nasmPath")
@assembler.command()
def from_dir(nasmpath, hackpath):
    assemblerFromDir(nasmpath, hackpath)


@click.argument("configfile", type=click.Path("r"))
@assembler.command()
def from_config(configfile):
    conf = configFile(configfile)

    helpers.createDir(conf.outDir)

    print(" 1/1 gerando novos arquivos .hackpath")
    print(" destine: {}".format(conf.outDir))

    for n in conf.getTests():
        fNasm = open(path.join(conf.inDir, n + ".nasm"), "r")
        fHack = open(path.join(conf.outDir, n + ".hack"), "w")
        helpers.createDir(conf.outDir)
        assembler = Assembler(fNasm, fHack)
        print("\t" + n + ".hack")


@click.argument("name")
@click.argument("inram")
@click.argument("inrom")
@click.argument("intst")
@click.argument("time")
@hw.command()
def run_single(name, inram, inrom, intst, time):
    print("---- cpu ----")
    test = cpuTest("")
    test.run_cpu_test("", name, inram, inrom, intst, int(time))


@click.argument("tstfolder")
@hw.command()
def all(tstfolder):
    print("---- cpu ----")
    test = cpuTest(tstfolder)
    test.run()


@click.group()
@click.option("--debug", "-b", is_flag=True, help="Enables verbose mode.")
@click.pass_context
def cli(ctx, debug):
    pass


#   ctx.obj.verbose = verbose

cli.add_command(hw)
cli.add_command(assembler)

if __name__ == "__main__":
    cli()

    # convert_cpu()
    # run_cpu_test(
    #    "add0",
    #    "tstAssembly/tests/add/add0_in.mif",
    #    "tstAssembly/hack/add.hack",
    #    "tstAssembly/tests/add/add0_tst.mif",
    #    300,
    # )
    #
