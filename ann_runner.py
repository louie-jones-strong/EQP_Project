import numpy as np
import random

def main(structure_array,bias_on,bias,input_weights,inputs,Htan_on):

    node_info ,weight_info,number_of_layers,layer_info,number_of_outputs,number_of_inputs,number_of_nodes,number_of_lines = network_setup(structure_array,bias_on,input_weights)

    outputs = run_net(node_info,weight_info,inputs,number_of_layers,layer_info,bias_on,bias,number_of_outputs,number_of_inputs,Htan_on)


    return outputs

def run_net(node_info,weight_info,inputs,number_of_layers,layer_info,bias_on,bias,number_of_outputs,number_of_inputs,Htan_on):
    outputs = np.zeros((number_of_outputs))

    for loop in range(number_of_inputs):
        node_info[loop][0] = inputs[loop] / 10

    for loop in range(1,number_of_layers):#layer loop
        for loop2 in range(int(layer_info[loop][0]),int(layer_info[loop][1])): #node loop


             temp = 0
             for loop3 in range(int(node_info[loop2][1]),int(node_info[loop2][2])):#weight loop
                 temp += weight_info[loop3][0] * node_info[  int(weight_info[loop3][1])  ][0]
            
             if bias_on == True:
                temp += node_info[loop2][4] * bias
             node_info[loop2][3] = temp
             if loop == number_of_layers -1 or Htan_on == False:#output layer
                node_info[loop2][0] = temp
             else:
                node_info[loop2][0] = htan(temp)
    loop2 = 0
    for loop in range(layer_info[number_of_layers-1][0],layer_info[number_of_layers-1][1]):
        outputs[loop2] = node_info[loop][0]*10
        loop2 += 1

    return outputs

def htan(i):
    #i = i / 100
    if i > 19:
        output = 1.0
    elif i < -19:
        output = -1.0
    else:
       #(e^z-e^(-z))/(e^z+e^(-z))
        E = 2.7182818284590452353602874713527
        temp = pow(E,i)
        temp2 = pow(E,(i * -1))
        output = (temp - temp2)/(temp + temp2)
    return output

def network_setup (structure_array,bias_on,input_weights):
    number_of_inputs = structure_array[0]
    number_of_layers = len(structure_array)
    number_of_outputs = structure_array[-1]
    
    
    number_of_weights = 0
    number_of_nodes = structure_array[0]
    
    for loop in range(1,number_of_layers):
        number_of_weights += structure_array[loop-1] * structure_array[loop]
        number_of_nodes += structure_array[loop]

    weight_info = np.zeros((number_of_weights,3))  #weights_info[weight number][vaule,left,right]
    node_info   = np.zeros((number_of_nodes,5))    #node_info[node number][outputvaule,start of lines,end of lines,input vaule,bias weight]
    layer_info  = np.zeros((number_of_layers,2),dtype=int)   #weights_info[layer number][start,last]

    number_of_lines = 0
    start_next_layer = 0
    last_next_layer = structure_array[0]
    
    layer_info[0][0] = start_next_layer
    layer_info[0][1] = last_next_layer

    #loop to setup all weights and nodes
    for loop in range(1,number_of_layers):#layer loop


        start_previous_layer = start_next_layer
        last_previous_layer = last_next_layer

        start_next_layer = last_previous_layer
        last_next_layer = start_next_layer + structure_array[loop]


        layer_info[loop][0] = start_next_layer
        layer_info[loop][1] = last_next_layer

        for loop2 in range(start_next_layer,last_next_layer):#node loop 
            


             node_info[loop2][0] = 0               #value
             node_info[loop2][1] = number_of_lines #to
              
             for loop3 in range(start_previous_layer,last_previous_layer):#line loop
                 if input_weights[0] == "test":
                     weight_info[number_of_lines][0] = random.randint(-1000,1000)/1000
                 else:
                    weight_info[number_of_lines][0] = input_weights[number_of_lines]
                 
                 weight_info[number_of_lines][1] = loop3 #to 
                 weight_info[number_of_lines][2] = loop2 #from

                 number_of_lines += 1 



             node_info[loop2][2] = number_of_lines#from



    for loop in range(layer_info[0][1],number_of_nodes):
        if input_weights[0] == "test":
            node_info[loop][4] = random.randint(-1000,1000)/1000
        else:
            node_info[loop][4] = input_weights[number_of_lines]#value for bias weight


        number_of_lines += 1 

    return node_info,weight_info,number_of_layers,layer_info,number_of_outputs,number_of_inputs,number_of_nodes,number_of_lines