import re

class QuickSelector:
    def __init__(self, path: str, seq_file: str):
        rs = re.compile(r"^S '(.*?)' (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+)$")
        r = re.compile(r'^I (\d+) (\d)$')
        rq = re.compile(r'^R1 0 0 0 (.*?) .+$')
        self._lines = []
        self._quality = {}
        self._image_count = 0
        self._reference_image = None
        self._line_idx_for_first_image = None
        pattern_ok = False
        self._path = path
        self._ser_file = seq_file.replace('.seq', '.ser')
        with open(f"{path}/{seq_file}") as file:
            line_idx = 0
            qual_idx = 0
            for line in file:
                self._lines.append(line)
                if not pattern_ok:
                    m = re.match(rs, line)
                    if m:
                        self._reference_image = int(m.group(6))
                        pattern_ok = True                        
                else:                    
                    m = re.match(r, line)
                    if m:
                        self._image_count += 1
                        if self._image_count == 1:
                            self._line_idx_for_first_image = line_idx
                    else:
                        m = re.match(rq, line)
                        if m:
                            quality = float(m.group(1))
                            self._quality[qual_idx] = quality
                            qual_idx += 1
                            
                line_idx += 1

    @property                        
    def image_count(self):
        return self._image_count
    
    def output_as_script(self, seq_fname: str, idx0: int, oidx: int, number: int, ratio: float, wavelets: list, rmgreen: str,
                         sat_amount: float, sat_bg: float, asinh_stretch: float, asinh_bp: float):
        result = []
        lines = self._lines.copy()
        
        quality = []
        for i in range(idx0, idx0+number):
            quality.append((i, self._quality[i]))
        
        quality.sort(key=lambda x: x[1], reverse=True)
        quality = quality[:int(number*ratio)]
        
        to_keep = {}
        for i in quality:
            to_keep[i[0]] = 1
        
        result.append(f'unselect {seq_fname} 1 {self._image_count}\n')

        r = re.compile(r'^I (\d+) (\d)$')
        
        first_e = None
        last_e = None

        wavelets_len = len(wavelets)
        wavelets_str = " ".join(wavelets)
            
        for i in range(idx0, idx0+number):
            idx = self._line_idx_for_first_image + i
            line = lines[idx]
            
            m = re.match(r, line)
            
            if idx0 <= i < idx0+number:
                if m:
                    # e = int(i in to_keep and m.group(2))
                    e = int(i in to_keep)
            else:
                e = 0
                
            if e:
                fnb = int(m.group(1))+1
                if first_e is None:
                    first_e = fnb
                last_e = fnb
            else:
                if first_e is not None:
                    result.append(f'select {seq_fname} {first_e} {last_e}\n')
                    first_e = last_e = None
        
        if first_e is not None:
            result.append(f'select {seq_fname} {first_e} {last_e}\n')
        
        result.append(f"stack {seq_fname} sum -filter-included -out=img/seqselector.fit\n")
        result.append("load img/seqselector.fit\n")

        if wavelets_len>0:
            result.append(f"wavelet {wavelets_len} 2\n")
            result.append(f"wrecons {wavelets_str}\n")
        if rmgreen == 'y':
            result.append("rmgreen\n")

        if asinh_stretch != 0.0 or asinh_bp != 0.0:
            result.append(f"asinh -human {asinh_stretch} {asinh_bp}\n")

        if sat_amount != 0.0 or sat_bg != 0.0:
            result.append(f"satu {sat_amount} {sat_bg}\n")
        result.append(f"savetif img/seqselector{oidx}\n")

        
        # result.append("close\n")
        # result.append(f"load {self._ser_file}\n")
        return result
        