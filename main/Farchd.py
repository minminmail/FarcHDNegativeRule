# ***********************************************************************

# /**
#  * <p>Title: Farchd</p>
#  * <p>Description: It contains the implementation of the Farchd algorithm</p>
#  * <p>Company: KEEL </p>
#  * @author Written by Jesus Alcala (University of Granada) 09/02/2011

#  */

# **********************************************************************/
from DataBase import DataBase
from RuleBase import RuleBase
from MyDataSet import MyDataSet
import datetime

# * <p>It contains the implementation of the Chi algorithm</p>
# *
# * @author Written by Alberto Fern谩ndez (University of Granada) 02/11/2007
# * @version 1.0
# * @since JDK1.5

class Farchd:
    train_myDataSet = None
    val_myDataSet = None
    test_myDataSet = None

    outputTr = ""
    outputTst = ""

    fileDB = ""
    fileRB = ""
    fileTime = ""
    fileHora = ""
    data_string = ""
    fileRules = ""
    evolution = ""

    rulesStage1 = None
    rulesStage2 = None
    rulesStage3 = None

    dataBase = None
    ruleBase = None

    apriori = None

    population = None

    # algorithm parameters
    # int
    nLabels = None
    populationSize = None
    depth = None
    K_parameter = None
    maxTrials = None
    typeInference = None
    BITS_GEN = None
    double = None
    minsup = None
    minconf = None
    alpha = None

    # boolean
    somethingWrong = False  # to check if everything is correct.

    def __init__(self, parameters):
        print("__init__ of Fuzzy_Chi begin...")
        self.train_myDataSet = MyDataSet()
        self.val_myDataSet = MyDataSet()
        self.test_myDataSet = MyDataSet()
        self.startTime = datetime.datetime.now()

        try:
            self.fileToSavePath = parameters.file_path
            inputTrainingFile = parameters.getInputTrainingFiles()
            print("Reading the training set: "+ inputTrainingFile)
            self.train_myDataSet.readClassificationSet(inputTrainingFile, True, parameters.file_path)
            print("Reading the validation set: ")
            inputValidationFile = parameters.getValidationInputFile()
            self.train_myDataSet.readClassificationSet(inputTrainingFile, True, parameters.file_path)
            print("Reading the test set: ")
            self.test_myDataSet.readClassificationSet(parameters.getInputTestFiles(), False, parameters.file_path)
            print(" ********* test_myDataSet.myDataSet readClassificationSet finished !!!!!! *********")
        except IOError as ioError:
            print("I/O error: " + str(ioError))
            self.somethingWrong = True
        except Exception as e:
            print("Unexpected error:" + str(e))
            self.somethingWrong = True
        self.somethingWrong = self.somethingWrong or self.train_myDataSet.hasMissingAttributes()



    this.outputTr = parameters.getTrainingOutputFile();
    this.outputTst = parameters.getTestOutputFile();

    this.fileDB = parameters.getOutputFile(0);
    this.fileRB = parameters.getOutputFile(1);
    this.data = parameters.getTrainingInputFile();
    this.fileTime = (parameters.getOutputFile(1)).substring(0, (parameters.getOutputFile(1)).lastIndexOf(
        '/')) + "/time.txt";
    this.fileHora = (parameters.getOutputFile(1)).substring(0, (parameters.getOutputFile(1)).lastIndexOf(
        '/')) + "/hora.txt";
    this.fileRules = (parameters.getOutputFile(1)).substring(0, (parameters.getOutputFile(1)).lastIndexOf(
        '/')) + "/rules.txt";

    // Now
    we
    parse
    the
    parameters
    long
    seed = Long.parseLong(parameters.getParameter(0));

    this.nLabels = Integer.parseInt(parameters.getParameter(1));
    this.minsup = Double.parseDouble(parameters.getParameter(2));
    this.minconf = Double.parseDouble(parameters.getParameter(3));
    this.depth = Integer.parseInt(parameters.getParameter(4));
    this.K = Integer.parseInt(parameters.getParameter(5));
    this.maxTrials = Integer.parseInt(parameters.getParameter(6));
    this.populationSize = Integer.parseInt(parameters.getParameter(7));
    if (this.populationSize % 2 > 0)  this.populationSize++;
    this.alpha = Double.parseDouble(parameters.getParameter(8));
    this.BITS_GEN = Integer.parseInt(parameters.getParameter(9));
    this.typeInference = Integer.parseInt(parameters.getParameter(10));

    Randomize.setSeed(seed);

}



    self.outputTr = parameters.getTrainingOutputFile()
    print(" *********self.outputTr is  *********" + str(self.outputTr))
    self.outputTst = parameters.getTestOutputFile()
    print(" ********* self.outputTst *********" + str(self.outputTst))

    self.fileDB = parameters.getOutputFile(0)
    self.fileRB = parameters.getOutputFile(1)
    # Now we parse the parameters

    # self.nLabels = parameters.getParameter(0)
    self.nLabels = parameters.getParameter(0)
    print("nLabels is :" + str(self.nLabels))
    aux = str(parameters.getParameter(1)).lower()  # Computation of the compatibility degree
    print("parameter 1 aux is :" + str(aux))
    self.combinationType = self.PRODUCT
    if aux == "minimum":
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
        self.ruleBase = RuleBase()
        self.ruleBase.set_six_parameter_init(self.dataBase, self.inferenceType, self.combinationType,
                                             self.ruleWeight,
                                             self.train_myDataSet.getNames(), self.train_myDataSet.getClasses())

        print("Data Base:\n" + self.dataBase.printString())
        self.ruleBase.generation(self.train_myDataSet)
        # added by rui for negative rules
        self.ruleBase.generate_negative_rules(self.train_myDataSet, self.negative_confident_value)
        self.negative_rule_number = len(self.ruleBase.negative_rule_base_array)

        print("self.fileDB = " + str(self.fileDB))
        print("self.fileRB = " + str(self.fileRB))
        self.dataBase.writeFile(self.fileDB, "1", None)
        self.ruleBase.writeFile(self.fileRB)

        # Finally we should fill the training and test output files
        self.outputTr = self.fileToSavePath + "\\" + self.outputTr
        self.outputTst = self.fileToSavePath + "\\" + self.outputTst

        accTra = self.doOutput(self.val_myDataSet, self.outputTr, False)
        accTst = self.doOutput(self.test_myDataSet, self.outputTst, False)

        print("Accuracy for normal rules obtained in training: " + str(accTra))
        print("Accuracy for normal rules obtained in test: " + str(accTst))
        print("Normal rule Algorithm Finished")
        # 1. get the sub train myDataSet from negative rules
        self.granularity_database_array = [DataBase() for x in range(self.negative_rule_number)]
        self.granularity_rule_Base_array = [RuleBase() for x in range(self.negative_rule_number)]

        # from negative rule get small_disjunct_train array
        self.extract_small_disjunct_train_array_step_one(self.train_myDataSet)

        # need to get below 4 values:
        # self.train_myDataSet.getnInputs(), self.nLabels,
        # self.train_myDataSet.getRanges(), self.train_myDataSet.getNames()
        nVars = self.train_myDataSet.getnVars()
        nInputs = self.train_myDataSet.getnInputs()

        while self.more_granularity and self.negative_rule_number > 0:

            for i in range(0, self.negative_rule_number):
                # 2. for each sub train myDataSet, do self.granularity_data_base[i]= DataBase()
                self.granularity_database_array[i] = DataBase()
                # 3. self.granularity_data_base[i].setMultipleParameters(......)

                self.my_dataset_train_sub_zone[i].set_nVars(nVars)
                self.my_dataset_train_sub_zone[i].set_nInputs(nInputs)

                print("size of sub zone :" + str(self.my_dataset_train_sub_zone[i].size()))
                sub_x_array = self.my_dataset_train_sub_zone[i].get_x()
                self.granularity_database_array[i].setMultipleParameters(self.my_dataset_train_sub_zone[i].getnInputs(),
                                                                         self.nLabels,
                                                                         self.my_dataset_train_sub_zone[
                                                                             i].get_granularity_zone_ranges(
                                                                             sub_x_array),
                                                                         self.my_dataset_train_sub_zone[i].getNames())
                #  added by rui for granularity rules
                self.granularity_rule_Base_array[i] = RuleBase()

                # self.granularity_rule_Base_array[i].set_six_parameter_init(self.granularity_database_array[i],
                #
                #                                                            self.inferenceType, self.combinationType,
                #                                                            self.ruleWeight,
                #                                                            self.my_dataset_train_sub_zone[i].getNames(),
                #                                                            self.my_dataset_train_sub_zone[
                #                                                                i].getClasses())
                self.granularity_rule_Base_array[i].set_six_parameter_init(self.granularity_database_array[i],
                                                                           self.inferenceType, self.combinationType,
                                                                           self.ruleWeight,
                                                                           self.my_dataset_train_sub_zone[
                                                                               i].getNames(),
                                                                           self.my_dataset_train_sub_zone[
                                                                               i].getClasses())
            self.generate_granularity_rules()
            self.prunerules_granularity_rules()

            print("self.fileDB = " + str(self.fileDB))
            print("self.fileRB = " + str(self.fileRB))
            for i in range(0, self.negative_rule_number):
                self.granularity_database_array[i].writeFile(self.fileDB, "2", i)

            # Finally we should fill the training and test output files with granularity rule result

            accTra = self.doOutput(self.val_myDataSet, self.outputTr, True)
            accTst = self.doOutput(self.test_myDataSet, self.outputTst, True)
            print("Accuracy for granularity  rules obtained in training data is : " + str(accTra))
            print("Accuracy for granularity  rules obtained in test data is: " + str(accTst))
            # print("Accuracy for normal rules obtained in test: " + str(accTst))
            self.nLabels = int(self.nLabels) + 1
            # print(" self.nLabels after being added by one " + str(self.nLabels))
            self.decide_more_granularity_or_not()

    # """
    #    * It generates the output file from a given dataset and stores it in a file
    #    * @param dataset myDataset input dataset
    #    * @param filename String the name of the file
    #    *
    #    * @return The classification accuracy
    # """


def doOutput(self, dataset, filename, granularity_rule):
    try:
        output = ""
        hits = 0
        self.output = dataset.copyHeader()  # we insert the header in the output file
        # We write the output for each example
        # print("before loop in Fuzzy_Chi")
        data_number = dataset.getnData()
        print("in doOutput dataset.getnData()" + str(dataset.getnData()))
        for i in range(0, data_number):
            # print(" In the doOutput the loop number i is  " + str(i))
            # for classification:
            # print("before classificationOutput in Fuzzy_Chi")
            class_out_here = None
            if granularity_rule:
                for j in range(0, self.negative_rule_number):

                    # classOut = self.classification_Output_granularity(dataset.getExample(j), j)
                    classOut = self.classification_Output_pruned_granularity(dataset.getExample(i), j)
                    if classOut is not "?":
                        class_out_here = classOut

                if class_out_here is None:  #
                    classOut = self.classificationOutput(dataset.getExample(i))
                else:
                    classOut = class_out_here

            else:
                classOut = self.classificationOutput(dataset.getExample(i))

            # arrived here, print("before getOutputAsStringWithPos in Fuzzy_Chi")
            self.output = self.output + dataset.getOutputAsStringWithPos(i) + " " + classOut + "\n"
            # not arrive here, print("before getOutputAsStringWithPos in Fuzzy_Chi")
            if dataset.getOutputAsStringWithPos(i) == classOut:
                hits = hits + 1
        # print("before open file in Fuzzy_Chi")
        file = open(filename, "w+")
        file.write(output)
        file.close()
    except Exception as excep:
        print("There is exception in doOutput in Fuzzy chi class !!! The exception is :" + str(excep))
    if dataset.size() != 0:
        print(" in doOutput the hits is " + str(hits) + " ,the dataset.size() is " + str(dataset.size()))
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
        # print("In Fuzzy_Chi,classOut >= 0, to call getOutputValue")
        self.output = self.train_myDataSet.getOutputValue(classOut)
    return self.output


def classification_Output_granularity(self, example, zone_area_number):
    self.output = "?"
    # Here we should include the algorithm directives to generate the
    # classification output from the input example

    classOut = self.granularity_rule_Base_array[zone_area_number].FRM_Granularity(example)
    if classOut >= 0:
        # print("In Fuzzy_Chi,classOut >= 0, to call getOutputValue")
        self.output = self.my_dataset_train_sub_zone[zone_area_number].getOutputValue(classOut)
    return self.output


def classification_Output_pruned_granularity(self, example, zone_area_number):
    self.output = "?"
    # Here we should include the algorithm directives to generate the
    # classification output from the input example

    classOut = self.granularity_rule_Base_array[zone_area_number].FRM_Pruned_Granularity(example)
    if classOut >= 0:
        # print("In Fuzzy_Chi,classOut >= 0, to call getOutputValue")
        self.output = self.my_dataset_train_sub_zone[zone_area_number].getOutputValue(classOut)
    return self.output

    # added by rui for granularity rules


def generate_granularity_rules(self):
    # from negative rule get small_disjunct_train array
    # for each small disjunct train generate positive rules, save into priority rule base
    for i in range(0, self.negative_rule_number):
        sub_train_zone = self.my_dataset_train_sub_zone[i]
        self.generation_rule_step_two(sub_train_zone, sub_train_zone.size(), i)
    for i in range(0, self.negative_rule_number):
        print(" The loop i number is :" + str(i))
        self.granularity_rule_Base_array[i].write_File_for_granularity_rule(self.fileRB)

    # generate granularity rules

    # make the small disjunct label as L0S0 L0S1,L1S0,L1S1,

    # check accurate rate ,need to consider the granularity rules and positive rules


def extract_small_disjunct_train_array_step_one(self, train):
    self.negative_rule_number = len(self.ruleBase.negative_rule_base_array)
    x_array = [[] for x in range(self.negative_rule_number)]
    output_integer = [[] for x in range(train.size())]
    output = [[] for x in range(train.size())]
    train_x_array = train.get_x()
    # print("generate granularity rules begin :")
    data_row_number = len(self.ruleBase.data_row_array)

    for m in range(0, self.negative_rule_number):
        x_array[m] = []
        output_integer[m] = []
        output[m] = []
    self.my_dataset_train_sub_zone = [MyDataSet() for x in range(self.negative_rule_number)]

    for i in range(0, self.negative_rule_number):
        for dr in range(0, data_row_number):
            same_label_num = 0
            negative_rule_here = self.ruleBase.negative_rule_base_array[i]
            for j in range(0, self.ruleBase.n_labels):
                # print(" self.data_row_array[dr].label_values[j]" + str(self.ruleBase.data_row_array[dr].label_values[j]))
                # print(" negative_rule_here.antecedent[j]: " + str(negative_rule_here.antecedent[j].label))
                if self.ruleBase.data_row_array[dr].label_values[j] == negative_rule_here.antecedent[j].label:
                    same_label_num = same_label_num + 1
            if same_label_num == self.ruleBase.n_labels:
                # added the related __X in new sub zone train data set
                # print("train_x_array[dr]" + str(train_x_array[dr]))
                x_array[i].append(train_x_array[dr])
                output_integer[i].append(train.getOutputAsIntegerWithPos(dr))
                output[i].append(train.getOutputAsStringWithPos(dr))
        print(" output_integer length is： " + str(len(output_integer[i])))
        print(" x_array length is： " + str(len(x_array[i])))

    for k in range(0, self.negative_rule_number):
        print(" my_dataset_train_sub_zone[ " + str(k) + " ] :" + str(self.my_dataset_train_sub_zone[k]))
        num_sub_zone = len(x_array[k])
        # set my data set X array
        self.my_dataset_train_sub_zone[k].set_x(x_array[k])
        self.my_dataset_train_sub_zone[k].set_output_integer_array(output_integer[k])
        self.my_dataset_train_sub_zone[k].set_output_array(output[k])
        self.my_dataset_train_sub_zone[k].set_ndata(num_sub_zone)
        print("num_sub_zone " + str(k) + " is  :" + str(num_sub_zone))
        # set the rule base nClasses value
        # nclasses_number = self.my_dataset_train_sub_zone[k].calculate_nclasses_for_small_granularity_zone(output_integer[k])
        nclasses_number = self.nClasses
        print("nclasses_number of " + str(k) + " is  :" + str(nclasses_number))
        self.my_dataset_train_sub_zone[k].set_nClasses(nclasses_number)
        number_of_data = self.my_dataset_train_sub_zone[k].size()
        print(" The my_dataset_train_sub_zone " + str(k) + " number is :" + str(number_of_data))


def generation_rule_step_two(self, sub_train, sub_zone_number, area_number):
    print("In generation, the area_number is :" + str(area_number))
    print("In generation, the size of sub train is :" + str(sub_train.size()))
    for i in range(0, sub_train.size()):
        granularity_rule = self.granularity_rule_Base_array[area_number].searchForBestAntecedent(
            sub_train.getExample(i), sub_train.getOutputAsIntegerWithPos(i))
        self.granularity_data_row_array.append(granularity_rule.data_row_here)
        granularity_rule.assingConsequent(sub_train, self.ruleWeight)
        if not (self.granularity_rule_Base_array[area_number].duplicated_granularity_rule(granularity_rule)) and (
                granularity_rule.weight > self.granularity_confident_value):
            granularity_rule.granularity_sub_zone = sub_zone_number
            self.granularity_rule_Base_array[area_number].granularity_rule_Base.append(granularity_rule)

    print("The total granularity_data_row_array is " + str(len(self.granularity_data_row_array)))
    print(" In area_number " + str(area_number) + " ,The total granularity_rule_Base rule number is  : " + str(
        len(self.granularity_rule_Base_array[area_number].granularity_rule_Base)))


def prunerules_granularity_rules(self):
    for i in range(0, self.negative_rule_number):
        print("in prunerules_granularity_rules the i is: " + str(i))
        negative_rule = self.ruleBase.negative_rule_base_array[i]
        for j in range(0, len(self.granularity_rule_Base_array[i].granularity_rule_Base)):
            granularity_rule = self.granularity_rule_Base_array[i].granularity_rule_Base[j]

            if granularity_rule.weight > 0:
                # if negative_rule.class_value == granularity_rule.class_value:
                self.granularity_rule_Base_array[i].granularity_prune_rule_base.append(granularity_rule)
                print(" Added a new pruned granularity rule in  granularity_prune_rule_base, rule weight is :" + str(
                    granularity_rule.weight))
    for i in range(0, self.negative_rule_number):
        print(" The loop i number is :" + str(i))
        self.granularity_rule_Base_array[i].write_File_for_pruned_granularity_rule(self.fileRB)


def decide_more_granularity_or_not(self):
    # print("compare granularity rule and negative rule to see if negative granularity rule has been generated ")
    for i in range(0, self.negative_rule_number):
        negative_rule = self.ruleBase.negative_rule_base_array[i]
        for j in range(0, len(self.granularity_rule_Base_array[i].granularity_rule_Base)):
            granularity_rule = self.granularity_rule_Base_array[i].granularity_rule_Base[j]
            # print(" negative_rule.class_value" + str(negative_rule.class_value))
            # print(" granularity_rule.class_value" + str(granularity_rule.class_value))
            if negative_rule.class_value == granularity_rule.class_value:
                self.more_granularity = False
                # print(" Set the self.more_granularity = False")
                break
            if not self.more_granularity:
                break
        if not self.more_granularity:
            break
