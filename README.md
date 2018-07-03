# simple-neural-net

This new program will take 8 command-line arguments:

    neural_net_descr_file
        like p1, this describes the NN; sample is in p2NET0;
        use the simple sigmoid function at each neuron

    input_filename
        file containing the inputs to the NN; this file will be in csv format,
        e.g. see p2SEEDS.csv

    low_train_rng
        index of first record in the input file to be used to train the NN

    hi_train_rng
        index just PAST last record in the input file to be used to train the NN;
        note that this acts like python's  low:high  indexes for lists etc

    low_test_rng
        index of first record in the input file to be used to test the NN

    hi_test_rng
        index just PAST last record in the input file to be used to test the NN;
        note that this acts like python's  low:high  indexes for lists etc

    num_epochs
        number of iterations to perform over the train input records before 
        beginning the testing phase

    print_internals_flag
        this flag will be 0 or 1; if 1, print the internal values of each neuron
        in the NN  before training and after training (before testing); print one
        line per neuron, containing this info:
            bias 
            weights
            output (if one has been computed by training)
            delta  (if one has been computed by training)


We will back-propagate changes to weights but will leave biases un-altered.

Our discussions about backprop may include comments about values for momentum
and learning-rate.  We will NOT be employing those values in our nets.
They are not represented in our command-line args.  If you want to code a
value for learning-rate, just use 1.0 which should cause it to have no effect.


We will pre-process the data for our network before feeding it into the net:

    Normalize the values in each attribute to work well with the sigmoid
    function.  We will discuss details of how to do that in class.

    Labels can be represented as a one-hot version of their index into a
    list of valid labels.  Our network will have one neuron in the output
    layer for each possible label in the list of labels.  This will match
    with the one-hot representation.  Again, we will discuss details in class.


At the end of each training epoch which is a multiple of 10, print this kind of
information in this format:

     0     70 of 210   0.3333
    10     96 of 210   0.4571
    20    139 of 210   0.6619

where in the last line, 20 is the epoch number, 139 is the number correct
of 210 which is the total number tested;  and 0.6619 is 139/210 rounded to
4 decimal places.


At the end of the test phase, print the result in this form:

    test result:  141 of 210  0.6714

