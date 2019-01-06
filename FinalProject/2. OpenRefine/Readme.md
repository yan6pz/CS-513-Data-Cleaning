## Data Cleaning with OpenRefine

### farmersmarket.csv
##### Yan Shterev

**FMID** :

	1.	Verify FMID contains only unique values:
		1.1.	Sort the values in FMID.
		1.2.	Blank down and verify that 0 cells were blanked down.
		
**City, Country, State** :
	
	1.	Remove the special characters - *% @  # ! \ [ ] ( ) ? '* using value.replace(/%@#!\\\[\]\(\)\?/,"")
	2.	Trim leading and trailing white spaces and collapse consecutive white spaces. 
	3.	Make a facet and perform the cluster operation using the *key-collison* method and *fingerprint* function. Merge the relevant clusters. 

	

**Season1Date** :
	1.	Remove the special characters - *% @  # ! \ [ ] ( ) ? '* using value.replace(/%@#!\\\[\]\(\)\?/,"")
	1.	Split the column values using * to * as separator, we get 2 columns as a result. 
	2.	Rename the first column as *Season1DateStart* and second column as *Season1DateEnd*.
	3. 	Convert the values in the column to ISO 'd/M/y' format using value.toDate('d/M/y').
	4. 	Repeat 1, 2 and 3 for *Season2Date*, *Season3Date* and *Season4Date*.
	
	
**Season1Time** :
	1.	Remove the special characters - *% @  # ! \ [ ] ( ) ? '* using value.replace(/%@#!\\\[\]\(\)\?/,"")
	1.	Split the column values using *;* as separator. Each of the new columns will represent values for given day of the week. 
	2. 	Repeat 1 for *Season2Time*, *Season3Time* and *Season4Time*.
	

**updateTime** :

	1.	Convert the values in the column to ISO 'd/M/y H:m:s' format using value.toDate('d/M/y H:m:s'). 










