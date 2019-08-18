# labels

labels = []


def branchesAndInfos(labels):
    branches = [makeLabel(label) for label in labels]
    infos = [labelInfo(branch) for branch in branches]
    return (branches, infos)


def labelInfo(label):
    print_info = f'print_info("{label}");'
    return label + ':' + ' ' + print_info


# label numbering

label_counts = {}


def newLabelNumber(name):
    try:
        label_counts[name] += 1
    except KeyError:
        label_counts[name] = 1

    return label_counts[name]


def makeLabel(name):
    global labels
    global label_counts
    label = name + '_' + str(newLabelNumber(name))
    labels += [label]
    return label

# for this to work, numbers can't be used
# in label names. for instance,
# makeLabel('hello1') yields 'hello11' when
# first called ('hello1' + '1'), and if
# makeLabel is called nine more times and
# then called with 'hello', it will yield
# 'hello11' ('hello' + '11'). how could this
# be avoided aside from restricting input?

# different numberings for different strings?
# that would make the code easier to follow
