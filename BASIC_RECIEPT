# This file is under the property of John Lloyd P. Landicho
# All of this was uploaded on GitHub.
# github.com/johnlloydpenamante

# Variables and value na given sa instruction
venue_rental = 3500.0
sound_system = 2500.0
decoration = 1800.0

# Gastos kada tao.
food_rate = 85.0
drinks_rate = 25.0
kit_rate = 40.0

# Given value ng sponsorship na kasama sa ibabawas mamaya sa subtotal
base_sponsorship = 5000.0

# User Inputs
num_participants = int(input("Enter total number of participants: "))
num_sponsors = int(input("Enter total number of sponsors: "))

# ito yung input for sponsors
sponsors = float(input("Enter the total amount of donations from Sponsors: "))

# Total Sponsorship na nakuha namin sa event
sponsorship = sponsors
total_sponsorship = base_sponsorship + sponsorship

# Formula ng gastos kada participants
total_food = food_rate * num_participants
total_drinks = drinks_rate * num_participants
total_kits = kit_rate * num_participants

# Budget Totals
gross_expenses = venue_rental + sound_system + decoration + total_food + total_drinks + total_kits
subtotal = gross_expenses - total_sponsorship
contingency_fund = subtotal * 0.10
final_total_budget = subtotal + contingency_fund

# mula sa line nato guys ay yung OUTPUT neto guys.

# kung naguguluhan kayo sa design dedma nyo nalangs output lang naman to

#yung design na ginamit ko kasi is yung ASCII standard table design, so pag d kayo familiar sa ASCII dont mind it nalang

line = "+" + "-" * 32 + "+" + "-" * 10 + "+"

print("\n" + "\t" +line)
print(f"\t|\t    {'BSIT - 1A CCS EVENT':^48}|")
print("\t"+line)
print(f"\t| {'Category / Item':<30} | {'Amount (P)':>13} |")


print("\t"+line)
print(f"\t| {'Food':<30}\t | {total_food:>13,.2f} |")
print(f"\t| {'Drinks':<30}\t| {total_drinks:>13,.2f}\t|")
print(f"\t| {'Event Kits':<30}\t | {total_kits:>13,.2f} |")
print(f"\t| {'Venue Rental':<30}\t | {venue_rental:>13,.2f} |")
print(f"\t| {'Sound System':<30}\t | {sound_system:>13,.2f} |")
print(f"\t| {'Decoration':<30}\t | {decoration:>13,.2f} |")


print("\t" + line)
print(f"\t| {'Gross Expenses':<30}\t   | {gross_expenses:>13,.2f} |")
print(f"\t| {'Base Sponsorship'}\t   \t\t  | {-base_sponsorship:>13,.2f} |")
print(f"\t| {'Additional Sponsorships'}\t\t\t | {-sponsorship:.2f} |")
print(f"\t| {'Total Sponsorship Deducted\t\t':<30}\t|{ -total_sponsorship:.2f}|")


print("\t" + line)
print(f"\t| {'Subtotal'}\t\t\t\t\t| {subtotal:.2f}|")
print(f"\t| {'Contingency (10%)'}\t\t\t| {contingency_fund:.2f} |")
print("\t"+line)
print(f"\t| {'FINAL TOTAL BUDGET REQUIRED':<30} \t| {final_total_budget:>13,.2f} \t\t\t|")
print("\t"+line)