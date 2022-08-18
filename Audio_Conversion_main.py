import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from Sentiment_Analysis_main import analyse
import matplotlib.pyplot as plt
import stat


def perform_audio_analysis(audio_path, download_path, title):
	r = sr.Recognizer()
	try:
		storage_path = os.getcwd() + "/Audio"
		if not os.path.exists(storage_path):
			os.makedirs(storage_path)
			# Giving everyone read, write, and executive permissions on the folder
			os.chmod(storage_path, stat.S_IXUSR | stat.S_IWUSR | stat.S_IXOTH | stat.S_IWOTH | stat.S_IXGRP | stat.S_IWGRP |
		         stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

		sound = AudioSegment.from_mp3(audio_path)
		sound.export(storage_path + "/file.wav", format="wav")

		sound = AudioSegment.from_wav(storage_path + "/file.wav")

		chunks = split_on_silence(sound, min_silence_len=500, silence_thresh=sound.dBFS-14, keep_silence=500)

		folder_name = "Audio"
		if not os.path.isdir(folder_name):
			os.mkdir(folder_name)
			os.chmod(folder_name, stat.S_IXUSR | stat.S_IWUSR | stat.S_IXOTH | stat.S_IWOTH | stat.S_IXGRP | stat.S_IWGRP |
			         stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

		whole_text = ""

		# process each chunk
		for i, audio_chunk in enumerate(chunks, start=1):
			chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
			audio_chunk.export(chunk_filename, format="wav")
			with sr.AudioFile(chunk_filename) as source:
				audio_listened = r.record(source)
				try:
					text = r.recognize_google(audio_listened)
				except sr.UnknownValueError as e:
					print("Error:", str(e))
				else:
					text = f"{text.capitalize()}. "
					print(chunk_filename, ":", text)
					whole_text += " " + text

		# return the text for all chunks detected

		def main_graph(title, whole_text):
			rankSum = analyse(-1, whole_text, download_path, title, "")  # Overall rankSum dictionary with all relative frequencies
			rankSum = dict(sorted(rankSum.items(), key=lambda item: item[1]))
			fig, ax1 = plt.subplots()
			ax1.bar(rankSum.keys(), rankSum.values())
			fig.autofmt_xdate()

			path = download_path + "/Audio_Graph"
			if not os.path.exists(path):
				os.makedirs(path)
				# Giving everyone read, write, and executive permissions on the folder
				os.chmod(path, stat.S_IXUSR | stat.S_IWUSR | stat.S_IXOTH | stat.S_IWOTH | stat.S_IXGRP | stat.S_IWGRP |
				         stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

			plt.title('Aggregate relative frequencies (RankSums) based on audio file')
			plt.xlabel('Emotion')
			plt.ylabel('RankSum Value (in ascending order)')
			plt.savefig(path + "/FigureAggregate.png")

		main_graph(title, whole_text)
		return True

	except AttributeError:
		return False
