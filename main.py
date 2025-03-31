# START q0 -
# q0 q1 a
# q0 q2 b
# q0 q3 c
# q1 q2 b
# q2 q3 a
# q1 q4 c
# q2 q4 b
# q3 q4 a
# q4 q5 a
# q5 q4 a

def citesteSigma(lines):
    # parsam lines pana la end
    sigma = []
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            continue
        elif line == "End":
            break
        elif line != "Sigma:":
            sigma.append(line)
    return sigma

def citesteStates(lines):
    states = []
    startState = None
    finalStates = []
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            continue
        elif line == "End":
            break
        elif line != "States:":
            lineParse = line.split()
            states.append(lineParse[0].strip(',').strip())
            for token in lineParse: # verificam daca este start sau finish, pentru flag-uri respectiva
                token = token.strip(',')
                token = token.strip()
                if(token == "S" and startState != None):
                    print("Prea multe start States! (max allowed = 1)")
                    return -1
                if(token == "S" and startState == None):
                    startState = lineParse[0].strip(',').strip()
                if(token == "F"):
                    finalStates.append(lineParse[0].strip(',').strip())
    if(startState == None):
        print("Automatul nu contine niciun startState! (min allowed = 1, max allowed = 1)")
        return -1
    return states, startState, finalStates


def citesteTransitions(lines):
    transitions = {}
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            continue
        if line == "End":
            break
        if line != "Transitions:":
            left, middle, right = line.split(",")
            left = left.strip()
            middle = middle.strip()
            right = right.strip()
            # TODO: CHECK NFA si sa apartina states si sigma
            if transitions.get(left, None) == None:
                transitions[left] = [(middle, right)]
            else:
                transitions[left].append((middle, right))
    return transitions


def citire(filename):
    sigma = []
    states = {}
    startState = ""
    finalStates = []
    # pentru fiecare nod
    # vedem ce muchii are, de forma transitions[nod_curent] = lista de tupluri de forma (cuvant_acceptat, nod_urmator)
    transitions = {}
    sigmaIndex, statesIndex, trasitionsIndex = -1, -1, -1
    with open(filename) as f:
        linii = f.readlines()
        lineIndex = -1
        for line in linii:
            line = line.strip()
            lineIndex += 1
            if line[0] == "#":
                continue
            else:
                if line == "Sigma:":
                    sigmaIndex = lineIndex
                elif line == "States:":
                    statesIndex = lineIndex
                elif line == "Transitions:":
                    transitionsIndex = lineIndex
        # acum avem indecsii la linii
        # verificam daca ii avem pe toti, daca nu aruncam o eroare
        if sigmaIndex == -1 or statesIndex == -1 or transitionsIndex == -1: # clar una din ele nu este, aruncam o eroare
            print("Date introduse gresit, lipsesc field-urile Sigma/States/Transitions!")
            return -1
        sigma = citesteSigma(linii[sigmaIndex:]) # aici nu avem erori daca mi-a fost transmis ca datele sunt corecte
        verif = citesteStates(linii[statesIndex:])
        if verif == -1:
            print("Intrare fisier stari invalida!")
            return -1
        else:
            states, startState, finalStates = verif
        transitions = citesteTransitions(linii[transitionsIndex:])
    if finalStates == []:
        print("Automatul nu contine nici o stare finala!")
        return -1
    return sigma, states, startState, finalStates, transitions

# verificam daca limbajul este corect definit
def verificare(sigma, states, startState, finalStates, transitions):
    for transition in transitions:
        if transition not in states:
            print(f"Automatul nu contine starea {transition}")
            return -1
        v = []
        for muchie, nod_nou in transitions[transition]:
            if muchie not in sigma:
                print(f"Automatul nu admite in limbaj cuvantul {muchie}")
                return -1
            if nod_nou not in states:
                print(f"Automatul nu contine starea {nod_nou}!")
                return -1
            v.append(muchie)
        if (len(v) != len(set(v))):
            print("Automatul este NFA!")
            return 2
    return 1;

def DFS(actual_state, finalStates, transitions, visited):
    visited[actual_state] = True
    if actual_state in finalStates:
        return 1
    for symbol, next_state in transitions.get(actual_state, []):
        print(actual_state)
        if next_state not in visited:
            if DFS(next_state, finalStates, transitions, visited) == 1:
                return 1
    return 0


def verificareAcceptance(startState, finalStates, transitions, isNfa):
    viz = {}
    result = DFS(startState, finalStates, transitions, viz)
    if result == 1:
        if isNfa == 1:
            return 2
        return 1
    else:
        if isNfa == 0:
            return -1
        else:
            return -2
    return 0

def main():
    result = citire("nfa_config_file.txt")
    if result == -1:
        print("Automatul contine erori! Verificati mesajul anterior!")
        return
    sigma, states, startState, finalStates, transitions = result
    finalCheck = verificare(sigma, states, startState, finalStates, transitions)
    if finalCheck == -1:
        print("Automatul contine erori! Verificati mesajul anterior!")
        return
    isNfa = (finalCheck == 2)

    print("Sigma: ", sigma)
    print("States: ", states)
    print("startState: ", startState)
    print("finalStates: ", finalStates)
    print("transitions: ", transitions)
    acceptance = verificareAcceptance(startState, finalStates, transitions, isNfa)
    if  acceptance == 1:
        print("Dfa Acceptat!")
    elif acceptance == 2:
        print("Nfa Acceptat!")
    elif acceptance == -1:
        print("Dfa Invalid!")
    elif acceptance == -2:
        print("Nfa Invalid!")
    else:
        print("Eroare!")
if __name__ == '__main__':
    main()