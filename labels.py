# labels

from typing import List, Tuple, Union
LABELS = []


def branches_and_infos(labels: Union[Tuple[str, str, str], Tuple[str, str, str, str], Tuple[str, str]]) -> Tuple[List[str], List[str]]:
    branches = [make_label(label) for label in labels]
    infos = [label_info(branch) for branch in branches]
    return branches, infos


def label_info(label: str) -> str:
    return '{}: print_info("{}");'.format(label, label)


# label numbering

LABEL_COUNTS = {}


def new_label_number(name: str) -> int:
    try:
        LABEL_COUNTS[name] += 1
    except KeyError:
        LABEL_COUNTS[name] = 1

    return LABEL_COUNTS[name]


def make_label(name: str) -> str:
    label = '{}_{}'.format(name, str(new_label_number(name)))

    LABELS.append(label)

    return label


# for this to work, numbers can't be used
# in label names. for instance,
# make_label('hello1') yields 'hello11' when
# first called ('hello1' + '1'), and if
# make_label is called nine more times and
# then called with 'hello', it will yield
# 'hello11' ('hello' + '11'). how could this
# be avoided aside from restricting input?

# different numberings for different strings?
# that would make the code easier to follow
