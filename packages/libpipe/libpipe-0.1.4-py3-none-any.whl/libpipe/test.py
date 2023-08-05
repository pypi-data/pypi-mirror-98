import sys

import casacore.tables as pt

class MsData(object):

    def __init__(self, data, flag, freqs, time, ant1, ant2, ant_names):
        self.data = data
        self.flag = flag
        self.freqs = freqs
        self.time = time
        self.ant1 = ant1
        self.ant2 = ant2
        self.ant_names = ant_names

    def save(self, h5_file):
        with msutils.h5_tables.open_file(h5_file, 'w') as h5:
            group = h5.create_group("/", 'ms', 'MS data')
            h5.create_array(group, 'data', self.data, "I")
            h5.create_array(group, 'flag', self.flag, "Flags")
            h5.create_array(group, 'time', self.time, "Time")
            h5.create_array(group, 'freqs', self.freqs, "Frequencies (Hz)")
            h5.create_array(group, 'ant1', self.ant1, "Antenna 1")
            h5.create_array(group, 'ant2', self.ant2, "Antenna 2")
            h5.create_array(group, 'ant_names', self.ant_names, "Names of stations")


def get_ms_freqs(ms_table):
    t_spec_win = pt.table(ms_table.getkeyword('SPECTRAL_WINDOW'), readonly=True, ack=False)
    freqs = t_spec_win.getcol('CHAN_FREQ').squeeze()
    t_spec_win.close()

    return freqs


def main():
    ms_file = sys.argv[1]
    baselines = '*&&&'

    with pt.taql(f"select from $ms_file where mscal.baseline($baselines)") as t:
        data = t.getcol(col_data)
        flag = t.getcol('FLAG')
        a1 = t.getcol('ANTENNA1')
        a2 = t.getcol('ANTENNA2')
        time = t.getcol('TIME')
        
        freqs = get_ms_freqs(t)

    ant_name = pt.table(os.path.join(ms_file, 'ANTENNA')).getcol('NAME')
      
    ms = MsData(data, flag, freqs, time, a1, a2, ant_name)
    
    ms.save('test.h5')


if __name__ == '__main__':
    main()
