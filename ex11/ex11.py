############################################################
# FILE : ex11.py
# WRITER : Inbar Leibovich , inbarlei , 21395389
# EXERCISE : intro2cse ex11 2020
# DESCRIPTION: 
# STUDENTS I DISCUSSED THE EXERCISE WITH: 
# WEB PAGES I USED: 
# NOTES: For more
############################################################
import itertools
from collections import Counter


class Node:
    def __init__(self, data, positive_child=None, negative_child=None):
        """ Initiate node """
        self.data = data
        self.positive_child = positive_child
        self.negative_child = negative_child
        self.number = 0

    def __str__(self):
        return self.data

    def add_to_number(self):
        self.number += 1

    def set_number(self, num):
        self.number = num


class Record:
    def __init__(self, illness, symptoms):
        """ Initiate record """
        self.illness = illness
        self.symptoms = symptoms


def parse_data(filepath):
    """ Translate data into list of records """
    with open(filepath) as data_file:
        records = []
        for line in data_file:
            words = line.strip().split()
            records.append(Record(words[0], words[1:]))
        return records


class Diagnoser:
    def __init__(self, root):
        """ Initiate diagnoser with tree root """
        self.root = root

    def diagnose(self, symptoms):
        """ Find an illness that matches the symptoms """
        # Get the root
        current_node = self.root
        # While current_node has children (is not a leaf)
        while current_node.positive_child is not None:
            # Advance according to the symptom
            if current_node.data in symptoms:
                current_node = current_node.positive_child
            else:
                current_node = current_node.negative_child
        # Return disease
        return current_node.data

    def calculate_success_rate(self, records):
        """ Calculate success rate for the records given """
        successes = 0
        # Check if each record is diagnosed correctly
        for r in records:
            if self.diagnose(r.symptoms) == r.illness:
                successes += 1
        # Return success rate
        return successes / len(records)

    def all_illnesses(self):
        """ Return a list of all illnesses ordered by how common """
        # Add all leaf nodes to counter
        c = self.check_node(self.root, Counter())
        illnesses = []
        # Add illnesses to list starting with the most common
        for disease in c.most_common():
            illnesses.append(disease[0])
        return illnesses

    def check_node(self, node, counter):
        """ Add leaves to counter through recursion """
        # Make sure node given is a Node object
        if node is None:
            return
        # If it is a leaf node, add it to counter
        if node.positive_child is None and node.positive_child is None:
            counter[node.data] += 1
            return counter
        else:
            # Recursion step: go to positive and negative children
            self.check_node(node.positive_child, counter)
            self.check_node(node.negative_child, counter)
            return counter

    def paths_to_illness(self, illness):
        """ Get all paths on tree that lead to given illness """
        all_paths = []
        self.get_path(self.root, [], illness, all_paths)
        return all_paths

    def get_path(self, node, path, illness, all_paths):
        """ Get paths from node to illness. When illness
        is reached, add the path to all_paths """
        # Make sure node is a Node object
        if node is None:
            return
        # If node is a leaf
        if node.positive_child is None and node.negative_child is None:
            # If leaf contains given illness, add path to all_paths
            if node.data == illness:
                all_paths.append(path)
        else:
            # Call positive child
            self.get_path(node.positive_child, path[:] + [True], illness,
                          all_paths)
            # Call negative child
            self.get_path(node.negative_child, path + [False], illness,
                          all_paths)

    def minimize(self, remove_empty=False):
        """ Get rid of unnecessary nodes """
        self.root = self.minimize_helper(self.root, remove_empty)

    def minimize_helper(self, node, remove_empty):
        """ Get rid of unnecessary nodes """
        # Check if positive child is a question
        if node.positive_child.positive_child:
            node.positive_child = self.minimize_helper(node.positive_child,
                                                       remove_empty)
        # Check if negative child is a question
        if node.negative_child.negative_child:
            node.negative_child = self.minimize_helper(node.negative_child,
                                                       remove_empty)
        # If children are equal, set node to one of the children
        if self.check_equal(node.positive_child, node.negative_child):
            node = node.positive_child
        # If a child is empty, and remove_empty is True,
        # replace node with other child
        if node and remove_empty:
            if node.positive_child or node.negative_child:
                if not node.positive_child or node.positive_child.data == None:
                    node = node.negative_child
                elif not node.negative_child or node.negative_child.data == None:
                    node = node.positive_child
        return node

    def check_equal(self, pos, neg):
        """ Check if node pos is the same as node neg """
        if pos is None and neg is None:
            return True
        if pos is None or neg is None or pos.data != neg.data:
            return False
        else:
            return self.check_equal(pos.positive_child, neg.positive_child) \
                   and self.check_equal(pos.negative_child, neg.negative_child)


def build_tree(records, symptoms):
    """ Build a tree and return its root """
    # Create equivalent "tree" as an array
    syms = [0] * (2 ** len(symptoms))
    for r in records:
        # Find the location in array of the illness, based on symptoms
        num = 0
        for s in symptoms:
            num *= 2
            if s in r.symptoms:
                num += 1
        # Put illness in array
        if syms[num] == 0:
            syms[num] = [r.illness]
        else:
            syms[num].append(r.illness)
    # Build the tree and return the root
    return get_tree(symptoms, 0, syms)


def get_tree(symptoms, num, syms):
    """ Build tree and return root """
    # Caluclate number in tree corresponding to location in array
    num *= 2
    # If multiple symptoms, create
    if len(symptoms) > 1:
        pos = get_tree(symptoms[1:], num + 1, syms)
        neg = get_tree(symptoms[1:], num, syms)
    # If this is the last symptom, create illness nodes
    else:
        pos = Node(None)
        neg = Node(None)
        if syms[num]:
            c = Counter(syms[num])
            neg = Node(c.most_common(1)[0][0])
        if syms[num + 1]:
            c = Counter(syms[num + 1])
            pos = Node(c.most_common(1)[0][0])
    # Return node
    return Node(symptoms[0], pos, neg)


def print_tree(node):  # Delete this
    """ Print tree for debugging purposes """
    print('data: ', node.data)
    if node.positive_child:
        print('positive: ', end="")
        print_tree(node.positive_child)
        print('negative: ', end="")
        print_tree(node.negative_child)
    print()


def optimal_tree(records, symptoms, depth):
    """ Build the optimal tree for given depth """
    root = None
    success = 0
    # Try all combinations of symptoms matching depth
    for x in itertools.combinations(symptoms, depth):
        # Build tree and put into diagnoser
        node = build_tree(records, x)
        d = Diagnoser(node)
        # Calculate tree success
        cur_success = d.calculate_success_rate(records)
        # If it is the most successful thus far, record
        if success < cur_success or success == 0:
            success = cur_success
            root = node
    # Return root of best tree
    return root


def more_optimal_tree(records, symptoms, depth):
    """ Get an optimized tree of given depth """
    # Get root to tree
    root = build_tree(records, symptoms)
    # How many layers must be removed
    num_to_remove = len(symptoms) - depth
    for _ in range(num_to_remove):
        # Write how many records are under each node
        put_numbers(root, records)
        # Get which nodes must be removed to decrease one layer
        fails, parents, children = more_optimal_tree_helper(root, None,
                                                            records, 0)
        # Remove nodes as necessary
        if parents == [None]:
            root = children[0][0]
        else:
            for p, c in zip(parents, children):
                if c[1]:
                    p.positive_child = c[0]
                else:
                    p.negative_child = c[0]
    # When done, return root
    return root


def put_numbers(node, records):
    """ Save number of records under node in node.number """
    node.set_number(0)
    # Leaf nodes
    if node.positive_child is None:
        for r in records:
            if node.data == r.illness:
                node.add_to_number()
    # Question nodes - add the numbers in leaf nodes
    else:
        positives = []
        negatives = []
        for r in records:
            if node.data in r.symptoms:
                positives.append(r)
            else:
                negatives.append(r)
        pos = put_numbers(node.positive_child, positives)
        neg = put_numbers(node.negative_child, negatives)
        node.set_number(pos + neg)
    # Return number at this node
    return node.number


def more_optimal_tree_helper(node, parent, records, pos):
    """ Choose how to remove a layer from under this node """
    # To replace this node find its more successful child
    f3, chosen_child = calculate_remove_layer(node, pos)
    # If node cannot be replaced from below
    if not node.positive_child.positive_child:
        return f3, [parent], [chosen_child]
    # Otherwise find best place to remove layer
    elif node.positive_child and node.negative_child:
        # Best place to remove from each child
        f1, p1, c1 = more_optimal_tree_helper(node.positive_child,
                                              node, records, 1)
        f2, p2, c2 = more_optimal_tree_helper(node.negative_child,
                                              node, records, 0)
        # If better to remove from children than current node
        if f1 + f2 < f3:
            return f1 + f2, p1 + p2, c1 + c2
        # Otherwise remove current node
        else:
            return f3, [parent], [chosen_child]


def calculate_remove_layer(node, pos):
    """ Calculate losses for removing the less successful child """
    # number of records under negative node
    remove_neg = node.negative_child.number
    # number of records under positive node
    remove_pos = node.positive_child.number
    # Return success rate and chosen child
    if remove_neg > remove_pos:
        return remove_pos, (node.negative_child, pos)
    else:
        return remove_neg, (node.positive_child, pos)


if __name__ == "__main__":

    # Manually build a simple tree.
    #                cough
    #          Yes /       \ No
    #        fever           healthy
    #   Yes /     \ No
    # influenza   cold
    one = Node("influenza", None, None)
    two = Node("influenza", None, None)
    flu_leaf = Node("influenza", one, two)
    cold_leaf = Node("cold", None, None)
    inner_vertex = Node("fever", flu_leaf, cold_leaf)
    healthy_leaf = Node("healthy", None, None)
    root = Node("cough", inner_vertex, healthy_leaf)

    diagnoser = Diagnoser(root)

    # Simple test
    diagnosis = diagnoser.diagnose(["cough"])
    if diagnosis == "cold":
        print("Test passed")
    else:
        print("Test failed. Should have printed cold, printed: ", diagnosis)

    # Test 2
    records = parse_data('Data/tiny_data.txt')
    print(diagnoser.calculate_success_rate(records))

    # Test 3
    print(diagnoser.all_illnesses())

    # Test 4
    print(diagnoser.paths_to_illness('colddd'))

    # Test 5
    symptoms = set()
    for r in records:
        print(r.illness)
        for s in r.symptoms:
            symptoms.add(s)
    print('symptoms', symptoms)
    root = build_tree(records, list(symptoms))
    diagnoser = Diagnoser(root)
    print(diagnoser.paths_to_illness('healthy'))

    # Test 6
    record1 = Record("influenza", ["cough", "fever", "headache"])
    record2 = Record("cold", ["cough", "fever"])
    records = [record1, record1, record1, record2]

    n = (build_tree(records, ["cough", "fever"]))
    u = (optimal_tree(records, ["cough", "fever"], 1))
    v = (build_tree(records, ["cough"]))
    d = Diagnoser(n)
    print_tree(d.root)
    d.minimize(False)
    print_tree(d.root)

    # Test 7
    r1 = Record("1", ["a", "b", "c"])
    r2 = Record("2", ["a", "b"])
    r3 = Record("3", ["a", "c"])
    r4 = Record("4", ["a"])
    r5 = Record("5", ["b", "c"])
    r6 = Record("6", ["b"])
    r7 = Record("7", ["c"])
    r8 = Record("8", [])

    records = [r1, r2, r3, r4, r5, r6, r7, r8] + [r1, r5, r6, r3]

    m = more_optimal_tree(records, ["a", "b", "c"], 2)
    print('hiii')
    print_tree(m)
