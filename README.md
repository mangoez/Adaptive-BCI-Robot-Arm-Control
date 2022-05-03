# Adaptive-BCI-Robot-Arm-Control
Continuously record motor imagery, process it to train a model and classify new trials in real time.
The prediction will allow the user to control a robotic arm

1. move_robot.py continuously reads a file called all_pred.csv and will send the command to the Arduino and move a robot arm via serial communication
2. run_eeg.py is a notebook that interfaces with the g.tec Unicorn Hybrid EEG and continuously runs and saves data to a CSV file called data.csv
3. record_MI_session.py will present a series of commands to tell the user to perform a kind of motor imagery and send the start/end of the trial via UDP to read_data.py to let it know the trial has started/finished so that it can crop the latest trial
4. read_data.py will receive the motor imagery class via UDP and then slices out the trial from data.csv the EEG is writing to constantly. It will then preprocess it for the model and using the last n-trials to train the model, it will then classify the latest trial 

These programs all run in PARALLEL at once which is very chaotic. Will write a program that will interface these 4 programs when I can be bothered. 
