# DEC-Hackathon - The Travel Agency Use Case

This project was created in the spirit of the Data Engineering Community Hackathon by the Data Benders team.

![](DEC-Hackathon/travel-image.jpg)

*Image by [fonsheijnsbroek_amsterdam_photos](https://unsplash.com/@fonsheijnsbroek_amsterdam_photos) on Unsplash*

## Introduction

As a data engineer at a travel agency, you have been tasked with integrating data from a public REST API for countries information. This data will be used to recommend travel destinations to our customers based on some different factors like language, continents, regions, currency and many more.

*Disclaimer: This data was gotten from the [world country api](https://restcountries.com/v3.1/all).*

## Factors Considered While Choosing Tools Used
- Simplicity

- Scalability

- Not time-consuming

- Data Volume

- Data Velocity

- Data Variety

- Cost Effectivenes

## Tools Used

The following tools and skills were used in this project:
* **Python** used for extraction and transformation: Python was used because of the requests library to extract data from APIs and it's ability to transform data especially if the data is not so large as in this usecase.

* **PostgreSQL** for data storage: This was used to store the data for analysis because the data output after transformation is in structured format. This was hosted on a free hosting platform called 'Aiven' to allow remote access. However, in a company setting, it would be advised to host this on the company's cloud. Warehouses like Redshift, BigQuery, etc are not encouraged at this stage because it would be a big solution for a small usecase as this. Considering scalability, postgres can still suffice unless it can no longer handle the company's data at some point in time.

* **Airflow** used for Orchestration: At first, we thought this was an overly technical solution for a usecase like this and thought of using a simple cron job instead. However, we considered that since this was a travel agency, there could be variety of data that could spring up so it was best to start with Airflow since it's open-source and won't incur any extra costs asides the hosting. 

## Data Extraction and Transformation Steps

- Step 1: Fetch Data from the API

- Step 2: Extract Required Fields

    The fields we needed include:
    - Country name
    - Independence status
    - United Nations membership
    - Start of the week
    - Official country name
    - Common native name
    - Currency (code, name, symbol)
    - Country code (concatenate idd root and idd suffix)
    - Capital
    - Region
    - Sub region
    - Languages
    - Area
    - Population
    - Continents

- Step 3: Make Necessary Transformations
    
    The transformations made include:

    - Dropped duplicates
    - Replaced empty strings (null) with None
    - Transformed the continents column to align with the correct country's continenent
    - Split and modeled the data into three dataframes to be inserted into the postgres database: Countries, Country_languages (bridge table) and languages

- Step 4: Load DataFrames to PostgreSQL database


## Questions 

1. How many countries speaks French?
2. How many countries speaks english?
3. How many country have more than 1 official language?
4. How many country official currency is Euro?
5. How many country is from West europe?
6. How many country has not yet gain independence?
7. HHow many distinct continent and how many country from each?
8. How many country whose start of the week is not Monday?
9. How many countries are not a United Nation member?
10. How many countries are United Nation member?
11. Least 2 countries with the lowest population for each continents?
12. Top 2 countries with the largest Area for each continent?
13. Top 5 countries with the largest Area?
14. Top 5 countries with the lowest Area?

## Answers to Stated Questions

### 1. What are the earliest and latest times of the rides?

```sql
SELECT Min(time) AS earliest_time, Max(time) AS latest_time
FROM uber2014
```

**Results**

According to the results, the uber rides went round the clock.

![](Earliest%20and%20Latest%20Time.PNG)


### 2. How many rides were there in each month?

```sql
SELECT TO_CHAR(date, 'Month') AS month, COUNT(*)
FROM uber2014
GROUP BY month
ORDER BY COUNT(*) DESC
```

**Results**

The rides increased as time advanced. This could be a proof that the marketing strategies of Uber are working or customers are satisfied with the services and refer their friends and family. 

![](Rides%20by%20Month.PNG)

### 3. What were the total rides for the top 10 pickup counties?

```sql
SELECT DISTINCT(county), COUNT(*)
FROM uber2014
GROUP BY county
ORDER BY COUNT(*) DESC
LIMIT 10
```

**Results**

For context, New York County and Kings County are the same as Manhattan and Brooklyn respectively. According to the results, Manhattan has the most rides.

![](Top%2010%20Rides%20by%20County.PNG)

Let's do a little comparison with the 2014 New York population in some counties.

![](New%20York%20Population.PNG)

With this comparison, we can't just conclude that Uber is mostly used by the Manhattan people because our data doesn't provide the number of unique users unlike the population census results that is per head count. 

However, I would advise that Uber focuses more on regions that have relatively less population and population density so they won't attract attention from the government that they are causing traffic. These regions could be Bronx, Brooklyn(Kings) and Queens counties in the New York City. 

They can also extend their tentacles outside New York City. 

### 4. What were the total rides for the bottom 10 pickup counties?

```sql
SELECT DISTINCT(county), COUNT(*)
FROM uber2014
GROUP BY county
ORDER BY COUNT(*) 
LIMIT 10
```

**Results**

Depending on the goals of Uber, they could either close down theur services in these regions that have extremely low patronage or strategize on how to increase awareness and take out any competition that might be there. 

![](Bottom%2010%20Rides%20by%20County.PNG)

### 5. What were the total rides for the respective pickup locations?

```sql
SELECT DISTINCT(location), COUNT(*)
FROM uber2014
GROUP BY location
ORDER BY COUNT(*) DESC
```

**Results**

Take note that New York City is in New York State and are somewhat different. New York City comprises five boroughs: Brooklyn (Kings), Queens, Manhattan, the Bronx, and Staten Island (Richmond). 

According to the results, Uber is well known in New York City than other states in United States. 

![](Rides%20by%20Locations.PNG)

### 6. What were the total rides by day?
```sql
SELECT TO_CHAR(date, 'day') AS day, COUNT(*)
FROM uber2014
GROUP BY day
ORDER BY COUNT(*) DESC
```

**Results**

Looking at these results, there's not much gap amongst the total rides for the different days so we can't just outrightly conclude that most people use Uber on certain days. 

![](Rides%20by%20Day.PNG)

### 7. How many vehicles are allocated to the registered base stations and locations?

```sql
SELECT DISTINCT(base_region), base_name, COUNT(*)
FROM uber2014
GROUP BY base_region, base_name
ORDER BY COUNT(*) DESC
```

**Results**

For comtext, let me briefly explain what Base stations mean. 

See Base stations as the administrative houses of the uber riders. Just like how you go to your workplace when you want to answer to a physical meeting hosted by your employer, that's how uber riders see the base stations. 

These base stations provide support to the uber riders, pass information, and also track the movement of the registered riders. 

The base_name are the names for each  company associated with the assigned base codes while base regions are where they are located. 

![](Rides%20by%20Bases.PNG)

### 8. According to your answer in number 7, is it advisable to register more base stations or stick to the already registered base stations?

According to the results, it's obvious that the base stations are only located in New York City. So what about the regions outside New York City(NYC? 

What happens to the uber riders there?

To make informed decisions, it's best to look at how often riders request for support both within and outside NYC and also revise the goals of uber. 

If uber wants to stick to providing services only within NYC, then there's no need to have base stations outside NYC. 

However, if the request for support is high, then it's best to register more base stations outside NYC so that the riders would be satistfied which also increases the number of riders through referrals and indirectly increases the number of those that would also request for rides. 

In this case, it's a win-win for everyone. 

##  Conclusion/Recommendations

This is a quick reminder that this data is data from 2014. Based on the findings from this data, Uber shouldn't rush into decisions to increase the awareness of their services. 

Seeing that their services is in a crucial industry as Transportation, they should ensure that decisions made should be in not just their favour but also the favour of the masses by considering factors like population, population density, request for support from riders, economic state of regions in the US, and many other factors. 

Lastly, the decisions made should not put them in the tight spot with government regarding traffic congestion and security of customers. 