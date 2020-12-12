# Import
import twint

# From
#from pyspark.sql import SparkSession
#from optimus import Optimus

# SPARK: Session
#spark = SparkSession.builder.appName('optimus').getOrCreate()
#op = Optimus(spark)

# TWINT: Config
c = twint.Config()

# TWINT: CSV Storage. Use only one "c.Storage_" and comment bellow.
#c.Store_csv = True                     #   Store_csv       (bool)      Set to True to write as a csv file
#c.Output = "renuncia_01.csv"           #   Output          (string)    Name of the output file
#
# TWINT: JSON Storage. Use only one "c.Storage_" and comment above.
c.Store_json = True                    #   Store_csv       (bool)      Set to True to write as a json file
c.Output = "scraped_tweet/renuncia_test_01.json"     #   Output          (string)    Name of the output file

# Time
c.Since = "2020-12-01 00:00:00"        #   Since           (string)    Filter Tweets sent since date (Example: 2017-12-27 00:00:00)
c.Until = "2020-12-02 00:00:00"        #   Until           (string)    Filter Tweets sent until date (Example: 2017-12-31 00:00:00)
#c.Timedelta = "7"                      #   Timedelta       (int)       Time interval for every request (days)
#c.Year = "2020"                        #   Year            (string)    Filter Tweets before the specified year

# TWINT: Language
c.Lang = "es"                          #   Lang            (string)    Compatible language codes: https://github.com/twintproject/twint/wiki/Langauge-codes

# TWINT: Hashtag, Phrase, Keyword
c.Search = "#RenunciaPiñera"           #   Search          (string)    Search terms

# TWINT: User
#c.Username = "yeiyeiyei"               #   Username        (string)    Twitter user's username
#c.User_id = "14910859"                 #   User_id         (string)    Twitter user's user_id
#c.User_full = True                     #   User_full       (bool)      Set to True to display full user information. By default, only usernames are shown.

# TWINT: Geo (Plaza Dignidad)
#c.Geo = "-33.4631754,-70.5896814,1km"  #   Geo             (string)    Geo coordinates (lat,lon,5km/5mi)
#c.Location = True                      #   Location        (bool)      Set to True to attempt to grab a Twitter user's location (slow)
#c.Near = "Santiago"                    #   Near            (string)    Near a certain City (Example: london)

# TWINT: Tweets
#c.Email = True                         # Email             (bool)      Set to True to show Tweets that _might_ contain emails.
#c.Phone = True                         # Phone             (bool)      Set to True to show Tweets that _might_ contain phone numbers.
#c.Verified = True                      # Verified          (bool)      Set to True to only show Tweets by _verified_ users

# TWINT: Pandas
c.Store_pandas = True
c.Pandas = True                        # Pandas            (bool)      Enable Pandas integration.

# TWINT:
c.Count = True
c.Debug = True
#c.Elasticsearch = ""                   #   Elasticsearch   (string)    Elasticsearch instance
#

# TWINT: Search
twint.run.Search(c)
