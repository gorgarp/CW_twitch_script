import csv
import os
import sys
import traceback

# path to input csv file
path_to_file = 'input.csv'

def read_csv(csv_inputs):
    """
    :param csv_inputs:
    :return:
    """
    try:
        # checks if csv file exists
        if os.path.exists(csv_inputs):
            with open(csv_inputs, newline='', encoding='utf-8') as f:
                # reads a csv file to the python list
                reader = csv.reader(f, quotechar='"',
                                    delimiter=',',
                                    quoting=csv.QUOTE_ALL,
                                    skipinitialspace=True,
                                    escapechar='\\')
                # coverts all not-empty records to python list except csv header
                data = [x for x in list(reader)[1:] if x]
            return data
        else:
            print("File {} does not exists".format(str(csv_inputs)))
            sys.exit(1)
    except Exception:
        print(traceback.format_exc())
        print("File {} not found or format is wrong".format(csv_inputs))
        sys.exit(1)


def save_file(path, text):
    """
    :param path: path  to save output file
    :param text: text to  save
    :return:
    """
    try:
        # saves python string to .txt file
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        print("Result saved to {}".format(path))
    except Exception:
        print("Exception in save_file: {}".format(str(e)))
        print(traceback.format_exc())


def main():
    """
    :return:
    """
    try:
        # reads csv file to list of lists
        data = read_csv(path_to_file)
        # asks user to enter number
        while True:
            streamamount = input("How many to give away?" )
            # checks if user entered a  number, but not jsut a letter or word
            if not streamamount.isdigit():
                print("Please enter number. Please try again")
                # if input is not valid - we need to try again
                continue
            # if  input is correct we need to move on:)
            break
        # pattern for each line in output file, means $tip "name" "payoutamount" coins and payoutamount is limited ny 2 decimals
        pattern = '$tip {} {:0.2f} flux'
        # lsit to store all the lines, like $tip "name" "payoutamount" coins
        result_lines = []

        # step 1 - we need to define the 'total' for each user
        for line in data:
            # loyalty and messages from string, like 1000,56.00 to python float
            loyalty = float(line[1].replace(',', ''))
            messages = float(line[2].replace(',', ''))
            # calculates total Loyalty is 1 point per point in the field. Messages is .2 points per point in the field
            total = loyalty + messages * 15
            line.append(total)
        # calculate the totals of the all users
        total_all_records = sum([x[3] for x in data])
        print("all users totals: {:0.2f}".format(total_all_records))

        # calculate coins for each user and adds to 'result_lines' list
        for line in data:
            user_percent = line[3] / total_all_records
            result_lines.append(pattern.format(line[0], user_percent * int(streamamount)))

        # joins all list via new line character and saves to file
        save_file('output_message1to15.txt', '\n'.join(result_lines))

    except Exception as e:
        print("Exception in main: {}".format(str(e)))
        print(traceback.format_exc())


# start point of the script

# we should check if the method is main to call it from other scripts and threds
if __name__ == '__main__':
    main()
