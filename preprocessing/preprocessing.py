""" preprocessing.py
Program that preprocesses .csv (that was created using setup_dataframe.py) into

Author: Nils Visser

Last edited: 13-08-2024
"""

import pandas as pd
import re
import contractions
from preprocessing_helper import *
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


def make_sentences_df(input_dataset):
    """
    Converts incoherent lines into sentences (based on sentence ending e.g: ?.!)
    (incoherent lines are lines that should belong together, but have been split previously)
    :return: dataframe with sentences.
    """
    df = input_dataset
    df = df.dropna(subset=['preprocessed_text'])
    df = df.drop(columns=['line_information', 'speaker_status', 'line_number', 'utterance_count'])
    line_merge_number = []
    i = 0
    for sentence in df['preprocessed_text']:
        matches = ["?", "!", "."]
        if any([x in sentence for x in matches]):
            line_merge_number.append(i)
            i += 1
        else:
            line_merge_number.append(i)

    df['line_merge_number'] = line_merge_number

    df2 = pd.DataFrame(columns=df.columns)
    for number in df['line_merge_number'].unique():
        tobe_merged_data = df.loc[(df['line_merge_number'] == number)]
        if len(tobe_merged_data) <= 1:
            df2 = df2.append(tobe_merged_data)
        else:
            original_text_merged = ''.join(tobe_merged_data['text'].to_list())
            processed_text_merged = ''.join(tobe_merged_data['preprocessed_text'].to_list())
            if processed_text_merged[:-1] == 0:
                new_row = {'scenario': tobe_merged_data['scenario'].values[0],
                           'text': original_text_merged,
                           'source_file': tobe_merged_data['source_file'].values[0],
                           'preprocessed_text': processed_text_merged,
                           'line_merge_number': None
                           }
                df2 = df2.append(new_row, ignore_index=True)

    df2 = df2.drop(columns=['text', 'line_merge_number'])
    return df2


def preprocess_line(utterance, mask_pauses, remove_repetitions, remove_masks):
    """
    Cleans text using regular expressions and custom functions.
    Also creates masks for filled and unfilled pauses.
    :param mask_pauses: Remove unfilled pauses with <mask> (if set true)
    :param remove_repetitions: Removes all masks (set true for healthy speech)

    :return:
    """
    expanded_words = []
    for word in utterance.split():
        # using contractions.fix --> he's --> he is
        expanded_words.append(contractions.fix(word))
    utterance = ' '.join(expanded_words)

    # +... Trailing off pause (speaker forgets about what is about to say)
    unfilled_pauses = ["(..)", "(...)", "+..."]
    for pause in unfilled_pauses:
        utterance = utterance.replace(pause, "UNFILLEDPAUSE")

    # Replace filler pauses with FILLERPAUSE
    filler_pauses = ["&-um", "&-uh", "&-er", "&-mm" "&-eh", "&-like", "&-youknow", "&-hm", "&-sighs"]
    for pause in filler_pauses:
        utterance = utterance.replace(pause, "FILLERPAUSE")

    # Remove all actions: (e.g. &=points:picture)
    r = re.findall(r"\W\W\w+\W\w+", utterance)
    for regex in r:
        if not contains_whitespace(regex):
            utterance = utterance.replace(regex, "")

    # Remove all unicode errors   \W\d+\w\d+\W
    r = re.findall(r"\W\d+\w\d+\W", utterance)
    for regex in r:
        if not contains_whitespace(regex):
            utterance = utterance.replace(regex, "")

    # Remove all characters that start with 2 special chars and have text succeeding it:
    r = re.findall(r"\W\W\w+", utterance)
    for regex in r:
        # if regex[0] != " " and regex[1] != " ":
        if not contains_whitespace(regex):
            # This prevents second and first letter being a space to be removed.
            # e.g. : ") Cinderella" removes the word Cinderella too, which we don't want.
            utterance = utterance.replace(regex, "")

    # Remove anything between [ and ]
    r = re.findall(r"\[(.*?)\]", utterance)
    for regex in r:
        utterance = utterance.replace(regex, "")

    # Remove anything between < and >
    r = re.findall(r"\<(.*?)\>", utterance)
    for regex in r:
        utterance = utterance.replace(regex, "")

    # Remove anything &+
    r = re.findall(r"\&+[a-zA-Z]+", utterance)
    for regex in r:
        utterance = utterance.replace(regex, "")

    special_characters = ['(.)', '[/]', '[//]', '‡', 'xxx', '+< ', '„', '+', '"" /..""', '+"/.', '+"', '+/?', '+//.',
                          '+//?', '[]', '<>', '_', '-', '^', ')', '(', ':', 'www .', '*PAR', '+/', '@o', '<', '>',
                          '//..', '//', '/..', '/', '"', 'ʌ', '..?', '0.', '0 .', '"" /.']

    # Remove remaining special chars
    for special_character in special_characters:
        utterance = utterance.replace(special_character, "")

    utterance = re.sub(' +', ' ', utterance)

    # Remove special characters from starting sentence
    remove_startswiths = [" ", ",", "!", ".", "?", "."]
    for start_string in remove_startswiths:
        if utterance.startswith(start_string):
            utterance = utterance[1:]

    # Replace all pauses with <mask> (if set true)
    if mask_pauses:
        utterance = utterance.replace("UNFILLEDPAUSE", "<mask>")
        utterance = utterance.replace("FILLERPAUSE", "<mask>")

    # Removes all masks (set true for healthy speech)
    if remove_masks:
        utterance = utterance.replace("<mask>", "")

    # Removes stuttering and bigram stuttering
    if remove_repetitions:
        utterance = remove_all_repetitions(utterance)

    utterance = re.sub(' +', ' ', utterance)  # Remove final whitespaces (e.g. double space)

    return utterance


def preprocess_dataset(input_dataset_filename, mask_pauses, remove_repetitions, remove_masks):
    df = pd.read_csv(input_dataset_filename, encoding='utf8')
    df = df.dropna()

    speaker_status = []  # Add speaker status / 1 for interviewer, 2 for participant
    current_status = 0
    for line_information in df['line_information']:
        if line_information == "*INV" or line_information == "*IN1" or line_information == "*IN2":
            current_status = 1
        elif line_information == "*PAR":
            current_status = 2

        speaker_status.append(current_status)
    df["speaker_status"] = speaker_status
    df = df.loc[(df['speaker_status'] == 2)]

    # Not selected scenarios: "Cinderella_Intro", "Sandwich_Intro", "Important_Event_Intro", "Repetition", "BNT", "Sandwich_Other","Sandwich_Picture", "VNT"
    selected_scenarios = ["Important_Event", "Speech", "Stroke", "Cinderella", "Sandwich", "Window", "Cat", "Umbrella",
                          "Flood"]

    df = df[df.scenario.isin(selected_scenarios)]
    df = df.loc[(df['line_information'] == "*PAR")]

    preprocessed_text = []
    for text in df['text']:
        preprocessed_line = preprocess_line(text, mask_pauses, remove_repetitions, remove_masks)
        preprocessed_text.append(preprocessed_line)

    df['original_text'] = df['text']
    df['preprocessed_text'] = preprocessed_text
    return df


if __name__ == "__main__":
    # preprocessed_df = preprocess_dataset("protocol_aphasia_anomic.csv", True, True, False)
    # df_aphasia = make_sentences_df(preprocessed_df)
    # df_aphasia.to_csv("protocol_aphasia_anomic_preprocessed.csv")

    # preprocessed_df = preprocess_dataset("protocol_control.csv", True, False, True)
    # df_control = make_sentences_df(preprocessed_df)
    # df_control.to_csv("protocol_control_preprocessed.csv")

    preprocessed_df = preprocess_dataset("protocol_aphasia_anomic.csv", False, False, False)
    df_control = make_sentences_df(preprocessed_df)
    df_control.to_csv("aphasia_pauses.csv")

    preprocessed_df = preprocess_dataset("protocol_control.csv", False, False, False)
    df_control = make_sentences_df(preprocessed_df)
    df_control.to_csv("control_pauses.csv")
