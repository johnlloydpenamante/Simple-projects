#property of Landicho, Johnlloyd P.
#Do not reupload!

#"cont" is a variable
cont = True
#set the default value of variable cont into True, to run your program
while cont == True:
	sub1 = float(input("Enter Grade #1: "))
	sub2 = float(input("Enter Grade #2: "))
	sub3 = float(input("Enter Grade #3: "))

#formula
	average = (sub1 + sub2 + sub3) / 3
#the solution, to make the output limited in 2 decimal point
	print(f"{average:.2f}")
	if average >= 75:
			print("Congrats, You passed!!")
	else:
			print("Sorry, You failed:(")
	
#logic to rerun your program
	q1 = str(input("Do you want to compute another grade? (y/n): "))
	if q1 == "y":
		cont = True
	else:
			break