import numpy as np
import matplotlib.pyplot as plt
import  PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import u_MOhm,u_uF,u_ns,u_Ohm,u_kOhm

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io

def transient_analysis(netlist=str, step_time = str, stop_time = str):
    
    s_t = step_time + "e-9"  
    step_time = eval(s_t)
    
    e_t = stop_time + "e-9"    
    stop_time = eval(e_t)
    
    circuit = Circuit('Capacitor Charging Circuit')



    circuit.V(1, 'n_input', circuit.gnd, 2)
    circuit.PulseVoltageSource(2, 'n_swp', circuit.gnd, initial_value=0, pulsed_value=1, pulse_width=1, period=2,
                               delay_time=2@u_ns, rise_time=0, fall_time=0, phase=None, dc_offset=0)
    circuit.VoltageControlledSwitch(1, 'n_switch', 'n_input', 'n_swp', circuit.gnd, model='switch_model')
    circuit.model('switch_model', 'SW', Ron=.001@u_Ohm, Roff=1@u_MOhm)
    circuit.R(1, 'n_switch', 'n_resistor', 1@u_kOhm)
    circuit.C(1, 'n_resistor', 'n_c1', 1@u_uF)
    print(circuit)

        
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)
    analysis = simulator.transient(step_time=step_time, end_time=stop_time, use_initial_condition=True) # notice `use_initial_condition`
    time_values = analysis.time
    v_pulse = analysis.nodes['n_swp']
    v_c1 = analysis.nodes['n_c1']
    
    fig, ax = plt.subplots(figsize=(8,4))
    
    ax.set(xlabel="Time [s]",
           ylabel="Voltage [V]",
           title ="Transient Analysis")

    ax.plot(time_values, v_pulse, label='$V_{c1}$')
    ax.plot(time_values, v_c1, label='$V_{pulse}$')
    
    ax.grid(color='gray', alpha=0.5, linestyle='dashed', linewidth=0.5)
    
    ax.legend()

    
    image_path = 'trainsent.jpeg'
    plt.savefig(image_path)
    plt.close()
   
   # Load the saved image as a PIL.Image object
    image = Image.open(image_path)
   
   # Convert the image to bytes
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='JPEG')
    image_bytes.seek(0)

    return image_bytes
