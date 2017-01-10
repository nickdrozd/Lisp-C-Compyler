from instrseqs import BranchSeq

labels = []

def labelsAndBranches(labelNames):
        labels = [makeLabel(label) for label in labelNames]
        branches = [BranchSeq(label) for label in labels]
        return labels, branches

ifLabelNames = 'TRUE_BRANCH', 'FALSE_BRANCH', 'AFTER_IF'
lambdaLabelNames = 'FUNC_ENTRY', 'AFTER_LAMBDA'

ifLabelsBranches = lambda: labelsAndBranches(ifLabelNames)
lambdaLabelsBranches = lambda: labelsAndBranches(lambdaLabelNames)

# label numbering

label_counts = {}

def newLabelNumber(name):
	try:
		label_counts[name] += 1
	except:
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

