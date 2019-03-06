## author: Cody Rountree

def tokenize(a_string):
    nums = "0123456789"
    letters = "abcdefghijklmnopqrstuvwxyz"
    operators = "+-*/"
    assignment = "="

    start_transitions = ["identifier", "number", "operator", "assignment", "start", "error"]
    identifier_transitions = ["identifier", "identifier", "operator", "assignment", "start", "error"]
    number_transitions = ["error", "number", "operator", "assignment", "start", "error"]
    operator_transitions = ["identifier", "number", "error", "assignment", "start", "error"]
    assignment_transitions = ["identifier", "number", "operator", "error", "start", "error"]
    error_transitions = ["error", "error", "error", "error", "error", "error"]

    current_state = ""
    current_transitions = start_transitions
    token = []

    for i in range(len(a_string)):
        current_character = a_string[i]
        if (current_character in letters):
            if (current_state != current_transitions[0]):
                current_state = current_transitions[0]
                current_transitions = identifier_transitions
                if (current_state != "start"):
                    token.append(current_state)
        elif (current_character in nums):
            if (current_state != current_transitions[1]):
                current_state = current_transitions[1]
                current_transitions = number_transitions
                if (current_state != "start"):
                    token.append(current_state)
        elif (current_character in operators):
            if (current_state != current_transitions[2]):
                current_state = current_transitions[2]
                current_transitions = operator_transitions
                if (current_state != "start"):
                    token.append(current_state)
        elif (current_character in assignment):
            if (current_state != current_transitions[3]):
                current_state = current_transitions[3]
                current_transitions = assignment_transitions
                if (current_state != "start"):
                    token.append(current_state)
        elif (current_character == " "):
            if (current_state != current_transitions[4]):
                current_state = current_transitions[4]
                current_transitions = start_transitions
                if (current_state != "start"):
                    token.append(current_state)
        else:
            if (current_state != current_transitions[5]):
                current_state = current_transitions[5]
                current_transitions = error_transitions
                if (current_state != "start"):
                    token.append(current_state)

    return token


def recognize(a_list):

    max_index = len(a_list) - 1

    if (max_index == 0):
        if (a_list[max_index] == "number" or a_list[max_index] == "identifier"):
            return True

    elif (max_index > 1):
        if (a_list[max_index] == "number" or a_list[max_index] == "identifier"):
            del(a_list[max_index])
            a_list.append("expression")
            while (a_list[max_index - 1] != "assignment"):
                if (a_list[max_index - 1] == "operator"):
                    if (a_list[max_index - 2] == "number" or a_list[max_index - 2] == "identifier"):
                        del(a_list[max_index - 1])
                        del(a_list[max_index - 2])
                        max_index = max_index - 2
                        if (max_index == 0 and a_list[max_index] == "expression"):
                            return True
                    else:
                        return False
                    if (max_index == 1):
                        return False
                else:
                    return False
            if (max_index == 2):
                if (a_list[max_index - 2] == "identifier" and a_list[max_index - 1] == "assignment" and a_list[
                    max_index] == "expression"):
                    return True
    return False


if __name__ == '__main__':

    fh = open("examples.txt")
    for line in fh:
        clean_line = line.strip()
        the_token = tokenize(clean_line)
        final_string = ""
        for i in range(len(the_token)):
            final_string = final_string + the_token[i] + " "
        print(clean_line + " tokenizes as " + final_string)
        if ("error" not in the_token):
            is_valid = recognize(the_token)
            validity_statement = ""
            if (is_valid):
                validity_statement = "is a Valid Statement"
            else:
                validity_statement = "is an Invalid Statement"
            print("\t\t" + clean_line + " " + validity_statement)
    fh.close()
