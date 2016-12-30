from ctext import labelText

# global counters
labels = []
label_count = 0

def branchesAndInfos(labels):
	branches = [makeLabel(label) for label in labels]
	infos = [labelInfo(branch) for branch in branches]
	return (branches, infos)

def labelInfo(label):
	print_info = 'print_info("%(label)s");' % locals()
	return (label + ':' + ' ' + print_info)

# label numbering

def newLabelNumber():
	global label_count
	# can we just take len(labels)?
	label_count += 1
	return label_count

def makeLabel(name):
	global labels
	label = name + '_' + str(newLabelNumber())
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

