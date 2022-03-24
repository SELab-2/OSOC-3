## General information

In this folder there are two examples of the data we will receive from the Tally form.
The `manual_test_tally.json` was created by manually filling in the form, and the `auto_test_tally.json` was an automated test submisson by Tally.

To fill in the form for yourself: go to https://tally.so/r/wkjyM3

## Form structure

The data is structured as a `JSON` file. 
The `data` field contains all the general information about the form. The `fields` field inside the data field is a list containing information about every question. 

Every question has a (unique) `key` and a `label` containing the actual question. There is also a `type` field that specifies the type of question (text, multiple choice,...). The `value` field contains the answer to the question.

For multiple choice questions, the value will contain an  `id` that will correlate with the selected answer from the `options` field.

For checkbox questions, the value can contain multiple, comma separated `id`s that will again tell which answers have been clicked.

There are other possible types of questions, such as uploading your CV, etc. Just have a look at the examples to see how these are structured.







