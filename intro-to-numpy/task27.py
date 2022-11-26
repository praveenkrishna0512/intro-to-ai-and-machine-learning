import numpy as np
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