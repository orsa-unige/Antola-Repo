
test_list = [

    {
        "obj":   "test1",
        "bins":  [1,2],
        "ndit":  2,
    },

    {
        "obj":   "test2",
        "bins":  [6,4],
        "filts": [2,3],
        "dits":  [0.1, 0.2],
        "ndit":  2,
    },

    {
        "obj":   "test3",
        "bins":  [3],
        "ndit":  1,
    },

]

###############################
### Bias in binning 1 and 2 ###
###############################

bias_list = [

    {
        "obj":   "bias",
        "bins":  [1,2],
        "ndit":  50,
    },

    # {
    #     "obj":   "bias",
    #     "bins":  [3],
    #     "ndit":  30,
    # },

]

bias_binning_1 = [

    {
        "obj":   "bias",
        "bins":  [1],
        "ndit":  40,
    },
]

bias_binning_2 = [

    {
        "obj":   "bias",
        "bins":  [2],
        "ndit":  40,
    },
]

bias_binning_3 = [

    {
        "obj":   "bias",
        "bins":  [3],
        "ndit":  40,
    },
]

bias_binning_4 = [

    {
        "obj":   "bias",
        "bins":  [4],
        "ndit":  40,
    },

]

bias_binning_5 = [

    {
        "obj":   "bias",
        "bins":  [5],
        "ndit":  40,
    },

]

bias_binning_6 = [

    {
        "obj":   "bias",
        "bins":  [6],
        "ndit":  40,
    },

]

#################################
### Flat U in binning 1 and 2 ###
#################################

flat_U = [

    ########### U ###########
    
    {
        "obj":  "flat U",
        "bins":  [1,2],
        "ndit":  3,
        "dits":  [1800.0],
        "filts": [1,2],
    },
]

##############################
### Flat BVRI in binning 1 ###
##############################

flat_BVRI_binning_1 = [
    
    ########### B ###########

    {
        "obj":  "flat B",
        "bins":  [1],
        "ndit":  5,
        "dits":  [3.0],
        "filts": [2],
    },

    {
        "obj":  "flat B",
        "bins":  [1],
        "ndit":  5,
        "dits":  [10.0],
        "filts": [2],
    },
    
    ########### V ###########

    {
        "obj":  "flat V",
        "bins":  [1],
        "ndit":  5,
        "dits":  [1.0],
        "filts": [3],
    },

    {
        "obj":  "flat V",
        "bins":  [1],
        "ndit":  5,
        "dits":  [4.0],
        "filts": [3],
    },
    
    ########### R ###########

    {
        "obj":  "flat R",
        "bins":  [1],
        "ndit":  5,
        "dits":  [1.0],
        "filts": [4],
    },

    {
        "obj":  "flat R",
        "bins":  [1],
        "ndit":  5,
        "dits":  [3.0],
        "filts": [4],
    },
    
    ########### I ###########

    {
        "obj":  "flat I",
        "bins":  [1],
        "ndit":  5,
        "dits":  [30.0],
        "filts": [5],
    },

    {
        "obj":  "flat I",
        "bins":  [1],
        "ndit":  5,
        "dits":  [60.0],
        "filts": [5],
    },
    
    ######## Halpha ########

    {
        "obj":  "flat Halpha",
        "bins":  [1],
        "ndit":  5,
        "dits":  [20.0],
        "filts": [6],
    },

    {
        "obj":  "flat Halpha",
        "bins":  [1],
        "ndit":  5,
        "dits":  [40.0],
        "filts": [6],
    },

]
##############################
### Flat BVRI in binning 2 ###
##############################

flat_BVRI_binning_2 = [
    
    ########### B ###########

    {
        "obj":  "flat B",
        "bins":  [2],
        "ndit":  5,
        "dits":  [1.0],
        "filts": [2],
    },

    {
        "obj":  "flat B",
        "bins":  [2],
        "ndit":  5,
        "dits":  [3.0],
        "filts": [2],
    },
    
    ########### V ###########

    {
        "obj":  "flat V",
        "bins":  [2],
        "ndit":  5,
        "dits":  [0.5],
        "filts": [3],
    },

    {
        "obj":  "flat V",
        "bins":  [2],
        "ndit":  5,
        "dits":  [1.0],
        "filts": [3],
    },
    
    ########### R ###########

    {
        "obj":  "flat R",
        "bins":  [2],
        "ndit":  5,
        "dits":  [0.4],
        "filts": [4],
    },

    {
        "obj":  "flat R",
        "bins":  [2],
        "ndit":  5,
        "dits":  [0.8],
        "filts": [4],
    },
    
    ########### I ###########

    {
        "obj":  "flat I",
        "bins":  [2],
        "ndit":  5,
        "dits":  [10.0],
        "filts": [5],
    },

    {
        "obj":  "flat I",
        "bins":  [2],
        "ndit":  5,
        "dits":  [25.0],
        "filts": [5],
    },
    
    ######## Halpha ########

    {
        "obj":  "flat Halpha",
        "bins":  [2],
        "ndit":  5,
        "dits":  [10.0],
        "filts": [6],
    },

    {
        "obj":  "flat Halpha",
        "bins":  [2],
        "ndit":  5,
        "dits":  [20.0],
        "filts": [6],
    },

]


##############################
### Flat BVRI in binning 3 ###
##############################

flat_BVRI_binning_3 = [
    
    ########### B ###########

    {
        "obj":  "flat B",
        "bins":  [3],
        "ndit":  5,
        "dits":  [0.7],
        "filts": [2],
    },

    {
        "obj":  "flat B",
        "bins":  [3],
        "ndit":  5,
        "dits":  [1.5],
        "filts": [2],
    },
    
    ########### V ###########

    {
        "obj":  "flat V",
        "bins":  [3],
        "ndit":  5,
        "dits":  [0.25],
        "filts": [3],
    },

    {
        "obj":  "flat V",
        "bins":  [3],
        "ndit":  5,
        "dits":  [0.55],
        "filts": [3],
    },
    
    ########### R ###########

    {
        "obj":  "flat R",
        "bins":  [3],
        "ndit":  5,
        "dits":  [0.2],
        "filts": [4],
    },

    {
        "obj":  "flat R",
        "bins":  [3],
        "ndit":  5,
        "dits":  [0.45],
        "filts": [4],
    },
    
    ########### I ###########

    {
        "obj":  "flat I",
        "bins":  [3],
        "ndit":  5,
        "dits":  [9],
        "filts": [5],
    },

    {
        "obj":  "flat I",
        "bins":  [3],
        "ndit":  5,
        "dits":  [15],
        "filts": [5],
    },
    
    ######## Halpha ########

    {
        "obj":  "flat Halpha",
        "bins":  [3],
        "ndit":  5,
        "dits":  [5],
        "filts": [6],
    },

    {
        "obj":  "flat Halpha",
        "bins":  [3],
        "ndit":  5,
        "dits":  [9.5],
        "filts": [6],
    },

]

##############################
### Flat BVRI in binning 4 ###
##############################

flat_BVRI_binning_4 = [
    
    ########### B ###########

    {
        "obj":  "flat B",
        "bins":  [4],
        "ndit":  5,
        "dits":  [0.25],
        "filts": [2],
    },

    {
        "obj":  "flat B",
        "bins":  [4],
        "ndit":  5,
        "dits":  [0.45],
        "filts": [2],
    },
    
    ########### V ###########

    {
        "obj":  "flat V",
        "bins":  [4],
        "ndit":  5,
        "dits":  [0.1],
        "filts": [3],
    },

    {
        "obj":  "flat V",
        "bins":  [4],
        "ndit":  5,
        "dits":  [0.1],
        "filts": [3],
    },
    #è al limite di saturazione già con 0.1 quindi è replicato due volte...bisogna farlo su cielo?
    
    ########### R ###########

    #satura anche con 0.1s
    
    ########### I ###########

    {
        "obj":  "flat I",
        "bins":  [6],
        "ndit":  5,
        "dits":  [3],
        "filts": [5],
    },

    {
        "obj":  "flat I",
        "bins":  [4],
        "ndit":  5,
        "dits":  [7],
        "filts": [5],
    },
    
    ######## Halpha ########

    {
        "obj":  "flat Halpha",
        "bins":  [4],
        "ndit":  5,
        "dits":  [2.5],
        "filts": [6],
    },

    {
        "obj":  "flat Halpha",
        "bins":  [4],
        "ndit":  5,
        "dits":  [5.5],
        "filts": [6],
    },

]
