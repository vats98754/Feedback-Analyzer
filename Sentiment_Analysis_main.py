import os
import pathlib
import stat
import traceback
from collections import Counter

import nltk
from matplotlib import pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
from nltk.corpus import stopwords
import re
import emoji
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

current_path = str(pathlib.Path().resolve())


def analyse(i, text, download_path, title, question_name, reliability=-1):
	try:
		def emojis_extractor(text):
			emoj = {'Emoji': ['👏 🏾',
	                  '👏 🏼',
	                  '👏 🏽',
	                  '👨 \u200d ❤ ️ \u200d 👨',
	                  '👩 \u200d ❤ ️ \u200d 👨',
	                  '👩 \u200d ❤ ️ \u200d 👩',
	                  '🤤',
	                  '😘',
	                  '😋',
	                  '😛',
	                  '😝',
	                  '😜',
	                  '😂',
	                  '💪',
	                  '💪 🏿',
	                  '💪 🏻',
	                  '💪 🏾',
	                  '💪 🏼',
	                  '💪 🏽',
	                  '🙏',
	                  '🙏 🏿',
	                  '🙏 🏻',
	                  '🙏 🏾',
	                  '🙏 🏼',
	                  '🙏 🏽',
	                  '🌝',
	                  '😀',
	                  '😁',
	                  '💗',
	                  '🤝',
	                  '💟',
	                  '♥',
	                  '💘',
	                  '💝',
	                  '✔',
	                  '🌺',
	                  '🤗',
	                  '💏',
	                  '👨 \u200d ❤ ️ \u200d 💋 \u200d 👨',
	                  '💋',
	                  '👩 \u200d ❤ ️ \u200d 💋 \u200d 👨',
	                  '👩 \u200d ❤ ️ \u200d 💋 \u200d 👩',
	                  '😽',
	                  '😗',
	                  '😚',
	                  '😙',
	                  '🕺',
	                  '🕺 🏿',
	                  '🕺 🏻',
	                  '🕺 🏾',
	                  '🕺 🏼',
	                  '🕺 🏽',
	                  '💁 \u200d ♂ ️',
	                  '💁 🏿 \u200d ♂ ️',
	                  '💁 🏻 \u200d ♂ ️',
	                  '💁 🏾 \u200d ♂ ️',
	                  '💁 🏼 \u200d ♂ ️',
	                  '💁 🏽 \u200d ♂ ️',
	                  '🤓',
	                  '👐',
	                  '👐 🏿',
	                  '👐 🏻',
	                  '👐 🏾',
	                  '👐 🏼',
	                  '👐 🏽',
	                  '🙌',
	                  '🙌 🏿',
	                  '🙌 🏻',
	                  '🙌 🏾',
	                  '🙌 🏼',
	                  '🙌 🏽',
	                  '😌',
	                  '🤣',
	                  '🤘',
	                  '🤘 🏿',
	                  '🤘 🏻',
	                  '🤘 🏾',
	                  '🤘 🏼',
	                  '🤘 🏽',
	                  '😴',
	                  '🙂',
	                  '😇',
	                  '😍',
	                  '😃',
	                  '😆',
	                  '😅',
	                  '😄',
	                  '😊',
	                  '😎',
	                  '👍',
	                  '👍 🏿',
	                  '👍 🏻',
	                  '👍 🏾',
	                  '👍 🏼',
	                  '👍 🏽',
	                  '💕',
	                  '✌',
	                  '✌ 🏿',
	                  '✌ 🏻',
	                  '✌ 🏾',
	                  '✌ 🏼',
	                  '✌ 🏽',
	                  '🖖',
	                  '🖖 🏿',
	                  '🖖 🏻',
	                  '🖖 🏾',
	                  '🖖 🏼',
	                  '🖖 🏽',
	                  '👋',
	                  '👋 🏿',
	                  '👋 🏻',
	                  '👋 🏾',
	                  '👋 🏼',
	                  '👋 🏽',
	                  '😉',
	                  '💃',
	                  '💃 🏿',
	                  '💃 🏻',
	                  '💃 🏾',
	                  '💃 🏼',
	                  '💃 🏽',
	                  '💛',
	                  '🤙',
	                  '🤙 🏿',
	                  '🤙 🏻',
	                  '🤙 🏾',
	                  '🤙 🏼',
	                  '🤙 🏽',
	                  '👏',
	                  '👏 🏿',
	                  '👏 🏻',
	                  '💓',
	                  '😥',
	                  '😞',
	                  '😓',
	                  '🤕',
	                  '😷',
	                  '🤒',
	                  '😶',
	                  '☹',
	                  '😦',
	                  '😭',
	                  '🤥',
	                  '😐',
	                  '😔',
	                  '😪',
	                  '🙁',
	                  '😫',
	                  '🙃',
	                  '😩',
	                  '😟',
	                  '🤐',
	                  '💔',
	                  '😑',
	                  '😤',
	                  '🤦 \u200d ♂ ️',
	                  '🤦 🏿 \u200d ♂ ️',
	                  '🤦 🏻 \u200d ♂ ️',
	                  '🤦 🏾 \u200d ♂ ️',
	                  '🤦 🏼 \u200d ♂ ️',
	                  '🤦 🏽 \u200d ♂ ️',
	                  '🙅 \u200d ♂ ️',
	                  '🙅 🏿 \u200d ♂ ️',
	                  '🇬 🇱',
	                  '🙅 🏾 \u200d ♂ ️',
	                  '🙅 🏼 \u200d ♂ ️',
	                  '🙅 🏽 \u200d ♂ ️',
	                  '🤷 \u200d ♂ ️',
	                  '🤷 🏿 \u200d ♂ ️',
	                  '🤷 🏻 \u200d ♂ ️',
	                  '🤷 🏾 \u200d ♂ ️',
	                  '🖕',
	                  '🖕 🏿',
	                  '🖕 🏻',
	                  '🖕 🏾',
	                  '🖕 🏼',
	                  '🖕 🏽',
	                  '👊',
	                  '👊 🏿',
	                  '👊 🏻',
	                  '👊 🏾',
	                  '👊 🏼',
	                  '👊 🏽',
	                  '😣',
	                  '🤦',
	                  '🤦 🏿',
	                  '🤦 🏻',
	                  '🤦 🏾',
	                  '🤦 🏼',
	                  '🤦 🏽',
	                  '🤷',
	                  '🤷 🏿',
	                  '🤷 🏻',
	                  '🤷 🏾',
	                  '🤷 🏼',
	                  '🤷 🏽',
	                  '😡',
	                  '😈',
	                  '😏',
	                  '👎',
	                  '👎 🏿',
	                  '👎 🏻',
	                  '👎 🏾',
	                  '👎 🏼',
	                  '👎 🏽',
	                  '😒',
	                  '🙅 \u200d ♀ ️',
	                  '🙅 🏿 \u200d ♀ ️',
	                  '🙅 🏻 \u200d ♀ ️',
	                  '🙅 🏾 \u200d ♀ ️',
	                  '🙅 🏼 \u200d ♀ ️',
	                  '🙅 🏽 \u200d ♀ ️',
	                  '😠',
	                  '👿',
	                  '😵',
	                  '😱',
	                  '😮',
	                  '🙄',
	                  '😯',
	                  '🙆 \u200d ♂ ️',
	                  '🙆 🏿 \u200d ♂ ️',
	                  '🙆 🏻 \u200d ♂ ️',
	                  '🙆 🏾 \u200d ♂ ️',
	                  '🙆 🏼 \u200d ♂ ️',
	                  '🙆 🏽 \u200d ♂ ️',
	                  '🙆 \u200d ♀ ️',
	                  '🙆 🏿 \u200d ♀ ️',
	                  '🙆 🏻 \u200d ♀ ️',
	                  '🙆 🏾 \u200d ♀ ️',
	                  '🙆 🏼 \u200d ♀ ️',
	                  '🙆 🏽 \u200d ♀ ️',
	                  '😧',
	                  '😲',
	                  '🤞',
	                  '🤞 🏿',
	                  '🤞 🏻',
	                  '🤞 🏾',
	                  '🤞 🏼',
	                  '🤞 🏽',
	                  '😰',
	                  '😨',
	                  '😳',
	                  '😬',
	                  '🤢',
	                  '🤧'],
	        'Emotion': ['Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Happy',
	                    'Sad',
	                    'Sad',
	                    'Sad',
	                    'Sad',
	                    'Sad',
	                    'Sad',
	                    'Sad',
	                    'Sad',
	                    'Sad',
	                    'Sad',
	                    'Sad',
	                    'Sad',
	                    'Sad',
	                    'Sad',
	                    'Sad',
	                    'Sad',
	                    'Sad',
	                    'Sad',
	                    'Sad',
	                    'Sad',
	                    'Sad',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Angry',
	                    'Surprise',
	                    'Surprise',
	                    'Surprise',
	                    'Surprise',
	                    'Surprise',
	                    'Surprise',
	                    'Surprise',
	                    'Surprise',
	                    'Surprise',
	                    'Surprise',
	                    'Surprise',
	                    'Surprise',
	                    'Surprise',
	                    'Surprise',
	                    'Surprise',
	                    'Surprise',
	                    'Surprise',
	                    'Surprise',
	                    'Surprise',
	                    'Fear',
	                    'Fear',
	                    'Fear',
	                    'Fear',
	                    'Fear',
	                    'Fear',
	                    'Fear',
	                    'Fear',
	                    'Fear',
	                    'Fear',
	                    'Fear',
	                    'Fear']}
			a = " ".join(c for c in text if c in emoji.UNICODE_EMOJI).split()
			for i in a:
				try:
					text = text.replace(i, " " + emoj['Emotion'][emoj["Emoji"].index(i)] + " ")
				except Exception as e:
					print(traceback.format_exc())
					pass
			return text.lower()

		def removing_contradictions(text):
			if text.count("n't"):
				text = text.replace("n't", " not")
			text = re.sub("ai\snot", "am not", text)
			text = re.sub("wo\snot", "will not", text)
			return text

		def removing_not(text):
			d = {'not sad': 'Happy', 'not bad': 'Happy', 'not boring': 'Happy', 'not wrong': 'Happy', 'not bored': 'Happy',
			     'not jealous': 'Happy', 'not happy': 'Sad', 'not well': 'Sad', 'not suitable': 'Angry',
			     'not right': 'Angry',
			     'not good': 'Sad', 'not excited': 'Angry', 'not funny ': 'Sad', 'not  kind': 'Sad', 'not proud': 'Angry',
			     'not cool': 'Angry', 'not funny': 'Angry', 'not kind': 'Angry', 'not open': 'Angry', 'not safe': 'Fear',
			     'not enough': 'Empty', 'not know': 'Sad', 'not knowing': 'Sad', 'not believe': 'Angry',
			     'not believing': 'Angry',
			     'not understand': 'Sad', 'not understanding': 'Sad', 'no doubt': 'Happy', 'not think': 'Sad',
			     'not thinking': 'Sad',
			     'not recognise': 'Sad', 'not recognising': 'Sad', 'not forget': 'Angry', 'not forgetting': 'Angry',
			     'not remember': 'Sad',
			     'not remembering': 'Sad', 'not imagine': 'Sad', 'not imagining': 'Sad', 'not mean': 'Sad',
			     'not meaning': 'Sad',
			     'not agree': 'Angry', 'not agreeing': 'Sad', 'not disagree': 'Happy', 'not disagreeing': 'Happy',
			     'not deny': 'Sad',
			     'not denying': 'Sad', 'not promise': 'Angry', 'not promising': 'Angry', 'not satisfy': 'Sad',
			     'not satisfying': 'Sad',
			     'not realise': 'Sad', 'not realising': 'Sad', 'not appear': 'Angry', 'not appearing': 'Angry',
			     'not please': 'Sad', 'not pleasing': 'Sad', 'not impress': 'Sad', 'not impressing': 'Sad',
			     'not surprise': 'Sad', 'not surprising': 'Sad', 'not concern': 'Sad', 'not concerning': 'Sad',
			     'not have': 'Sad', 'not having': 'Sad',
			     'not own': 'Sad', 'not owning': 'Sad', 'not possess': 'Sad', 'not possessing': 'Sad', 'not lack': 'Sad',
			     'not lacking': 'Sad',
			     'not consist': 'Sad', 'not consisting': 'Sad', 'not involve': 'Sad', 'not involving': 'Sad',
			     'not include': 'Sad', 'not including': 'Sad', 'not contain': 'Sad',
			     'not containing': 'Sad', 'not love': 'Sad', 'not like': 'Angry',
			     'not hate': 'Happy', 'not hating': 'Happy', 'not adore': 'Sad', 'not adoring': 'Sad', 'not prefer': 'Sad',
			     'not preferring': 'Sad', 'not care': 'Angry', 'not mind': 'Angry', 'not minding': 'Sad',
			     'not want': 'Angry', 'not wanting': 'Sad',
			     'not need': 'Angry', 'not needing': 'Angry', 'not desire': 'Sad', 'not desiring': 'Sad', 'not wish': 'Sad',
			     'not wishing': 'Sad', 'not hope': 'Sad', 'not hoping': 'Sad', 'not appreciate': 'Sad',
			     'not appreciating': 'Sad',
			     'not value': 'Sad', 'not valuing': 'Sad', 'not owe': 'Sad', 'not owing': 'Sad', 'not seem': 'Sad',
			     'not seeming': 'Sad', 'not fit': 'Sad', 'not fitting': 'Sad', 'not depend': 'Sad',
			     'not depending': 'Sad', 'not matter': 'Sad', 'not afford': 'Sad', 'not affording': 'Sad', 'not aim': 'Sad',
			     'not aiming': 'Sad', 'not attempt': 'Angry', 'not attempting': 'Angry', 'not ask': 'Angry',
			     'not asking': 'Angry', 'not arrange': 'Angry', 'not arranging': 'Angry', 'not beg': 'Angry',
			     'not begging': 'Angry', 'not begin': 'Angry', 'not beginning': 'Angry', 'not caring': 'Angry',
			     'not choose': 'Angry', 'not choosing': 'Angry', 'not claim': 'Angry', 'not claiming': 'Angry',
			     'not consent': 'Angry', 'not consenting': 'Angry', 'not continue': 'Angry', 'not continuing': 'Angry',
			     'not dare': 'Angry', 'not daring': 'Angry', 'not decide': 'Sad',
			     'not deciding': 'Sad', 'not demand': 'Angry', 'not demanding': 'Angry', 'not deserve': 'Angry',
			     'not deserving': 'Angry', 'not expect': 'Angry',
			     'not expecting': 'Angry', 'not fail': 'Happy', 'not failing': 'Happy', 'not get': 'Sad',
			     'not getting': 'Sad',
			     'not hesitate': 'Sad', 'not hesitating': 'Sad', 'not hurry': 'Happy', 'not hurrying': 'Happy',
			     'not intend': 'Sad', 'not intending': 'Sad', 'not learn': 'Angry', 'not learning': 'Angry',
			     'not liking': 'Angry', 'not loving': 'Sad', 'not manage': 'Angry',
			     'not managing': 'Angry', 'not neglect': 'Sad', 'not neglecting': 'Sad', 'not offer': 'Angry',
			     'not offering': 'Angry',
			     'not plan': 'Angry', 'not planing': 'Angry', 'not prepare': 'Angry',
			     'not preparing': 'Angry', 'not pretend': 'Angry', 'not pretending': 'Angry', 'not proceed': 'Angry',
			     'not proceeding': 'Angry',
			     'not propose': 'Angry', 'not proposing': 'Sad', 'not refuse': 'Sad', 'not refusing': 'Sad',
			     'not start': 'Sad',
			     'not starting': 'Sad', 'not stop': 'Happy', 'not stopping': 'Happy', 'not struggle': 'Angry',
			     'not struggling': 'Angry',
			     'not swear': 'Angry', 'not swearing': 'Angry', 'not threaten': 'Happy', 'not threatening': 'Happy',
			     'not try': 'Angry', 'not trying': 'Angry', 'not volunteer': 'Angry',
			     'not volunteering': 'Angry', 'not wait': 'Angry', 'not waiting': 'Angry', 'not feel': 'Sad',
			     'not feeling': 'Sad', "not able": "Sad", "not do": "Sad"}

			f = re.findall("not\s\w+", text)
			for i in f:
				try:
					text = text.replace(i, d[i])
				except Exception as e:
					print(traceback.format_exc())
					pass
			text = text.lower()
			return text

		def removing_shortcuts(text):
			full_words = []
			shortcuts = {'u': 'you', 'y': 'why', 'r': 'are', 'doin': "doing", 'm': 'am',
			             'b4': 'before', 'ty': 'thank you', 'wlcm': 'welcome', 'bc': 'because', '<3': 'love',
			             'xoxo': 'love',
			             'ttyl': 'talk to you later', 'gr8': 'great', 'bday': 'birthday', 'awsm': 'awesome', 'gud': 'good',
			             'h8': 'hate',
			             'lv': 'love', 'dm': 'direct message', 'rt': 'retweet', 'wtf': 'hate', 'idgaf': 'hate',
			             'irl': 'in real life', 'yolo': 'you only live once', "don't": "do not", 'g8': 'great',
			             "won't": "will not", 'tbh': 'to be honest', 'caj': 'casual', 'Ikr': 'I know, right?',
			             'omw': 'on my way',
			             'ofc': 'of course', 'Idc': "I don't care", 'Irl': 'In real life', 'tbf': 'To be fair',
			             'obvs': 'obviously', 'v': 'very', 'atm': 'at the moment',
			             'col': 'crying out loud', 'gbu': 'god bless you', 'gby': 'god bless you', 'gotcha': 'I got you',
			             'hehe': 'laughing', 'haha': 'laughing', 'hf': 'have fun',
			             'hry': 'hurry', 'hw': 'hardwork', 'idc': 'i don’t care', 'ikr': 'i know right', 'k': 'ok',
			             'lmao': 'laughing my ass off', 'lol': 'laughing out loud',
			             'n1': 'nice one', 'na': 'not available', 'qt': 'cutie', 'qtpi': 'cutie pie',
			             'rip': 'rest in peace',
			             'sry': 'sorry', 'tc': 'take care',
			             'thnks': 'thanks', 'thx': 'thanks', 'thnk': 'thanks', 'txt': 'text',
			             'ugh': 'disgusted', 'w8': 'wait', "not sad": "happy"}

			for token in text:
				if token in shortcuts.keys():
					token = shortcuts[token]
				full_words.append(token)
			text = " ".join(full_words)
			return text

		def removing_stopwords(text):
			stop_words = set(stopwords.words('english'))
			stop = [x.lower() for x in stop_words]
			return [word for word in text if not word in stopwords.words()]

		def lemmatization(words_big):
			lemma = WordNetLemmatizer()
			stemmed_words = [lemma.lemmatize(word, 'v') for word in words_big]
			stemmed_words = [lemma.lemmatize(word, 'n') for word in stemmed_words]
			return " ".join(stemmed_words)

		def cleaning(text):
			text = text.lower()
			text = emojis_extractor(text)
			text = re.sub(r'http\S+|www.\S+', '', text)
			text = removing_contradictions(text)
			text = removing_not(text)
			text = text.split()
			text = removing_shortcuts(text)
			text = ' '.join([i for i in text.split() if not i.isdigit()])
			text = word_tokenize(text)
			words_alpha = removing_stopwords(text)
			words_big = [word for word in words_alpha if len(word) > 2]
			clean_text = lemmatization(words_big)
			clean_text = clean_text.replace('   ', ' ')
			clean_text = clean_text.replace('  ', ' ')
			return clean_text

		cleaned_text = cleaning(text)
		lemma_words = cleaned_text.split()

		emotion_list = []
		with open(current_path + '/emotions.txt', 'r') as file:
			for line in file:
				clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
				word, emotion = clear_line.split(': ')

				if word in lemma_words:
					emotion_list.append(emotion)

		w = Counter(emotion_list)

		emo_dict = {}
		score = SentimentIntensityAnalyzer().polarity_scores(cleaned_text)
		emo_dict['NEGATIVE'] = score['neg']
		emo_dict['POSITIVE'] = score['pos']
		w['NEGATIVE'] = score['neg']
		w['POSITIVE'] = score['pos']
		polar_score = w['NEGATIVE'] + w['POSITIVE']

		want_report = (reliability != -1)
		emotions_exist = len(emotion_list) > 0

		for e in w:
			if emotions_exist:
				if want_report:
					emo_dict[e] = reliability * w[e] / len(emotion_list)
				else:
					emo_dict[e] = 0.5 * w[e] / len(emotion_list)
			# The default value of reliability[i] = 0.5 is that of unranked questions.

		if (polar_score > 0 or len(emo_dict) > 2) and i != -1:
			# 3 is lower bound because every dict should have keys 'NEGATIVE' and 'POSITIVE'.
			# and if i == -1, then the input is an audio file
			fig, ax1 = plt.subplots()
			ax1.bar(emo_dict.keys(), emo_dict.values())
			fig.autofmt_xdate()

			path = download_path + "/Graphs for " + title + "/" + question_name + ("/Graphs not accounting for Reliability" if not want_report
			                                                 else "/Graphs accounting for Reliability") + \
			       ("/IndividualData_Without_Report" if not want_report else "/IndividualData_With_Report")

			if not os.path.exists(path):
				os.makedirs(path)
				# Giving everyone read, write, and executive permissions on the folder
				os.chmod(path, stat.S_IXUSR | stat.S_IWUSR | stat.S_IXOTH | stat.S_IWOTH | stat.S_IXGRP | stat.S_IWGRP |
				         stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

			plt.savefig(path + "/Figure" + str(i) + ("_Without_Report.png" if not want_report else "_With_Report.png"))

		return emo_dict

	except AttributeError as e:
		print(traceback.format_exc())
		return {}