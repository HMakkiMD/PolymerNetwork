import glob, os, time

filename = 'product.itp' #sys.argv[1]
print('Beginning atomistic itp generation .........')
# arrange and order .itp file
from itp_modify import itp_modify
itp_modify(filename)

maps = {} 
block_names = []

# constructing a dic showing blocks and their composed bead names
for fname in glob.glob(os.path.dirname(os.path.abspath(__file__))+"/Mapping/*.map"):
    with open(fname) as g:
        lines = g.readlines()
        for i in range(len(lines)):
            if 'molecule' in lines[i]:
                block_name = lines[i+1].split()[0]
                block_names.append(block_name)
            elif 'martini' in lines[i]:
                maps[f'{block_name}'] = lines[i+1].split()
            elif 'mapping' in lines[i]:
                ff = lines[i+1].split()[0]

atoms,define,bonds,constraints,angles,dihedrals,pairs,excl = {},{},{},{},{},{},{},{}
headers = ['atoms','constraints','bonds','angles','dihedrals','pairs','exclusions']

# separating each section of the blocks
for fname in glob.glob(os.path.dirname(os.path.abspath(__file__))+"/Mapping/*.itp"):
    itp_modify(fname)
    with open(fname[:-4]+'_modified.txt') as g:
        lines = g.readlines()
        block_name = lines[1].split()[0]
        flag = ''
        for i in range(2, len(lines)):
            temp = lines[i].split()
            
            # find out in which section we are
            if '#define' in lines[i]:
                flag = 'define'
            elif 'atoms' in lines[i]:
                flag = 'atoms'
                continue
            elif 'bonds' in lines[i]:
                flag = 'bonds'
                continue
            elif 'constraints' in lines[i]:
                flag = 'constraints'
                continue
            elif 'angles' in lines[i]:
                flag = 'angles'
                continue
            elif 'dihedrals' in lines[i]:
                flag = 'dihedrals'
                continue
            elif 'pairs' in lines[i]:
                flag = 'pairs'
                continue
            elif 'exclusions' in lines[i]:
                flag = 'exclusions'
                continue
            
            # pour each section of the block into a dic based on the block name
            if flag == 'define':
                try:
                    define[f'{block_name}'].append(lines[i])
                except KeyError:
                    define[f'{block_name}'] = [lines[i]]
            elif flag == 'atoms':
                try:
                    atoms[f'{block_name}'].append(temp)
                except KeyError:
                    atoms[f'{block_name}'] = [temp]
            elif flag == 'bonds':
                try:
                    bonds[f'{block_name}'].append(temp)
                except KeyError:
                    bonds[f'{block_name}'] = [temp]
            elif flag == 'constraints':
                try:
                    constraints[f'{block_name}'].append(temp)
                except KeyError:
                    constraints[f'{block_name}'] = [temp]
            elif flag == 'angles':
                try:
                    angles[f'{block_name}'].append(temp)
                except KeyError:
                    angles[f'{block_name}'] = [temp]
            elif flag == 'dihedrals':
                try:
                    dihedrals[f'{block_name}'].append(temp)
                except KeyError:
                    dihedrals[f'{block_name}'] = [temp]
            elif flag == 'pairs':
                try:
                    pairs[f'{block_name}'].append(temp)
                except KeyError:
                    pairs[f'{block_name}'] = [temp]
            elif flag == 'exclusions':
                try:
                    excl[f'{block_name}'].append(temp)
                except KeyError:
                    excl[f'{block_name}'] = [temp]
            
# read the CG itp file            
with open(filename[:-4]+'_modified.txt') as f:
    lines = f.readlines()

# construct the initial atomistic itp file
with open(filename[:-4]+'_atomistic.itp', 'w') as g:
    g.write('[ moleculetype ]\n')
    moleculetype = lines[1].split()[0]
    g.write(f'{moleculetype}   3\n')

# read the CG gro file
with open(filename[:-4]+'.gro') as f:
    gro = f.readlines()

    x = 3
    resnr,cgnr,nr = 0,0,0
    seq,seq2,at_atoms,at_bonds,at_const,at_ang,at_dih,at_pairs,at_excl = [],[],[],[],[],[],[],[],[]
    seq2line = ''
    delgro = []
    
    # read lines of [atoms] section
    while '[' not in lines[x]:
        temp = lines[x].split()
        seq.append(temp[4])           # keep the sequence of bead names
        seq2line += f'{temp[0]}  '    # keep the sequence of bead numbers
        for i in maps:
            # check if the sequence of bead names match with one of blocks
            if maps[i] == seq:
                
                resnr += 1
                cgnr  += 1
                
                # pour the constraints of the matched block to total constraints
                try:
                    constraints[i]
                except KeyError:
                    pass
                else:
                    for k in range(len(constraints[i])):
                        line = ''
                        for h in range(len(constraints[i][k])):
                            if h in [0,1]:
                                line += '%7d  ' %(int(constraints[i][k][h])+nr)   # modify the atom no.
                            else:
                                line += '%7s  ' %(constraints[i][k][h])
                        at_const.append(line+'\n')
                # pour the bonds of the matched block to total bonds        
                try:
                    bonds[i]
                except KeyError:
                    pass
                else:
                    for k in range(len(bonds[i])):
                        line = ''
                        for h in range(len(bonds[i][k])):
                            if h in [0,1]:
                                line += '%7d  ' %(int(bonds[i][k][h])+nr)
                            else:
                                line += '%7s  ' %(bonds[i][k][h])
                        at_bonds.append(line+'\n')
                # pour the pairs of the matched block to total pairs
                try:
                    pairs[i]
                except KeyError:
                    pass
                else:
                    for k in range(len(pairs[i])):
                        line = ''
                        for h in range(len(pairs[i][k])):
                            if h in [0,1]:
                                line += '%7d  ' %(int(pairs[i][k][h])+nr)
                            else:
                                line += '%7s  ' %(pairs[i][k][h])
                        at_pairs.append(line+'\n')
                # pour the angles of the matched block to total angles
                try:
                    angles[i]
                except KeyError:
                    pass
                else:
                    for k in range(len(angles[i])):
                        line = ''
                        for h in range(len(angles[i][k])):
                            if h in [0,1,2]:
                                line += '%7d  ' %(int(angles[i][k][h])+nr)
                            else:
                                line += '%7s  ' %(angles[i][k][h])
                        at_ang.append(line+'\n')
                angle_index = len(at_ang)
                # pour the dihedrals of the matched block to total dihedrals        
                try:
                    dihedrals[i]
                except KeyError:
                    pass
                else:
                    for k in range(len(dihedrals[i])):
                        line = ''
                        for h in range(len(dihedrals[i][k])):
                            if h in [0,1,2,3]:
                                line += '%7d  ' %(int(dihedrals[i][k][h])+nr)
                            else:
                                line += '%7s  ' %(dihedrals[i][k][h])
                        at_dih.append(line+'\n')
                dihedral_index = len(at_dih)
                # pour the exclusions of the matched block to total pairs
                try:
                    excl[i]
                except KeyError:
                    pass
                else:
                    for k in range(len(excl[i])):
                        line = ''
                        for h in range(len(excl[i][k])):
                            if h in [0,1]:
                                line += '%7d  ' %(int(excl[i][k][h])+nr)
                            else:
                                line += '%7s  ' %(excl[i][k][h])
                        at_excl.append(line+'\n')
                        
                # pour the atoms of the matched block to total atoms
                try:
                    atoms[i]       # to not raise error when the atoms of block is empty
                except KeyError:
                    pass
                else:
                    for j in range(len(atoms[i])):
                        nr += 1       # atom number
                        if j > 0:     # check that the beads is still the same or changed
                            if atoms[i][j][3] != atoms[i][j-1][3]:
                                cgnr += 1    # add cgnr if the bead is changed
                        at_atoms.append('%8s\t  %-10s %6s   %-5s  %-6s  %7s   %-8s  %-7s\n'\
                                %(str(nr),atoms[i][j][1],str(resnr),i,atoms[i][j][4],\
                                  str(cgnr),atoms[i][j][6],atoms[i][j][7]))
                
                # modify the gro file
                
                for j in range(len(seq2line.split())):
                    if lines[int(seq2line.split()[j])+2].split()[4] == 'DEL':  # keep the number of line that should be deleted in gro file
                        delgro.append(int(seq2line.split()[j])+1)
                    gro[int(seq2line.split()[j])+1] = '%5s' %(str(resnr))+'%-5s' %(i)+gro[int(seq2line.split()[j])+1][10:]
                
                seq = []                # reset the sequence of bead names
                seq2.append(seq2line.split())
                seq2line = ''           # reset the sequence of bead numbers
                        
        x += 1
    
    # delete lines that contain 'DEL' beads
    delgro.sort(reverse=True)
    gro[1] = '%5d\n' %(int(gro[1].split()[0])-len(delgro))
    for j in delgro:
        gro.pop(j)

    bondlist = []
    bonds_beg,const_beg = 0,0
    # find the position of bonds section in CG itp file
    for i in range(x,len(lines)):
        if bonds_beg != 0 and '[' in lines[i]:
            bonds_end = i
            break
        if 'bonds' in lines[i]:
            bonds_beg = i+1
    # find the position of constraints section in CG itp file
    for i in range(x,len(lines)):
        if const_beg != 0 and '[' in lines[i]:
            const_end = i
            break
        if 'constraints' in lines[i]:
            const_beg = i+1
    # write all bonds and constraints to bondlist var
    if  bonds_beg != 0:
        for i in range(bonds_beg,bonds_end):
            bondlist.append([lines[i].split()[0],lines[i].split()[1]])
    if  const_beg != 0:
        for i in range(const_beg,const_end):
            bondlist.append([lines[i].split()[0],lines[i].split()[1]])
print('|................... 1%')
print('Finding the bonds between the blocks ......')

# find the bonds between different blocks    
new_cgbonds = []    
i = 0
while i < len(bondlist):
    been = False
    j = 0
    while j < len(seq2) and been == False:
        if (bondlist[i][0] in seq2[j]) and (bondlist[i][1] in seq2[j]):
            been = True
        j += 1
    if been == False:
        new_cgbonds.append(bondlist[i])
    i += 1



tempbonds = []   # list containing substituted cgbonds due to deleting 'DEL' beads
for i in range(len(new_cgbonds)-1,-1,-1):
    flag = True
    if lines[int(new_cgbonds[i][0])+2].split()[4] == 'DEL':
        for j in range(len(bondlist)):
            tt = ''
            if new_cgbonds[i][0] == bondlist[j][0]:
                tt = bondlist[j][1]
            elif new_cgbonds[i][0] == bondlist[j][1]:
                tt = bondlist[j][0]
            if tt != '' and new_cgbonds[i][1] != tt and {new_cgbonds[i][1], tt} not in tempbonds:
                tempbonds.append([new_cgbonds[i][1], tt])
                flag = False
        if flag == False:
            new_cgbonds.pop(i)
    elif lines[int(new_cgbonds[i][1])+2].split()[4] == 'DEL':
        for j in range(len(bondlist)):
            tt = ''
            if new_cgbonds[i][1] == bondlist[j][0]:
                tt = bondlist[j][1]
            elif new_cgbonds[i][1] == bondlist[j][1]:
                tt = bondlist[j][0]
            if tt != '' and new_cgbonds[i][0] != tt and {new_cgbonds[i][0], tt} not in tempbonds:
                tempbonds.append({new_cgbonds[i][0], tt})
                flag = False
        if flag == False:
            new_cgbonds.pop(i)
for i in range(len(tempbonds)):
    tempbonds[i] = list(tempbonds[i])
new_cgbonds += tempbonds
print('|................... 2%')
print('Adding new bonds, constraints and exclusions to itp file .....')

inp_def = []
new_atbonds = []
# read the input bonds
try:
    with open('Mapping/input_bonds.txt') as f:
        inp_lines = f.readlines()
except FileNotFoundError:
    pass
else:
    inp_bonds = []
    with open('Mapping/input_bonds.txt') as f:
        inp_lines = f.readlines()
        for i in range(len(inp_lines)):
            new_line = ''
            if '#define' in inp_lines[i]:
                inp_def.append(inp_lines[i])
            elif inp_lines[i].split()[0][0] == '[':
                for j in inp_lines[i]:
                    if j not in ['[',']','\n']:
                        new_line += j
                inp_bonds.append([new_line.split()[0],new_line.split()[1]])
                for j in range(i+1,len(inp_lines)):
                    if '[' not in inp_lines[j]:
                        inp_bonds[-1].append(inp_lines[j].split())
                    else:
                        break
    # find new bonds and add them to at_bonds
    for i in new_cgbonds:
        for j in range(len(inp_bonds)):
            first,second,line = '','',''
            # check if the bead names match the inputs
            if lines[int(i[0])+2].split()[4] == inp_bonds[j][0] and lines[int(i[1])+2].split()[4] == inp_bonds[j][1]:
                # check if the bead number and atom name match the inputs
                for m in range(2,len(inp_bonds[j])):
                    for k in range(len(at_atoms)):
                        if at_atoms[k].split()[5] == i[0] and at_atoms[k].split()[4] == inp_bonds[j][m][0]:
                            first = int(at_atoms[k].split()[0])
                        if at_atoms[k].split()[5] == i[1] and at_atoms[k].split()[4] == inp_bonds[j][m][1]:
                            second = int(at_atoms[k].split()[0])
                    if first != '' and second != '':
                        line += '%7d  %7d  ' %(first,second)
                        try:
                            inp_bonds[j][m][2]
                        except IndexError:
                            pass
                        else:
                            for h in range(2,len(inp_bonds[j][m])):
                                line += '%7s  ' %(inp_bonds[j][m][h])
                            at_bonds.append(line+'\n')
                            new_atbonds.append([first,second])
            elif lines[int(i[0])+2].split()[4] == inp_bonds[j][1] and lines[int(i[1])+2].split()[4] == inp_bonds[j][0]:
                # check if the bead number and atom name match the inputs
                for m in range(2,len(inp_bonds[j])):
                    for k in range(len(at_atoms)):
                        if at_atoms[k].split()[5] == i[1] and at_atoms[k].split()[4] == inp_bonds[j][m][0]:
                            first = int(at_atoms[k].split()[0])
                        if at_atoms[k].split()[5] == i[0] and at_atoms[k].split()[4] == inp_bonds[j][m][1]:
                            second = int(at_atoms[k].split()[0])
                    if first != '' and second != '':
                        line += '%7d  %7d  ' %(first,second)
                        try:
                            inp_bonds[j][m][2]
                        except IndexError:
                            pass
                        else:
                            for h in range(2,len(inp_bonds[j][m])):
                                line += '%7s  ' %(inp_bonds[j][m][h])
                            at_bonds.append(line+'\n')
                            new_atbonds.append([first,second])

# read the input constraints
try:
    with open('Mapping/input_constraints.txt') as f:
        inp_lines = f.readlines()
except FileNotFoundError:
    pass
else:
    inp_constraints = []
    with open('Mapping/input_constraints.txt') as f:
        inp_lines = f.readlines()
        for i in range(len(inp_lines)):
            new_line = ''
            if '#define' in inp_lines[i]:
                inp_def.append(inp_lines[i])
            elif inp_lines[i].split()[0][0] == '[':
                for j in inp_lines[i]:
                    if j not in ['[',']','\n']:
                        new_line += j
                inp_constraints.append([new_line.split()[0],new_line.split()[1]])
                for j in range(i+1,len(inp_lines)):
                    if '[' not in inp_lines[j]:
                        inp_constraints[-1].append(inp_lines[j].split())
                    else:
                        break
    # find new constraints and add them to at_const
    for i in new_cgbonds:
        for j in range(len(inp_constraints)):
            first,second,line = '','',''
            # check if the bead names match the inputs
            if lines[int(i[0])+2].split()[4] == inp_constraints[j][0] and lines[int(i[1])+2].split()[4] == inp_constraints[j][1]:
                # check if the bead number and atom name match the inputs
                for m in range(2,len(inp_constraints[j])):
                    for k in range(len(at_atoms)):
                        if at_atoms[k].split()[5] == i[0] and at_atoms[k].split()[4] == inp_constraints[j][m][0]:
                            first = int(at_atoms[k].split()[0])
                        if at_atoms[k].split()[5] == i[1] and at_atoms[k].split()[4] == inp_constraints[j][m][1]:
                            second = int(at_atoms[k].split()[0])
                    if first != '' and second != '':
                        line += '%7d  %7d  ' %(first,second)
                        for h in range(2,len(inp_constraints[j][m])):
                            line += '%7s  ' %(inp_constraints[j][m][h])
                        at_const.append(line+'\n')
                        new_atbonds.append([first,second])
            elif lines[int(i[0])+2].split()[4] == inp_constraints[j][1] and lines[int(i[1])+2].split()[4] == inp_constraints[j][0]:
                # check if the bead number and atom name match the inputs
                for m in range(2,len(inp_constraints[j])):
                    for k in range(len(at_atoms)):
                        if at_atoms[k].split()[5] == i[1] and at_atoms[k].split()[4] == inp_constraints[j][m][0]:
                            first = int(at_atoms[k].split()[0])
                        if at_atoms[k].split()[5] == i[0] and at_atoms[k].split()[4] == inp_constraints[j][m][1]:
                            second = int(at_atoms[k].split()[0])
                    if first != '' and second != '':
                        line += '%7d  %7d  ' %(first,second)
                        for h in range(2,len(inp_constraints[j][m])):
                            line += '%7s  ' %(inp_constraints[j][m][h])
                        at_const.append(line+'\n')
                        new_atbonds.append([first,second])

# read the input exclusions
try:
    with open('Mapping/input_exclusions.txt') as f:
        inp_lines = f.readlines()
except FileNotFoundError:
    pass
else:
    inp_exclusions = []
    with open('Mapping/input_exclusions.txt') as f:
        inp_lines = f.readlines()
        for i in range(len(inp_lines)):
            new_line = ''
            if inp_lines[i].split()[0][0] == '[':
                for j in inp_lines[i]:
                    if j not in ['[',']','\n']:
                        new_line += j
                inp_exclusions.append([new_line.split()[0],new_line.split()[1]])
                for j in range(i+1,len(inp_lines)):
                    if '[' not in inp_lines[j]:
                        inp_exclusions[-1].append(inp_lines[j].split())
                    else:
                        break
    # find new exclusions and add them to at_excl
    for i in new_cgbonds:
        for j in range(len(inp_exclusions)):
            first,second,line = '','',''
            # check if the bead names match the inputs
            if lines[int(i[0])+2].split()[4] == inp_exclusions[j][0] and lines[int(i[1])+2].split()[4] == inp_exclusions[j][1]:
                # check if the bead number and atom name match the inputs
                for m in range(2,len(inp_exclusions[j])):
                    for k in range(len(at_atoms)):
                        if at_atoms[k].split()[5] == i[0] and at_atoms[k].split()[4] == inp_exclusions[j][m][0]:
                            first = int(at_atoms[k].split()[0])
                        if at_atoms[k].split()[5] == i[1] and at_atoms[k].split()[4] == inp_exclusions[j][m][1]:
                            second = int(at_atoms[k].split()[0])
                    if first != '' and second != '':
                        line += '%7d  %7d  ' %(first,second)
                        at_excl.append(line+'\n')
            elif lines[int(i[0])+2].split()[4] == inp_exclusions[j][1] and lines[int(i[1])+2].split()[4] == inp_exclusions[j][0]:
                # check if the bead number and atom name match the inputs
                for m in range(2,len(inp_exclusions[j])):
                    for k in range(len(at_atoms)):
                        if at_atoms[k].split()[5] == i[1] and at_atoms[k].split()[4] == inp_exclusions[j][m][0]:
                            first = int(at_atoms[k].split()[0])
                        if at_atoms[k].split()[5] == i[0] and at_atoms[k].split()[4] == inp_exclusions[j][m][1]:
                            second = int(at_atoms[k].split()[0])
                    if first != '' and second != '':
                        line += '%7d  %7d  ' %(first,second)
                        at_excl.append(line+'\n')
print('||||................ 20%')
print('Processing new angles')
                   
# find second order and third order atoms (needed for finding angles and dihedrals)
all_bonds = at_bonds + at_const
sec_atoms = set()          # atoms that are connected to bridge atom
sec_atoms_details = {}
for i in new_atbonds:
    for j in [0,1]:
        sec_atoms_details[f'{i[j]}'] = []
        for k in range(len(all_bonds)):#-len(new_atbonds)):   # dont consider the bridges
            if int(all_bonds[k].split()[0]) == i[j]:
                sec_atoms.add(all_bonds[k].split()[1])
                sec_atoms_details[f'{i[j]}'].append(all_bonds[k].split()[1])
            elif int(all_bonds[k].split()[1]) == i[j]:
                sec_atoms.add(all_bonds[k].split()[0])
                sec_atoms_details[f'{i[j]}'].append(all_bonds[k].split()[0])
sec_atoms = list(sec_atoms)
fir_atoms = list(sec_atoms_details.keys())    # bridge atoms
print('||||||.............. 30%')
print('Processing new dihedrals')

ter_atoms = set()         # atoms that are connected to sec_atoms
ter_atoms_details = {}
for i in sec_atoms:
    ter_atoms_details[f'{i}'] = []
    for k in range(len(all_bonds)):#-len(new_atbonds)):
        if all_bonds[k].split()[0] == i:# and all_bonds[k].split()[1] not in fir_atoms:
            ter_atoms.add(all_bonds[k].split()[1])
            ter_atoms_details[f'{i}'].append(all_bonds[k].split()[1])
        elif all_bonds[k].split()[1] == i:# and all_bonds[k].split()[0] not in fir_atoms:
            ter_atoms.add(all_bonds[k].split()[0])
            ter_atoms_details[f'{i}'].append(all_bonds[k].split()[0])
ter_atoms = list(ter_atoms)
# delete empty lines
for i in sec_atoms:
    if ter_atoms_details[i] == []:
        ter_atoms_details.pop(i)
print('||||||||............ 40%')
print('Adding new angles.....')

# read the input angles
try:
    with open('Mapping/input_angles.txt') as f:
        inp_lines = f.readlines()
except FileNotFoundError:
    pass
else:
    inp_angles = []
    with open('Mapping/input_angles.txt') as f:
        inp_lines = f.readlines()
        for i in range(len(inp_lines)):
            new_line = []
            if '#define' in inp_lines[i]:
                inp_def.append(inp_lines[i])
            else:
                for j in range(len(inp_lines[i].split())):
                    new_line.append(inp_lines[i].split()[j])
                inp_angles.append(new_line)

# add new angles
first,second,third = '','',''
for i in new_atbonds:
    first  = str(i[0])
    second = str(i[1])
    for j in sec_atoms_details[f'{second}']:
        third = j
        param = ''
        for k in inp_angles:
            if (at_atoms[int(first) -1].split()[1] == k[0] and \
                at_atoms[int(second)-1].split()[1] == k[1] and \
                at_atoms[int(third) -1].split()[1] == k[2]) or \
               (at_atoms[int(first) -1].split()[1] == k[2] and \
                at_atoms[int(second)-1].split()[1] == k[1] and \
                at_atoms[int(third) -1].split()[1] == k[0]):
                for h in range(3,len(k)):
                    param += ('  '+k[h])
                break

        if len(set([first,second,third])) == 3:
            flag = True
            for h in range(angle_index,len(at_ang)):
                if (at_ang[h].split()[0] == first  and \
                    at_ang[h].split()[1] == second and \
                    at_ang[h].split()[2] == third) or \
                   (at_ang[h].split()[2] == first  and \
                    at_ang[h].split()[1] == second and \
                    at_ang[h].split()[0] == third):
                    flag = False
            if flag == True:
                if param.split() == []:
                    try:
                        with open('undefined_angles.txt') as f:
                            f.readline()
                    except FileNotFoundError:
                        with open('undefined_angles.txt', 'w') as f:
                            f.write('%7s  %7s  %7s \n' %(first,second,third))
                    else:
                        with open('undefined_angles.txt', 'a') as f:
                            f.write('%7s  %7s  %7s \n' %(first,second,third))
                else:
                    at_ang.append('%7s  %7s  %7s %s \n' %(first,second,third,param[1:]))


                    
for i in new_atbonds:
    first  = str(i[1])
    second = str(i[0])
    for j in sec_atoms_details[f'{second}']:
        third = j
        param = ''
        for k in inp_angles:
            if (at_atoms[int(first) -1].split()[1] == k[0] and \
                at_atoms[int(second)-1].split()[1] == k[1] and \
                at_atoms[int(third) -1].split()[1] == k[2]) or \
               (at_atoms[int(first) -1].split()[1] == k[2] and \
                at_atoms[int(second)-1].split()[1] == k[1] and \
                at_atoms[int(third) -1].split()[1] == k[0]):
                for h in range(3,len(k)):
                    param += ('  '+k[h])
                break

        if len(set([first,second,third])) == 3:
            flag = True
            for h in range(angle_index,len(at_ang)):
                if (at_ang[h].split()[0] == first  and \
                    at_ang[h].split()[1] == second and \
                    at_ang[h].split()[2] == third) or \
                   (at_ang[h].split()[2] == first  and \
                    at_ang[h].split()[1] == second and \
                    at_ang[h].split()[0] == third):
                    flag = False
            if flag == True:
                if param.split() == []:
                    try:
                        with open('undefined_angles.txt') as f:
                            f.readline()
                    except FileNotFoundError:
                        with open('undefined_angles.txt', 'w') as f:
                            f.write('%7s  %7s  %7s \n' %(first,second,third))
                    else:
                        with open('undefined_angles.txt', 'a') as f:
                            f.write('%7s  %7s  %7s \n' %(first,second,third))
                else:
                    at_ang.append('%7s  %7s  %7s %s \n' %(first,second,third,param[1:]))
print('||||||||||.......... 50%')
print('Adding new dihedrals.....')

# read the input dihedrals
try:
    with open('Mapping/input_dihedrals.txt') as f:
        inp_lines = f.readlines()
except FileNotFoundError:
    pass
else:
    inp_dihedrals = []
    with open('Mapping/input_dihedrals.txt') as f:
        inp_lines = f.readlines()
        for i in range(len(inp_lines)):
            new_line = []
            if '#define' in inp_lines[i]:
                inp_def.append(inp_lines[i])
            else:
                for j in range(len(inp_lines[i].split())):
                    new_line.append(inp_lines[i].split()[j])
                inp_dihedrals.append(new_line)

# add new dihedrals
first,second,third,fourth = '','','',''
for i in new_atbonds:   # finding new dihedrals which have the brigde in one side
    first  = str(i[0])
    second = str(i[1])
    for j in sec_atoms_details[f'{second}']:
        third = j
        try:
            ter_atoms_details[third]
        except KeyError:
            pass
        else:
            for k in ter_atoms_details[third]:
                fourth = k
                param = ''
                for h in inp_dihedrals:
                    if (at_atoms[int(first) -1].split()[1] == h[0] and \
                        at_atoms[int(second)-1].split()[1] == h[1] and \
                        at_atoms[int(third) -1].split()[1] == h[2] and \
                        at_atoms[int(fourth)-1].split()[1] == h[3]) or \
                       (at_atoms[int(first) -1].split()[1] == h[3] and \
                        at_atoms[int(second)-1].split()[1] == h[2] and \
                        at_atoms[int(third) -1].split()[1] == h[1] and \
                        at_atoms[int(fourth)-1].split()[1] == h[0]):
                        for m in range(4,len(h)):
                            param += ('  '+h[m])
                        break

                if len(set([first,second,third,fourth])) == 4:
                    flag = True
                    for h in range(dihedral_index,len(at_dih)):
                        if (at_dih[h].split()[0] == first  and \
                            at_dih[h].split()[1] == second and \
                            at_dih[h].split()[2] == third  and \
                            at_dih[h].split()[3] == fourth) or \
                           (at_dih[h].split()[3] == first  and \
                            at_dih[h].split()[2] == second and \
                            at_dih[h].split()[1] == third  and \
                            at_dih[h].split()[0] == fourth):
                            flag = False
                    if flag == True:
                        if param.split() == []:
                            try:
                                with open('undefined_dihedrals.txt') as f:
                                    f.readline()
                            except FileNotFoundError:
                                with open('undefined_dihedrals.txt', 'w') as f:
                                    f.write('%7s  %7s  %7s  %7s \n' %(first,second,third,fourth))
                            else:
                                with open('undefined_dihedrals.txt', 'a') as f:
                                    f.write('%7s  %7s  %7s  %7s \n' %(first,second,third,fourth))
                        else:
                            at_dih.append('%7s  %7s  %7s  %7s %s \n' %(first,second,third,fourth,param[1:]))
                            if 'charmm' not in ff:
                                at_pairs.append('%7s  %7s  %7s \n' %(first,fourth,'1')) 

print('||||||||||||||...... 70%')                                

for i in new_atbonds:   # finding new dihedrals which have the brigde in the other side
    first  = str(i[1])
    second = str(i[0])
    for j in sec_atoms_details[f'{second}']:
        third = j
        try:
            ter_atoms_details[third]
        except KeyError:
            pass
        else:
            for k in ter_atoms_details[third]:
                fourth = k
                param = ''
                for h in inp_dihedrals:
                    if (at_atoms[int(first) -1].split()[1] == h[0] and \
                        at_atoms[int(second)-1].split()[1] == h[1] and \
                        at_atoms[int(third) -1].split()[1] == h[2] and \
                        at_atoms[int(fourth)-1].split()[1] == h[3]) or \
                       (at_atoms[int(first) -1].split()[1] == h[3] and \
                        at_atoms[int(second)-1].split()[1] == h[2] and \
                        at_atoms[int(third) -1].split()[1] == h[1] and \
                        at_atoms[int(fourth)-1].split()[1] == h[0]):
                        for m in range(4,len(h)):
                            param += ('  '+h[m])
                        break

                if len(set([first,second,third,fourth])) == 4:
                    flag = True
                    for h in range(dihedral_index,len(at_dih)):
                        if (at_dih[h].split()[0] == first  and \
                            at_dih[h].split()[1] == second and \
                            at_dih[h].split()[2] == third  and \
                            at_dih[h].split()[3] == fourth) or \
                           (at_dih[h].split()[3] == first  and \
                            at_dih[h].split()[2] == second and \
                            at_dih[h].split()[1] == third  and \
                            at_dih[h].split()[0] == fourth):
                            flag = False
                    if flag == True:
                        if param.split() == []:
                            try:
                                with open('undefined_dihedrals.txt') as f:
                                    f.readline()
                            except FileNotFoundError:
                                with open('undefined_dihedrals.txt', 'w') as f:
                                    f.write('%7s  %7s  %7s  %7s \n' %(first,second,third,fourth))
                            else:
                                with open('undefined_dihedrals.txt', 'a') as f:
                                    f.write('%7s  %7s  %7s  %7s \n' %(first,second,third,fourth))
                        else:
                            at_dih.append('%7s  %7s  %7s  %7s %s \n' %(first,second,third,fourth,param[1:]))
                            if 'charmm' not in ff:
                                at_pairs.append('%7s  %7s  %7s \n' %(first,fourth,'1'))                

print('||||||||||||||||||.. 90%')

for i in new_atbonds:   # finding new dihedrals which have the brigde in the middle
    second = str(i[0])
    third  = str(i[1])
    for j in sec_atoms_details[f'{second}']:
        first = j
        for k in sec_atoms_details[f'{third}']:
            fourth = k
            param = ''
            for h in inp_dihedrals:
                if (at_atoms[int(first) -1].split()[1] == h[0] and \
                    at_atoms[int(second)-1].split()[1] == h[1] and \
                    at_atoms[int(third) -1].split()[1] == h[2] and \
                    at_atoms[int(fourth)-1].split()[1] == h[3]) or \
                   (at_atoms[int(first) -1].split()[1] == h[3] and \
                    at_atoms[int(second)-1].split()[1] == h[2] and \
                    at_atoms[int(third) -1].split()[1] == h[1] and \
                    at_atoms[int(fourth)-1].split()[1] == h[0]):
                    for m in range(4,len(h)):
                        param += ('  '+h[m])
                    break
                        
            if len(set([first,second,third,fourth])) == 4:
                flag = True
                for h in range(dihedral_index,len(at_dih)):
                    if (at_dih[h].split()[0] == first  and \
                        at_dih[h].split()[1] == second and \
                        at_dih[h].split()[2] == third  and \
                        at_dih[h].split()[3] == fourth) or \
                       (at_dih[h].split()[3] == first  and \
                        at_dih[h].split()[2] == second and \
                        at_dih[h].split()[1] == third  and \
                        at_dih[h].split()[0] == fourth):
                        flag = False
                if flag == True:
                    if param.split() == []:
                        try:
                            with open('undefined_dihedrals.txt') as f:
                                f.readline()
                        except FileNotFoundError:
                            with open('undefined_dihedrals.txt', 'w') as f:
                                f.write('%7s  %7s  %7s  %7s \n' %(first,second,third,fourth))
                        else:
                            with open('undefined_dihedrals.txt', 'a') as f:
                                f.write('%7s  %7s  %7s  %7s \n' %(first,second,third,fourth))
                    else:
                        at_dih.append('%7s  %7s  %7s  %7s %s \n' %(first,second,third,fourth,param[1:]))
                        if 'charmm' not in ff:
                            at_pairs.append('%7s  %7s  %7s \n' %(first,fourth,'1'))
    
print('|||||||||||||||||||| 99%')

names   = [at_atoms,at_const,at_bonds,at_ang,at_dih,at_pairs,at_excl]

with open(filename[:-4]+'_atomistic.itp', 'a') as g:
    
    # write the defines section to atomistic itp file (if exist)
    defi = set()
    if len(inp_def) != 0:
        define['inp'] = inp_def
    for y in define:
        for z in range(len(define[f'{y}'])):
            define[f'{y}'][z] = define[f'{y}'][z].split()
            line = ''
            for q in range(len(define[f'{y}'][z])):
                line += '%s    ' %(define[f'{y}'][z][q])
            line += '\n'
            defi.add(line)
    defi = list(defi)
    defi.sort()
    for y in defi:
        g.write(y)
    
    # write each section to atomistic itp file (if exist)
    for y in range(len(headers)):
        if len(names[y]) != 0:
            g.write(f'[ {headers[y]} ]\n')
            for z in names[y]:
                g.write(z)

# write the modified gro file
with open(filename[:-4]+'_modified.gro', 'w') as g:
    for y in gro:
        g.write(y)

os.system(f'rm {filename[:-4]}_modified.txt')
for fname in glob.glob(os.path.dirname(os.path.abspath(__file__))+"/Mapping/*.txt"):
    if 'input_' not in fname:
        os.system(f'rm {fname}')
print('|||||||||||||||||||| 100%')
print('Finished!')
            
