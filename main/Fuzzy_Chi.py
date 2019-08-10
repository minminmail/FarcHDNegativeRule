# ***********************************************************************

# This file is part of KEEL-software, the Data Mining tool for regression,
# classification, clustering, pattern mining and so on.
#
# Copyright (C) 2004-2010
#
# F. Herrera (herrera@decsai.ugr.es)
# L. S谩nchez (luciano@uniovi.es)
# J. Alcal谩-Fdez (jalcala@decsai.ugr.es)
# S. Garc铆a (sglopez@ujaen.es)
# A. Fern谩ndez (alberto.fernandez@ujaen.es)
# J. Luengo (julianlm@decsai.ugr.es)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/

# **********************************************************************/
from DataBase import DataBase
from RuleBase import RuleBase
from MyDataSet import MyDataSet


# * <p>It contains the implementation of the Chi algorithm</p>
# *
# * @author Written by Alberto Fern谩ndez (University of Granada) 02/11/2007
# * @version 1.0
# * @since JDK1.5

class Fuzzy_Chi:
    train_myDataSet = None
    val_myDataSet = None
    test_myDataSet = None
    outputTr = ""
    outputTst = ""
    fileDB = ""
    fileRB = ""
    nClasses = None
    nLabels = None
    combinationType = None
    inferenceType = None
    ruleWeight = None
    dataBase = None
    ruleBase = None

    # Configuration flags.
    MINIMUM = 0
    # Configuration flags.
    PRODUCT = 1
    #  Configuration flags.
    CF = 0
    # Configuration flags.
    PCF_IV = 1
    #  Configuration flags.
    # MCF = 2
    # Configuration flags.
    NO_RW = 3
    # Configuration flags.
    PCF_II = 3
    #  Configuration flags.
    WINNING_RULE = 0
    #  Configuration flags.
    ADDITIVE_COMBINATION = 1
    # We may declare here the algorithm's parameters
    somethingWrong = False  # to check if everything is correct.

    #  Default constructor

    # * It reads the data from the input files (training, validation and test) and parse all the parameters
    # * from the parameters array.
    # * @param parameters parseParameters It contains the input files, output files and parameters

    def __init__(self, parameters):
        print("__init__ of Fuzzy_Chi begin...")
        self.train_myDataSet = MyDataSet()
        self.val_myDataSet = MyDataSet()
        self.test_myDataSet = MyDataSet()
        try:
            print("Reading the training set: ")
            inputTrainingFile = parameters.getInputTrainingFiles()
            print("In Fuzzy Chi init method the training file is :" + inputTrainingFile)
            self.train_myDataSet.readClassificationSet(inputTrainingFile, True)
            print(" ********* train_myDataSet.myDataSet readClassificationSet finished !!!!!! *********")

            print("Reading the validation set: ")
            inputValidationFile = parameters.getValidationInputFile()
            self.val_myDataSet.readClassificationSet(inputValidationFile, False)
            print(" ********* val_myDataSet.myDataSet readClassificationSet finished !!!!!! *********")

            print("Reading the test set: ")
            self.test_myDataSet.readClassificationSet(parameters.getInputTestFiles(), False)
            print(" ********* test_myDataSet.myDataSet readClassificationSet finished !!!!!! *********")

        except IOError as ioError:
            print("I/O error: " + str(ioError))
            self.somethingWrong = True
        except Exception as e:
            print("Unexpected error:" + str(e))
            self.somethingWrong = True
        #
        #     #We may check if there are some numerical attributes, because our algorithm may not handle them:
        #     #somethingWrong = somethingWrong || train.hasNumericalAttributes();
        print(" ********* Three type of myDataSet readClassificationSet finished !!!!!! *********")
        self.somethingWrong = self.somethingWrong or self.train_myDataSet.hasMissingAttributes()

        self.outputTr = parameters.getTrainingOutputFile()
        self.outputTst = parameters.getTestOutputFile()

        self.fileDB = parameters.getOutputFile(0)
        self.fileRB = parameters.getOutputFile(1)
        # Now we parse the parameters

        # self.nLabels = parameters.getParameter(0)
        self.nLabels = parameters.getParameter(0)
        print("nLabels is :" + str(self.nLabels))
        aux = str(parameters.getParameter(1)).lower()  # Computation of the compatibility degree
        print("parameter 1 aux is :" + str(aux))
        self.combinationType = self.PRODUCT
        if (aux == "minimum"):
            self.combinationType = self.MINIMUM
        aux = str(parameters.getParameter(2)).lower()
        print("parameter 2 aux is :" + str(aux))
        self.ruleWeight = self.PCF_IV
        if aux == "Certainty_Factor".lower():
            self.ruleWeight = self.CF
        elif aux == "Average_Penalized_Certainty_Factor".lower():
            self.ruleWeight = self.PCF_II
        elif aux == "No_Weights".lower():
            self.ruleWeight = self.NO_RW
        aux = str(parameters.getParameter(3)).lower()
        print("parameter 3 aux is :" + str(aux))
        self.inferenceType = self.WINNING_RULE
        if aux == "Additive_Combination".lower():
            self.inferenceType = self.ADDITIVE_COMBINATION

            # It launches the algorithm

    def execute(self):
        if self.somethingWrong:  # We do not execute the program
            print("An error was found, the data-set have missing values")
            print("Please remove those values before the execution")
            print("Aborting the program")
            # We should not use the statement: System.exit(-1);
        else:
            # We do here the algorithm's operations
            print("No errors, Execute in Fuzzy Chi execute :")
            self.nClasses = self.train_myDataSet.getnClasses()
            self.dataBase = DataBase()
            self.dataBase.setMultipleParameters(self.train_myDataSet.getnInputs(), self.nLabels,
                                                self.train_myDataSet.getRanges(), self.train_myDataSet.getNames())
            print("DataBase object has been created......")
            self.ruleBase = RuleBase(self.dataBase, self.inferenceType, self.combinationType, self.ruleWeight,
                                     self.train_myDataSet.getNames(), self.train_myDataSet.getClasses())

            print("Data Base:\n" + self.dataBase.printString())
            self.ruleBase.Generation(self.train_myDataSet)

            print("self.fileDB = " + str(self.fileDB))
            print("self.fileRB = " + str(self.fileRB))
            self.dataBase.writeFile(self.fileDB)
            self.ruleBase.writeFile(self.fileRB)

            # Finally we should fill the training and test output files
            accTra = self.doOutput(self.val_myDataSet, self.outputTr)
            accTst = self.doOutput(self.test_myDataSet, self.outputTst)

            print("Accuracy obtained in training: " + str(accTra))
            print("Accuracy obtained in test: " + str(accTst))
            print("Algorithm Finished")

    # """
    #    * It generates the output file from a given dataset and stores it in a file
    #    * @param dataset myDataset input dataset
    #    * @param filename String the name of the file
    #    *
    #    * @return The classification accuracy
    # """
    def doOutput(self, dataset, filename):
        try:
            output = ""
            hits = 0
            self.output = dataset.copyHeader()  # we insert the header in the output file
            # We write the output for each example
            print("before loop in Fuzzy_Chi")
            print("dataset.getnData()" + str(dataset.getnData()))
            for i in range(0, dataset.getnData()):
                # for classification:
                print("before classificationOutput in Fuzzy_Chi")
                classOut = self.classificationOutput(dataset.getExample(i))
                print("before getOutputAsStringWithPos in Fuzzy_Chi")
                self.output = self.output + dataset.getOutputAsStringWithPos(i) + " " + classOut + "\n"
                print("before getOutputAsStringWithPos in Fuzzy_Chi")
                if (dataset.getOutputAsStringWithPos(i) == classOut):
                    hits = hits + 1
            print("before open file in Fuzzy_Chi")
            file = open(filename, "w")
            file.write(output)
            file.close()
        except Exception as excep:
            print("There is exception in doOutput in Fuzzy chi class !!! The exception is :" + str(excep))
        if dataset.size() != 0:
            return 1.0 * hits / dataset.size()
        else:
            return 0

        # * It returns the algorithm classification output given an input example
        # * @param example double[] The input example
        # * @return String the output generated by the algorithm

    def classificationOutput(self, example):
        self.output = "?"
        # Here we should include the algorithm directives to generate the
        # classification output from the input example
        classOut = self.ruleBase.FRM(example)
        if classOut >= 0:
            print("In Fuzzy_Chi,classOut >= 0, to call getOutputValue")
            self.output = self.train_myDataSet.getOutputValue(classOut)
        return self.output
