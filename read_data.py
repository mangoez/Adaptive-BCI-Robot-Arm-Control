import socket
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.signal import welch
from scipy.signal import welch, freqz, butter, filtfilt
from sklearn.ensemble import RandomForestClassifier as rfc
import serial

# Open the serial port. 
ser = serial.Serial(port='COM3', baudrate=115200, timeout=1)


def plot_spectrum(data, sf, window_sec, band=None, dB=False):
    """Plot the periodogram, Welch's and multitaper PSD.

    Requires MNE-Python >= 0.14.

    Parameters
    ----------
    data : 1d-array
        Input signal in the time-domain.
    sf : float
        Sampling frequency of the data.
    band : list
        Lower and upper frequencies of the band of interest.
    window_sec : float
        Length of each window in seconds for Welch's PSD
    dB : boolean
        If True, convert the power to dB.
    """
    sns.set(style="white", font_scale=1.2)
    # Compute the PSD
    freqs_welch, psd_welch = welch(data, sf, nperseg=window_sec*sf)
    sharey = False

    # Optional: convert power to decibels (dB = 10 * log10(power))
    if dB:
        psd_welch = 10 * np.log10(psd_welch)
        sharey = True
    
    return freqs_welch, psd_welch
def psd_of_window(trial, n_freqs, zeros=0, fs=250, low=7, high=30):
            channels = trial.shape[1]
            temp = np.zeros((channels, n_freqs))
    
            for j in range(channels):
                trial_pad = np.pad(trial[:, j], [(zeros, zeros)], mode='constant')
                freqs, psd = plot_spectrum(trial_pad, fs, (32), [low, high], dB=True)

                low_ind = np.where(freqs == low)[0][0]
                high_ind = np.where(freqs == high)[0][0]

                psd_sliced = psd[low_ind: high_ind]
                freqs_sliced = freqs[low_ind: high_ind]

                temp[j, :] = psd_sliced

            return np.ravel(temp)

serverAddressPort   = ("127.0.0.1", 12345)
bufferSize = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.bind(serverAddressPort)
length = 0

count = 1
events = []
X_list = []
y_list = []
all_pred = []
model = rfc(n_estimators=300)

while True:
    if UDPClientSocket.recv is not None:
        msgFromServer, addr = UDPClientSocket.recvfrom(bufferSize)
        msg = int(msgFromServer.decode(encoding = 'UTF-8',errors = 'strict'))
        print("Direction: ", msg)

        data = pd.read_csv('DIY_EEG/data.csv', sep=',',header=None)
        print(data.shape)
        print("Seconds from last timepoint: ", (data.shape[0]-length)/250)
        length = data.shape[0]

        data = data.to_numpy()
        trial = data[-int(4.5*250):-int(2.5*250), :8]
        # print("Trial shape", trial.shape)

        if msg == 1:
            #np.savetxt('Trials/Trial_R_'+str(count), trial, delimiter=',', fmt='%.3f', newline='\n')
            events.append([data[-1, -2], 1])
            print(events[-1])
        elif msg == -1:
            #np.savetxt('Trials/Trial_L_'+str(count), trial, delimiter=',', fmt='%.3f', newline='\n')
            events.append([data[-1, -2], -1])
            print(events[-1])
        else:
            print("ERROR SAVING")
        np.savetxt('DIY_EEG/events.csv', events, delimiter=',', fmt='%.3f')
        


        # Process data
        low = 7
        high = 24
        n_freqs = 34
        zeros = 0
        fs = 250
        # Re-reference the data to electrode Cz, this is standard in the literature
        Cz = trial[:, 2]
        Fz_cz = trial[:, 0] - Cz
        C3_cz = trial[:, 1] - Cz
        C4_cz = trial[:, 3] - Cz
        PO7_cz = trial[:, 4] - Cz
        Pz_cz = trial[:, 5] - Cz
        Oz_cz = trial[:, 6] - Cz
        PO8_cz = trial[:, 7] - Cz

        selected_electrodes = (np.vstack((Fz_cz, C3_cz, C4_cz, Pz_cz, PO7_cz, Oz_cz, PO8_cz))).T
        channels = selected_electrodes.shape[1]

        print("Selected electrode shape: ", selected_electrodes.shape)





        # Take in a trial of size [channels, samples] and spit out the feature vector
        # Feature vector is the frequencies of each channel concatenated
        X_trial = psd_of_window(trial, n_freqs, zeros, fs, low, high)
        X_trial = np.reshape(X_trial, (1, X_trial.shape[0]))
        print(X_trial.shape)


        if count > 2:
            model = model.fit(X_arr, y_list)
            y_pred = model.predict(X_trial)

            all_pred.append(y_pred)
            np.savetxt('DIY_EEG/all_pred.csv', all_pred, delimiter=',')

            print('\n')
            print("="*100)
            print("PREDICTION: ", y_pred, "REAL: ", msg)
            print("="*100)
            print('\n')
        
        X_list.append(np.squeeze(X_trial))
        y_list.append(msg)
        X_arr = np.array(X_list)
        print("Training array size: ", X_arr.shape)

        count += 1
        if msg == 0:
            count = 1

            

        


        