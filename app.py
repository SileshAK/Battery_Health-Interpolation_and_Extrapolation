import pandas as pd
import seaborn
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from flask import Flask,request, url_for, redirect, render_template
from datetime import datetime, timedelta
import mpld3

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/h4',methods=['POST','GET'])
def h4():
    return render_template("4.html")

@app.route('/h3',methods=['POST','GET'])
def h3():
    return render_template("3.html")

@app.route('/inter3',methods=['POST','GET'])
def inter3():
    df=pd.read_csv('ASN00003.csv')

    df['datetime'] = pd.to_datetime(df['record_create_timestamp'])
    df.set_index('datetime', inplace=True)
    resampled_df = df.resample('Min').mean()
    df_interpolated = resampled_df.interpolate(method='time')
    df_interpolated=df_interpolated.drop(df_interpolated.columns[[0]],axis=1)
    df1 = df_interpolated.head(60)

    return render_template('interpolate_asn3.html',  tables=[df1.to_html(classes='data')])

@app.route('/inter4',methods=['POST','GET'])
def inter4():
    df=pd.read_csv('ASN00004.csv')

    df['datetime'] = pd.to_datetime(df['record_create_timestamp'])
    df.set_index('datetime', inplace=True)
    resampled_df = df.resample('Min').mean()
    df_interpolated = resampled_df.interpolate(method='time')
    
    df1 = df_interpolated.head(60)

    return render_template('interpolate_asn4.html',  tables=[df1.to_html(classes='data')], titles=df1.columns.values)

@app.route('/extra3',methods=['POST','GET'])
def extra3():
    return render_template("extra_asn3.html")

@app.route('/predict3',methods=['POST','GET'])
def predict3():
    k =int(request.form.get('mins'))
    
    df = pd.read_csv('ASN00003.csv')
    df=df.drop(df.columns[[0,1,2,3,4,7,8,9,10]],axis=1)
    st = '24-05-2023 14:22'
    df['record_create_timestamp'] = pd.to_datetime(df['record_create_timestamp'])
    df.set_index('record_create_timestamp', inplace=True)
    for i in range(k):
        extrapolation_time = pd.to_datetime(st)
        extrapolation_time=extrapolation_time+timedelta(minutes=i)
        time_diff = (df.index[-1] - df.index[-2]).total_seconds() / 60

        value_diff = df['state_of_charge'].iloc[-1] - df['state_of_charge'].iloc[-2]

        extrapolated_value = df['state_of_charge'].iloc[-1] + (value_diff / time_diff) * (extrapolation_time - df.index[-1]).total_seconds() / 60
        if(extrapolated_value<=0):
            
            break

        new_row = pd.Series({ 'state_of_charge': extrapolated_value},name=extrapolation_time)

        df = df.append(new_row)

    df1 = df.tail(k)

    return render_template('extra_asn3.html',  tables=[df1.to_html(classes='data')], titles=df1.columns.values)

@app.route('/extra4',methods=['POST','GET'])
def extra4():
    return render_template("extra_asn4.html")

@app.route('/predict4',methods=['POST','GET'])
def predict4():
    k =int(request.form.get('mins'))
    
    df = pd.read_csv('ASN00004.csv')
    df=df.drop(df.columns[[0,1,2,3,4,7,8,9,10]],axis=1)
    st = '24-05-2023 14:22'
    df['record_create_timestamp'] = pd.to_datetime(df['record_create_timestamp'])
    df.set_index('record_create_timestamp', inplace=True)
    for i in range(k):
        extrapolation_time = pd.to_datetime(st)
        extrapolation_time=extrapolation_time+timedelta(minutes=i)
        time_diff = (df.index[-1] - df.index[-2]).total_seconds() / 60

        value_diff = df['state_of_charge'].iloc[-1] - df['state_of_charge'].iloc[-2]

        extrapolated_value = df['state_of_charge'].iloc[-1] + (value_diff / time_diff) * (extrapolation_time - df.index[-1]).total_seconds() / 60
        if(extrapolated_value<=0):
            break

        new_row = pd.Series({ 'state_of_charge': extrapolated_value},name=extrapolation_time)

        df = df.append(new_row)

    df1 = df.tail(k)

    return render_template('extra_asn4.html',  tables=[df1.to_html(classes='data')], titles=df1.columns.values)




@app.route('/i3_dataset',methods=['POST','GET'])
def i3_dataset():
    return render_template("minuteInterpolated3.csv")

@app.route('/i4_dataset',methods=['POST','GET'])
def i4_dataset():
    return render_template("minuteInterpolated4.csv")






@app.route('/plot',methods=['POST','GET'])
def plot():
    
    k =int(request.form.get('mins'))
    
    df = pd.read_csv('ASN00004.csv')
    df=df.drop(df.columns[[0,1,2,3,4,7,8,9,10]],axis=1)
    st = '24-05-2023 14:22'
    df['record_create_timestamp'] = pd.to_datetime(df['record_create_timestamp'])
    df.set_index('record_create_timestamp', inplace=True)
    for i in range(k):
        extrapolation_time = pd.to_datetime(st)
        extrapolation_time=extrapolation_time+timedelta(minutes=i)
        time_diff = (df.index[-1] - df.index[-2]).total_seconds() / 60

        value_diff = df['state_of_charge'].iloc[-1] - df['state_of_charge'].iloc[-2]

        extrapolated_value = df['state_of_charge'].iloc[-1] + (value_diff / time_diff) * (extrapolation_time - df.index[-1]).total_seconds() / 60
        if(extrapolated_value<=0):
            break

        new_row = pd.Series({ 'state_of_charge': extrapolated_value},name=extrapolation_time)

        df = df.append(new_row)

    df2 = df.tail(k)

    # Scatter plot
    plt.plot( df2['state_of_charge'])
    plt.xlabel('Time')
    plt.ylabel('State of charge')
    plt.title('Plot')

    # Convert plot to HTML format
    html_plot = mpld3.fig_to_html(plt.gcf())

    return render_template('plot.html', html_plot=html_plot)


@app.route('/plot2',methods=['POST','GET'])
def plot2():
    df=pd.read_csv('ASN00004.csv')

    df['datetime'] = pd.to_datetime(df['record_create_timestamp'])
    df.set_index('datetime', inplace=True)
    resampled_df = df.resample('Min').mean()
    df_interpolated = resampled_df.interpolate(method='time')
    df1 = df_interpolated.head(100)
    
    plt.plot(df1['state_of_charge'])
    plt.xlabel('Time')
    plt.ylabel('State of charge')
    plt.title('Plot')
    
    # Convert plot to HTML format
    html_plot = mpld3.fig_to_html(plt.gcf())

    return render_template('plot2.html', html_plot=html_plot)


if __name__ == '__main__':
    app.run(debug=True)
