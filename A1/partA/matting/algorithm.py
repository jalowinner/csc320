## CSC320 Winter 2017 
## Assignment 1
## (c) Kyros Kutulakos
##
## DISTRIBUTION OF THIS CODE ANY FORM (ELECTRONIC OR OTHERWISE,
## AS-IS, MODIFIED OR IN PART), WITHOUT PRIOR WRITTEN AUTHORIZATION 
## BY THE INSTRUCTOR IS STRICTLY PROHIBITED. VIOLATION OF THIS 
## POLICY WILL BE CONSIDERED AN ACT OF ACADEMIC DISHONESTY

##
## DO NOT MODIFY THIS FILE ANYWHERE EXCEPT WHERE INDICATED
##

# import basic packages
import numpy as np
import scipy.linalg as sp
import cv2 as cv

# If you wish to import any additional modules
# or define other utility functions, 
# include them here

#########################################
## PLACE YOUR CODE BETWEEN THESE LINES ##
#########################################


#########################################

#
# The Matting Class
#
# This class contains all methods required for implementing 
# triangulation matting and image compositing. Description of
# the individual methods is given below.
#
# To run triangulation matting you must create an instance
# of this class. See function run() in file run.py for an
# example of how it is called
#
class Matting:
    #
    # The class constructor
    #
    # When called, it creates a private dictionary object that acts as a container
    # for all input and all output images of the triangulation matting and compositing 
    # algorithms. These images are initialized to None and populated/accessed by 
    # calling the the readImage(), writeImage(), useTriangulationResults() methods.
    # See function run() in run.py for examples of their usage.
    #
    def __init__(self):
        self._images = { 
            'backA': None, 
            'backB': None, 
            'compA': None, 
            'compB': None, 
            'colOut': None,
            'alphaOut': None, 
            'backIn': None, 
            'colIn': None, 
            'alphaIn': None, 
            'compOut': None, 
        }

    # Return a dictionary containing the input arguments of the
    # triangulation matting algorithm, along with a brief explanation
    # and a default filename (or None)
    # This dictionary is used to create the command-line arguments
    # required by the algorithm. See the parseArguments() function
    # run.py for examples of its usage
    def mattingInput(self): 
        return {
            'backA':{'msg':'Image filename for Background A Color','default':None},
            'backB':{'msg':'Image filename for Background B Color','default':None},
            'compA':{'msg':'Image filename for Composite A Color','default':None},
            'compB':{'msg':'Image filename for Composite B Color','default':None},
        }
    # Same as above, but for the output arguments
    def mattingOutput(self): 
        return {
            'colOut':{'msg':'Image filename for Object Color','default':['color.tif']},
            'alphaOut':{'msg':'Image filename for Object Alpha','default':['alpha.tif']}
        }
    def compositingInput(self):
        return {
            'colIn':{'msg':'Image filename for Object Color','default':None},
            'alphaIn':{'msg':'Image filename for Object Alpha','default':None},
            'backIn':{'msg':'Image filename for Background Color','default':None},
        }
    def compositingOutput(self):
        return {
            'compOut':{'msg':'Image filename for Composite Color','default':['comp.tif']},
        }
    
    # Copy the output of the triangulation matting algorithm (i.e., the 
    # object Color and object Alpha images) to the images holding the input
    # to the compositing algorithm. This way we can do compositing right after
    # triangulation matting without having to save the object Color and object
    # Alpha images to disk. This routine is NOT used for partA of the assignment.
    def useTriangulationResults(self):
        if (self._images['colOut'] is not None) and (self._images['alphaOut'] is not None):
            self._images['colIn'] = self._images['colOut'].copy()
            self._images['alphaIn'] = self._images['alphaOut'].copy()

    # If you wish to create additional methods for the 
    # Matting class, include them here

    #########################################
    ## PLACE YOUR CODE BETWEEN THESE LINES ##
    #########################################

    #########################################
            
    # Use OpenCV to read an image from a file and copy its contents to the 
    # matting instance's private dictionary object. The key 
    # specifies the image variable and should be one of the
    # strings in lines 54-63. See run() in run.py for examples
    #
    # The routine should return True if it succeeded. If it did not, it should
    # leave the matting instance's dictionary entry unaffected and return
    # False, along with an error message
    def readImage(self, fileName, key):
        success = False
        msg = 'Placeholder'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        if (self._images[key] is None):
            msg = "wrong key"
        else:
            try:
                self._images[key] = cv.imread(filename)
                success = True
            except IOError:
                msg = "wrong filename"
                success = False
        #########################################
        return success, msg

    # Use OpenCV to write to a file an image that is contained in the 
    # instance's private dictionary. The key specifies the which image
    # should be written and should be one of the strings in lines 54-63. 
    # See run() in run.py for usage examples
    #
    # The routine should return True if it succeeded. If it did not, it should
    # return False, along with an error message
    def writeImage(self, fileName, key):
        success = False
        msg = 'Placeholder'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        if (self._images[key] is None):
            msg = "wrong key"
        else:
            try:
                self._images[key] = cv.imwrite(filename)
                success = True
            except IOError:
                msg = "wrong filename"
                success = False

        #########################################
        return success, msg

    # Method implementing the triangulation matting algorithm. The
    # method takes its inputs/outputs from the method's private dictionary 
    # ojbect. 
    def triangulationMatting(self):
        """
success, errorMessage = triangulationMatting(self)
        
        Perform triangulation matting. Returns True if successful (ie.
        all inputs and outputs are valid) and False if not. When success=False
        an explanatory error message should be returned.
        """

        success = False
        msg = 'Placeholder'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        backA = self._images['backA']
        backB = self._images['backB']
        compA = self._images['compA']
        compB = self._images['compB'] 

        if ((backA is not None) and (backB is not None) and (compA is not None) and (compB is not None)):
            if ((backA.shape == backB.shape) and (backA.shape == compA.shape) and (backA.shape == compB.shape)):
                self._images['colOut'] = np.zeros([backA.shape[0], backA.shape[1], 3])
                self._images['alphaOut'] = np.zeros([backA.shape[0], backA.shape[1]])
                for i in range(backA.shape[0]):
                    for j in range(backA.shape[1]):
                        deltaA = compA - backA
                        deltaB = compB - backB
                        delta = np.concatenate((deltaA, deltaB), axis = 0)
                        identity = np.identity(3)
                        twoIdentities = np.concatenate((identity, identity), axis = 0)
                        comps = np.concatentate(((-1)*compA, (-1)*compB), axis = 0)
                        A = np.concatentate((twoIdentities, comps.T), axis = 1)
                        x = np.dot(np.linalg.pinv(A), delta.T)
                        self._images['colOut'][i, j] = np.clip(x[0:3], 0.0, 255.0)
                        #if(x[3] <= 0.0):
                            #self._images['alphaOut'][i, j] = 0.0
                        #else if(x[3] > 1.0):
                            #self._images['alphaOut'][i, j] = 255.0
                        #else:
                            #self._images['alphaOut'][i, j] = x[3] * 255.0
                success = True
        else:
            success = False
            msg = "source error"
        #########################################

        return success, msg

        
    def createComposite(self):
        """
success, errorMessage = createComposite(self)
        
        Perform compositing. Returns True if successful (ie.
        all inputs and outputs are valid) and False if not. When success=False
        an explanatory error message should be returned.
"""

        success = False
        msg = 'Placeholder'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################

        #########################################

        return success, msg


