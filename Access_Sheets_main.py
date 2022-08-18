import gspread
import string
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os
from oauth2client.service_account import ServiceAccountCredentials
from Sentiment_Analysis_main import analyse
import matplotlib.pyplot as plt

plt.rcParams.update({'figure.max_open_warning': 0})
import pathlib
from numpy import array
import traceback

current_path = str(pathlib.Path().resolve())


def col2num(col) -> int:
	num = 0
	for c in col:
		if c in string.ascii_letters:
			num = num * 26 + (ord(c.upper()) - ord('A')) + 1
	return num


def report_data(file_name, start_col, end_col, min_value, max_value, is_ranked, analyzed_col_num, download_path):
	try:
		scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
		         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
		creds = ServiceAccountCredentials.from_json_keyfile_name(current_path + "/creds.json", scope)
		# TODO: client_email = 'anvay-971@avian-insight-318815.iam.gserviceaccount.com'

		client = gspread.authorize(creds)

		# Ensure the raw data begins at the second row, the first row being the questions in the GForm
		# (DON'T PRE-PROCESS SHEET)
		sheet = client.open(file_name).sheet1

		start_col_num = col2num(start_col)
		end_col_num = col2num(end_col)
		relevant_col_count = end_col_num - start_col_num + 1
		row_count = len(sheet.col_values(start_col_num))  # ensure with client that first column is filled
		data_row_count = row_count - (3 if is_ranked else 2)

		rank_of_ratings = []  # list of ranks for each question

		analyzed_col = sheet.col_values(analyzed_col_num)  # The column to be analysed in list form
		question_name = str(analyzed_col[0])
		text_analyzed_col = analyzed_col[(3 if is_ranked else 2):]  # We are doing a python slice here to
		# exclude the column names, question polarities, and question ranks (if given) from the first few rows

		for k in range(len(text_analyzed_col), data_row_count):
			text_analyzed_col.append("")

		relative_text_positivity = [0.0] * len(
			text_analyzed_col)  # average rating for each candidate's textual response

		polarity_of_ratings = sheet.row_values(2)[
		                      start_col_num - 1: end_col_num]  # list of polarities for each column's ratings
		if is_ranked:
			rank_of_ratings = sheet.row_values(3)[start_col_num - 1: end_col_num]

		num_ranked_cols = 0
		for j in range(relevant_col_count):
			if not (polarity_of_ratings[j] == "none" or polarity_of_ratings[j] == "n/a" or polarity_of_ratings[
				j] == "na" or polarity_of_ratings[j] == "neutral"):
				num_ranked_cols += 1

		converted_rank_of_ratings = []

		for x in rank_of_ratings:
			converted_rank_of_ratings.append(float(x) if x != "" else float(num_ranked_cols + 1))

		# TODO: Add a third row wherein the rating questions themselves are ranked. This is optional, and the default
		#  is a simple average. For the question with rank x, its reliability includes weighted_rank[j] = (n+1-x)/n,
		#  given that there are n quantitative, non-neutral questions. For the ith responder and for j non-neutral Qs,
		#  reliability[i] = abs(relative_text_positivity[i] - 2*sum(data[i][j] * weighted_rank[j])/((n+1)*max_value)), where:
		#  relative_text_positivity = positive_score / polar_score,
		#  2*sum(data[i][j] * weighted_rank[j])/((n+1)*max_value)) is between 0 and 1 (inclusive) and is summed over all j, and
		#  reliability[i] is between 0 and 1 (inclusive)

		data_for_ratings = sheet.get_all_values()
		data_for_ratings = array(data_for_ratings)
		data_for_ratings = data_for_ratings[3 if is_ranked else 2: row_count, start_col_num - 1: end_col_num].tolist()

		for x in range(data_row_count):
			for y in range(relevant_col_count):
				if data_for_ratings[x][y] == '':
					data_for_ratings[x][y] = '0.0'

		clean_data_for_ratings = []

		for sublist in data_for_ratings:
			float_sublist = []
			for x in sublist:
				float_sublist.append(float(x))
			clean_data_for_ratings.append(float_sublist)

		# TODO: Add the code to pull the third row onwards of numerical ratings data. Then, for negative ratings, take
		#  (max_rating - current_rating). Add all these ratings up and divide by number of ratings AND include the
		#  margin of error when comparing in 'if' statements.

		for x in range(data_row_count):
			for y in range(relevant_col_count):
				if polarity_of_ratings[y] == "pos" or polarity_of_ratings[y] == "positive" or polarity_of_ratings[
					y] == "good":
					clean_data_for_ratings[x][y] = float(clean_data_for_ratings[x][y])

				elif polarity_of_ratings[y] == "neg" or polarity_of_ratings[y] == "negative" or polarity_of_ratings[
					y] == "bad":
					clean_data_for_ratings[x][y] = min_value + max_value - float(clean_data_for_ratings[x][y])

				elif polarity_of_ratings[y] == "none" or polarity_of_ratings[y] == "n/a" or polarity_of_ratings[
					y] == "na" or polarity_of_ratings[y] == "neutral":
					clean_data_for_ratings[x][y] = 0.0

		for i in range(data_row_count):
			text = text_analyzed_col[i]
			lower_case = text.lower()
			cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))

			score = SentimentIntensityAnalyzer().polarity_scores(cleaned_text)
			negative_score = score['neg']
			positive_score = score['pos']
			polar_score = negative_score + positive_score

			if polar_score > 0:
				relative_positivity = positive_score / polar_score
			elif text == "":
				relative_positivity = 0.0
			else:
				relative_positivity = 0.5

			relative_text_positivity[i] = relative_positivity

		ratings_average = [0.0] * data_row_count  # Store the ith row's average in the (x-3)th element of ratings_average.
		reliability = [0.0] * data_row_count  # Stores how consistent each person's quantitative positivity is with
		# their qualitative positivity; i.e. their theoretical reliability.

		for i in range(data_row_count):
			for j in range(relevant_col_count):
				if is_ranked:
					ratings_average[i] += clean_data_for_ratings[i][j] * (
								num_ranked_cols + 1 - converted_rank_of_ratings[j]) / float(num_ranked_cols)
				else:
					ratings_average[i] += clean_data_for_ratings[i][j] / float(relevant_col_count)

			if num_ranked_cols == 0:
				ratings_average[i] = 0.5
			elif not is_ranked:
				ratings_average[i] /= max_value
			else:
				ratings_average[i] = 2 * ratings_average[i] / ((num_ranked_cols + 1) * max_value)

			reliability[i] = 1 - abs(ratings_average[i] - relative_text_positivity[i])

		def scatterplot():
			fig, ax1 = plt.subplots()
			ax1.scatter(relative_text_positivity, ratings_average)
			fig.autofmt_xdate()

			path = download_path + "/Graphs for " + file_name + "/" + question_name + "/Graphs accounting for Reliability"
			if not os.path.exists(path):
				os.makedirs(path)

			plt.title('Scatter Plot of Numerical vs Textual Positivity')
			plt.xlabel('Relative Text Positivity')
			plt.ylabel('Calculated Numerical Positivity')
			fig.savefig(path + "/Scatter_Plot_of_Numerical_vs_Textual_Positivity.png")

		scatterplot()

		return reliability

	except Exception as e:
		print(traceback.format_exc())
		reliability = []
		return reliability


def access_sheets_without_report(file_name, analyzed_col_num, download_path):
	try:
		scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
		         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
		creds = ServiceAccountCredentials.from_json_keyfile_name(current_path + "/creds.json", scope)
		# TODO: client_email = 'anvay-971@avian-insight-318815.iam.gserviceaccount.com'

		client = gspread.authorize(creds)

		# Ensure the raw data begins at the second row, the first row being the questions in the GForm
		# (DON'T PRE-PROCESS SHEET)
		sheet = client.open(file_name).sheet1

		analyzed_col = sheet.col_values(analyzed_col_num)  # The column to be analysed in list form
		question_name = str(analyzed_col[0])
		analyzed_col = analyzed_col[1:]  # We are doing a python slice here to
		# exclude the column names from the first row (keyword)

		num_records = len(analyzed_col)

		rankSum = {}  # Overall rankSum dictionary with all relative frequencies

		def mergeDicts(x, y):
			mergedDict = {k: x.get(k, 0) + y.get(k, 0) for k in set(x) | set(y)}
			return mergedDict

		for i in range(num_records):
			text = analyzed_col[i]
			local_dict = analyse(i, text, download_path, file_name, question_name)
			rankSum = mergeDicts(rankSum, local_dict)

		rankSum = dict(sorted(rankSum.items()))  # Sorting rankSum by the relative frequency of its keys

		# Function to produce the main graph of all the rankSums
		def main_graph():
			rankSumCopy = rankSum
			rankSumCopy = dict(sorted(rankSumCopy.items(), key=lambda item: item[1]))
			fig, ax1 = plt.subplots()
			ax1.bar(rankSumCopy.keys(), rankSumCopy.values())
			fig.autofmt_xdate()

			path = download_path + "/Graphs for " + file_name + "/" + question_name + "/Graphs not accounting for Reliability"
			if not os.path.exists(path):
				os.makedirs(path)

			plt.title('Aggregate relative frequencies (RankSums)')
			plt.xlabel('Emotion')
			plt.ylabel('RankSum Value (in ascending order)')
			fig.savefig(path + "/AggregateFigure_Without_Report.png")

		main_graph()

		return True, rankSum, question_name

	except Exception as e:
		print(traceback.format_exc())
		return False, {}, ""


def access_sheets_with_report(file_name, analyzed_col_num, download_path, is_ranked, reliability):
	try:
		scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
		         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
		creds = ServiceAccountCredentials.from_json_keyfile_name(current_path + "/creds.json", scope)
		# TODO: client_email = 'anvay-971@avian-insight-318815.iam.gserviceaccount.com'

		client = gspread.authorize(creds)

		# Ensure the raw data begins at the second row, the first row being the questions in the GForm
		# (DON'T PRE-PROCESS SHEET)
		sheet = client.open(file_name).sheet1

		analyzed_col = sheet.col_values(analyzed_col_num)  # The column to be analysed in list form
		question_name = str(analyzed_col[0])
		text_analyzed_col = analyzed_col[(3 if is_ranked else 2):]  # We are doing a python slice here to
		# exclude the column names from the first row (keyword)

		num_records = len(text_analyzed_col)

		rankSum = {}  # Overall rankSum dictionary with all relative frequencies

		def mergeDicts(x, y):
			mergedDict = {k: x.get(k, 0) + y.get(k, 0) for k in set(x) | set(y)}
			return mergedDict

		for i in range(num_records):
			text = text_analyzed_col[i]
			local_dict = analyse(i, text, download_path, file_name, question_name, reliability[i])
			rankSum = mergeDicts(rankSum, local_dict)

		rankSum = dict(sorted(rankSum.items()))  # Sorting rankSum by the relative frequency of its keys

		# Function to produce the main graph of all the rankSums
		def main_graph():
			rankSumCopy = rankSum
			rankSumCopy = dict(sorted(rankSumCopy.items(), key=lambda item: item[1]))
			fig, ax1 = plt.subplots()
			ax1.bar(rankSumCopy.keys(), rankSumCopy.values())
			fig.autofmt_xdate()

			path = download_path + "/Graphs for " + file_name + "/" + question_name + "/Graphs accounting for Reliability"
			if not os.path.exists(path):
				os.makedirs(path)

			plt.title('Aggregate relative frequencies (RankSums)')
			plt.xlabel('Emotion')
			plt.ylabel('RankSum Value (in ascending order)')
			fig.savefig(path + "/AggregateFigure_With_Report.png")

		main_graph()

		return True, rankSum, question_name

	except Exception as e:
		print(traceback.format_exc())
		return False, {}, ""
