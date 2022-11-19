# imports 
import os
import string

# reshapes game to matrix format
def reshape_game(game, size):
    game_matrix = [game[i:i+size] for i in range(0, len(game), size)]
    return game_matrix

# creates unit clauses (where the numbers already are) 
def unit_clauses(game_matrix):
    first_clauses = []
    for row_index, row in enumerate(game_matrix):
        for column_index, value in enumerate(row): 
            if not value == '.':
                literal = str(row_index+1) + str(column_index+1) + str(value)
                first_clauses.append([literal])
    return first_clauses

# does the same as unit_clauses() but for games encoded in base-17
def unit_clauses_base_17(game_matrix):
    chars = string.digits[1:] + string.ascii_uppercase[:7]
    chars_list = list(chars)
    first_clauses = []
    for row_index, row in enumerate(game_matrix):
        for column_index, value in enumerate(row): 
            if not value == '.':
                literal_base_17 = chars_list[row_index] + chars_list[column_index] + str(value) 
                literal_base_10 = str(int(literal_base_17, base=17))
                first_clauses.append([literal_base_10])
    return first_clauses

# parses rules file into list of clauses 
def parse_rules(rules_file):
    f_rules = open(rules_file)
    temp1 = f_rules.read().split('\n')
    temp2 = [clause.replace(' 0', '') for clause in temp1]
    rules_list = [clause.split(' ') for clause in temp2]
    del rules_list[0]
    del rules_list[-1]
    return rules_list

# writes list of clauses into a DIMACS style string 
def write_dimacs(cnf, size):
    line1 = f'p cnf {size**3} {len(cnf)} \n'
    for clause in cnf: 
        line = ' '.join(clause) + ' 0' + '\n'
        line1 += line
    return line1

# change depending on game type 
game_file = r'testsets/16x16.txt'
rules_file = r'rules/sudoku-rules-16x16.txt'
game_size = 16 # 4, 9, 16
save_directory = f'DIMACS_{game_size}x{game_size}'

# mod to use other unit clause function
def main(games, rules, size, directory):
    # prepares game file for reading 
    f = open(games)
    test_set = f.read().split('\n')
    # creates directory for saving DIMACS files
    if not os.path.exists(directory):
        os.makedirs(directory)
    # iterates through each game and applies steps for DIMACS conversion
    for i, game in enumerate(test_set):
        # reshapes game to matrix form
        game_mat = reshape_game(game, size)
        # creates first unit clauses 
        # for normally encoded games 
        if size == 16: 
            first_clauses = unit_clauses_base_17(game_mat)
        # for base-17 encoded games 
        else: first_clauses = unit_clauses(game_mat)   
        # parses rule file into clauses
        rules_clauses = parse_rules(rules)
        # combines unit & rules clauses to form final CNF
        final_cnf = first_clauses + rules_clauses
        # writes CNF into a DIMCAS string
        dimacs_cnf = write_dimacs(final_cnf, size)
        # saves string to dimacs.cnf file 
        f_name = f'sudoku_{size}x{size}_nr_{i+1}.cnf'
        filepath = os.path.join(directory, f_name)
        f = open(filepath, 'w')
        f.write(dimacs_cnf)
        f.close()

if __name__ == '__main__': 
    main(game_file, rules_file, game_size, save_directory)










