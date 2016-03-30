from baluhn import generate, verify
import time
import sys
fHand = open("./Input/customerrecords.txt")
confHand = open("./Configuration/issuerconfig.conf")
accountsFileHand = open("./Output/accounts.txt", "w")
cardsFileHand = open("./Output/cards.txt","w")
cardAccountsFileHand = open("./Output/cardaccounts.txt","w")
accountOverideLimitsFileHand = open("./Output/accountoverridelimits.txt","w")
cardOverideLimitsFileHand = open("./Output/cardoverridelimits.txt","w")
statementsFileHand = open("./Output/statements.txt","w")
accountBalancesFileHand = open("./Output/accountbalances.txt", "w")
lastPANHand = open("./configuration/lastcard.conf")
lastCardNumGenerated = int(lastPANHand.read())
cardsProducedCount = 0
thisYearMonth = time.strftime("%Y%m")[2:]
def configParamsParser(confHand):
	returnValue = str()
	config = confHand.read()
	config = config.split(',')
	try:
		BIN = config[0]
	except:
		print "BIN not specified in config file."
		quit()
	try:
		PANLength = config[1]
	except:
		print "PAN Length not specified in config file"
		quit()
	try:
		cardStatus = config[2]
	except:
		print "Card Status not specified in config file"
		quit()
	try:
		currency = config[3]
	except:
		print "Currency not specified in config file"
		quit()
	try:
		cardProgram = config[4]
	except:
		print "Card Program not specified in config file"
		quit()
	try:
		discretionaryData = config[5]
	except:
		print " Discretionary data not specified in config file"
		quit()
	try:
		cardDuration = config[6]
	except:
		print "Card duration not spsecified in config file"
		quit()
	try:
		FINAddress = config[7]
	except:
		print "Financial institution address not specified in config file"
		quit()
	try:
		FINCity = config[8]
	except:
		print "Financial institution city not specified in config file"
		quit()
	try:
		FINCountry = config[9]
	except:
		print "Financial institution country not specified in config file"
		quit()
	try:
		mailerDest = config[10]
	except:
		print "Mailer Destination not specified in config file"
		quit()
	try: 
		FINVIPStatus = config[11]
	except:
		print "Financial institution VIP status not specified in config file"
		quit()
	returnValue =  BIN + ', ' + PANLength + ', ' + cardStatus + ', ' + currency + ', ' + cardProgram + ', ' + discretionaryData + ', ' + cardDuration+ ', ' + FINAddress + ', ' + FINCity + ', ' + FINCountry + ', ' + mailerDest + ', ' + FINVIPStatus
	return returnValue

def accountsFileWriter(accountsFileContent):
	accountsFileHand.write(accountsFileContent)

def cardsFileWriter(cardsFileContent):
	cardsFileHand.write(cardsFileContent)
	
def cardAccountsFileWriter(cardAccountsFileContent):
	cardAccountsFileHand.write(cardAccountsFileContent)

def accountOverideLimitsWriter(accountOverideLimitsContent):
	accountOverideLimitsFileHand.write(accountOverideLimitsContent)

def cardOverideLimitsWriter(cardOverideLimitsContent):
	cardOverideLimitsFileHand.write(cardOverideLimitsContent)

def statementFileWriter(statementsFileContent):
	statementsFileHand.write(statementsFileContent)

def accountBalancesFileWriter(accountBalancesFileContent):
	accountBalancesFileHand.write(accountBalancesFileContent)
	
def cardProFileReader(fHand, cardsProducedCount, FINLevelConfig, lastCardNumGenerated):
	errorGenerated = 0
	if errorGenerated == 0:
		for cardDetails in fHand:
			lines = str()
			cardsProducedCount +=1
			lines = cardDetails.split(",")
			try: #Populating accountID and AccountType
				accountID = lines[0].strip()
				accountType = lines[1].strip()
				if accountType not in ("10", "20"):
					print "Invalid account Type in record", cardsProducedCount, ". The valid account types are 10 for Savings and 20 for Current"
					errorGenerated +=1
			except:
				print "Card File creation failed due to error in account details"
				quit()
			try: #Populating customerID
				customerID = lines[2].strip()
				if len(customerID) > 25:
					print "Customer ID must be populated with a maximum of 25 characters. The value for record %d is %d characters long" % (cardsProducedCount, len(customerID))
					errorGenerated +=1
			except: pass
			try: #Populating cardHolderFName
				cardHolderFName = lines[3].strip()
				if len(cardHolderFName)> 20:
					print "Card Holder First name must be populated with a maximum of 20 characters. The value for record %d is %d characters long" % (cardsProducedCount, len(cardHolderFName))
					errorGenerated +=1
			except: pass
			try: #Populating cardHolderMName
				cardHolderMName = lines[4].strip()
				if len(cardHolderMName)> 10:
					print "Card Holder Middle name must be populated with a maximum of 10 characters. The value for record %d is %d characters long" % (cardsProducedCount, len(cardHolderMName))
					errorGenerated +=1
			except: pass
			try: #Populating cardHolderLName
				cardHolderLName = lines[5].strip()
				if len(cardHolderLName)> 10:
					print "Card Holder Last name must be populated with a maximum of 20 characters. The value for record %d is %d characters long" % (cardsProducedCount, len(cardHolderLName))
					errorGenerated +=1
			except: pass
			try: #Populating nameOnCard
				nameOnCard = lines[6].strip()
				if len(nameOnCard)> 26:
					print "The Cardholder Name on card must be populated with a maximum of 26 characters. The value for record %d is %d characters long" % (cardsProducedCount, len(nameOnCard))
					errorGenerated +=1
			except:
				print "Card File creation failed due to error in Cardholder name on card"
				errorGenerated +=1
			try: #Populating cardHolderAddress. 
				cardHolderAddress = FINLevelConfig.split(",")[7].strip()#We first attempt to use the default value from FINLevelConfig.
				if len(lines[7].strip()) > 1:
					cardHolderAddress = lines[7].strip()#We overwrite the value  with the content of the input file if the corresponding value is populated.
				if len(cardHolderAddress) > 30:
					print "The Cardholder Address must be populated with a maximum of 30 characters. The value for record %d is %d characters long" % (cardsProducedCount, len(cardHolderAddress))
					errorGenerated +=1
			except: pass
			try: #Populating cardHolderCity
				cardHolderCity = FINLevelConfig.split(",")[8].strip()#We first attempt to use the default value from FINLevelConfig.
				if len(lines[8].strip())>1:
					cardHolderCity = lines[8].strip()#We overwrite the value  with the content of the input file if the corresponding value is populated.
				if len(cardHolderCity)> 20:
					print "The Cardholder Address must be populated with a maximum of 30 characters. The value for record %d is %d characters long" % (cardsProducedCount, len(cardHolderCity))
					errorGenerated +=1
			except: pass
			try: #Populating cardHolderCountry
				cardHolderCountry = FINLevelConfig.split(",")[9].strip()#We first attempt to use the default value from FINLevelConfig.
				if len(lines[9].strip())>1:
					cardHolderCountry = lines[9].strip()#We overwrite the value  with the content of the input file if the corresponding value is populated.
				if len(cardHolderCountry) > 3:
					print "The Cardholder Country must be populated with a maximum of 3 characters. The value for record %d is %d characters long" % (cardsProducedCount, len(cardHolderCountry))
					errorGenerated +=1
			except: pass
			try: #Populating cardHolderVIPStatus
				cardHolderVIPStatus = FINLevelConfig.split(",")[11].strip()#We first attempt to use the default value from FINLevelConfig.
				if len(lines[10].strip(" ")) > 1:
					cardHolderVIPStatus =lines[10].strip(" ")#We overwrite the value  with the content of the input file if the corresponding value is populated.
				if int(cardHolderVIPStatus) > 1:
					print "Invalid value used for card holder VIP status"
					errorGenerated += 1
			except:
				pass
				
			FINLevelNow = str(FINLevelConfig).split(",")
			accountsFileContent = "U" + ',' + accountID + ',' + accountType + ',' + FINLevelNow[3].translate(None, "',").strip() + ',' + customerID +'\n'
			luhnDigit = generate(str(lastCardNumGenerated + cardsProducedCount))
			lastCreatedCard = str(int(lastCardNumGenerated) + int(cardsProducedCount))
			currentPAN = str(int(lastCardNumGenerated) + int(cardsProducedCount)) + str(luhnDigit)
			expiryDate = int(str(int(thisYearMonth[0:2]))) + int(FINLevelNow[6].translate(None,",'"))
			expiryDate = str(expiryDate) + str(thisYearMonth[2:])
			cardsFileContent = "U" + "," + str(currentPAN) + "," + "000" +","+ FINLevelNow[4].translate(None, "',").strip() + ',' + accountType + "," + FINLevelNow[2].translate(None, "',").strip() + "," + "," + expiryDate + "," + "," + "," + "," +"4"+ "," + "," + "," + "," + "," + "," + "," + cardHolderFName + "," + cardHolderMName + "," + cardHolderLName + "," + nameOnCard + "," + cardHolderAddress + "," + "," + cardHolderCity + "," + "," + ","+ cardHolderCountry + "," + "," + FINLevelNow[10].translate(None, "',").strip() + "," + "," + cardHolderVIPStatus +"," + "," + FINLevelNow[5].translate(None, "',").strip() + "," + "," + "," + "," +"," + customerID +'\n'
			cardsFileContent = cardsFileContent.translate(None, "\n") + "\n"
			cardAccountsFileContent = "U" + "," + str(currentPAN) + ","+ "000"+ "," + accountID + "," + accountType + "," + "1" + "," + accountType + "\n"
			accountOverideLimitsContent = str()
			cardOverideLimitsContent = str()
			statementsFileContent = str()
			accountBalancesFileContent = str()
			if errorGenerated == 0:
				accountsFileWriter(accountsFileContent)
				cardsFileWriter(cardsFileContent)
				cardAccountsFileWriter(cardAccountsFileContent)
				accountOverideLimitsWriter(accountOverideLimitsContent)
				cardOverideLimitsWriter(cardOverideLimitsContent)
				statementFileWriter(statementsFileContent)
				accountBalancesFileWriter(accountBalancesFileContent)
	returnValue  = lastCreatedCard + "," + str(cardsProducedCount) + "," + str(errorGenerated)
	return returnValue

def lastPANWriter(lastCardNumGenerated)	:
	writelastPANHand = open("./configuration/lastcard.conf", "w")
	writelastPANHand.write(lastCardNumGenerated)
	writelastPANHand.close()

FINLevelConfig = configParamsParser(confHand)
cardsProducedEndPANAndCount = cardProFileReader(fHand, cardsProducedCount,FINLevelConfig, lastCardNumGenerated)
lastCardNumGenerated, cardsProducedCount, errorGenerated = cardsProducedEndPANAndCount.split(",")
if errorGenerated != "0":
	accountsFileHand.close()
	fHand.close()
	confHand.close()
	cardsFileHand.close()
	cardAccountsFileHand.close()
	accountOverideLimitsFileHand.close()
	cardOverideLimitsFileHand.close()
	statementsFileHand.close()
	accountBalancesFileHand.close()
	print "Card production file failed due to error at record %s. Reference the error above to fix" % (cardsProducedCount)
	quit()
else:
	accountsFileHand.close()
	fHand.close()
	confHand.close()
	cardsFileHand.close()
	cardAccountsFileHand.close()
	accountOverideLimitsFileHand.close()
	cardOverideLimitsFileHand.close()
	statementsFileHand.close()
	accountBalancesFileHand.close()
	lastPANWriter(lastCardNumGenerated)
	print "Accounts.txt written"
	print "Cards.txt written"
	print "cardaccounts.txt written"
	print "accountoverridelimits.txt written"
	print "cardoverridelimits.txt written"
	print "statements.txt written"
	print "accountbalances.txt written"
	print "Card production successful for %s records. Retrieve the card files from the output folder" % (cardsProducedCount)
	quit()