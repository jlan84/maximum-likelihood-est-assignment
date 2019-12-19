#  Siméon Poisson Meets Willie Nelson
Today we'll be working with a dataset provided by the city of Austin's open data initiative.  In order to give you some extra touches with Spark, we'll ask that you read the data into a Spark DataFrame, and attempt to do the data slicing & aggregation using that framework.

# Steps
## 1. Read in the Data
Create a `SparkSession` object, and read in the csv file. If you're on a docker instance, you'll want to copy the data over there first.  Note, when reading in the data, you'll want to use two keyword arguments, , `header='true',  inferSchema='true'` so that you'll have nice column names.  It will also convert the latitudes and longitudes to floats, even though we won't be using those.

## 2. Create a Date Object Column
We'll be using `PySpark` functions to quickly access various quantities like `dayofmonth`, ect from columns, however, we might still like to be able to differentiate between weekday and weekend behavior.  To do so, create a `udf` to map the "Published Date" string to a `datetime` object.  <a href="https://docs.python.org/3.8/library/datetime.html#strftime-and-strptime-format-codes">This table</a> of format codes for creating `datetime`  might be useful.

## 3. Find Incident Types
We can see that incidents are categorical variables.  Create a list of unique incident types.

## 4. Create a Subsample of the Data
One of the categories you'll have seen is "Loose Livestock".  Since we're all being data wranglers today, lets focus on those incidents only.  Additionally, let's restrict ourselves to 2018, since both the 2017 and 2019 data have missing months.

Once you have done so, you can create an aggregation DataFrame by grouping on month and day of month.  Note, `pyspark.sql.functions` provide vectorized operations that allow you to retrieve both values without having to create new columns.

Create a local python list that is just the resulting daily counts from this aggregation.  Note, that the `collect` method will return an array of `Row` object, so you'll need to map the row object to just the value of interest.  Note, you wont create entries for days on which there are not incidents, so you'll need to zero-pad the array for all days in which no accidents occurred.

## 5.  Perform MLE
The `scipy.stats` module has a class for the Poisson distribution.  If we look at it's functions, we'll note that they provide a `logpmf` function that will give you the log likelihood for a number of observations, given you provide a value for lambda.  We can perform MLE visually by plotting the distribution of the sum of log likelihoods (SLL) as a function of the value of lambda.

To do so, start by writing a function that returns the SLL for a particular value of lambda, and then evaluate this function over an array of lambda values.  

## 6. Check your Results
We're going to check our results in two ways. First, we'll run a Kolmogorov Smirnov test (kstest) to see how good our best fit is. Again, `scipy.stats` provides a class for this.  Note, this can be a little tricky to use so we'll be a little more explicit.

To run this test, we need to provide three arguments.  The first is the list of incident counts, the second, the string `poisson` (this indicates the PMF we're checking against), and the third, is a list of parameters for the distribution.  This list should contain only one value, the parameter value from MLE.

Our second check is visual.  Create a histogram (make sure `density=True`) of the number of daily incidents, as well as the PMF for the Poisson distribution based on the parameter identified by MLE.

## 7. Segment the Data
The previous step should reveal that we don't end up creating a great model here.  Both MLE and the Poisson distribution have baked in assumptions that the data is independent and identically distributed, and that assumption may not be true for such a coarse selection of data.  Let's start by creating separate DataFrames for incidents on the weekend and week days. PySpark does not provide this function, so we will have to create a column using `udf`s.  

Once we've done so, the next two steps are going to be looking at further visualizations of the data.  We're looking to see if segments of the data violate the assumption of the Poisson Distribution, particularly that the time between incidents are independent.  By visualizing slices of the data, we can examine if there are slices that show abnormal variation in the rates that we will see.

## 8. Create Hourly Visualizations
Now that we have segments for the weekends or weekdays, let's look at average numbers of incidents as a function of the hour of day.  Again, you'll need to take care to zero-pad days where no such data exists (you should do this after you've collected to a local python list).

*Hint:* You might also find it useful to rename your aggregation columns so they are easier to work with locally.  PySpark makes this easy with the `withColumnRenamed` method.

*Stretch Goal:* You'll find that in the middle of the day there are no incidents (probably due to laws surrounding moving livestock).  It's tough to compare data when there is a big gap in the middle, so experiment with ways to visualize the data without the gap.

## 9. Look for seasonal Variation
You should also create groupings for the week of the year (`pyspark` does have a function for that).  You'll probably note seasonal effects that you'll want to eliminate.

## 10. Run MLE on a Subset
Look at the distributions from the previous two steps.  Think of cuts that you can make that look like they will make the interval more well behaved (and therefore a better fit for Poisson).  Create a new visualization for the SLL.

## 11. Run Checks Again
Rerun the checks of the K-S test and visualizing your results.  

<b>Important Note</b> - you should absolutely, positively, not continually alter your boundaries till you get a p-value greater than .05 for your KS test.  We know that our alternative hypothesis (that the data is not from the PMF) can occur randomly, so it's OK if you didn't choose a window that causes a viable fit.

The solutions will have a distribution that has a p-value slightly larger than .05, but the visualization will demonstrate that we should still question if this is a good fit.

## Further Investigation
If you have completed all the steps with time remaining, consider different ways of segmenting the data that might cause the intervals to be lower variance as well.  You can also consider looking at hourly groupings instead of daily groupings (but the zero-padding becomes only slightly trickier).