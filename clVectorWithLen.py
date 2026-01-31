import math
#####################################
#Fill in the classname of the object#
#####################################
class clInterfaceScript:
    #####################################
    #Constructor class (stay's this way)#
    #####################################
    def __init__(self):
        print ('clInterfaceScript::__init__->start')
        self.Tracker_CoordX=[]
        self.Tracker_Length_X=[]
        self.Tracker_CoordY=[]
        self.Tracker_Length_Y=[]
        self.Tracker_CoordZ=[]
        self.Tracker_Length_Z=[]

        try:
            print ('clInterfaceScript::__init__->start')
        except:
            traceback.print_exc()
    ####################################
    #Destructor class (stay's this way)#
    ####################################
    def __del__(self):
        print ('clInterfaceScript::__del__->start')

    ###########
    #Functions#
    ###########
    def calculate_all(self,x_dimension,y_dimension,z_dimension):
        print('calculate_all')
        i = 0
        j = 0
        z = 0
        
        while i < x_dimension:
           Tracker_Length_2 = []
           while j > y_dimension:
               Tracker_Length_3 = []
               while z < z_dimension:
                    self.Tracker_CoordX.append([i,j,z])
                    v = math.sqrt((i*i)+(j*j))
                    p = math.sqrt((v*v)+(z*z))
                    Tracker_Length_3.append(p)
                    print (p)
                    z = z + 1
               z = 0     
               j = j + 1
               Tracker_Length_2.append(Tracker_Length_3)
           j = 0    
           i = i + 1
           self.Tracker_Length_X.append(Tracker_Length_2)
           
   	
		#Calculate the second trio
        i=0
        j=10
        z=0
		

        while i < x_dimension:
           Tracker_Length_2 = []
           while j > -1:
               Tracker_Length_3 = []
               while z < z_dimension:
                    self.Tracker_CoordY.append([i,j,z])
                    v = math.sqrt((i*i)+(j*j))
                    p = math.sqrt((v*v)+(z*z))
                    Tracker_Length_3.append(p)
                    print (p)
                    z = z + 1
               z = 0     
               j = j - 1
               Tracker_Length_2.append(Tracker_Length_3)
           j = 0    
           i = i + 1
           self.Tracker_Length_Y.append(Tracker_Length_2)

	    #Calculate the third trio
        i=10
        j=0
        z=0
		
		
        while i > -1:
           Tracker_Length_2 = []
           while j < y_dimension:
               Tracker_Length_3 = []
               while z < z_dimension:
                    self.Tracker_CoordZ.append([i,j,z])
                    v = math.sqrt((i*i)+(j*j))
                    p = math.sqrt((v*v)+(z*z))
                    Tracker_Length_3.append(p)
                    print (p)
                    z = z + 1
               z = 0     
               j = j + 1
               Tracker_Length_2.append(Tracker_Length_3)
           j = 0    
           i = i - 1
           self.Tracker_Length_Z.append(Tracker_Length_2)

    def bestfit(self,trio_1,trio_2,trio_3):
        tol = 2
        counter_1 = 0
        counter_2 = 0
        counter_3 = 0
        
        element_1=[]
        element_1_Y=[]
        BlockListNumberX=[]
        counter_X_L1 = 0
        for element_1 in self.Tracker_Length_X:
            counter_X_L2 = 0
            for element_1_Y in element_1:
                counter_X_L3 = 0
                for element_1_Z in element_1_Y:
                    if trio_1 < (element_1_Z + tol) and trio_1 > (element_1_Z - tol):
                        for elements_coord in self.Tracker_CoordX:
                             if elements_coord[0] == counter_X_L1 and elements_coord[1] == counter_X_L2 and elements_coord[2] == counter_X_L3:
                                 BlockListNumberX.append(elements_coord)
                                 print('Done')
                    counter_X_L3 = counter_X_L3 + 1    
                counter_X_L2 = counter_X_L2 + 1        
            counter_X_L1 = counter_X_L1 + 1
        
        BlockListNumberY=[]
        element_1=[]
        element_1_Y=[]
        counter_Y_L1 = 0
        for element_1 in self.Tracker_Length_Y:
            counter_Y_L2 = 0
            for element_1_Y in element_1:
                counter_Y_L3 = 0
                for element_1_Z in element_1_Y:
                    if trio_2 < (element_1_Z + tol) and trio_2 > (element_1_Z - tol):
                        for elements_coord in self.Tracker_CoordY:
                             if elements_coord[0] == counter_Y_L1 and elements_coord[1] == counter_Y_L2 and elements_coord[2] == counter_Y_L3:
                                 BlockListNumberY.append(elements_coord)
                                 print('TEST')
                    counter_Y_L3 = counter_Y_L3 + 1
                counter_Y_L2 = counter_Y_L2 + 1
            counter_Y_L1 = counter_Y_L1 + 1
             
        BlockListNumberZ=[]
        element_1_Y=[]
        counter_Z_L1 = 0                         
        for element_1 in self.Tracker_Length_Z:
            counter_Z_L2 = 0
            for element_1_Y in element_1:
                counter_Z_L3 = 0
                for element_1_Z in element_1_Y:
                     if trio_3 < (element_1_Z + tol) and trio_3 > (element_1_Z - tol):
                        for elements_coord in self.Tracker_CoordZ:
                             if elements_coord[0] == counter_Z_L1 and elements_coord[1] == counter_Z_L2 and elements_coord[2] == counter_Z_L3:
                                 BlockListNumberZ.append(elements_coord)
                                 print('Cold')
                     counter_Z_L3 = counter_Z_L3 + 1            
                counter_Z_L2 = counter_Z_L2 + 1                
            counter_Z_L1 = counter_Z_L1 + 1
            
        blockTolerance=10
        print(len(BlockListNumberX))
        i = 0
        j = 0
        k = 0
        while i < len(BlockListNumberX):
            while j < len(BlockListNumberY):
                while k < len(BlockListNumberZ):
                    elements_coord_1 = BlockListNumberX[i]
                    elements_coord_2 = BlockListNumberY[j]
                    elements_coord_3 = BlockListNumberZ[k]
                                   
                
                    if (elements_coord_1[0] < (elements_coord_2[0] + blockTolerance) and 
                        elements_coord_1[0] > (elements_coord_2[0] - blockTolerance) and
                        elements_coord_1[0] < (elements_coord_3[0] + blockTolerance) and
                        elements_coord_1[0] > (elements_coord_3[0] - blockTolerance) and
                        elements_coord_1[1] < (elements_coord_2[1] + blockTolerance) and
                        elements_coord_1[1] > (elements_coord_2[1] - blockTolerance) and
                        elements_coord_1[1] < (elements_coord_3[1] + blockTolerance) and
                        elements_coord_1[1] > (elements_coord_3[1] - blockTolerance) and
                        elements_coord_1[2] < (elements_coord_2[2] + blockTolerance) and 
                        elements_coord_1[2] > (elements_coord_2[2] - blockTolerance) and
                        elements_coord_1[2] < (elements_coord_3[2] + blockTolerance) and
                        elements_coord_1[2] > (elements_coord_3[2] - blockTolerance)):
                            print (elements_coord_1[0])
                            print (elements_coord_1[1])
                            print (elements_coord_1[2])
                            return elements_coord_1
                    k = k + 1
                j = j + 1
            i = i + 1
            
            
            
            
##########################################
#Created for manual testing of the methods on the class  #
##########################################################
def main():
    meInterfaceScript = clInterfaceScript()
    #Test the function manually
    meInterfaceScript.calculate_all(100,100,100)
    #To implement tolerances
    bestFitValue = meInterfaceScript.bestfit(50,50,50)
    
if __name__ == "__main__":
    main()
