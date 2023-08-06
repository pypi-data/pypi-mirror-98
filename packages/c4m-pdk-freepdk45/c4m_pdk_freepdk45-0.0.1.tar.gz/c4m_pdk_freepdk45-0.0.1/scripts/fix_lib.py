from sys import argv
assert len(argv) == 3
import re

cell_pattern = re.compile(r'\s*cell\s*\((?P<cell>\w+)\)\s*\{')
# area_pattern = re.compile(r'(?P<area>\s*area\s*:\s*)\d+.\d+\s*;')
qpin_pattern = re.compile(r'\s*pin\s*\(q\)\s*\{')
ckpin_pattern = re.compile(r'\s*pin\s*\(ck\)\s*\{')

with open(argv[1], "r") as fin:
    with open(argv[2], "w") as fout:
        is_flipflop = False
        for line in fin:
            m = cell_pattern.match(line)
            if m:
                cell = m.group("cell")
                is_flipflop = cell.startswith("sff")
                has_reset = cell.startswith("sff1r")
                if is_flipflop:
                    fout.write(line)
                    fout.write('        ff (IQ,IQN) {\n')
                    fout.write('            next_state : "i" ;\n')
                    fout.write('            clocked_on : "ck" ;\n')
                    if has_reset:
                        fout.write('            clear : "nrst\'" ;\n')
                    fout.write('        }\n')
                    continue
            elif is_flipflop:
                m = qpin_pattern.match(line)
                if m:
                    fout.write(line)
                    fout.write('            function : "IQ" ;\n')
                    continue

                m = ckpin_pattern.match(line)
                if m:
                    fout.write(line)
                    fout.write('            clock : true ;\n')
                    continue

            fout.write(line)

print("Fixed {}".format(argv[1]))