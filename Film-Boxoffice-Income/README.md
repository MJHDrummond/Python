# Film-Boxoffice-Income
- Project start date: 16 October 2017.
- End date: 3 November 2017.
- Upload date: 20 November 2017.
#

Joint project with colleague during the Big Data and Business Intelligence Traineeship.

Our goal was to choose a business case and implement the skills and tools developed during the traineeship. We choose to investigate and analyse the film weekend boxoffice income for The Netherlands from 2003 to the present day.

Step 1: We first had to identify and retrieve the required data which we accomplished by creating APIs to download the [boxoffice data](http://boxofficenl.net/) and specific [film details](https://www.themoviedb.org/?language=en). [Weather data](http://www.knmi.nl/home) was also downloaded to investigate any possible correlations of weather and income.
Step 2: In order to couple these datasets a great deal of cleansing had to take place due to the high number of duplicate film entries in the film details dataset. The majority of the allotted project time was taken up by this stage.
Step 3: Finally the analysis could take place where we investigated correlations, specific film genre income and implemented time series analysis to determine any trends or seasonality in the film income.

We concluded that since 2003 there has been an overall increase in popularity of the cinema reflected in the increased boxoffice income. The top 3 best selling genres are adventure, animation and fantasy. There is no strict correlation between the weather and film income but it can be said that during extreme weather variations, such as heavy rain, very high wind speeds, freezing temperatures or very high temperatures, then film income decreases. Finally, the highest film incomes occur during the christmas vacation period and the lowest during the summer period.

If you see any bugs or have any suggestions for improvement when looking through the scripts please feel free to let me know.

Thanks!
