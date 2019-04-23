import csv
import urllib

OutputFile = 'gather_to_upload.tsv'

with open(OutputFile, 'w') as fout:
	for classID in range(1, 8):
		with open('L%02d.csv' % classID) as fin:
			marksTable = csv.reader(fin, dialect='excel')
			rowID = 0
			for row in marksTable:
				rowID += 1
				if rowID < 3:
					continue

				stuName = row[0].replace('\t', ' ')
				stuID = row[1]
				scoreTotal = float(row[3])
				#print stuName, stuID, scoreTotal
				assert 0.0 <= scoreTotal <= 5.0

				if row[4]:
					scoreImage = float(row[4])
				else:
					scoreImage = None
				if row[5]:
					scoreFont = float(row[5])
				else:
					scoreFont = None
				if row[6]:
					scoreLoop = float(row[6])
				else:
					scoreLoop = None
				if row[7]:
					scoreCreativity = float(row[7])
				else:
					scoreCreativity = None
				if row[8]:
					scoreReadability = float(row[8])
				else:
					scoreReadability = None

				assert scoreReadability is None or scoreReadability < 0.0
				comment = row[9]

				if not comment.rstrip():		# no submission
					continue

				mergedComment = comment + '\n'
				mergedComment += '-----------------------------------\n'
				if scoreImage is not None:
					mergedComment += 'Use of an image: ' + str(scoreImage) + '\n'
				if scoreFont is not None:
					mergedComment += 'Use of a custom font: ' + str(scoreFont) + '\n'
				if scoreLoop is not None:
					mergedComment += 'Use of loops: ' + str(scoreLoop) + '\n'
				if scoreCreativity is not None:
					mergedComment += 'Creativity: ' + str(scoreCreativity) + '\n'
				if scoreReadability is not None:
					mergedComment += 'Readability: ' + str(scoreReadability) + '\n'
				mergedComment += '-----------------------------------\n'
				mergedComment += 'Total: ' + str(scoreTotal)
				mergedComment = urllib.quote(mergedComment)
				#print urllib.unquote(mergedComment)

				fout.write('%s\t%s\t%s\t%s\n' % (stuName, stuID, scoreTotal, mergedComment))


print '\nJob done.'
