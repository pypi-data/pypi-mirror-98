# Cognify - Insai Cognition Lab



# Getting Started

To get started, you just need install the cognify library. The libary is constantly evolving so stay tuned for new updates.

## Install

Begin by installing the cognify library, by running in your terminal

`pip install cognify`

Next, you need to add a separate config file containing the database credentials. This file is **provided upon request**. It will need to be added to the folder where cognify was installed.

To find this folder simply run

`pip show cognify`

This should give you the location of the cognify library

![title](pictures\LibraryLocation.png)

Navigate to that the cognify folder and copy the config file.

## Import libraries

#  Retrieving data

All recorded data is stored securely in a database. We have created simple functions to retrieve data based on your user id. Therefore, only you have access to your data.  

## EEG

See the recordings connected to a specific user. 

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
Retrieve the raw eeg data from the database based on the metric id. Each recording has a single metric id. Convert the eeg data into a Pandas dataframe. Each column represents the electrical activity from a given electrode

```python
metricId = 'ckkymq9fx5695271gntqvd743uk'
eeg = dataset.get_eeg(metricId)
df_eeg = dataset.eeg_to_df(eeg)
df_eeg.head()
```

    Each buffer is 3 seconds long
    Each buffer is sampled every 1.5 seconds
    The number of buffers skipped 0
    Number of timestamps:  82944
    Number of unique timestamps:  82944
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
      <th>2021-02-09 23:22:17.403875</th>
      <td>95.703125000000000000000000000000</td>
      <td>413.574218750000000000000000000000</td>
      <td>325.195312500000000000000000000000</td>
      <td>74.707031250000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-02-09 23:22:17.407781</th>
      <td>-186.523437500000000000000000000000</td>
      <td>-100.585937500000000000000000000000</td>
      <td>-19.531250000000000000000000000000</td>
      <td>-104.003906250000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-02-09 23:22:17.411687</th>
      <td>-285.644531250000000000000000000000</td>
      <td>-529.296875000000000000000000000000</td>
      <td>-397.949218750000000000000000000000</td>
      <td>-196.289062500000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-02-09 23:22:17.415593</th>
      <td>-38.574218750000000000000000000000</td>
      <td>-149.414062500000000000000000000000</td>
      <td>-156.738281250000000000000000000000</td>
      <td>-56.640625000000000000000000000000</td>
    </tr>
    <tr>
      <th>2021-02-09 23:22:17.419500</th>
      <td>228.515625000000000000000000000000</td>
      <td>273.437500000000000000000000000000</td>
      <td>87.402343750000000000000000000000</td>
      <td>119.140625000000000000000000000000</td>
    </tr>
  </tbody>
</table>
</div>



### MNE
Retrieve the raw eeg data based on the metric id. Export the eeg data directly to MNE. A bandpass filtered [1, 40] Hz is applied by default, but this can be removed. 
It returns:
    - Raw data in MNE format
    - Events related to the task
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

### Dataframe

Retrieve the raw ppg data from the database based on the metric id. With some simple preprocessing, the heart rate can be retrieved from this signal.

```python
metricId = 'cklv4n4gk9375316nk687ui65p'
ppg = dataset.get_ppg(metricId)
df_ppg = dataset.ppg_to_df(ppg)

```

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




![png](docs/images/output_16_1.png)


### Heart rate (In development)

Calculate the heart rate of the signal from the ppg signal. Simple preprocessing is done to clean up the signal and extract the heart rate. The segment width (in seconds) and segment overlap (in seconds) can be configured to obtain the heart rate.

```python
metricId = 'cklvxp8nw150056716nk44eebuep'
df_hr = heartrate.get_hr(metricId,segment_width=30, segment_overlap = 0.9)
```

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
```




    [<matplotlib.lines.Line2D at 0x24a208cf970>]




![png](docs/images/output_20_1.png)


## Accelerometer and Gyroscope

### Dataframe

Retrieve the raw accelerometer and gyroscope data from the database based on the metric id. It may be useful to use these streams to detect motion artifact and denoise the other biosignals.

```python
metricId = 'ckjsogpjw2206420ypu7iuepcth'
accel = dataset.get_xyz(metricId,'Accelerometer')
gyro = dataset.get_xyz(metricId,'Gyroscope')
df_accel = dataset.motion_to_df(accel)
df_gyro = dataset.motion_to_df(gyro)
```

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



    09-Mar-21 17:22:50 | WARNING | findfont: Font family ['normal'] not found. Falling back to DejaVu Sans.
    


![png](docs/images/output_24_3.png)



![png](docs/images/output_24_4.png)


# Recommendations

* [nbdev docs](http://nbdev.fast.ai/)

## Install collapsible headings and toc2

There are two jupyter lab extensions that I highly recommend when working with projects like this. They are:

* [Collapsible headings](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/collapsible_headings/readme.html): This lets you fold and unfold each section in your notebook, based on its markdown headings. You can also hit `left` to go to the start of a section, and `right` to go to the end
* [TOC2](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/toc2/README.html): This adds a table of contents to your notebooks, which you can navigate either with the Navigate menu item it adds to your notebooks, or the TOC sidebar it adds. These can be modified and/or hidden using its settings.

## Expose Lab server to public

./ngrok http 8888


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
    Converted index.ipynb.
    
