from cgi import test
from lib2to3.pgen2.token import EQUAL
from math import nan
from statistics import mean, multimode
import numpy as np
from matplotlib import pyplot as plt

from prepare_data import *

def compute_death_rate_first_100_days(n_cases_cumulative, n_deaths_cumulative):
    '''
    Computes the average number of deaths recorded for every confirmed case
    that is recorded from the first day to the 100th day (inclusive).
    Parameters
    ----------
    n_cases_cumulative: np.ndarray
        2D `ndarray` with each row representing the data of a country, and the columns
        of each row representing the time series data of the cumulative number of
        confirmed cases in that country, i.e. the ith row of `n_cases_cumulative`
        contains the data of the ith country, and the (i, j) entry of
        `n_cases_cumulative` is the cumulative number of confirmed cases on the
        (j + 1)th day in the ith country.
    n_deaths_cumulative: np.ndarray
        2D `ndarray` with each row representing the data of a country, and the columns
        of each row representing the time series data of the cumulative number of
        confirmed deaths (as a result of COVID-19) in that country, i.e. the ith
        row of `n_deaths_cumulative` contains the data of the ith country, and
        the (i, j) entry of `n_deaths_cumulative` is the cumulative number of
        confirmed deaths on the (j + 1)th day in the ith country.
    
    Returns
    -------
    Average number of deaths recorded for every confirmed case from the first day
    to the 100th day (inclusive) for each country as an `ndarray` such that the
    entry in the ith row corresponds to the death rate in the ith country as
    represented in `n_cases_cumulative` and `n_deaths_cumulative`.
    Note
    ----
    `n_cases_cumulative` and `n_deaths_cumulative` are such that the ith row in the 
    former and that in the latter contain data of the same country. In addition,
    if there are no confirmed cases for a particular country, the expected death
    rate for that country should be zero. (Hint: to deal with NaN look at
    `np.nan_to_num`)
    '''
    n_deaths_cumulative_100 = n_deaths_cumulative[:, 0:100]
    n_cases_cumulative_100 = n_cases_cumulative[:, 0:100]
    death_rate_by_day = np.divide(n_deaths_cumulative_100, n_cases_cumulative_100, out=np.zeros_like(n_deaths_cumulative_100), where=n_cases_cumulative_100!=0)
    ave_death_rate = np.ravel(death_rate_by_day[:, 99:100])
    return ave_death_rate


def compute_increase_in_cases(n_cases_cumulative):
  '''
  Computes the daily increase in confirmed cases for each country, starting
  from the first day.

  Parameters
  ----------
  n_cases_cumulative: np.ndarray
    2D `ndarray` with each row representing the data of a country, and the columns
    of each row representing the time series data of the cumulative number of
    confirmed cases in that country, i.e. the ith row of `n_cases_cumulative`
    contains the data of the ith country, and the (i, j) entry of
    `n_cases_cumulative` is the cumulative number of confirmed cases on the
    (j + 1)th day in the ith country.
  
  Returns
  -------
  Daily increase in cases for each country as a 2D `ndarray` such that the (i, j)
  entry corresponds to the increase in confirmed cases in the ith country on
  the (j + 1)th day, where j is non-negative.

  Note
  ----
  The number of cases on the zeroth day is assumed to be 0, and we want to
  compute the daily increase in cases starting from the first day.
  '''

  
  return np.diff(n_cases_cumulative, prepend=0)

def find_max_increase_in_cases(n_cases_increase):
  '''
  Finds the maximum daily increase in confirmed cases for each country.

  Parameters
  ----------
  n_cases_increase: np.ndarray
    2D `ndarray` with each row representing the data of a country, and the columns
    of each row representing the time series data of the daily increase in the
    number of confirmed cases in that country, i.e. the ith row of 
    `n_cases_increase` contains the data of the ith country, and the (i, j) entry of
    `n_cases_increase` is the daily increase in the number of confirmed cases on the
    (j + 1)th day in the ith country.
  
  Returns
  -------
  Maximum daily increase in cases for each country as a 1D `ndarray` such that the
  ith entry corresponds to the increase in confirmed cases in the ith country as
  represented in `n_cases_increase`.
  '''
  return np.amax(n_cases_increase, axis = 1)
  
def compute_n_masks_purchaseable(healthcare_spending, mask_prices):
    '''
    Computes the total number of masks that each country can purchase if she
    spends all her emergency healthcare spending on masks.
    Parameters
    ----------
    healthcare_spending: np.ndarray
        2D `ndarray` with each row representing the data of a country, and the columns
        of each row representing the time series data of the emergency healthcare
        spending made by that country, i.e. the ith row of `healthcare_spending`
        contains the data of the ith country, and the (i, j) entry of
        `healthcare_spending` is the amount which the ith country spent on healthcare
        on (j + 1)th day.
    mask_prices: np.ndarray
        1D `ndarray` such that the jth entry represents the cost of 100 masks on the
        (j + 1)th day.
    
    Returns
    -------
    Total number of masks which each country can purchase as a 1D `ndarray` such
    that the ith entry corresponds to the total number of masks purchaseable by the
    ith country as represented in `healthcare_spending`.
    Note
    ----
    The masks can only be bought in batches of 100s.
    '''
    return np.sum(np.floor(healthcare_spending / mask_prices), axis=1) * 100

def compute_stringency_index(stringency_values):
  '''
  Computes the daily stringency index for each country.

  Parameters
  ----------
  stringency_values: np.ndarray
    3D `ndarray` with each row representing the data of a country, and the columns
    of each row representing the time series data of the stringency values as a
    vector. To be specific, on each day, there are four different stringency
    values for 'school closing', 'workplace closing', 'stay at home requirements'
    and 'international travel controls', respectively. For instance, the (i, j, 0)
    entry represents the `school closing` stringency value for the ith country
    on the (j + 1)th day.
  
  Returns
  -------
  Daily stringency index for each country as a 2D `ndarray` such that the (i, j)
  entry corresponds to the stringency index in the ith country on the (j + 1)th
  day.

  In this case, we shall assume that 'stay at home requirements' is the most
  restrictive regulation among the other regulations, 'international travel
  controls' is more restrictive than 'school closing' and 'workplace closing',
  and 'school closing' and 'workplace closing' are equally restrictive. Thus,
  to compute the stringency index, we shall weigh each stringency value by 1,
  1, 3 and 2 for 'school closing', 'workplace closing', 'stay at home
  requirements' and 'international travel controls', respectively. Then, the 
  index for the ith country on the (j + 1)th day is given by
  `stringency_values[i, j, 0] + stringency_values[i, j, 1] +
  3 * stringency_values[i, j, 2] + 2 * stringency_values[i, j, 3]`.

  Note
  ----
  Use matrix operations and broadcasting to complete this question. Please do
  not use iterative approaches like for-loops.
  '''
  mult_matrix = np.array([1, 1, 3, 2])
  return stringency_values @ mult_matrix

def average_increase_in_cases(n_cases_increase, n_adj_entries_avg=7):
  '''
  Averages the increase in cases for each day using data from the previous
  `n_adj_entries_avg` number of days and the next `n_adj_entries_avg` number
  of days.

  Parameters
  ----------
  n_cases_increase: np.ndarray
    2D `ndarray` with each row representing the data of a country, and the columns
    of each row representing the time series data of the daily increase in the
    number of confirmed cases in that country, i.e. the ith row of 
    `n_cases_increase` contains the data of the ith country, and the (i, j) entry of
    `n_cases_increase` is the daily increase in the number of confirmed cases on the
    (j + 1)th day in the ith country.
  n_adj_entries_avg: int
    Number of days from which data will be used to compute the average increase
    in cases. This should be a positive integer.
  
  Returns
  -------
  Mean increase in cases for each day, using data from the previous
  `n_adj_entries_avg` number of days and the next `n_adj_entries_avg` number
  of days, as a 2D `ndarray` such that the (i, j) entry represents the
  average increase in daily cases on the (j + 1)th day in the ith country,
  rounded down to the smallest integer.
  
  The average increase in cases for a particular country on the (j + 1)th day
  is given by the mean of the daily increase in cases over the interval
  [-`n_adj_entries_avg` + j, `n_adj_entries_avg` + j]. (Note: this interval
  includes the endpoints).

  Note
  ----
  Since this computation requires data from the previous `n_adj_entries_avg`
  number of days and the next `n_adj_entries_avg` number of days, it is not
  possible to compute the average for the first and last `n_adj_entries_avg`
  number of days. Therefore, set the average increase in cases for these days
  to `np.nan` for all countries.
  '''
  n = n_adj_entries_avg
  cumsum_arr = np.cumsum(n_cases_increase, axis=1, dtype=int)
  minus_arr_a = cumsum_arr[:, n * 2:]
  minus_arr_b = np.concatenate((np.zeros((len(n_cases_increase), 1)), cumsum_arr[:, :n * -2 - 1]), axis = 1)
  result = np.full(((len(n_cases_increase), len(n_cases_increase[0]))), np.nan)
  result[:, n:-n] = np.floor((minus_arr_a - minus_arr_b) / (n * 2 + 1))
  return result

def is_peak(n_cases_increase_avg, n_adj_entries_peak=7):
  '''
  Determines whether the (j + 1)th day was a day when the increase in cases
  peaked in the ith country.

  Parameters
  ----------
  n_cases_increase_avg: np.ndarray
    2D `ndarray` with each row representing the data of a country, and the columns
    of each row representing the time series data of the average daily increase in the
    number of confirmed cases in that country, i.e. the ith row of 
    `n_cases_increase` contains the data of the ith country, and the (i, j) entry of
    `n_cases_increase` is the average daily increase in the number of confirmed
    cases on the (j + 1)th day in the ith country. In this case, the 'average'
    is computed using the output from `average_increase_in_cases`.
  n_adj_entries_peak: int
    Number of days that determines the size of the window in which peaks are
    to be detected. 
  
  Returns
  -------
  2D `ndarray` with the (i, j) entry indicating whether there is a peak in the
  daily increase in cases on the (j + 1)th day in the ith country.

  Suppose `a` is the average daily increase in cases, with the (i, j) entry
  indicating the average increase in cases on the (j + 1)th day in the ith
  country. Moreover, let `n_adj_entries_peak` be denoted by `m`.

  In addition, an increase on the (j + 1)th day is deemed significant in the
  ith country if `a[i, j]` is greater than 10 percent of the mean of all
  average daily increases in the country.

  Now, to determine whether there is a peak on the (j + 1)th day in the ith
  country, check whether `a[i, j]` is maximum in {`a[i, j - m]`, `a[i, j - m + 1]`,
  ..., `a[i, j + m - 1]`, `a[i, j + m]`}. If it is and `a[i, j]` is significant,
  then there is a peak on the (j + 1)th day in the ith country; otherwise,
  there is no peak.

  Note
  ----
  Let d = `n_adj_entries_avg` + `n_adj_entries_peak`, where `n_adj_entries_avg`
  is that used to compute `n_cases_increase_avg`. Observe that it is not
  possible to detect a peak in the first and last d days, i.e. these days should
  not be peaks.
  
  As described in `average_increase_in_cases`, to compute the average daily
  increase, we need data from the previous and the next `n_adj_entries_avg`
  number of days. Hence, we won't have an average for these days, precluding
  the computation of peaks during the first and last `n_adj_entries_avg` days.

  Moreover, similar to `average_increase_in_cases`, we need the data over the
  interval [-`n_adj_entries_peak` + j, `n_adj_entries_peak` + j] to determine
  whether the (j + 1)th day is a peak.

  Hint: to determine `n_adj_entries_avg` from `n_cases_increase_avg`,
  `np.count_nonzero` and `np.isnan` may be helpful.
  '''
  count_nan = np.count_nonzero(np.isnan(n_cases_increase_avg[0]))
  n_adj_entries_avg = int(count_nan / 2)
  rows = len(n_cases_increase_avg)
  cols = len(n_cases_increase_avg[0])
  
  # Calculate if significant
  sig_threshold_arr = np.nansum(n_cases_increase_avg, axis=1) / ((cols - count_nan) * 10)
  is_sig_arr = n_cases_increase_avg > sig_threshold_arr[:, None]
  
  # Calculate if maximum
  slide_arr = np.lib.stride_tricks.sliding_window_view(n_cases_increase_avg[:, n_adj_entries_avg:-n_adj_entries_avg], n_adj_entries_peak * 2 + 1 ,axis=1)
  half_slide_arr = np.lib.stride_tricks.sliding_window_view(n_cases_increase_avg[:,n_adj_entries_avg:-n_adj_entries_peak-n_adj_entries_avg-1], n_adj_entries_peak, axis=1)
  max_arr = np.full((rows, cols), 0)
  calculated_max = np.nanmax(slide_arr, axis = 2)
  max_arr[:, n_adj_entries_peak+n_adj_entries_avg:-n_adj_entries_peak-n_adj_entries_avg] = calculated_max
  is_new_arr = np.full((rows, cols), False)
  calculated_is_new_arr = ~np.any(np.equal(half_slide_arr, np.reshape(calculated_max, (len(calculated_max), len(calculated_max[0]), 1))), axis=2)
  is_new_arr[:, n_adj_entries_peak+n_adj_entries_avg:-n_adj_entries_peak-n_adj_entries_avg] = calculated_is_new_arr
  is_max_arr = n_cases_increase_avg == max_arr
  is_truly_max_arr = is_max_arr & is_new_arr

  # Return true if both significant and maximum
  is_sig_and_max_arr = is_sig_arr & is_truly_max_arr
  return is_sig_and_max_arr

def visualise_increase(n_cases_increase, n_cases_increase_avg=None):
  '''
  Visualises the increase in cases for each country that is represented in
  `n_cases_increase`. If `n_cases_increase_avg` is passed into the
  function as well, visualisation will also be done for the average increase in
  cases for each country.

  NOTE: If more than 5 countries are represented, only the plots for the first 5
  countries will be shown.
  '''
  days = np.arange(1, n_cases_increase.shape[1] + 1)
  plt.figure()
  for i in range(min(5, n_cases_increase.shape[0])):
    plt.plot(days, n_cases_increase[i, :], label='country {}'.format(i))
  plt.legend()
  plt.title('Increase in Cases')

  if n_cases_increase_avg is None:
    plt.show()
    return
  
  plt.figure()
  for i in range(min(5, n_cases_increase_avg.shape[0])):
    plt.plot(days, n_cases_increase_avg[i, :], label='country {}'.format(i))
  plt.legend()
  plt.title('Average Increase in Cases')
  plt.show()

def visualise_peaks(n_cases_cumulative, n_adj_entries_avg=7, n_adj_entries_peak=7):
  '''
  Visualises peaks for each of the country that is represented in
  `n_cases_cumulative`.
  
  NOTE: If there are more than 5 countries, only the plots for the first 5
  countries will be shown.
  '''
  n_cases_increase = compute_increase_in_cases(n_cases_cumulative)
  n_cases_increase_avg = average_increase_in_cases(n_cases_increase,\
    n_adj_entries_avg)
  peaks = is_peak(n_cases_increase_avg, n_adj_entries_peak)
  days = np.arange(1, n_cases_increase.shape[1] + 1)

  plt.figure()

  for i in range(min(5, n_cases_cumulative.shape[0])):
    plt.plot(days, n_cases_increase_avg[i, :], label='country {}'.format(i))
    peak = (np.nonzero(peaks[i, :]))[0]
    peak_days = peak + 1 # since data starts from day 1, not 0
    plt.scatter(peak_days, n_cases_increase_avg[i, peak])
  
  plt.legend()
  plt.show()

if __name__ == "__main__":
  df = get_data()
  n_cases_cumulative = get_n_cases_cumulative(df)
  n_deaths_cumulative = get_n_deaths_cumulative(df)
  healthcare_spending = get_healthcare_spending(df)
  mask_prices = get_mask_prices(healthcare_spending.shape[1])
  stringency_values = get_stringency_values(df)
  n_cases_top_cumulative = get_n_cases_top_cumulative(df)
  test_increase = compute_increase_in_cases(n_cases_cumulative)
  test_ave_incr = average_increase_in_cases(test_increase)
  visualise_peaks(n_cases_cumulative)


