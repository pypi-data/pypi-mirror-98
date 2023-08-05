# Cognify - Insai Cognition Lab



# Getting Started

To get started, you just need install the cognify library. The libary is constantly evolving so stay tuned for new updates.

## Install

Begin by installing the cognify library, by running in your terminal

`pip install cognify`

Next, you need to add a separate config file containing the database credentials. This file is **provided upon request**. It will need to be added to the folder where cognify was installed.

To find the installation location simply run

`pip show cognify`

This should give you the location of the cognify library

![title](pictures\LibraryLocation.png)

Navigate to that the cognify folder and place the `settings.ini` file that will be provided inside the folder.

## Import libraries

#  Data Retrieval

It is important after recording your biometric data to have access to the raw data. This section shows how to extract the raw data from your device depending on the biosignal (EEG, PPG, Acelerometer or Gyroscope). 

All recorded data is stored securely in a database. 

We have created simple functions to retrieve the raw data based on your User ID. **Therefore, only you have access to your data.**

You will obtain your User ID after creating your profile on the Insai platform (https://insai.app/signup)

## EEG

To begin, you can view all the recordings from a specific user, based on their User ID.

As you can observe, the creation data and type of recording are displayed to identify the recording you want to analyze.

After identifying the recording you want to analyze, note down the Metric ID, this is unique to each recording and serves as an identifier to get access to all biometric data linked to that recording.


In this example, my User ID is `ck9jusufs000016pbioyzehto`

And the recording I will analyse will be a reading session recorded at 6:35am, 2021-03-09. The metric ID is `ckm1n2i2y24577515snzllm3jxe`


```python
userId='ck9jusufs000016pbioyzehto'
recordings = dataset.get_recordings(userId)
recordings.tail()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>metricId</th>
      <th>type</th>
      <th>userId</th>
      <th>createdAt</th>
      <th>startTime</th>
      <th>stopTime</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>142</th>
      <td>cklujacpy119754916nk1jpgwsxp</td>
      <td>Reading</td>
      <td>ck9jusufs000016pbioyzehto</td>
      <td>2021-03-04 07:14:52.006</td>
      <td>"2021-03-04T07:14:51.837Z"</td>
      <td>2021-03-04T07:52:18.146Z</td>
    </tr>
    <tr>
      <th>143</th>
      <td>cklvxp8nw150056716nk44eebuep</td>
      <td>Reading</td>
      <td>ck9jusufs000016pbioyzehto</td>
      <td>2021-03-05 06:46:07.389</td>
      <td>"2021-03-05T06:46:07.128Z"</td>
      <td>2021-03-05T07:04:40.952Z</td>
    </tr>
    <tr>
      <th>144</th>
      <td>cklvyhjl8120897116nkythrdgkl</td>
      <td>Reading</td>
      <td>ck9jusufs000016pbioyzehto</td>
      <td>2021-03-05 07:08:07.916</td>
      <td>"2021-03-05T07:08:07.720Z"</td>
      <td>2021-03-05T08:12:21.094Z</td>
    </tr>
    <tr>
      <th>145</th>
      <td>ckm1n2i2y24577515snzllm3jxe</td>
      <td>Reading</td>
      <td>ck9jusufs000016pbioyzehto</td>
      <td>2021-03-09 06:35:07.402</td>
      <td>"2021-03-09T06:35:07.234Z"</td>
      <td>2021-03-09T06:48:31.988Z</td>
    </tr>
    <tr>
      <th>146</th>
      <td>ckm32gn98122155015snwkcr5u8y</td>
      <td>Reading</td>
      <td>ck9jusufs000016pbioyzehto</td>
      <td>2021-03-10 06:33:47.708</td>
      <td>"2021-03-10T06:33:47.401Z"</td>
      <td>2021-03-10T07:00:59.551Z</td>
    </tr>
  </tbody>
</table>
</div>



### Dataframe

After identifying the recording I want to analyze and the associated Metric ID `ckm1n2i2y24577515snzllm3jxe`. I can now begin retrieving the raw EEG data from the database.

The EEG data is retrieved and converted into a Pandas Dataframe.

In this format, each column represents the electrical activity from a given electrode and the timestamp is provided as the index.

*There is additional information regarding how the data was sent from the device to the computer (using buffers).*

```python
metricId = 'ckm1n2i2y24577515snzllm3jxe'
eeg = dataset.get_eeg(metricId)
df_eeg = dataset.eeg_to_df(eeg)
df_eeg.head()
```

    Each buffer is 3 seconds long
    Each buffer is sampled every 1.5 seconds
    The number of buffers skipped 0
    Number of timestamps:  337920
    Number of unique timestamps:  337920
    Some timestamps had different data values, this affected approximately 0.00 % of the data
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TP9</th>
      <th>AF7</th>
      <th>AF8</th>
      <th>TP10</th>
    </tr>
    <tr>
      <th>time</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2021-03-09 06:35:05.812125000</th>
      <td>-1000.000000000000000000000000000000</td>
      <td>-1000.000000000000000000000000000000</td>
      <td>-662.109375000000000000000000000000</td>
      <td>-1000.000000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-03-09 06:35:05.816031250</th>
      <td>-1000.000000000000000000000000000000</td>
      <td>-431.152343750000000000000000000000</td>
      <td>-374.023437500000000000000000000000</td>
      <td>-859.863281250000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-03-09 06:35:05.819937500</th>
      <td>172.851562500000000000000000000000</td>
      <td>275.390625000000000000000000000000</td>
      <td>24.902343750000000000000000000000</td>
      <td>64.453125000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-03-09 06:35:05.823843750</th>
      <td>-962.402343750000000000000000000000</td>
      <td>436.523437500000000000000000000000</td>
      <td>223.144531250000000000000000000000</td>
      <td>684.570312500000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-03-09 06:35:05.827750000</th>
      <td>-388.671875000000000000000000000000</td>
      <td>-265.136718750000000000000000000000</td>
      <td>-81.054687500000000000000000000000</td>
      <td>-181.152343750000000000000000000000</td>
    </tr>
  </tbody>
</table>
</div>



### MNE

Alternatively, the data can directly be exported to MNE.

By default, a bandpass filtered [1, 40] Hz is applied by default, but this can be removed. 

It returns:
- Raw data in MNE format
- Events related to the task (if a task was undertaken on the Insai Platform: **N-back, Digit Span or Sternberg**)
- Raw data in a dataframe

```python
metricId = 'ckkymq9fx5695271gntqvd743uk'
raw,events,df_eeg = dataset.eeg_to_mne(metricId)
```

    Each buffer is 3 seconds long
    Each buffer is sampled every 1.5 seconds
    The number of buffers skipped 0
    Number of timestamps:  82944
    Number of unique timestamps:  82944
    Some timestamps had different data values, this affected approximately 0.00 % of the data
    Creating RawArray with float64 data, n_channels=4, n_times=41856
        Range : 0 ... 41855 =      0.000 ...   163.496 secs
    Ready.
    

Display the data information

```python
raw.info
```




    <Info | 8 non-empty values
     bads: []
     ch_names: TP9, AF7, AF8, TP10
     chs: 4 EEG
     custom_ref_applied: False
     dig: 7 items (3 Cardinal, 4 EEG)
     highpass: 1.0 Hz
     lowpass: 40.0 Hz
     meas_date: unspecified
     nchan: 4
     projs: []
     sfreq: 256.0 Hz
    >



## PPG

The Metric ID `cklv4n4gk9375316nk687ui65p` can be used to retrieve the PPG data from a specific recording, you can retrieve the PPG data from the database.

PPG can be used to retrieve the heart rate and more in-depth heart-related metrics, such as pulse rate variability (PRV), which has shown some correlations with Heart Rate Variability (HRV).

### Dataframe

The PPG data is retrieved and converted into three Pandas Dataframes.

Each dataframe contains the signal and timestamps for a given sensor channel.

There are three channels `Ambient`, `Infrared` and `Red`.

With some simple preprocessing, the heart rate can be retrieved from the `Infrared` signal.

```python
metricId = 'cklv4n4gk9375316nk687ui65p'
ppg = dataset.get_ppg(metricId)
df_ppg = dataset.ppg_to_df(ppg)

```

**Ambient**

```python
df_ppg[0]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Ambient</th>
    </tr>
    <tr>
      <th>timestamp</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2021-03-04 17:12:31.211250</th>
      <td>31455.000000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-03-04 17:12:31.226875</th>
      <td>31449.000000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-03-04 17:12:31.242500</th>
      <td>31395.000000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-03-04 17:12:31.258125</th>
      <td>31488.000000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-03-04 17:12:31.273750</th>
      <td>31532.000000000000000000000000000000</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
    </tr>
    <tr>
      <th>2021-03-04 17:21:08.351875</th>
      <td>33073.000000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-03-04 17:21:08.367500</th>
      <td>33066.000000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-03-04 17:21:08.383125</th>
      <td>33069.000000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-03-04 17:21:08.398750</th>
      <td>33080.000000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-03-04 17:21:08.414375</th>
      <td>33117.000000000000000000000000000000</td>
    </tr>
  </tbody>
</table>
<p>33102 rows × 1 columns</p>
</div>



**Infrared**

```python
df_ppg[1]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Infrared</th>
    </tr>
    <tr>
      <th>timestamp</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2021-03-04 17:12:31.211250</th>
      <td>238546.000000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-03-04 17:12:31.226875</th>
      <td>238704.000000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-03-04 17:12:31.242500</th>
      <td>238496.000000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-03-04 17:12:31.258125</th>
      <td>238286.000000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-03-04 17:12:31.273750</th>
      <td>237916.000000000000000000000000000000</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
    </tr>
    <tr>
      <th>2021-03-04 17:21:08.351875</th>
      <td>248397.000000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-03-04 17:21:08.367500</th>
      <td>248360.000000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-03-04 17:21:08.383125</th>
      <td>248397.000000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-03-04 17:21:08.398750</th>
      <td>248290.000000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-03-04 17:21:08.414375</th>
      <td>248326.000000000000000000000000000000</td>
    </tr>
  </tbody>
</table>
<p>33102 rows × 1 columns</p>
</div>



**Red**

```python
df_ppg[2]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Red</th>
    </tr>
    <tr>
      <th>timestamp</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2021-03-04 17:12:31.211250</th>
      <td>25.000000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-03-04 17:12:31.226875</th>
      <td>0E-30</td>
    </tr>
    <tr>
      <th>2021-03-04 17:12:31.242500</th>
      <td>0E-30</td>
    </tr>
    <tr>
      <th>2021-03-04 17:12:31.258125</th>
      <td>0E-30</td>
    </tr>
    <tr>
      <th>2021-03-04 17:12:31.273750</th>
      <td>0E-30</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
    </tr>
    <tr>
      <th>2021-03-04 17:21:08.351875</th>
      <td>36.000000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-03-04 17:21:08.367500</th>
      <td>0E-30</td>
    </tr>
    <tr>
      <th>2021-03-04 17:21:08.383125</th>
      <td>0E-30</td>
    </tr>
    <tr>
      <th>2021-03-04 17:21:08.398750</th>
      <td>0E-30</td>
    </tr>
    <tr>
      <th>2021-03-04 17:21:08.414375</th>
      <td>0E-30</td>
    </tr>
  </tbody>
</table>
<p>33102 rows × 1 columns</p>
</div>



```python
begin, end  = 1500,2500
plt.subplot(311)
plt.plot(df_ppg[0].to_numpy()[begin:end])
plt.ylabel('Ambient')
plt.subplot(312)
plt.plot(df_ppg[1].to_numpy()[begin:end])
plt.ylabel('IR')
plt.subplot(313)
plt.plot(df_ppg[2].to_numpy()[begin:end])
plt.ylabel('Red')
plt.xlabel("seconds")
```




    Text(0.5, 0, 'seconds')



    11-Mar-21 12:24:35 | WARNING | findfont: Font family ['normal'] not found. Falling back to DejaVu Sans.
    


![png](docs/images/output_23_2.png)


### Heart rate (In development)

The heart rate can be calculated from the PPG signal.

Simple preprocessing can done to clean up the signal and extract the heart rate.

The segment width (in seconds) and segment overlap (in seconds) can be configured to obtain the heart rate.

```python
metricId = 'cklvxp8nw150056716nk44eebuep'
df_hr = heartrate.get_hr(metricId,segment_width=30, segment_overlap = 0.9)
```

    G:\Programs\anaconda3\lib\site-packages\scipy\interpolate\fitpack2.py:253: UserWarning: 
    The maximal number of iterations maxit (set to 20 by the program)
    allowed for finding a smoothing spline with fp=s has been reached: s
    too small.
    There is an approximation returned but the corresponding weighted sum
    of squared residuals does not satisfy the condition abs(fp-s)/s < tol.
      warnings.warn(message)
    

```python
df_hr.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>timestamp</th>
      <th>hr</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.0</td>
      <td>95.929464</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3.0</td>
      <td>96.145675</td>
    </tr>
    <tr>
      <th>2</th>
      <td>6.0</td>
      <td>93.090909</td>
    </tr>
    <tr>
      <th>3</th>
      <td>9.0</td>
      <td>91.569231</td>
    </tr>
    <tr>
      <th>4</th>
      <td>12.0</td>
      <td>91.366417</td>
    </tr>
  </tbody>
</table>
</div>



```python
plt.plot(df_hr['hr'])
plt.title('Heart rate over time')
plt.xlabel('Time (s)')
plt.ylabel('Heart rate (bpm)')
```




    Text(0, 0.5, 'Heart rate (bpm)')




![png](docs/images/output_27_1.png)


## Accelerometer and Gyroscope

The Metric ID `ckjsogpjw2206420ypu7iuepcth` can be used to retrieve the Accelerometer (Accel) and Gyroscope (Gyro) data from a specific recording, you can retrieve the Accel and Gyro data from the database.

Accelerometer and Gyroscope may be useful to use to detect motion artifact and denoise other biosignals.

### Dataframe

The Accel and Gyro data is retrieved and converted into Dataframes.

Each dataframe contains the signal along the `X`,`Y` and `Z` axis and the associated timestamps.


```python
metricId = 'ckjsogpjw2206420ypu7iuepcth'
accel = dataset.get_xyz(metricId,'Accelerometer')
gyro = dataset.get_xyz(metricId,'Gyroscope')
df_accel = dataset.motion_to_df(accel)
df_gyro = dataset.motion_to_df(gyro)
```

```python
df_accel.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>x</th>
      <th>y</th>
      <th>z</th>
      <th>timestamp</th>
    </tr>
    <tr>
      <th>time</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2021-01-11 14:44:53.210049072</th>
      <td>0.187011852800000000000000000000</td>
      <td>0.076599176000000000000000000000</td>
      <td>0.994751689600000000000000000000</td>
      <td>1610376293210.049000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-01-11 14:44:53.229279841</th>
      <td>0.182190072000000000000000000000</td>
      <td>0.078308161600000000000000000000</td>
      <td>0.994507548800000000000000000000</td>
      <td>1610376293210.049000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-01-11 14:44:53.248510610</th>
      <td>0.179138312000000000000000000000</td>
      <td>0.079101619200000000000000000000</td>
      <td>0.994629619200000000000000000000</td>
      <td>1610376293210.049000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-01-11 14:44:53.267740967</th>
      <td>0.178039678400000000000000000000</td>
      <td>0.078064020800000010000000000000</td>
      <td>0.988281958400000000000000000000</td>
      <td>1610376293267.741000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-01-11 14:44:53.286971736</th>
      <td>0.178100713600000000000000000000</td>
      <td>0.069946339200000000000000000000</td>
      <td>0.996521710400000000000000000000</td>
      <td>1610376293267.741000000000000000000000000000</td>
    </tr>
  </tbody>
</table>
</div>



```python
df_gyro.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>x</th>
      <th>y</th>
      <th>z</th>
      <th>timestamp</th>
    </tr>
    <tr>
      <th>time</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2021-01-11 14:44:53.209049072</th>
      <td>0.216827200000000000000000000000</td>
      <td>-3.080441600000000000000000000000</td>
      <td>1.061705600000000000000000000000</td>
      <td>1610376293209.049000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-01-11 14:44:53.228279841</th>
      <td>0.007476800000000000000000000000</td>
      <td>-3.409420800000000000000000000000</td>
      <td>0.852355200000000000000000000000</td>
      <td>1610376293209.049000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-01-11 14:44:53.247510610</th>
      <td>-0.022430400000000000000000000000</td>
      <td>-3.229977600000000000000000000000</td>
      <td>0.844878399999999900000000000000</td>
      <td>1610376293209.049000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-01-11 14:44:53.266740967</th>
      <td>-0.037384000000000000000000000000</td>
      <td>-3.110348800000000000000000000000</td>
      <td>1.031798400000000000000000000000</td>
      <td>1610376293266.741000000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-01-11 14:44:53.285971736</th>
      <td>0.186920000000000000000000000000</td>
      <td>-3.110348800000000000000000000000</td>
      <td>1.495360000000000000000000000000</td>
      <td>1610376293266.741000000000000000000000000000</td>
    </tr>
  </tbody>
</table>
</div>



```python
accel_np = df_accel.to_numpy()
times = (df_accel.timestamp-df_accel.timestamp.iloc[0])
print(np.shape(accel_np))
plt.figure(1)
plt.subplot(311)
plt.plot(times,accel_np[:,0])
plt.title('Accelerometer X')
plt.subplot(312)
plt.plot(times,accel_np[:,1])
plt.title('Y')
plt.subplot(313)
plt.plot(times,accel_np[:,2])
plt.title('Z')



gyro_np = df_gyro.to_numpy()
times = (df_gyro.timestamp-df_gyro.timestamp.iloc[0])
print(np.shape(gyro_np))
plt.figure(2)
plt.subplot(311)
plt.plot(times,gyro_np[:,0])
plt.title('Gyroscope X')
plt.subplot(312)
plt.plot(times,gyro_np[:,1])
plt.title('Y')
plt.subplot(313)
plt.plot(times,gyro_np[:,2])
plt.title('Z')
```

    (7521, 4)
    (7521, 4)
    




    Text(0.5, 1.0, 'Z')



    11-Mar-21 12:30:25 | WARNING | findfont: Font family ['normal'] not found. Falling back to DejaVu Sans.
    


![png](docs/images/output_33_3.png)



![png](docs/images/output_33_4.png)


# Analysis (coming soon)

# Recommendations

* [nbdev docs](http://nbdev.fast.ai/)

## Install collapsible headings and toc2

There are two jupyter lab extensions that I highly recommend when working with projects like this. They are:

* [Collapsible headings](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/collapsible_headings/readme.html): This lets you fold and unfold each section in your notebook, based on its markdown headings. You can also hit `left` to go to the start of a section, and `right` to go to the end
* [TOC2](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/toc2/README.html): This adds a table of contents to your notebooks, which you can navigate either with the Navigate menu item it adds to your notebooks, or the TOC sidebar it adds. These can be modified and/or hidden using its settings.

# Export

```python
from nbdev.export import *
notebook2script()
```

    Converted 00_core.ipynb.
    Converted 01_dataset.ipynb.
    Converted 02_model.ipynb.
    Converted 03_spectra.ipynb.
    Converted 04_metric.ipynb.
    Converted 05_report.ipynb.
    Converted 06_cognitive.ipynb.
    Converted 07_heartrate.ipynb.
    Converted 08_summary.ipynb.
    Converted Experiment1.ipynb.
    Converted Experiment2.ipynb.
    Converted Experiment_BehaviorVisualization.ipynb.
    Converted Experiment_Muse_HR.ipynb.
    Converted index.ipynb.
    
