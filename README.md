<h1>Amazon Top Seller DataScrap Pipeline</h1>


> **Warning**
> <p style="color:red"><b>IT IS NOT FOR COMMERCIAL USE AND DOES NOT INCLUDE ANY SENSITIVE INFORMATION</b></p>
 

<p>This script has been created to scrap top sellers with their links and prices daily with database connection and security flow.</p>
<p>Before using the script be sure you initialize your database following the instructions in the code and provide valid URL from amazon. Provided script uses NoSql database if you are using different database you need to change the code.</p>
<p>For initializing and accessing the database additional credential file is required. structure of the file explained in the code.</p>

<h2>Before Starting:</h2>
<ul>
      <li>👨‍💻 Cross Platform support</li>
      <li>👨‍💻 Different databases are valid for the code</li>
      <li>👨‍💻 Cronjob friendly</li>
      <li>👨‍💻 Supports multi regions for scraping</li>
</ul>

<h2>Usage:</h2>
<p>Using the script is easy simply running index.py file will start the process for getting help use</p>

```python3 index.py --help```

<p>For scraping you need to use <b>--scrape [countryCode]</b> 

```python3 index.py --scrape uk```
  
<p>And for validated country codes you should use <b>--info-country</b></p> 

```python3 index.py --info-country```

<h2>Data Example:</h2>

![dataExample](/assets/dataExample.png)
