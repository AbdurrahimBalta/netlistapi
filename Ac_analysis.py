from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import u_Hz, u_V,u_MHz,u_kOhm,u_kHz,u_uF
import matplotlib.pyplot as plt
import  PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
from PIL import Image
import io

import numpy as np
import matplotlib.pyplot as plt



def ac_analysis(netlist = str ,start_frequency = str,stop_frequency= str, voltage= str, freq = str):

    start_f = start_frequency + "@u_Hz"
    start_f = eval(start_f)
    
    stop_f = stop_frequency + "@u_MHz"
    stop_f = eval(stop_f)
    
    voltage_value = voltage + "@u_V"
    voltage_value = eval(voltage_value)
    
    freq_value = freq + "@u_kHz"
    freq_value = eval(freq_value)
    
    
    circuit = Circuit('AC Analizi')
    circuit.SinusoidalVoltageSource('input', 'in', circuit.gnd, amplitude=voltage_value, frequency=freq_value)
    circuit.R(1, 'in', 'n1', 1@u_kOhm)
    circuit.R(2, 'n1', 'out', 1@u_kOhm)
    circuit.C(1, 'out', circuit.gnd, 2.3@u_uF)
    circuit.C(2, 'n1', circuit.gnd, 1.4@u_uF)
    
    
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.ac(start_frequency=start_f, stop_frequency=stop_f, number_of_points=15,  variation='dec')
    
    frequency = analysis.frequency
    v_out = np.array(analysis['out'])   # the data points are complex numbers
    
        
        # calculate the gain (in dB) and phase from the signal
    mag = 20*np.log10(np.absolute(v_out))
    phase = np.angle(v_out, deg=True)
        
        # set up plot
    fig, ax_mag = plt.subplots(figsize=(10,5))
    ax_phase = ax_mag.twinx()

    # magnitude axis
    ax_mag.set_xlabel('Frequency (Hz)')
    ax_mag.set_ylabel('Magnitude (dB)')
    ax_mag.set_xscale('log')
    p1 = ax_mag.plot(frequency, mag, label="gain")
    
    # phase axis
    ax_phase.set_ylabel('Phase (deg)')
    ax_phase.set_xscale('log')
    p2 = ax_phase.plot(frequency, phase, label="phase", linestyle='dashed', color='red')
    
    # add grid
    ax_mag.grid(color='gray', alpha=0.5, linestyle='dashed', linewidth=0.5, which="both")
    
    lines = p1 + p2
    labels = [l.get_label() for l in lines]
    ax_mag.legend(lines, labels)
    
    image_path = 'deneme.jpeg'
    plt.savefig(image_path)
    plt.close()
    
    # Load the saved image as a PIL.Image object
    image = Image.open(image_path)
    
    # Convert the image to bytes
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='JPEG')
    image_bytes.seek(0)
    
    return image_bytes

    