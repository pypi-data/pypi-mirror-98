# cleantxt

cleaning text from noise for nlp tasks

## installation 
with pip

`pip install cleantxt`

install from source

`git clone https://github.com/jemiaymen/cleantxt.git`

go to the cleantxt directory

`cd cleantxt`

install with pip

`pip install .`

## usage

import text module

`from cleantxt import text`

clean text

`txt = text.clean_text('mella khaaaaaarya hadddddda mta3 @rassssssssssse la@__mbbbbbbouuutt     tfih')`

print the result

`mella kharya hada mta3 rase lambout tfih`