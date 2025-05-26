import hanlp

class FindLocations():
	def __init__(self, verbose=False):
		super(FindLocations, self).__init__()
		self.load_model()
		self.verbose = verbose

	def load_model(self):
		print("Loading model...")
		self.HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ERNIE_GRAM_ZH, device=0)
		print("Loaded model successfully!")

	def pre_process_text(self, text):
		text = text.replace(" ", "")
		text = text.replace("\n", "<SENTENCE END>")
		text = text.replace("。", "。<SENTENCE END>")
		text = text.replace("！", "！<SENTENCE END>")
		text = text.replace("？", "？<SENTENCE END>")
		sentences = [i for i in text.split("<SENTENCE END>") if i]

		if self.verbose:
			print(f"Preprocessed text: {sentences}")
		
		return sentences

	def ner(self, text):
		sentences = self.pre_process_text(text)
		doc = self.HanLP(sentences)

		if self.verbose:
			doc.pretty_print()
			#print(doc)

		return doc

	def locations(self, doc):
		locations = {}
		if "ner/msra" not in doc:
			return locations

		for index, sentence in enumerate(doc["ner/msra"]):
			for i in sentence:
				name = i[0]
				label = i[1]
				if label == "LOCATION" or label == "ORGANIZATION":
					if name in locations:
						locations[name]["mentioned"] += 1
					else:
						locations[name] = {"mentioned": 1, "label": label,"context": ''.join(doc["tok/fine"][index])}

		if self.verbose:
			print(f"Unique locations. Final result: {locations}")

		return locations

	def find_locations(self, text):
		doc = self.ner(text)
		locations = self.locations(doc)
		
		return locations