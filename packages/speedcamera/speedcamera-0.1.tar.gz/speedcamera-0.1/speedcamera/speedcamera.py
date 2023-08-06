
def speeding(lol):
	f = open(lol, "r")
	CarsArray = []
	TimesArray = []
	CPArray = []
	data = f.read().split("\n")
	for line in data:
		if " " not in line:
			LineCount = line
		else:
			line = line.split(" ")
			CarsArray.append(line[2])    
			TimesArray.append(line[0])   
			CPArray.append(line[1])      

	########### DATA READER ##############

	# 	LineCount
	#	CarsArray
	#	TimesArray
	#	CPArray

	########### MAIN PROGRAM #############

	carlist = {}
	scannedplates = []
	speedlist = []
	speedlimit = 110




	for i in range(0,len(CarsArray)):
		plate = CarsArray[i]
		if plate not in scannedplates:
	# for each car number plate set plate as variable, and check if its been scanned
	#the plate variable will be the compared to all other plates in to below loop and the loop will match up data entries with the same plate


			for x in range(0,len(CarsArray)):
				if CarsArray[x] == plate:
					carlist['Number plate:'] = CarsArray[x]
					carlist[CPArray[x]] = TimesArray[x]
	#For each plate in the list, check if it matches the plate being scanned for, if it does, add the index of the plate, the checkpoint and the time to carlist
	#this will add all lines in the data containing the numberplate variable to a dictionary containing the number plate, and a checkpoint key and time value

	#after the speed calculations are done,  carlist is reset so the next plate in the top loop can be scanned		


			#at this indentation carlist contains all lines of data for the number plate variable in the top for loop

			if '1' in carlist and '2' in carlist:
				#checking if the car hit checkpoints 1 and 2
				h,m,s = carlist['1'].split(":")
				hh,mm,ss = carlist['2'].split(":")
				#getting the hours, minutes and seconds for the times at checkpoints 1 and 2 from carlist and converting them to seconds

				time = (int(hh) * 3600 + int(mm) * 60 + int(ss)) - (int(h) * 3600 + int(m) * 60 + int(s))
				#the difference between the checkpoint times in seconds
				speed = 133/(time/3600)
				#calculate a cars speed based on how long it traveled and the distance between checkpoints
				if speed > 110:
					speedlist.append(carlist['2'] + ' 2 ' + carlist['Number plate:'] + ' ' + str(round(speed,1)))
					#check if a cars speed is over the speed limit, if it is, add the second checkpoint data and number plate to the list of speeding cars



			#second if statement in a row (not elif statement) so it is always run as car could be speeding from 2-3 and not 1-2
			if '2' in carlist and '3' in carlist:
				#checking if the car hit checkpoints 2 and 3
				h,m,s = carlist['2'].split(":")
				hh,mm,ss = carlist['3'].split(":")
				time = (int(hh) * 3600 + int(mm) * 60 + int(ss)) - (int(h) * 3600 + int(m) * 60 + int(s))
				speed = 57.5/(time/3600)
				if speed > 110:
					speedlist.append(carlist['3'] + ' 3 ' + carlist['Number plate:'] + ' ' + str(round(speed,1)))







			carlist={}
			#reseting carlist so a new plate can be scanned
		else:
			pass
		scannedplates.append(plate)
		#once a plate has been scanned, add it to list of scanned plates


	def get_time(speedlist):
		return speedlist[:9]
	#a function that returns the first 9 digits (the timestamp) of input

	speedlist.sort(key=get_time)
	#get_time returns the timestamp in speedlist and sort sorts it by return value

	for x in speedlist: print(x) #print out speeders!

