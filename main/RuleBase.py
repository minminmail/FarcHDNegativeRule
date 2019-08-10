# /***********************************************************************
#
# 	This file is part of KEEL-software, the Data Mining tool for regression,
# 	classification, clustering, pattern mining and so on.
#
# 	Copyright (C) 2004-2010
#
# 	F. Herrera (herrera@decsai.ugr.es)
#     L. S谩nchez (luciano@uniovi.es)
#     J. Alcal谩-Fdez (jalcala@decsai.ugr.es)
#     S. Garc铆a (sglopez@ujaen.es)
#     A. Fern谩ndez (alberto.fernandez@ujaen.es)
#     J. Luengo (julianlm@decsai.ugr.es)
#
# 	This program is free software: you can redistribute it and/or modify
# 	it under the terms of the GNU General Public License as published by
# 	the Free Software Foundation, either version 3 of the License, or
# 	(at your option) any later version.
#
# 	This program is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# 	GNU General Public License for more details.
#
# 	You should have received a copy of the GNU General Public License
# 	along with this program.  If not, see http://www.gnu.org/licenses/
#
# **********************************************************************/
from Fuzzy import Fuzzy
from DataBase import DataBase
from Rule import Rule
import Fuzzy_Chi


# * This class contains the representation of a Rule Set
# *
# * @author Written by Alberto Fern谩ndez (University of Granada) 29/10/2007
# * @version 1.0
# * @since JDK1.5

class RuleBase:
    ruleBase = []
    dataBase = DataBase()
    n_variables = None
    n_labels = None
    ruleWeight = None
    inferenceType = None
    compatibilityType = None
    names = []
    classes = []

    # /**
    #  * Rule Base Constructor
    #  * @param dataBase DataBase the Data Base containing the fuzzy partitions
    #  * @param inferenceType int the inference type for the FRM
    #  * @param compatibilityType int the compatibility type for the t-norm
    #  * @param ruleWeight int the rule weight heuristic
    #  * @param names String[] the names for the features of the problem
    #  * @param classes String[] the labels for the class attributes
    #  */

    def __init__(self, dataBase, inferenceType, compatibilityType, ruleWeight, names, classes):
        print("RuleBase init begin...")
        self.ruleBase = []
        self.dataBase = dataBase
        self.n_variables = dataBase.numVariables()
        self.n_labels = dataBase.numLabels()
        self.inferenceType = inferenceType
        self.compatibilityType = compatibilityType
        self.ruleWeight = ruleWeight
        self.names = names
        self.classes = classes

    # * It checks if a specific rule is already in the rule base
    # * @param r Rule the rule for comparison
    # * @return boolean true if the rule is already in the rule base, false in other case

    def duplicated(self, rule):
        i = 0
        found = False
        while (i < len(self.ruleBase)) and (not found):
            found = self.ruleBase[i].comparison(rule)
            i = i + 1
        return found

    # * Rule Learning Mechanism for the Chi et al.'s method
    # * @param train myDataset the training data-set

    def Generation(self, train):
        print("In Generation, the size of train is :" + str(train.size()))
        for i in range(0, train.size()):
            rule = self.searchForBestAntecedent(train.getExample(i), train.getOutputAsIntegerWithPos(i))
            rule.assingConsequent(train, self.ruleWeight)
            if not (self.duplicated(rule)) and (rule.weight > 0):
                self.ruleBase.append(rule)

    # * This function obtains the best fuzzy label for each variable of the example and assigns
    # * it to the rule
    # * @param example double[] the input example
    # * @param clas int the class of the input example
    # * @return Rule the fuzzy rule with the highest membership degree with the example

    def searchForBestAntecedent(self, example, clas):
        ruleInstance = Rule()
        ruleInstance.setTwoParameters(self.n_variables, self.compatibilityType)
        print("In searchForBestAntecedent ,self.n_variables is :" + str(self.n_variables))
        ruleInstance.setClass(clas)
        print("In searchForBestAntecedent ,self.n_labels is :" + str(self.n_labels))
        for i in range(0, self.n_variables):
            max_value = 0.0
            etq = -1
            per = None
            for j in range(0, self.n_labels):
                print("Inside the second loop of searchForBestAntecedent......")
                per = self.dataBase.membershipFunction(i, j, example[i])
                if per > max_value:
                    max_value = per
                    etq = j
            if max_value == 0.0:
                print("There was an Error while searching for the antecedent of the rule")
                print("Example: ")
                for j in range(0, self.n_variables):
                    print(example[j] + "\t")

                print("Variable " + str(i))
                exit(1)

            ruleInstance.antecedent[i] = self.dataBase.clone(i, etq)
        return ruleInstance

    # * It prints the rule base into an string
    # * @return String an string containing the rule base

    def printString(self):
        i = None
        j = None
        cadena_string = ""
        cadena_string += "@Number of rules: " + str(len(self.ruleBase)) + "\n\n"
        for i in range(0, len(self.ruleBase)):
            rule = self.ruleBase[i]
            cadena_string += str(i + 1) + ": "
            for j in range(0, self.n_variables - 1):
                cadena_string += self.names[j] + " IS " + rule.antecedent[j].name + " AND "
            j = j + 1
            cadena_string += self.names[j] + " IS " + rule.antecedent[j].name + ": " + str(
                self.classes[rule.clas]) + " with Rule Weight: " + str(rule.weight) + "\n"
        print("RuleBase cadena_string is:" + cadena_string)
        return cadena_string

    # * It writes the rule base into an ouput file
    # * @param filename String the name of the output file

    def writeFile(self, filename):
        outputString = ""
        outputString = self.printString()
        file = open(filename, "w")
        file.write(outputString)
        file.close()

    # * Fuzzy Reasoning Method
    # * @param example double[] the input example
    # * @return int the predicted class label (id)

    def FRM(self, example):
        if self.inferenceType == Fuzzy_Chi.Fuzzy_Chi.WINNING_RULE:
            return self.FRM_WR(example)
        else:
            return self.FRM_AC(example)

    # * Winning Rule FRM
    # * @param example double[] the input example
    # * @return int the class label for the rule with highest membership degree to the example
    def FRM_WR(self, example):
        class_value = -1
        max_value = 0.0
        for i in range(0, len(self.ruleBase)):
            rule = self.ruleBase[i]
            produc = rule.compatibility(example)
            produc *= rule.weight
            if produc > max_value:
                max_value = produc
                class_value = rule.clas
        return class_value

    # * Additive Combination FRM
    # * @param example double[] the input example
    # * @return int the class label for the set of rules with the highest sum of membership degree per class

    def FRM_AC(self, example):
        class_value = -1
        class_degrees = []
        for i in range(0, len(self.ruleBase)):
            rule = self.ruleBase[i]
            produc = rule.compatibility(example)
            produc *= rule.weight
            if rule.clas > (len(class_degrees) - 1):
                aux = [0.0 for x in range(len(class_degrees))]
                for j in range(0, len(aux)):
                    aux[j] = class_degrees[j]

                class_degrees = [0.0 for x in range(rule.clas + 1)]
                for j in range(0, len(aux)):
                    class_degrees[j] = aux[j]

            class_degrees[rule.clas] += produc

        max_value = 0.0
        for l in range(0, len(class_degrees)):
            if class_degrees[l] > max_value:
                max_value = class_degrees[l]
                class_value = l

        return class_value
