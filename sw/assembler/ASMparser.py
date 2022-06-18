import sys


class Parser:
    def __init__(self, inputFile):
        #       self.inputFile = inputFile
        self.file = inputFile  # self.openFile()  # arquivo de leitura

        self.lineNumber = 0  # linha atual do arquivo (nao do codigo gerado)
        self.currentCommand = ""  # comando atual
        self.currentLine = ""  # linha de codigo atual

        self.CommandType = {"A": "A_COMMAND", "C": "C_COMMAND", "L": "L_COMMAND"}

    def openFile(self):
        try:
            return open(self.inputFile, "r")
        except IOError:
            sys.exit("Erro: inputFile not found: {}".format(self.inputFile))

    def reset(self):
        self.file.seek(0)

    def close(self):
        self.file.close()

    def advanced(self):
        # Carrega uma instrução e avança seu apontador interno para o próxima
        # linha do arquivo de entrada. Caso não haja mais linhas no arquivo de
        # entrada o método retorna "Falso", senão retorna "Verdadeiro".
        # @return Verdadeiro se ainda há instruções, Falso se as instruções terminaram.
        while True:
            line = self.file.readline()
            if not line:
                return False
            self.currentLine = line
            line = line.split(";")[0].rstrip()
            if line.strip():
                self.currentCommand = line.replace(",", " ").split()
                return True

    def command(self):
        return self.currentCommand

    def commandType(self):
        if self.currentCommand[0] == "leaw":
            return self.CommandType["A"]
        elif self.currentCommand[0].count(":"):
            return self.CommandType["L"]
        else:
            return self.CommandType["C"]

    def symbol(self):
        return self.currentCommand[1].split("$")[1]

    def label(self):
        return self.currentCommand[0].split(":")[0]

    def instruction(self):
        return self.currentCommand


if __name__ == "__main__":
    p = Parser("add.nasm")

    while True:
        if p.advanced():
            print(p.currentLine)
            print("\t" + p.commandType())
            if p.commandType() == "L_COMMAND":
                print("\t" + p.label())
            elif p.commandType() == "A_COMMAND":
                print("\t" + p.symbol())
            else:
                print(p.currentCommand)

            pass
        else:
            break
