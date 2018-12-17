#!/usr/bin/env bash

input=$(cat resources/day5_input)

# construct the sed command we'll use to polymerize letter pairs
pairs=$(echo -n 'abcdefghijklmnopqrstuvwxyz' | sed 's/[[:lower:]]/&\U&|\U&\L&|/g' | sed 's/|$//')
final=$(echo $input | sed -E -e ':loop' -e "s/$pairs//g" -e 't loop')

echo $(echo -n $final | wc -c)

# Now, to find the most troublesome letter...
for letter in a b c d e f g h i j k l m n o p q r s t u v w x y z
do
    final_without_letter=$(echo $final | sed "s/$letter//gI" | sed -E -e ':loop' -e "s/$pairs//g" -e 't loop')
    echo $(echo -n $final_without_letter | wc -c) $letter >> day5_results.txt
done

sort -n day5_results.txt | head -n1
