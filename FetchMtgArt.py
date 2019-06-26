import mtgsdk as mtg
from PIL import Image 
import csv
import os
import errno
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from tqdm import tqdm
import time

old_frame_date = time.strptime('2003-07-27', '%Y-%m-%d')

with open('card_data.csv', "w+", encoding="utf-8") as csv_file:
	csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	csv_writer.writerow(["multiverse_id", "name", "set", "types", "Legendary", "mana_cost", "rarity", "p/t", "text"])

	for s in tqdm(mtg.Set.all()):
		path = "./images/SET_"+s.code+"/"
		if not os.path.exists(path):
			try:
				os.makedirs(path)
			except OSError as exc:
				if exc.errno != errno.EEXIST:
					raise
		cards = mtg.Card.where(set=s.code).where(type='creature|enchantment|artifact|instant|sorcery').where(layout='normal').all()

		old_frame = time.strptime(s.release_date, '%Y-%m-%d') <= old_frame_date
		for c in cards:
			if c.image_url is not None:
				try:
					response = requests.get(c.image_url)
					img = Image.open(BytesIO(response.content))
					img = img.resize((223, 311))
					if old_frame:
						img = img.crop((27,31,196,167))
						img = img.resize((182,134))
					else:
						img = img.crop((21,38,203,172))
					img.save(path + str(c.multiverse_id) + ".png")
					csv_writer.writerow([c.multiverse_id, c.name, c.set, c.types, 1 if 'Legendary' in c.supertypes else 0, c.mana_cost, c.rarity, c.power + "/" + c.toughness if c.power is not None and c.toughness is not None else None, c.text])
				except:
					pass