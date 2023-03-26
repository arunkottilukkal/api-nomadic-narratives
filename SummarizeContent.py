from flask import Flask, make_response, jsonify
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt.exceptions import DecodeError
import re
from heapq import nlargest



"""Summarization"""

def summarize_text(text, num_sentences):
    # Remove any unwanted characters or numbers from the text
    text = re.sub(r'\[[0-9]*\]', '', text)
    text = re.sub(r'\s+', ' ', text)

    # Split the text into individual sentences
    sentences = re.split('\.|\?|\!', text)

    # Remove any leading or trailing spaces in each sentence
    sentences = [sentence.strip() for sentence in sentences]

    # Remove any empty sentences
    sentences = [sentence for sentence in sentences if len(sentence) > 0]

    # Calculate the score for each sentence based on word frequency
    word_frequencies = {}
    for sentence in sentences:
        for word in sentence.split(' '):
            if word.lower() not in word_frequencies:
                word_frequencies[word.lower()] = 1
            else:
                word_frequencies[word.lower()] += 1

    # Determine the average word frequency
    maximum_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequency)

    # Calculate the score for each sentence based on sentence length
    sentence_scores = {}
    for sentence in sentences:
        if len(sentence.split(' ')) < 30:
            for word in sentence.split(' '):
                if word.lower() in word_frequencies.keys():
                    if sentence not in sentence_scores.keys():
                        sentence_scores[sentence] = word_frequencies[word.lower()]
                    else:
                        sentence_scores[sentence] += word_frequencies[word.lower()]

    # Select the top n sentences with the highest scores
    summarized_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)

    # Join the selected sentences into a summarized text
    summarized_text = ' '.join(summarized_sentences)

    return summarized_text


"""End of Summarization"""


summary = Namespace("English", description="Summarize English Contents")
summaryHeader = summary.parser()
summaryHeader.add_argument("Authorization", location="headers", required=True)

summaryContent = summary.model(
    "SummaryContent",
    {
    "sentence": fields.String(),
    "sentence_count": fields.Integer()
    }
)

@summary.route("/Summarize")
class Summary(Resource):
    @jwt_required()
    @summary.expect(summaryHeader, summaryContent)
    def post(self):
        data = summary.payload
        
        return {"Summarized": summarize_text(data.get('sentence'),int(data.get('sentence_count')))}, 201 #make_response(jsonify({"Summarized": data.get('sentence')}),201)


@summary.errorhandler(NoAuthorizationError)
def exceptionHandler(err):
    return make_response(jsonify({"message": str(err)}), 401)

@summary.errorhandler(DecodeError)
def exceptionHandler(err):
    return make_response(jsonify({"message": str(err)}), 401)


