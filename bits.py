#!/usr/bin/env python3

import click
import yaml
from myhdl import *
import sys
import os.path
import shutil

# TODO usar __init__ !
sys.path.insert(0, "./hw")
sys.path.insert(0, "./sw/assembler")
sys.path.insert(0, "./sw/vmtranslator")
from hw_util import *
from ASM import ASM
from ASMutil import ASMfromDir
from test_z01 import test_z01
from VMTranslate import VMTranslate


class configFile:
    def __init__(self, configFile):
        self.config = ""
        self.tests = ""
        self.name = ""
        self.vmDir = ""
        self.nasmDir = ""
        self.hackDir = ""
        self.tstDir = ""
        self.workDir = ""
        self.open(configFile)

    def clearDir(self, d):
        shutil.rmtree(d)

    def createDir(self, d):
        if os.path.exists(d) is False:
            os.makedirs(d)

    def open(self, configFile):
        try:
            with open(configFile, "r") as file:
                self.config = yaml.load(file, Loader=yaml.FullLoader)
                self.tests = self.config["test_files"]
                self.name = self.config["config"]["name"]
                self.workDir = os.path.dirname(os.path.abspath(configFile))
                self.vmDir = path.join(self.workDir, self.config["config"]["vmDir"])
                self.nasmDir = path.join(self.workDir, self.config["config"]["nasmDir"])
                self.hackDir = path.join(self.workDir, self.config["config"]["hackDir"])
                self.tstDir = path.join(self.workDir, self.config["config"]["tstDir"])
        except FileNotFoundError:
            print("%s: file not found" % self.confFileName)
            return False

    def getTests(self):
        return self.tests


@click.group()
def vm():
    pass


@click.group()
def asm():
    pass


@click.group()
def hw():
    pass


@click.argument("nasm", type=click.File("w"))
@click.argument("vm")
@vm.command()
def from_vm(vm, nasm):
    # VM can be file or folder
    v = VMTranslate(vm, nasm)
    v.run()


@click.argument("tstFile", type=click.Path("r"))
@vm.command()
def from_config(tstfile):
    conf = configFile(tstfile)
    conf.clearDir(conf.nasmDir)
    conf.createDir(conf.nasmDir)
    conf.clearDir(conf.hackDir)
    conf.createDir(conf.hackDir)

    # vm -> nasm
    for n in conf.getTests():
        name = n.split('.')[0]
        fNasm = open(os.path.join(conf.nasmDir, name + ".nasm"), "w")
        fVm = os.path.join(conf.vmDir, n)
        v = VMTranslate(fVm, fNasm)
        v.run()

    # nasm -> hack
    for n in conf.getTests():
        name = n.split('.')[0]
        fNasm = open(os.path.join(conf.nasmDir, name + ".nasm"), "r")
        fHack = open(os.path.join(conf.hackDir, name + ".hack"), "w")
        asm = ASM(fNasm, fHack)
        asm.run()
        print("\t" + name + ".hack")

    for n in conf.getTests():
        name = n.split('.')[0]
        cpu = test_z01()
        tstDir = os.path.join(conf.tstDir, name)
        tests = cpu.getTestFilesFromTestName(tstDir)
        for config in tests:
            config["romFile"] = os.path.join(conf.hackDir, name) + ".hack"
            config["runTime"] = 100000
            hwFronConf(cpu, config)

    # VM can be file or folder


@click.argument("hack", type=click.File("w"))
@click.argument("nasm", type=click.File("r"))
@asm.command()
def from_nasm(nasm, hack):
    asm = ASM(nasm, hack)
    asm.run()


@click.argument("hackPath")
@click.argument("nasmPath")
@asm.command()
def from_dir(nasmpath, hackpath):
    ASMfromDir(nasmpath, hackpath)


def asmFromConfig(conf):

    print(" 1/1 gerando novos arquivos .hackpath")
    print(" destine: {}".format(conf.hackDir))

    for n in conf.getTests():
        fNasm = open(path.join(conf.nasmDir, n + ".nasm"), "r")
        fHack = open(path.join(conf.hackDir, n + ".hack"), "w")
        asm = ASM(fNasm, fHack)
        asm.run()
        print("\t" + n + ".hack")


@click.argument("tstFile", type=click.Path("r"))
@asm.command()
def from_config(tstFile):
    conf = configFile(tstFile)
    conf.createDir(conf.hackDir)
    asmFromConfig(conf)


def hwFronConf(cpu, conf):
    cpu.updateConfig(conf)
    cpu.run()
    cpu.dump()
    memRef = ram_init_from_mif(conf["refMem"], False, False)
    memDump = ram_init_from_mif(conf["dumpMem"], False, False)
    if cpu.test(memRef, memDump) == 0:
        print("pass")
    else:
        print("fail")


@click.argument("time", default=50000)
@click.argument("path")
@click.argument("nasm")
@hw.command()
def from_dir(nasm, path, time):
    cpu = test_z01()
    tests = cpu.getTestFilesFromTestName(path)
    for config in tests:
        config["romFile"] = nasm
        config["runTime"] = time
        hwFronConf(config)


@click.argument("tstFile", type=click.Path("r"))
@hw.command()
def from_config(tstfile):
    conf = configFile(tstfile)
    conf.createDir(conf.hackDir)
    asmFromConfig(conf)
    for n in conf.getTests():
        cpu = test_z01()
        path = os.path.join(conf.tstDir, n)
        tests = cpu.getTestFilesFromTestName(path)
        for config in tests:
            config["romFile"] = os.path.join(conf.hackDir, n) + ".hack"
            config["runTime"] = 100000
            hwFronConf(cpu, config)

@click.group()
@click.option("--debug", "-b", is_flag=True, help="Enables verbose mode.")
@click.pass_context
def cli(ctx, debug):
    pass


#   ctx.obj.verbose = verbose

cli.add_command(hw)
cli.add_command(asm)
cli.add_command(vm)

if __name__ == "__main__":
    cli()
