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
        self.dimensions = 10
        self.Tracker_CoordX=[]
        self.Tracker_Length_X=[]
        self.Tracker_CoordY=[]
        self.Tracker_Length_Y=[]
        self.Tracker_CoordZ=[]
        self.Tracker_Length_Z=[]
        self.matrix = [[0,1,2,3,4,5,6,7,8,9],[0,1,2,3,4,5,6,7,8,9],[0,1,2,3,4,5,6,7,8,9],[0,1,2,3,4,5,6,7,8,9],[0,1,2,3,4,5,6,7,8,9],[0,1,2,3,4,5,6,7,8,9],[0,1,2,3,4,5,6,7,8,9],[0,1,2,3,4,5,6,7,8,9],[0,1,2,3,4,5,6,7,8,9],[0,1,2,3,4,5,6,7,8,9]]
        self.blok = []
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
    def getFromLenght(self,lenght_b1,lenght_b2,length_b3):
         b1_coord = getCoord_location(1,lenght_b1)
         b2_coord = getCoord_location(2,lenght_b2)
         b3_coord = getCoord_location(3,lenght_b3)
    #     
    def doMatch(self,possibleCoord_b1,possibleCoord_b2,possibleCoord_b3):
         while coord_b1 in possi
         

    def getCoord_location(self,beakon_nr,lineair):
        dimensions = len(self.matrix)
        blok = fillBlok()
        
        x = 0
        y = 0
        z = 0
        
        if beakon_nr == 1:
           while x < len(blok):
              level = blok(x)
              while y < len(level):
                  element = level(y)
                     for value in element:
                     
        elif beakon_nr == 2:
           while x < len(blok):
              level = blok(x)
              while y < len(level):
                  element = level(y)
                     for value in element:
                     
        elif beakon_nr == 3:
           while x < len(blok):
              level = blok(x)
              while y < len(level):
                  element = level(y)
                     for value in element:
                     
    def fillBlok(self)
        i = 0
        blok = []
        while i < dimensions:
            blok.append(self.matrix)
            i = i + 1
        return blok
        
    def getLineair_lenght_beakon(self,beakon_nr,i,j,k)
        dimensions = len(self.matrix)
        if beakon_nr == 1:
           return math.sqrt(((i*i) + (j*j)) * (k*k))    
        if beakon_nr == 2:
           x = j
           y = dim - i
           z = k
           return math.sqrt(((x*x) + (y*y)) * (z*z))
        if beakon_nr == 3:
           x = dim - j
           y = i
           z = k
           return math.sqrt(((x*x) + (y*y)) * (z*z))
        		
##########################################################
#Created for manual testing of the methods on the class  #
##########################################################
def main():

    meInterfaceScript = clInterfaceScript()
    #Test the function manually
    meInterfaceScript.calculate_all()
    #To implement tolerances
    bestFitCor = meInterfaceScript.getFromLenght(8,8,8)
    print(bestFitCor)
    
if __name__ == "__main__":
    main()
