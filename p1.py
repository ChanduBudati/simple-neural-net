#!/usr/bin/env python3

import sys
import math

class neuron:
	def __init__(self, data):
		data = data.split()
		self.layernum = int(data[0])
		self.neuronnum = int(data[1])
		self.bias = float(data[len(data)-1])
		self.weights = list()

		for i in range(2, len(data)-1):
			self.weights.append(float(data[i]))
		#print(self.weights)

	def evaluate(self, input):
		sum = 0
		for i in range(len(self.weights)):
			sum = sum + self.weights[i]*input[i]
		sum = sum + self.bias
		self.output = 1/(1 + math.exp(-1 * sum))



class layer:
	def __init__(self, nlist, parent):
		self.neurons = list()
		self.parent = parent
		for n in nlist:
			t = neuron(n)
			self.neurons.append(t)
	
	def run(self, input):
		for n in self.neurons:
			n.evaluate(input)
		self.parent.output = list()
		for n in self.neurons:
			self.parent.output.append(n.output)
		
		


class network:
	def __init__(self, inputs, neurons):
		self.input = list()
		self.output = list()
		self.layers = list()
		inputs = inputs.split()
		
		for i in inputs:
			self.input.append(float(i))	
		
		layerlength = int(neurons[len(neurons)-1][0])
		
		nlist = [[] for i in range(layerlength+1)]

		for neuron in neurons:
			nlist[int(neuron[0])].append(neuron)
		for i in nlist:
			l = layer(i, self)
			self.layers.append(l)
	
	def run(self):
		self.output = list()
		for i in self.input:
			self.output.append(i)
		for i in self.layers:
			i.run(self.output)
		for i in self.output:
			print(i)


def main():
	file = open(sys.argv[1],'r')
	data = file.read().splitlines()
	file.close()
	neuronlist = list()
	for i in range(len(data)):
		data[i] = data[i].split("#")[0]
		data[i] = data[i].strip()
	
		if data[i].find('inputs') != -1:
			inputlist = data[i].split(' ', 1)[1].strip()
		elif data[i] != '':
			neuronlist.append(data[i])

	n = network(inputlist, neuronlist)
	
	n.run()

			
main()
