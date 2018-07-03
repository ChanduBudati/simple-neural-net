#!/usr/bin/env python3
import sys
import csv
import math

class neuron:
	def __init__(self, data):
		data = data.split()
		self.output = 0
		self.delta = 0
		self.layernum = int(data[0])
		self.neuronnum = int(data[1])
		self.bias = float(data[len(data)-1])
		self.weights = list()

		for i in range(2, len(data)-1):
			self.weights.append(float(data[i]))

	def evaluate(self, input):
		self.input = list()
		for i in input:
			self.input.append(i)
		self.sum = 0
		for i in range(len(self.weights)):
			self.sum = self.sum + self.weights[i]*self.input[i]
		self.sum = self.sum + self.bias
		self.output = sig(self.sum)
class layer:
	def __init__(self, nlist, parent):
		self.output = list()
		self.neurons = list()
		self.parent = parent
		for n in nlist:
			t = neuron(n)
			self.neurons.append(t)
	
	def run(self, input):
		self.output = list()
		for i in range(len(self.neurons)):
			self.neurons[i].evaluate(input)
		self.parent.output = list()
		for i in range(len(self.neurons)):
			self.output.append(self.neurons[i].output)
			self.parent.output.append(self.neurons[i].output)
class network:
	def __init__(self, neurons):
		self.output = list()
		self.input = list()
		self.layers = list()
		layerlength = int(neurons[-1][0])
		nlist = [[] for i in range(layerlength+1)]
		for neuron in neurons:
			nlist[int(neuron[0])].append(neuron)
		for i in nlist:
			l = layer(i, self)
			self.layers.append(l)
	def run(self, inputs):
		self.output = list()
		self.input = list()
		for i in inputs:
			self.input.append(float(i))	
			self.output.append(float(i))
		for i in range(len(self.layers)):
			self.layers[i].run(self.output)

	def print(self):
		for layer in self.layers:
			for ner in layer.neurons:
				print("(" + str(ner.layernum) + "," + str(ner.neuronnum) + ")" + ":\t" +str(round(ner.bias,4)), end = "\t")
				print("[", end = " ")
				for w in ner.weights:
					print('{:07.2f}'.format(w), end=" ")
				print("]" + "\t"+str(round(ner.output,8))+"\t"+str(round(ner.delta,8)))

def sig(n):
	return(1/(1 + math.exp(-1 * n)))

def devsig(n):
	return(sig(n)*(1 - sig(n)))

def chweight(neuron):
	for i in range(len(neuron.weights)):
		neuron.weights[i] = neuron.weights[i] + neuron.delta*neuron.input[i]

def train(n, input, llen):
	for inp in input: 
		hpt = [0]*llen
		hpt[inp[-1]] = 1
		n.run(inp[0:-1])
		for i in range(len(n.layers[-1].neurons)):
			n.layers[-1].neurons[i].delta = devsig(n.layers[-1].neurons[i].sum) * (hpt[i] - n.layers[-1].neurons[i].output)
			chweight(n.layers[-1].neurons[i])
		for i in range(len(n.layers)-2, -1, -1):
			for j in range(len(n.layers[i].neurons)):
				sum = 0
				for neu in n.layers[i+1].neurons:
					sum = sum + neu.weights[j] * neu.delta
				n.layers[i].neurons[j].delta = devsig(n.layers[i].neurons[j].sum)*sum
				chweight(n.layers[i].neurons[j])

def test(n, input):
	count = 0
	crt = 0
	bool = 0
	for inp in input: 
		n.run(inp[0:-1])
		if (max(n.output) == n.output[inp[-1]]): #and n.output.count(max(n.output)) == 1):
			bool = 1
			crt = crt+1
		count = count+1
		#print('{:>64}'.format(str(n.output)) + "\t" + str(inp[-1]) + "\t" + str(bool))
	print(str(crt) + " " + str(count) + " " + str(round(crt/count,4)))
	
def main():
	net_dsc = "p2NET0"#sys.argv[1]
	in_file = "p2SEEDS.csv"#sys.argv[2]
	l_train = 0#int(sys.argv[3])
	h_train = 211#int(sys.argv[4])
	l_test = 0#int(sys.argv[5])
	h_test = 211#int(sys.argv[6])
	epoch = 8000#int(sys.argv[7])
	pflag = 1#int(sys.argv[8])
	
	file = open(in_file,'r')
	seeds = file.read().splitlines()
	file.close()
	for i in range(len(seeds)):
		seeds[i] = [float(j) for j in seeds[i].strip().split(',')]
	#max = [0]*len(seeds[0])
	#min = [sys.maxsize]*len(seeds[0])
	labels = list()
	labels.append(seeds[0][-1])
	for i in range(len(seeds)):
		if (labels[-1] != seeds[i][-1]):
			labels.append(int(seeds[i][-1]))
		for j in range(len(seeds[i])-1):
			seeds[i][j] = (seeds[i][j] - min(seeds[i]))/(max(seeds[i]) - min(seeds[i]))
		'''
		if(labels[-1] != i[-1]):
			labels.append(int(i[-1]))
		for j in range(len(i)):
			if(max[j] <= i[j]):
				max[j] = i[j]
			if(min[j] >= i[j]):
				min[j] = i[j]
		'''
	labellen = len(labels)
	for i in range(len(seeds)):
	#	for j in range(len(seeds[i])-1):
	#		seeds[i][j] = (seeds[i][j] - min[j])/(max[j] - min[j])
		seeds[i][-1] = labels.index(seeds[i][-1])
 	
	for i in seeds:
		print(i)

	file = open(net_dsc,'r')
	data = file.read().splitlines()
	file.close()
	neuronlist = list()
	inputlist = list()
	for i in range(len(data)):
		data[i] = data[i].split("#")[0]
		data[i] = data[i].strip()
		if data[i].find('inputs') != -1:
			inputlist = (data[i].split(' ', 1)[1].strip()).split()
		elif data[i] != '':
			neuronlist.append(data[i])
	n = network(neuronlist)

	if pflag == 1 :
		n.print()
		print()
	for i in range(epoch):
		train(n,  seeds[l_train: h_train], labellen)
		if(i%10 == 0):
			print(str(i) + ":\t", end = "")
			test(n, seeds[l_test:h_test])
	if pflag == 1 :
		print()
		n.print()
	print("test results: ", end = "")
	test(n, seeds[l_test:h_test])
'''
	for i in range(epoch):
		train(n,  seeds[l_train: h_train], labellen)
	test(n, seeds[l_test:h_test])
'''
main()
