import pandas as pd
import numpy as np
import timeit
from pm4py.objects.log.importer.xes import importer
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
from pm4py.algo.filtering.log.variants import variants_filter
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.evaluation.replay_fitness import evaluator as replay_fitness_evaluator
from pm4py.evaluation.precision import evaluator as precision_evaluator
from pm4py.evaluation.generalization import evaluator as generalization_evaluator
from pm4py.evaluation.simplicity import evaluator as simplicity_evaluator


def log_statistics(logpath):
    """
    Extracts log statistics such as #Events, #Cases, #Activities and #Variants, given the path of event log.

    Parameters:
        logpath (str): Path of event log

    Returns:
        events (int): Number of events
        cases (int): Number of traces
        activities (int): Number of activities
        variants (int): Number of variants
    """
    log = importer.apply(logpath)
    log_df = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)
    return len(log_df), log_df["case:concept:name"].nunique(), log_df["concept:name"].nunique(), len(variants_filter.get_variants(log))


def attribute_details(logpath):
    """
    Extracts all attribute values and segregate into list of numeric and string type attributes, given the path of event log.

    Parameters:
        logpath (str): Path of event log

    Returns:
        num_attr (List of int): List of attributes of type numeric
        str_attr (List of str): List of attributes of type string
    """
    xes_log = importer.apply(logpath)
    log_df = log_converter.apply(xes_log, variant=log_converter.Variants.TO_DATA_FRAME)
    log_df.drop(["concept:name", "time:timestamp", "case:concept:name"], axis=1, inplace=True, errors='ignore')
    num_attr = []
    str_attr = []

    for attr in log_df.columns:
        if log_df.dtypes[attr] == "float64":
            num_attr.append(attr)
        else:
            if log_df.dtypes[attr] != "datetime64[ns]":
                str_attr.append(attr)

    return num_attr, str_attr


def evaluate_logwithmodel(logpath):
    """
    Calculate and return evaluation measurements like fitness, precision, simplicity and generalization, given the path
    of event log.

    Parameters:
        logpath (str): Path of event log

    Returns:
        fitness (float): Fitness value measured using pm4py
        precision (float): Precision value measured using pm4py
        simplicity (float): Simplicity value measured using pm4py
        generalization (float): Generalization value measured using pm4py
    """
    xes_log = importer.apply(logpath)
    net, initial_marking, final_marking = inductive_miner.apply(xes_log)

    fitness = replay_fitness_evaluator.apply(xes_log, net, initial_marking, final_marking,
                                             variant=replay_fitness_evaluator.Variants.TOKEN_BASED)
    prec = precision_evaluator.apply(xes_log, net, initial_marking, final_marking,
                                     variant=precision_evaluator.Variants.ETCONFORMANCE_TOKEN)
    simp = simplicity_evaluator.apply(net)
    gen = generalization_evaluator.apply(xes_log, net, initial_marking, final_marking)

    return round(fitness['log_fitness'], 3), round(prec, 3), round(simp, 3), round(gen, 3)


def check_event_attr(logpath):
    """
    Checks for existence of event attributes, given the path of event log.

    Parameters:
        logpath (str): Path of event log

    Returns:
        attr (List of str): List of event attributes
    """
    log = importer.apply(logpath)
    log_df = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)
    log_df.drop(["concept:name", "time:timestamp", "case:concept:name"], axis=1, inplace=True, errors='ignore')
    attr = [value for value in log_df.columns.to_list() if value[:5] != "case:"]
    return attr


def get_position(act, act_list):
    """
    Returns the position of an element in the given list.

    Parameters:
        act (str): Element
        act_list (list of str): List of elements

    Returns:
        pos (int): Position of act in act_list
    """
    return act_list.index(act)


def update_tracker(cond, attr_value, thres, rule_tracker, rec_index, rule_index, pos):
    """
    Updates the rule_tracker dictionary with event index (rec_index), if it satisfies corresponding thresholds.

    Parameters:
        cond (str): Predicate value i.e, GTE, LTE etc
        attr_value (str): Event attribute
        thres (float or str): Threshold value
        rule_tracker (dict): Key-value pairs specific to a rule where key is an activity, pair is an event index
        rec_index (int): Index of event in event log
        rule_index (int): Index of rule
        pos (int): Position of activity in rule_tracker
    """
    if type(attr_value) == int or type(attr_value) == float:
        if cond == "NEQ":
            if attr_value != thres[rule_index][pos]:
                rule_tracker[pos] = rec_index
            else:
                rule_tracker[pos] = None
        elif cond == "EQ":
            if attr_value == thres[rule_index][pos]:
                rule_tracker[pos] = rec_index
            else:
                rule_tracker[pos] = None
        elif cond == "LT":
            if attr_value < thres[rule_index][pos]:
                rule_tracker[pos] = rec_index
            else:
                rule_tracker[pos] = None
        elif cond == "GT":
            if attr_value > thres[rule_index][pos]:
                rule_tracker[pos] = rec_index
            else:
                rule_tracker[pos] = None
        elif cond == "LTE":
            if attr_value <= thres[rule_index][pos]:
                rule_tracker[pos] = rec_index
            else:
                rule_tracker[pos] = None
        elif cond == "GTE":
            if attr_value >= thres[rule_index][pos]:
                rule_tracker[pos] = rec_index
            else:
                rule_tracker[pos] = None
        else:
            rule_tracker[pos] = None
    else:
        if cond == "NEQ":
            if attr_value != thres[rule_index][pos]:
                rule_tracker[pos] = rec_index
            else:
                rule_tracker[pos] = None
        elif cond == "EQ":
            if attr_value == thres[rule_index][pos]:
                rule_tracker[pos] = rec_index
            else:
                rule_tracker[pos] = None
        else:
            rule_tracker[pos] = None

def clear_successive(rule_tracker, pos):
    """
    Given a position, elements in the successive positions are cleared from the dictionary.

    Parameters:
        rule_tracker (dict): Key-value pairs specific to a rule where key is an activity, pair is an event index
        pos (int): Position of activity in rule_tracker
    """
    for val in range(pos,len(rule_tracker)):
        rule_tracker[pos] = None


def get_key(rule_tracker, value):
    """
    Given an event index, its corresponding key from the dictionary is returned.

    Parameters:
        rule_tracker (dict): Key-value pairs specific to a rule where key is an activity, pair is an event index
        value (int): Index of event in event log

    Returns:
        key (int): Position of value in rule_tracker
    """
    for key in rule_tracker:
        if rule_tracker[key] == value:
            return key


def deriving_events(df, act, attr, pred, thres, loc, new_act, window, order, vis):
    """
    Given an event log in the form of dataframe and, set of rules, the complete event derivation algorithm is applied.
    Transformed log in the form of dataframe is returned.

    Parameters:
        df (object): Event log dataframe
        act (List of str): List of activities in rule
        attr (List of str): List of attributes in rule
        pred (List of str): List of predicates in rule
        thres (List of float or str): List of thresholds in rule
        loc (List of str): List of locations for derived events in rule
        new_act (List of str): List of derived event's identifiers
        window (List of int): List of time windows in rule
        order (bool): Flag to denote if order of events in log is considered
        vis (bool): Flag to denote if activities in rule should be retained

    Returns:
        transformed_df (object): Transformed event log
    """
    temp = []
    first_rule_flag = True
    df_cols = df.columns.to_list()
    case_col = df_cols.index("case:concept:name") + 1
    act_col = df_cols.index("concept:name") + 1
    time_col = df_cols.index("time:timestamp") + 1

    # print(df.shape)

    for rule_index, rule in enumerate(act):
        rule_tracker = dict.fromkeys(np.arange(len(rule)))
        curr_time = None
        curr_tracker_index = None
        curr_traceid = df.iloc[0]["case:concept:name"]
        time_difference = 0
        rec_index = 0
        rule_actvities = [activity for sublist in act for activity in sublist]

        if order[rule_index]:
            for rec in df.itertuples():
                new_rec = None

                # denotes the begining of next trace
                if rec[case_col] != curr_traceid:
                    curr_traceid = rec[case_col]
                    rule_tracker = dict.fromkeys(np.arange(len(rule)))
                    curr_time = None

                # to check time window compliance
                if curr_time:
                    time_difference = (rec[time_col] - curr_time).total_seconds()

                    # if time difference is beyond the threshold, re-initialise the tracker
                    if time_difference > window[rule_index]:
                        rule_tracker = dict.fromkeys(np.arange(len(rule)))
                        curr_time = None

                if rec[act_col] in rule:
                    pos = get_position(rec[act_col], rule)
                    attr_col = df_cols.index(attr[rule_index][pos]) + 1

                    # first activity in act's sublist
                    if pos == 0:
                        # only one activity in the rule
                        if len(rule) == 1:
                            update_tracker(pred[rule_index][pos], rec[attr_col], thres, rule_tracker, rec_index,
                                           rule_index, pos)

                            if rule_tracker[pos] != None:
                                new_rec = [rec.Index]

                                for col in df.columns:
                                    if col == "case:concept:name":
                                        new_rec.append((rec[case_col]))
                                    elif col == "concept:name":
                                        new_rec.append((new_act[rule_index]))
                                    elif col == attr[rule_index][pos]:
                                        new_rec.append((rec[attr_col]))
                                    elif col == "time:timestamp":
                                        new_rec.append((rec[time_col]))
                                    else:
                                        new_rec.append("")

                                new_rec = tuple(new_rec)
                                rule_tracker = dict.fromkeys(np.arange(len(rule)))

                        # multiple activities in the rule
                        else:
                            # since this is the first activity, erase the rule tracker every time
                            rule_tracker = dict.fromkeys(np.arange(len(rule)))
                            update_tracker(pred[rule_index][pos], rec[attr_col], thres, rule_tracker, rec_index,
                                           rule_index, pos)
                            if rule_tracker[pos] != None:
                                curr_time = rec[time_col]

                    # last activity in act's sublist, denotes deriving new event if successful
                    elif pos == (len(rule) - 1):
                        if rule_tracker[pos - 1] != None:
                            update_tracker(pred[rule_index][pos], rec[attr_col], thres, rule_tracker, rec_index,
                                           rule_index, pos)

                            if rule_tracker[pos] != None:

                                # decide where to insert the new event
                                if loc[rule_index] == "start":
                                    start_event_index = min(filter(lambda x: x is not None, rule_tracker.values()))
                                    new_rec = [start_event_index]

                                    for col in df.columns:
                                        if col == "case:concept:name":
                                            new_rec.append((df.iloc[start_event_index]["case:concept:name"]))
                                        elif col == "concept:name":
                                            new_rec.append((new_act[rule_index]))
                                        elif col == attr[rule_index][pos]:
                                            new_rec.append((df.iloc[start_event_index][attr[rule_index][pos]]))
                                        elif col == "time:timestamp":
                                            new_rec.append((df.iloc[start_event_index]["time:timestamp"]))
                                        else:
                                            new_rec.append("")
                                else:
                                    new_rec = [rec.Index]

                                    for col in df.columns:
                                        if col == "case:concept:name":
                                            new_rec.append((rec[case_col]))
                                        elif col == "concept:name":
                                            new_rec.append((new_act[rule_index]))
                                        elif col == attr[rule_index][pos]:
                                            new_rec.append((rec[attr_col]))
                                        elif col == "time:timestamp":
                                            new_rec.append((rec[time_col]))
                                        else:
                                            new_rec.append("")

                                new_rec = tuple(new_rec)
                                rule_tracker = dict.fromkeys(np.arange(len(rule)))
                                curr_time = None

                    # any other position for activity in act's sublist
                    else:
                        if rule_tracker[pos - 1] != None:
                            update_tracker(pred[rule_index][pos], rec[attr_col], thres, rule_tracker, rec_index,
                                           rule_index, pos)
                            # clear the successive elements to maintain order
                            clear_successive(rule_tracker, pos + 1)

                    # if events part of rule needs to be retained
                    if vis:
                        if first_rule_flag:
                            temp.append(rec)

                        if new_rec:
                            temp.append(new_rec)
                    # if events part of rule needs to be dropped
                    else:
                        if rec[act_col] not in rule_actvities:
                            if first_rule_flag:
                                temp.append(rec)

                        if new_rec:
                            temp.append(new_rec)
                else:
                    if vis:
                        if first_rule_flag:
                            temp.append(rec)

                        if new_rec:
                            temp.append(new_rec)
                    else:
                        if rec[act_col] not in rule_actvities:
                            if first_rule_flag:
                                temp.append(rec)

                        if new_rec:
                            temp.append(new_rec)

                rec_index = rec_index + 1
        ###############################################################################################################
        else:
            for rec in df.itertuples():
                new_rec = None

                # denotes the beginning of next trace
                if rec[case_col] != curr_traceid:
                    curr_traceid = rec[case_col]
                    rule_tracker = dict.fromkeys(np.arange(len(rule)))
                    curr_time = None
                    curr_tracker_index = None

                # to check time window compliance
                if curr_time:
                    time_difference = (rec[time_col] - curr_time).total_seconds()

                    # if time difference is beyond the threshold, find the oldest event and remove it
                    if time_difference > window[rule_index]:

                        while next_event_flag:
                            # if there are no indexes stored in rule tracker yet
                            if len(set(rule_tracker.values())) == 1:
                                curr_time = None
                                curr_tracker_index = None
                                next_event_flag = False

                            # find the smallest index from rule tracker
                            else:
                                next_event_index = min(filter(lambda x: x is not None, rule_tracker.values()))
                                time_difference = (
                                            rec[time_col] - df.iloc[next_event_index]["time:timestamp"]).total_seconds()

                                # calculate difference from that
                                # YES None its value from rule tracker
                                if time_difference > window[rule_index]:
                                    key = get_key(rule_tracker, next_event_index)
                                    rule_tracker[key] = None

                                # NO means assign its time as curr time and set a flag for while
                                else:
                                    curr_time = df.iloc[next_event_index]["time:timestamp"]
                                    curr_tracker_index = get_key(rule_tracker, next_event_index)
                                    break

                if rec[act_col] in rule:
                    pos = get_position(rec[act_col], rule)
                    attr_col = df_cols.index(attr[rule_index][pos]) + 1

                    # curr_tracker_index determines the oldest event in rule tracker
                    if pos == curr_tracker_index:
                        prev_tracker_value = rule_tracker[pos]

                        update_tracker(pred[rule_index][pos], rec[attr_col], thres, rule_tracker, rec_index, rule_index,
                                       pos)

                        # if oldest event is changed, then also change curr_time's value to maintain time window
                        if prev_tracker_value != rule_tracker[pos]:
                            if len(set(rule_tracker.values())) == 1:
                                curr_time = None
                                curr_tracker_index = None
                                next_event_flag = False

                            # find the oldest dated event
                            else:
                                next_event_index = min(filter(lambda x: x is not None, rule_tracker.values()))
                                curr_time = df.iloc[next_event_index]["time:timestamp"]
                                curr_tracker_index = get_key(rule_tracker, next_event_index)
                    else:
                        update_tracker(pred[rule_index][pos], rec[attr_col], thres, rule_tracker, rec_index, rule_index,
                                       pos)

                    # mark the position of oldest event in rule tracker
                    if len(set(rule_tracker.values())) >= 2:
                        next_event_flag = True
                        next_event_index = min(filter(lambda x: x is not None, rule_tracker.values()))
                        curr_time = df.iloc[next_event_index]["time:timestamp"]
                        curr_tracker_index = get_key(rule_tracker, next_event_index)

                    if None not in rule_tracker.values():

                        # decide where to insert the new event
                        if loc[rule_index] == "start":
                            start_event_index = min(filter(lambda x: x is not None, rule_tracker.values()))
                            new_rec = [start_event_index]

                            for col in df.columns:
                                if col == "case:concept:name":
                                    new_rec.append((df.iloc[start_event_index]["case:concept:name"]))
                                elif col == "concept:name":
                                    new_rec.append((new_act[rule_index]))
                                elif col == attr[rule_index][pos]:
                                    new_rec.append((df.iloc[start_event_index][attr[rule_index][pos]]))
                                elif col == "time:timestamp":
                                    new_rec.append((df.iloc[start_event_index]["time:timestamp"]))
                                else:
                                    new_rec.append("")
                        else:
                            new_rec = [rec.Index]

                            for col in df.columns:
                                if col == "case:concept:name":
                                    new_rec.append((rec[case_col]))
                                elif col == "concept:name":
                                    new_rec.append((new_act[rule_index]))
                                elif col == attr[rule_index][pos]:
                                    new_rec.append((rec[attr_col]))
                                elif col == "time:timestamp":
                                    new_rec.append((rec[time_col]))
                                else:
                                    new_rec.append("")

                        new_rec = tuple(new_rec)

                        rule_tracker = dict.fromkeys(np.arange(len(rule)))
                        curr_time = None
                        curr_tracker_index = None

                    # if events part of rule needs to be retained
                    if vis:
                        if first_rule_flag:
                            temp.append(rec)

                        if new_rec:
                            temp.append(new_rec)
                    # if events part of rule needs to be dropped
                    else:
                        if rec[act_col] not in rule_actvities:
                            if first_rule_flag:
                                temp.append(rec)

                        if new_rec:
                            temp.append(new_rec)
                else:
                    if vis:
                        if first_rule_flag:
                            temp.append(rec)

                        if new_rec:
                            temp.append(new_rec)
                    else:
                        if rec[act_col] not in rule_actvities:
                            if first_rule_flag:
                                temp.append(rec)

                        if new_rec:
                            temp.append(new_rec)

                rec_index = rec_index + 1

        first_rule_flag = False

    transformed_df = pd.DataFrame(temp).drop("Index", axis=1)
    transformed_df.columns = df.columns.to_list()

    transformed_df = transformed_df.groupby(["case:concept:name"]).apply(
        lambda x: x.sort_values(["time:timestamp"], ascending=False)).reset_index(drop=True)
    transformed_df = transformed_df.groupby(["case:concept:name"]).apply(
        lambda x: x.sort_values(["time:timestamp"], ascending=True)).reset_index(drop=True)

    return transformed_df


def apply_trans(logpath, activities, attributes, predicates, thresholds, location, new_activities, window, order_flag,
                visual_flag):
    """
    Given an event log and, set of rules, they are channelised to event derivation algorithm.
    Evaluation metrics for transformed log and, statistics for original log and transformed log is
    calculated and returned.

    Parameters:
        logpath (str): Path of event log
        activities (List of str): List of activities in rule
        attributes (List of str): List of attributes in rule
        predicates (List of str): List of predicates in rule
        thresholds (List of float or str): List of thresholds in rule
        location (List of str): List of locations for derived events in rule
        new_activities (List of str): List of derived event's identifiers
        window (List of int): List of time windows in rule
        order_flag (bool): Flag to denote if order of events in log is considered
        visual_flag (bool): Flag to denote if activities in rule should be retained

    Returns:
        metrics (dict): Dictionary of evaluation measures like fitness, precision, simplicity and generalization for
        both the logs
    """
    xes_log = importer.apply(logpath)
    df = log_converter.apply(xes_log, variant=log_converter.Variants.TO_DATA_FRAME)

    df["time:timestamp"] = pd.to_datetime(df["time:timestamp"], format='%Y-%m-%d', utc=True)

    transformed_df = deriving_events(df, activities, attributes, predicates, thresholds, location, new_activities,
                                     window, order_flag, visual_flag)
    parameters = {log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: 'case:concept:name'}
    transformed_xes_log = log_converter.apply(transformed_df, parameters=parameters,
                                              variant=log_converter.Variants.TO_EVENT_LOG)
    xes_exporter.apply(transformed_xes_log, logpath[:-4] + "_modified.xes")


    metrics = dict.fromkeys(np.arange(2))
    metrics[0] = evaluate_logwithmodel(logpath)
    metrics[1] = evaluate_logwithmodel(logpath[:-4] + "_modified.xes")

    return metrics



if __name__ == "__main__":
    print("Run from a python module/program")