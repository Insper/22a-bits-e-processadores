import sys


class Code:
    def __init__(self):
        pass

    def _dest_to_string(self, dest):
        s = ""
        s = str(dest["(%A)"]) + str(dest["%D"]) + str(dest["%A"])
        return s

    def dest(self, mnemnonic):

        d = {"E": 0, "%A": 0, "%D": 0, "(%A)": 0}
        single_dest = ["incw", "decw", "notw", "negw"]
        none_dest = ["jmp", "je", "jg", "jge", "jl", "jle", "jne", "nop"]
        special_dest = ["movw"]
        begin = -1

        if mnemnonic[0] in (v for v in special_dest):
            begin = 2
        elif mnemnonic[0] in (v for v in single_dest):
            begin = 1
        elif mnemnonic[0] in (v for v in none_dest):
            begin = 0
        else:
            begin = 3

        if begin > 0:
            for i in mnemnonic[begin:]:
                d[i] = 1

        return self._dest_to_string(d)

    def comp(self, mnemnonic):
        ula = {
            "0": "101010",
            "1": "111111",
            "-1": "111010",
            "x": "001100",
            "y": "110000",
            "!x": "001101",
            "!y": "110001",
            "-x": "001111",
            "-y": "110011",
            "x+1": "011111",
            "1+x": "011111",
            "y+1": "110111",
            "1+y": "110111",
            "x-1": "001110",
            "y-1": "110010",
            "x+y": "000010",
            "y+x": "000010",
            "x-y": "010011",
            "y-x": "000111",
            "x&y": "000000",
            "y&x": "000000",
            "x|y": "010101",
            "y|x": "010101",
        }

        instruction = ""
        movInt = 0
        if mnemnonic[0] == "movw":
            instruction = mnemnonic[1]
            movInt = 1
        elif mnemnonic[0] == "addw":
            instruction = mnemnonic[1] + "+" + mnemnonic[2]
        elif mnemnonic[0] == "subw":
            instruction = mnemnonic[1] + "-" + mnemnonic[2]
        elif mnemnonic[0] == "rsubw":
            instruction = mnemnonic[2] + "-" + mnemnonic[1]
        elif mnemnonic[0] == "incw":
            instruction = mnemnonic[1] + "+1"
        elif mnemnonic[0] == "decw":
            instruction = mnemnonic[1] + "-1"
        elif mnemnonic[0] == "notw":
            instruction = "!" + mnemnonic[1]
        elif mnemnonic[0] == "negw":
            instruction = "-" + mnemnonic[1]
        elif mnemnonic[0] == "andw":
            instruction = mnemnonic[1] + "&" + mnemnonic[2]
        elif mnemnonic[0] == "orw":
            instruction = mnemnonic[1] + "|" + mnemnonic[2]
        elif mnemnonic[0] == "nop":
            instruction = "$0"
        elif (
            mnemnonic[0] == "jg"
            or mnemnonic[0] == "je"
            or mnemnonic[0] == "jge"
            or mnemnonic[0] == "jl"
            or mnemnonic[0] == "jne"
            or mnemnonic[0] == "jle"
            or mnemnonic[0] == "jmp"
        ):
            instruction = "x"

        r0 = "0"
        for i in range(0, len(mnemnonic) - movInt):
            if mnemnonic[i] == "(%A)":
                r0 = "1"
                break

        replace = {"(%A)": "y", "%D": "x", "%A": "y", "$": ""}
        for key, value in replace.items():
            instruction = instruction.replace(key, value)

        bin = ""
        if instruction in ula.keys():
            bin = ula[instruction]
        else:
            raise Exception("Instrucao mal formatada: {}".format(mnemnonic))

        return r0 + bin

    def jump(self, mnemnonic):
        j = {
            "jg": "001",
            "je": "010",
            "jge": "011",
            "jl": "100",
            "jne": "101",
            "jle": "110",
            "jmp": "111",
        }
        if mnemnonic[0] in j.keys():
            bin = j[mnemnonic[0]]
        else:
            bin = "000"
        return bin

    def toBinary(self, value):
        return f"{int(value):016b}"


def erroMsg(tst, result):
    return "Test fail: {} | code result: {}".format(tst, result)


def test_dest():
    test_vector = [
        [["movw", "%A", "%D"], "010"],
        [["movw", "%A", "(%A)"], "100"],
        [["movw", "%A", "%D", "(%A)"], "110"],
        [["movw", "(%A)", "%D"], "010"],
        [["addw", "(%A)", "%D", "%D"], "010"],
        [["incw", "%A"], "001"],
        [["incw", "%D"], "010"],
        [["incw", "(%A)"], "100"],
        [["nop"], "000"],
        [["subw", "%D", "(%A)", "%A"], "001"],
        [["rsubw", "%D", "(%A)", "%A"], "001"],
        [["decw", "%A"], "001"],
        [["decw", "%D"], "010"],
        [["notw", "%A"], "001"],
        [["notw", "%D"], "010"],
        [["negw", "%A"], "001"],
        [["negw", "%D"], "010"],
        [["andw", "(%A)", "%D", "%D"], "010"],
        [["andw", "%D", "%A", "%A"], "001"],
        [["orw", "(%A)", "%D", "%D"], "010"],
        [["orw", "%D", "%A", "%A"], "001"],
        [["jmp"], "000"],
        [["je"], "000"],
        [["jne"], "000"],
        [["jg"], "000"],
        [["jge"], "000"],
        [["jl"], "000"],
        [["jle"], "000"],
    ]

    code = Code()
    for t in test_vector:
        result = code.dest(t[0])
        assert result == t[1], erroMsg(t, result)


def test_comp():
    test_vector = [
        [["movw", "%A", "%D"], "0110000"],
        [["movw", "%D", "%A"], "0001100"],
        [["movw", "%D", "(%A)"], "0001100"],
        [["movw", "(%A)", "%A"], "1110000"],
        [["movw", "%A", "(%A)"], "0110000"],
        [["movw", "$1", "%D"], "0111111"],
        [["addw", "%A", "%D", "%D"], "0000010"],
        [["addw", "(%A)", "%D", "%D"], "1000010"],
        [["addw", "$1", "(%A)", "%D"], "1110111"],
        [["incw", "%A"], "0110111"],
        [["incw", "%D"], "0011111"],
        [["incw", "(%A)"], "1110111"],
        [["movw", "(%A)", "%D"], "1110000"],
        [["addw", "(%A)", "%D", "%D"], "1000010"],
        [["subw", "%D", "(%A)", "%A"], "1010011"],
        [["rsubw", "%D", "(%A)", "%A"], "1000111"],
        [["decw", "%A"], "0110010"],
        [["decw", "%D"], "0001110"],
        [["notw", "%A"], "0110001"],
        [["notw", "%D"], "0001101"],
        [["negw", "%A"], "0110011"],
        [["negw", "%D"], "0001111"],
        [["andw", "(%A)", "%D", "%D"], "1000000"],
        [["andw", "%D", "%A", "%A"], "0000000"],
        [["orw", "(%A)", "%D", "%D"], "1010101"],
        [["orw", "%D", "%A", "%A"], "0010101"],
        [["subw", "(%A)", "$1", "%A"], "1110010"],
        [["jmp"], "0001100"],
        [["je"], "0001100"],
        [["jne"], "0001100"],
        [["jg"], "0001100"],
        [["jge"], "0001100"],
        [["jl"], "0001100"],
        [["jle"], "0001100"],
    ]

    code = Code()
    for t in test_vector:
        result = code.comp(t[0])
        assert result == t[1], erroMsg(t, result)


def test_jump():
    test_vector = [
        [["movw", "%A", "%D"], "000"],
        [["addw", "%A", "%D", "%D"], "000"],
        [["movw", "%D", "%A"], "000"],
        [["movw", "%D", "(%A)"], "000"],
        [["incw", "%D"], "000"],
        [["nop"], "000"],
        [["movw", "(%A)", "%D"], "000"],
        [["addw", "(%A)", "%D", "%D"], "000"],
        [["subw", "%D", "(%A)", "%A"], "000"],
        [["rsubw", "%D", "(%A)", "%A"], "000"],
        [["decw", "%A"], "000"],
        [["decw", "%D"], "000"],
        [["notw", "%A"], "000"],
        [["notw", "%D"], "000"],
        [["negw", "%A"], "000"],
        [["negw", "%D"], "000"],
        [["andw", "(%A)", "%D", "%D"], "000"],
        [["andw", "%D", "%A", "%A"], "000"],
        [["orw", "(%A)", "%D", "%D"], "000"],
        [["orw", "%D", "%A", "%A"], "000"],
        [["jmp"], "111"],
        [["je"], "010"],
        [["jne"], "101"],
        [["jg"], "001"],
        [["jge"], "011"],
        [["jl"], "100"],
        [["jle"], "110"],
    ]
    code = Code()
    for t in test_vector:
        result = code.jump(t[0])
        assert result == t[1], erroMsg(t, result)


def test_toBinary():
    test_vector = [
        ["0", "0000000000000000"],
        ["1", "0000000000000001"],
        ["10", "0000000000001010"],
        ["100", "0000000001100100"],
        ["1000", "0000001111101000"],
        ["21845", "0101010101010101"],
        ["32767", "0111111111111111"],
        ["32767", "0111111111111111"],
        ["65535", "1111111111111111"],
    ]
    code = Code()
    for t in test_vector:
        result = code.toBinary(t[0])
        assert result == t[1], erroMsg(t, result)


if __name__ == "__main__":
    test_comp()
