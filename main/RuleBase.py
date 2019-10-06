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
from data_row import data_row
from MyDataSet import MyDataSet


# * This class contains the representation of a Rule Set
# *
# * @author Written by Alberto Fern谩ndez (University of Granada) 29/10/2007
# * @version 1.0
# * @since JDK1.5

class RuleBase:
    ruleBase = []
    # added by rui for negative rule
    negative_rule_base_array = []
    dataBase = DataBase()
    n_variables = None
    n_labels = None
    ruleWeight = None
    inferenceType = None
    compatibilityType = None
    names = []
    classes = []
    data_row_array = []
    granularity_data_row_array = []
    my_data_set_train_sub_zone = []

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
        self.granularity_rule_Base = []
        # added by rui for negative rule
        self.negative_rule_base_array = []
        self.dataBase = dataBase
        self.n_variables = dataBase.numVariables()
        self.n_labels = dataBase.numLabels()
        self.inferenceType = inferenceType
        self.compatibilityType = compatibilityType
        self.ruleWeight = ruleWeight
        self.names = names
        self.classes = classes
        self.data_row_array = []
        self.granularity_data_row_array = []

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

    def duplicated_granularity_rule(self, rule):
        i = 0
        found = False
        while (i < len(self.granularity_rule_Base)) and (not found):
            found = self.granularity_rule_Base[i].comparison(rule)
            i = i + 1
        return found

    def duplicated_negative_rule(self, rule):
        i = 0
        found = False
        while (i < len(self.negative_rule_base_array)) and (not found):
            found = self.negative_rule_base_array[i].comparison(rule)
            i = i + 1
        return found

    # * Rule Learning Mechanism for the Chi et al.'s method
    # * @param train myDataset the training data-set

    def generation(self, train):
        print("In generation, the size of train is :" + str(train.size()))
        for i in range(0, train.size()):
            rule = self.searchForBestAntecedent(train.getExample(i), train.getOutputAsIntegerWithPos(i))
            self.data_row_array.append(rule.data_row_here)
            rule.assingConsequent(train, self.ruleWeight)
            if not (self.duplicated(rule)) and (rule.weight > 0):
                self.ruleBase.append(rule)
        print("The total data_row is " + str(len(self.data_row_array)))

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
        example_feature_array = []
        for f_variable in range(0, self.n_variables):
            example_feature_array.append(example[f_variable])
        label_array = []

        for i in range(0, self.n_variables):
            max_value = 0.0
            etq = -1
            per = None
            for j in range(0, self.n_labels):
                # print("Inside the second loop of searchForBestAntecedent......")
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
            print(" The max_value is : " + str(max_value))
            print(" ,the j value is : " + str(j))
            ruleInstance.antecedent[i] = self.dataBase.clone(i, etq)  # self.dataBase[i][j]
            label_array.append(etq)
        data_row_temp = data_row()
        data_row_temp.set_three_parameters(clas, example_feature_array, label_array)
        ruleInstance.data_row_here = data_row_temp

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
                self.classes[rule.class_value]) + " with Rule Weight: " + str(rule.weight) + "\n"
        print("RuleBase cadena_string is:" + cadena_string)

        # added negative rule print into file

        cadena_string += "@Number of negative rules: " + str(len(self.negative_rule_base_array)) + "\n\n"
        for i in range(0, len(self.negative_rule_base_array)):
            negative_rule = self.negative_rule_base_array[i]
            cadena_string += str(i + 1) + ": "
            for j in range(0, self.n_variables - 1):
                cadena_string += self.names[j] + " IS " + negative_rule.antecedent[j].name + " AND "
            j = j + 1
            cadena_string += self.names[j] + " IS " + negative_rule.antecedent[j].name + ": " + str(
                self.classes[negative_rule.class_value]) + " with Rule Weight: " + str(negative_rule.weight) + "\n"

            # added for granularity rules

            cadena_string += "@Number of granularity rules: " + str(len(self.granularity_rule_Base)) + "\n\n"
            for i in range(0, len(self.granularity_rule_Base)):
                granularity_rule = self.granularity_rule_Base[i]
                cadena_string += str(i + 1) + ": "
                for j in range(0, self.n_variables - 1):
                    cadena_string += self.names[j] + " IS " + granularity_rule.antecedent[j].name + " AND "
                j = j + 1
                cadena_string += self.names[j] + " IS " + granularity_rule.antecedent[j].name + ": " + str(
                    self.classes[granularity_rule.class_value]) + " with Rule Weight: " + str(granularity_rule.weight) + "\n"

        return cadena_string

    # * It writes the rule base into an ouput file
    # * @param filename String the name of the output file

    def writeFile(self, filename):
        print("rule string to save is: " + self.printString())
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
                class_value = rule.class_value
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
            if rule.class_value > (len(class_degrees) - 1):
                aux = [0.0 for x in range(len(class_degrees))]
                for j in range(0, len(aux)):
                    aux[j] = class_degrees[j]

                class_degrees = [0.0 for x in range(rule.clas + 1)]
                for j in range(0, len(aux)):
                    class_degrees[j] = aux[j]

            class_degrees[rule.class_value] += produc

        max_value = 0.0
        for l in range(0, len(class_degrees)):
            if class_degrees[l] > max_value:
                max_value = class_degrees[l]
                class_value = l

        return class_value

    # added by rui for negative  rules
    def generate_negative_rules(self, train, confident_value_pass):
        confident_value = 0
        class_value_arr = self.get_class_value_array(train)
        for i in range(0, len(self.ruleBase)):
            rule_negative = Rule()
            rule_negative.antecedent = self.ruleBase[i].antecedent
            positive_rule_class_value = self.ruleBase[i].get_class()
            rule_negative.setClass(positive_rule_class_value)

            for j in range(0, len(class_value_arr)):
                class_type = int(class_value_arr[j])
                if positive_rule_class_value != class_type:  # need to get another class value for negative rule

                    rule_negative.setClass(class_type)  # change the class type in the rule
                    confident_value = rule_negative.calculate_confident(self.data_row_array)

                    if confident_value >= confident_value_pass:
                        rule_negative.weight = confident_value
                        if not (self.duplicated_negative_rule(rule_negative)):

                            for k in range(0, len(rule_negative.antecedent)):
                                print("antecedent L_ " + str(rule_negative.antecedent[j].label))
                            print("class value " + str(rule_negative.get_class()))
                            print(" weight  " + str(rule_negative.weight))

                            print("positive_rule_class_value" + str(positive_rule_class_value))
                            print("class_type" + str(class_type))
                            self.negative_rule_base_array.append(rule_negative)

    def get_class_value_array(self, train):
        class_value_array = []
        integer_array = train.getOutputAsInteger()
        for i in range(0, len(integer_array)):
            exist_yes = False
            for j in range(0, len(class_value_array)):
                if integer_array[i] == class_value_array[j]:
                    exist_yes = True
            if not exist_yes:
                class_value_array.append(integer_array[i])
        return class_value_array

    # added by rui for granularity rules
    def generate_granularity_rules_all_steps(self, train):
        # from negative rule get small_disjunct_train array
        self.extract_small_disjunct_train_array_step_one(train)
        # for each small disjunct train generate positive rules, save into priority rule base
        negative_rule_num = len(self.negative_rule_base_array)
        for i in range(0, negative_rule_num):
            sub_train_zone = self.my_data_set_train_sub_zone[i]
            self.generation_rule_step_two(sub_train_zone)

        # generate granularity rules


        # make the small disjunct label as L0S0 L0S1,L1S0,L1S1,

        # check accurate rate ,need to consider the granularity rules and positive rules

    def extract_small_disjunct_train_array_step_one(self, train):
        negative_rule_num = len(self.negative_rule_base_array)
        x_array = [[] for x in range(negative_rule_num)]
        output_integer = [[] for x in range(train.size())]
        train_x_array = train.get_x()
        # print("generate granularity rules begin :")
        data_row_number = len(self.data_row_array)

        for m in range(0, negative_rule_num):
            x_array[m] = []
            output_integer[m] = []
        self.my_data_set_train_sub_zone = [MyDataSet() for x in range(negative_rule_num)]

        for i in range(0, negative_rule_num):
            for dr in range(0, data_row_number):
                same_label_num = 0
                negative_rule_here = self.negative_rule_base_array[i]
                for j in range(0, self.n_labels):
                    print(" self.data_row_array[dr].label_values[j]" + str(self.data_row_array[dr].label_values[j]))
                    print(" negative_rule_here.antecedent[j]: " + str(negative_rule_here.antecedent[j].label))
                    if self.data_row_array[dr].label_values[j] == negative_rule_here.antecedent[j].label:
                        same_label_num = same_label_num + 1
                if same_label_num == self.n_labels:
                    # added the related __X in new sub zone train data set
                    print("train_x_array[dr]" + str(train_x_array[dr]))
                    x_array[i].append(train_x_array[dr])
                    output_integer[i].append(train.getOutputAsIntegerWithPos(dr))
            print(" output_integer length is " + str(len(output_integer[i])))

        for k in range(0, negative_rule_num):
            print(" my_data_set_train_sub_zone[ " + str(k) + " ] :" + str(self.my_data_set_train_sub_zone[k]))
            num_sub_zone = len(x_array[k])
            # set my data set X array
            self.my_data_set_train_sub_zone[k].set_x(x_array[k])
            self.my_data_set_train_sub_zone[k].set_output_integer_array(output_integer[k])
            self.my_data_set_train_sub_zone[k].set_ndata(num_sub_zone)
            print("num_sub_zone " + str(k) + " is  :" + str(num_sub_zone))
            # set the rule base nClasses value
            nclasses_number = self.my_data_set_train_sub_zone[k].calculate_nclasses_for_small_granularity_zone(output_integer[k])
            print("nclasses_number of " + str(k) + " is  :" + str(nclasses_number))
            self.my_data_set_train_sub_zone[k].set_nClasses(nclasses_number)


    def generation_rule_step_two(self, train):
        print("In generation, the size of train is :" + str(train.size()))
        for i in range(0, train.size()):
            granularity_rule = self.searchForBestAntecedent(train.getExample(i), train.getOutputAsIntegerWithPos(i))
            self.granularity_data_row_array.append(granularity_rule.data_row_here)
            granularity_rule.assingConsequent(train, self.ruleWeight)
            if not (self.duplicated_granularity_rule(granularity_rule)) and (granularity_rule.weight > 0):
                self.granularity_rule_Base.append(granularity_rule)
        print("The total granularity_data_row_array is " + str(len(self.granularity_data_row_array)))
        print("The total granularity_rule_Base has : " + str(len(self.granularity_rule_Base)))
