
# Analyzing water comsuption using data from Yorkshire Water


Improving on a project that was a part of my data analysis studies.

Data consists of the following two publicly available files from [datamillnorth.org](https://datamillnorth.org), licensed under [Open Data Commons Attribution License (ODC-By)](https://opendatacommons.org/licenses/by/1-0/):

* [Daily customer meter data - local area study](https://datamillnorth.org/dataset/yorkshire-water-daily-customer-meter-data--local-area-) ([direct link](https://datamillnorth.org/download/yorkshire-water-daily-customer-meter-data--local-area-/fb01ce66-423a-4111-9065-d989bdf0b3ce/Daily%20m3%201315.csv))
* [Water usage survey](https://datamillnorth.org/dataset/water-usage-survey) ([direct link](https://datamillnorth.org/download/water-usage-survey/64ce97ab-3cdc-4afc-8202-a4d510f44962/Yorkshire%20Water%20consumer%20habits.csv))


### Water usage survey data


The water usage survey data contains 13 819 anonymised responses from customers, compiled from December 2018 to March 2020. Among the survey results are answers to questions such as how many people live in the household, how many showers are in the household, how many times per week is washing machine used, and are there any significant leaks. In addition, the data contains information about the yearly water comsumption of households.

Notebook [habits_regression.ipynb](habits_regression.ipynb) applies a linear regression model to try to explain household water comsuption using the answers to the survey questions.

### Daily water meter data

The daily customer meter data contains water comsumption readings (in m<sup>3</sup>) from March 24th 2013 to April 22nd 2015. Additionally, data shows (anonymised) property identifier (1-2160), meter location (internal or external) and distribution management area (1 or 2).

As we can see from the graph below, readings from DMA 1 span a lot shorter time and they are fewer in number compared to readings from DMA 2.

![Number of measurements in different areas each day](img/num_of_measuremens.png)

<!-- <figure>
<img src="img/num_of_measuremens.png">
<figcaption>Figure 1</figcaption>
</figure> -->


Earlier, as part of my studies, I did the following analyses (in Finnish):
* [kmeans.ipynb](old_notes/kmeans.ipynb)
* [aikasarja_analyysi.ipynb](old_notes/aikasarja_analyysi.ipynb)

