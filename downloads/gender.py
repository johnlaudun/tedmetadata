import csv
import string

# Pronoun lists
male_pronouns = {'he', 'him', 'his', 'himself'}
female_pronouns = {'she', 'her', 'hers', 'herself'}
nonbinary_pronouns = {'they', 'them', 'their', 'theirs', 'themself'}

"""nonbinary_pronouns = {'they', 'them', 'their', 'theirs', 'themself', 
                    'e', 'ey', 'em', 'eir', 'eirs', 'eirself', 
                    'fae', 'faer', 'faers', 'faerself', 
                    'per', 'pers', 'perself',
                    've', 'ver', 'vis', 'verself',
                    'xe', 'xem', 'xyr', 'xyrs', 'xemself',
                    'ze', 'zie', 'hir', 'hirs', 'hirself', 
                    'sie', 'zir', 'zis', 'zim', 'zieself', 
                    'emself', 'tey', 'ter', 'tem', 'ters', 'terself'} """

def find_gender(input_description):
	global male_pronouns, female_pronouns, nonbinary_pronouns

	# Initialize score variables
	male_score = 0
	female_score = 0
	nonbinary_score = 0

	# Lower and isolate everyword of the description
	des_lst = input_description.lower().split()
	for word in des_lst:
		cleanword = word.strip(string.punctuation)

		# Add to the appropriate score
		if cleanword in male_pronouns:
			male_score = male_score + 1
		elif cleanword in female_pronouns:
			female_score = female_score + 1
		elif cleanword in nonbinary_pronouns:
			nonbinary_score = nonbinary_score + 1

	total = male_score + female_score + nonbinary_score

	if total == 0: # Only happens if there are no pronouns
		gender = 'no pronouns'
	# elif (nonbinary_score <= (.1)*total):
	# Note: The above line is too harsh. 
	
	# If there are two kinds of pronouns are zero
	elif (male_score == 0) and (female_score == 0):
		gender = 'non-binary'
	elif (male_score == 0) and (nonbinary_score == 0):
		gender = 'female'
	elif (female_score == 0) and (nonbinary_score == 0):
		gender = 'male'

	# If there is only one kind of pronoun that is zero
	elif (nonbinary_score <= 1):
		score = (female_score - male_score) / (female_score + male_score)
		if score > 0.3:
			gender = 'female'
		elif score < -0.3:
			gender = 'male'
		else:
			gender = 'undetected'
	elif (male_score == 0):
		score = (female_score - nonbinary_score) / (female_score + nonbinary_score)
		if score > 0.3:
			gender = 'female'
		elif score < -0.3:
			gender = 'nonbinary'
		else:
			gender = 'undetected'
	elif (female_score == 0):
		score = (male_score - nonbinary_score) / (male_score + nonbinary_score)
		if score > 0.3:
			gender = 'male'
		elif score < -0.3:
			gender = 'nonbinary'
		else:
			gender = 'undetected'
	else:
		gender = 'last case'

	return (gender, male_score, female_score, nonbinary_score)



# Open the CSV file as a dictionary 
with open("speakersTest.csv") as des_file:
	des_data = csv.DictReader(des_file)
	
	# Create an empty list of dictionaries
	name_lst = []
	for row in des_data:
		# Pull the description
		row_des = row['LongDescription']
		short_des = row['ShortDescription']
		both_des = row_des + short_des
		found_gender, ms, fs, ns = find_gender(both_des)

		row_dict = {'Name':row['Name'], 
					'Occupation':row['Occupation'],
					'ShortDescription':short_des,
					'LongDescription': row_des, 
					'Gender': found_gender,
					'MaleScore': ms,
					'FemaleScore': fs,
					'NonBinaryScore': ns}
		name_lst.append(row_dict)

with open('speakersGenderTest.csv', 'w') as csvfile:
	fields = ['Name', 'Occupation','ShortDescription', 'LongDescription', 'Gender',
	'MaleScore','FemaleScore','NonBinaryScore']
	writer = csv.DictWriter(csvfile, fieldnames = fields)
	writer.writeheader()

	writer.writerows(name_lst)

