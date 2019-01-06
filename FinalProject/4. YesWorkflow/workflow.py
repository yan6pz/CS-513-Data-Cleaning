# @begin DataCleanup  @desc Workflow for cleaning farmersmarket DataSet
# @in farmersmarket.csv  @uri file://initialdata/farmersmarket.csv

#     @out markets  @uri sqlite://database.db/markets
#     @out seasondates  @uri file://initialdata/seasondates
#     @out seasontimes  @uri file://initialdata/seasontimes
#     @out states  @uri file://initialdata/states
#     @out countries  @uri file://initialdata/countries
#     @out cities  @uri file://initialdata/cities
#     @out facebook  @uri file://initialdata/facebook
#     @out othermedia  @uri file://initialdata/othermedia
#     @out website  @uri file://initialdata/website

#     @begin SplitFarmersMarketWithOpenRefine  @desc Use OpenRefine to split FarmersMarket.csv
#     @in farmersmarket.csv  @uri file://initialdata/farmersmarket.csv
#     @out markets_extract.csv  @uri file://initialdata/market_extract.csv
#     @out seasondates_extract.csv  @uri file://initialdata/seasondates_extract.csv
#     @out seasontimes_extract.csv  @uri file://initialdata/seasontimes_extract.csv
#     @out states_extract.csv  @uri file://initialdata/states_extract.csv
#     @out countries_extract.csv  @uri file://initialdata/countries_extract.csv
#     @out cities_extract.csv  @uri file://initialdata/cities_extract.csv
#     @out facebook_extract.csv  @uri file://initialdata/facebook_extract.csv
#     @out othermedia_extract.csv  @uri file://initialdata/othermedia_extract.csv
#     @out website_extract.csv  @uri file://initialdata/website_extract.csv
#     @end SplitFarmersMarketWithOpenRefine
	 
#     @begin CleanMarketsWithOpenRefine  @desc Use OpenRefine to Clean Markets.csv
#     @in  markets_extract.csv  @uri file://initialdata/market_extract.csv
#     @param marketCleanionOperationsSequence
#     @out market_Clean.csv  @uri file://initialdata/market_Clean.csv
#     @end CleanMarketsWithOpenRefine

#     @begin ExtractCitiesWithOpenRefine  @desc Use OpenRefine to Clean cities.csv
#     @in cities_extract.csv  @uri file://initialdata/cities_extract.csv
#     @param citiesCleanionOperationsSequence
#     @out cities_Clean.csv  @uri file://initialdata/cities_Clean.csv
#     @end CleanCitiesWithOpenRefine

#     @begin CleanCountriesWithOpenRefine  @desc Use OpenRefine to Clean countries.csv
#     @in countries_extract.csv  @uri file://initialdata/countries_extract.csv
#     @param countriesCleanionOperationsSequence
#     @out countries_Clean.csv  @uri file://initialdata/countries_Clean.csv
#     @end CleanCountriesWithOpenRefine

#     @begin CleanStatesWithOpenRefine  @desc Use OpenRefine to Clean states.csv
#     @in states_extract.csv  @uri file://initialdata/states_extract.csv
#     @param statesCleanionOperationsSequence
#     @out states_Clean.csv  @uri file://initialdata/states_Clean.csv
#     @end CleanStatesWithOpenRefine

#     @begin CleanFacebookWithOpenRefine  @desc Use OpenRefine to Clean facebook.csv
#     @in facebook_extract.csv  @uri file://initialdata/facebook_extract.csv
#     @param facebookCleanionOperationsSequence
#     @out facebook_Clean.csv  @uri file://initialdata/facebook_Clean.csv
#     @end CleanFacebookWithOpenRefine

#     @begin CleanothermediaWithOpenRefine  @desc Use OpenRefine to Clean othermedia.csv
#     @in othermedia_extract.csv  @uri file://initialdata/othermedia_extract.csv
#     @param othermediaCleanionOperationsSequence
#     @out othermedia_Clean.csv  @uri file://initialdata/othermedia_Clean.csv
#     @end CleanothermediaWithOpenRefine

#     @begin CleanwebsiteWithOpenRefine  @desc Use OpenRefine to Clean website.csv
#     @in website_extract.csv  @uri file://initialdata/website_extract.csv
#     @param websiteCleanionOperationsSequence
#     @out website_Clean.csv  @uri file://initialdata/website_Clean.csv
#     @end CleanwebsiteWithOpenRefine

#     @begin CleanseasondatesWithOpenRefine  @desc Use OpenRefine to Clean seasondates.csv
#     @in seasondates_extract.csv  @uri file://initialdata/seasondates_extract.csv
#     @param seasondatesCleanionOperationsSequence
#     @out seasondates_Clean.csv  @uri file://initialdata/seasondates_Clean.csv
#     @end CleanseasondatesWithOpenRefine

#     @begin CleanseasontimesWithOpenRefine  @desc Use OpenRefine to Clean times.csv
#     @in seasontimes_extract.csv  @uri file://initialdata/seasontimes_extract.csv
#     @param seasontimesCleanionOperationsSequence
#     @out seasontimes_Clean.csv  @uri file://initialdata/times_Clean.csv
#     @end CleanseasontimesWithOpenRefine

	

#     @begin SQLOperationsOnMarkets  @desc Use SQLLite to load market_clean.csv into table Markets
#     @in market_Clean.csv  @uri file://initialdata/market_Clean.csv
#     @param marketLoadingSQLScript
#     @out Markets  @uri sqlite://database.db/Markets
#     @end SQLOperationsOnMarkets

#     @begin SQLOperationsOnCities  @desc Use SQLLite to load cities_clean.csv into table cities
#     @in cities_Clean.csv  @uri file://initialdata/cities_Clean.csv
#     @param citiesLoadingSQLScript
#     @out Cities  @uri sqlite://database.db/Cities
#     @end SQLOperationsOnCities

#     @begin SQLOperationsOnCountries  @desc Use SQLLite to load countries_clean.csv into table countries
#     @in countries_Clean.csv  @uri file://initialdata/countries_Clean.csv
#     @param countriesLoadingSQLScript
#     @out Countries  @uri sqlite://database.db/Countries
#     @end SQLOperationsOnCountries

#     @begin SQLOperationsOnStates  @desc Use SQLLite to load states_clean.csv into table states
#     @in states_Clean.csv  @uri file://initialdata/states_Clean.csv
#     @param statesLoadingSQLScript
#     @out States  @uri sqlite://database.db/States
#     @end SQLOperationsOnStates

#     @begin SQLOperationsOnFacebook  @desc Use SQLLite to load facebook_clean.csv into table facebook
#     @in facebook_Clean.csv  @uri file://initialdata/facebook_Clean.csv
#     @param facebookLoadingSQLScript
#     @out Facebook  @uri sqlite://database.db/Facebook
#     @end SQLOperationsOnFacebook

#     @begin SQLOperationsOnMedia  @desc Use SQLLite to load othermedia_clean.csv into table othermedia
#     @in othermedia_Clean.csv  @uri file://initialdata/othermedia_Clean.csv
#     @param otherMediaLoadingSQLScript
#     @out Othermedia  @uri sqlite://database.db/Othermedia
#     @end SQLOperationsOnMedia

#     @begin SQLOperationsOnWebsite  @desc Use SQLLite to load website_clean.csv into table website
#     @in website_Clean.csv  @uri file://initialdata/website_Clean.csv
#     @param websiteLoadingSQLScript
#     @out Website  @uri sqlite://database.db/Website
#     @end SQLOperationsOnWebsite

#     @begin SQLOperationsOnseasondates  @desc Use SQLLite to load seasondates_clean.csv into table seasondates
#     @in seasondates_Clean.csv  @uri file://initialdata/seasondates_Clean.csv
#     @param seasondatesLoadingSQLScript
#     @out Seasondates  @uri sqlite://database.db/Seasondates
#     @end SQLOperationsOnseasondates

#     @begin SQLOperationsOnseasontimes  @desc Use SQLLite to load times_clean.csv into table seasontimes
#     @in seasontimes_Clean.csv  @uri file://initialdata/times_Clean.csv
#     @param seasontimesLoadingSQLScript
#     @out Seasontimes  @uri sqlite://database.db/Seasontimes
#     @end SQLOperationsOnseasontimes


#     @begin SQLConstraintsCheck  @desc Use SQL to check integrity constraints and functional dependencies
#     @in Markets  @uri sqlite://database.db/Markets
#     @in Cities  @uri sqlite://database.db/Cities
#     @in Countries  @uri sqlite://database.db/Countries
#     @in States  @uri sqlite://database.db/States
#     @in Facebook  @uri sqlite://database.db/Facebook
#     @in Othermedia  @uri sqlite://database.db/Othermedia
#     @in Website  @uri sqlite://database.db/Website
#     @in Seasondates  @uri sqlite://database.db/Seasondates
#     @in Seasontimes  @uri sqlite://database.db/Seasontimes
#     @param IntegrityConstraintsANDFunctionalDependenciesScript
#     @out markets  @uri sqlite://database.db/markets
#     @out cities  @uri sqlite://database.db/cities
#     @out countries  @uri sqlite://database.db/countries
#     @out states  @uri sqlite://database.db/states
#     @out facebook  @uri sqlite://database.db/facebook
#     @out othermedia  @uri sqlite://database.db/othermedia
#     @out website  @uri sqlite://database.db/website
#     @out seasondates  @uri sqlite://database.db/seasondates
#     @out seasontimes  @uri sqlite://database.db/seasontimes
#     @end SQLConstraintsCheck

# @end DataCleanup
