#!/usr/bin/env python3

import click
import yaml
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
        self.nasmDir = ""
        self.hackDir = ""
        self.tstDir = ""
        self.workDir = ""
        self.open(configFile)

    def open(self, configFile):
        try:
            with open(configFile, "r") as file:
                self.config = yaml.load(file, Loader=yaml.FullLoader)
                self.tests = self.config["test_files"]
                self.name = self.config["config"]["name"]
                self.workDir = os.path.dirname(os.path.abspath(configFile))
                self.nasmDir = path.join(self.workDir, self.config["config"]["nasmDir"])
                self.hackDir = path.join(self.workDir, self.config["config"]["hackDir"])
                self.tstDir = path.join(self.workDir, self.config["config"]["tstDir"])
        except FileNotFoundError:
            print("%s: file not found" % self.confFileName)
            return False

    def getTests(self):
        return self.tests


class cpuTest:
    def __init__(self):
        self.config = ""
        self.testsConfig = []
        self.mem = []
        self.lst_data = []

    def updateConfig(self, config):
        self.lst_data = []
        self.mem = []
        self.config = config

    def baseAddress(self, folder, name):
        return path.join(folder, name)

    def getTestFilesFromTestName(self, tstFolder):
        for file in listdir(tstFolder):
            if "_in.mif" in file:
                name = file[:-7]
                mif = path.join(tstFolder, file)
                tst = path.join(tstFolder, name + "_tst.mif")
                basePath = os.path.join(tstFolder, name) + "{}"
                refMem = basePath.format("_tst.mif")
                dumpMem = basePath.format("_ram_dump.txt")
                inMem = basePath.format("_in.mif")
                trace = basePath.format("")
                self.testsConfig.append(
                    {
                        "tstFolder": tstFolder,
                        "name": name,
                        "ramFile": mif,
                        "tstFile": tst,
                        "basePath": basePath,
                        "refMem": refMem,
                        "dumpMem": dumpMem,
                        "inMem": inMem,
                        "trace": trace,
                    }
                )
        return self.testsConfig

    def run(self):
        print("--- %s ---" % self.config["name"])
        self.mem = ram_init_from_mif(self.config["inMem"])
        tb = z01_sim(self.mem, self.config["romFile"], self.lst_data)
        tb.config_sim(trace=True, name=self.config["trace"], tracebackup=False)
        tb.run_sim(self.config["runTime"])
        tb.quit_sim()

    def dump(self):
        mem_dump_file(self.mem, self.config["dumpMem"])
        lstWrite(self.lst_data, self.config["trace"])

    def test(self, ref, dut):
        if ram_test(ref, dut) == 0:
            return 0
        else:
            return 1


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


@click.argument("tstfile", type=click.Path("r"))
@assembler.command()
def from_config(tstfile):
    conf = configFile(tstFile)
    helpers.createDir(conf.hackDir)

    print(" 1/1 gerando novos arquivos .hackpath")
    print(" destine: {}".format(conf.hackDir))

    for n in conf.getTests():
        fNasm = open(path.join(conf.nasmDir, n + ".nasm"), "r")
        fHack = open(path.join(conf.hackDir, n + ".hack"), "w")
        assembler = Assembler(fNasm, fHack)
        print("\t" + n + ".hack")


@click.argument("time", default=50000)
@click.argument("path")
@click.argument("nasm")
@hw.command()
def from_dir(nasm, path, time):
    cpu = cpuTest()
    tests = cpu.getTestFilesFromTestName(path)
    for config in tests:
        config["romFile"] = nasm
        config["runTime"] = time
        cpu.updateConfig(config)
        cpu.run()
        cpu.dump()
        memRef = ram_init_from_mif(config["refMem"], False, False)
        memDump = ram_init_from_mif(config["dumpMem"], False, False)
        if cpu.test(memRef, memDump) == 0:
            print("pass")
        else:
            print("fail")


# TODO estruturar codigo compartilhado
@click.argument("tstfile", type=click.Path("r"))
@hw.command()
def from_config(tstfile):
    conf = configFile(tstfile)
    for n in conf.getTests():
        cpu = cpuTest()
        path = os.path.join(conf.tstDir, n)
        tests = cpu.getTestFilesFromTestName(path)
        for config in tests:
            config["romFile"] = os.path.join(conf.hackDir, n) + ".hack"
            config["runTime"] = 50000
            cpu.updateConfig(config)
            cpu.run()
            cpu.dump()
            memRef = ram_init_from_mif(config["refMem"], False, False)
            memDump = ram_init_from_mif(config["dumpMem"], False, False)
            if cpu.test(memRef, memDump) == 0:
                print("pass")
            else:
                print("fail")


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
