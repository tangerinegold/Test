# -*- coding: cp1251 -*-

# class Matrix begin ------------------------------------------------------------------------------
class Matrix():
    def _read_razdel(self, razdel):
        '''������ ������� �� �������'''
        # ������������ ��������� ������ (�������� �������) test
        zag = '! 0000 ' + self.js["OTCHET"] + ' ' + razdel + ' ' + self.js["YEAR"][2:4] + ' ' +\
              self.js["MONTH"] + ' ' + self.js["REGION"] + ';'

        t_matrix = {}
        # ����� �������
        start_str = False
        m_array = []
        for i in range(0, len(self.tm)):
            #print('i=', i)
            if start_str: #comment 2
                if '! 000' in self.tm[i]:
                    break
                else:
                    tmp_str = self.tm[i].replace(';','')
                    t_array = tmp_str.rsplit()
                    m_array.append(t_array)
            else:
                #print(self.tm[i], len(self.tm) - 2)
                if zag in self.tm[i] and i < len(self.tm) - 2:
                    start_str = True
        if m_array:
            t_matrix[razdel] = m_array
            #print(t_matrix)
            #print(m_array)
        else:
            t_matrix[razdel] = []
        return t_matrix[razdel]

    def _check_razdel(self, matrix, rzd_key):
        ''' �������� ������� - ����������� ���������� ����� � ���� ����� ��������''' 
        cnt_grf = int(self.js[rzd_key]["CNT_GRF"])
        cnt_str = int(self.js[rzd_key]["CNT_STR"])
        #print("RAZDEL:", rzd_key, "  GRAF:",cnt_grf, "    STROK:",cnt_str)
        # ��������� ���������� ���� � ������������ ������ ������
        error_flag = False
        for i in matrix:
            # ��������� �����
            if int(i[0]) > cnt_str:
                print('������ �������� �������. ���������� ���������� �����. ������:', cnt_str, ' �������:', i[0])
                print('   ������:', rzd_key, '   ������:', i)
                error_flag = True
            # ���������� ����
            if (len(i) - 1) != cnt_grf:
                print('������ �������� �������. �������� ���������� ����. ������:', cnt_grf, ' �������:', (len(i) - 1))
                print('   ������:', rzd_key, '   ������:', i)
                error_flag = True
        # �������� ������� � ������ ������
        if error_flag:
            matrix = []
        return matrix

    def _fill_razdel(self, matrix, rzd_key):
        ''' ���������� ����������� ����� ������''' 
        cnt_grf = int(self.js[rzd_key]["CNT_GRF"])
        cnt_str = int(self.js[rzd_key]["CNT_STR"])
        zero_str = list('0' * cnt_grf)
        tmp_matrix = []
        pred_str = 0
        for i in matrix:
            cur_str = int(i[0])
            propusk = cur_str - pred_str
            if propusk < 1:
                print('������ � �������', rzd_key, '����� ������� ������:', cur_str, ' �� ������ ���������� ������:', pred_str)
                return []
            if propusk > 1:
                for j in range(pred_str + 1, cur_str):
                    m_str = [str(j)] + zero_str
                    tmp_matrix.append(m_str)
            pred_str = cur_str
            tmp_matrix.append(i)
        ''' � ����� ����� ������, ������������� ����� ��������'''
        return tmp_matrix           
    
    def get_cell(self, razdel, stroka, grafa):
        ''' ��������� ������ �� �������, ������, ����� � ����� ����� ���� ��� �������� ��� � ���������'''
        try:
            if type(razdel) is int:
                razdel = str(razdel)
            if type(grafa) is str:
                grafa = int(grafa)
            if type(stroka) is str:
                stroka = int(stroka)
            razdel = razdel.rjust(2, '0')
            # ��������� ������ �� 1 (�.�. �������� ������� ���������� � ����)
            stroka -= 1
        except:
            print('������ ���������� ����� ��� ���������� ������. ������:', razdel, '  C�����:', stroka, '  �����:', grafa)
            #raise
            return None
        cell = None
        try:
            cell = self.matrix[razdel][stroka][grafa]
        except:
            print('������ ��� ���������� ������. ������:', razdel, '  C�����:', stroka, '  �����:', grafa)
            raise
        finally:
            return cell
                        


    def __init__(self, jsonf):
        ''' ������������� �������, �� ���� ���������� �������� ������'''
        self.js = jsonf       
        m_filename = self.js["MATRIX"].replace("%MATRIX_PATH%",self.js["MATRIX_PATH"])
        # m_filename = m_filename.replace('/','\\')
        try:
           mf = open(m_filename, 'r', encoding='cp1251')
        except:
           print('������ �������� ����� �������:', m_filename)
           raise
           sys.exit()
        self.tm = mf.readlines()
        for i in self.tm:
           i.replace('\n','')
        self.matrix = {}
        # 
        for i in self.js['RAZDELS']:
            self.matrix[i] = self._read_razdel(i)
            self.matrix[i] = self._check_razdel(self.matrix[i], i)
            self.matrix[i] = self._fill_razdel(self.matrix[i], i)
            #print(matrix[i])
            #for j in self.matrix[i]:
            #    print(j)

           
# class Matrix end --------------------------------------------------------------------------------


class Shapka:

    def _read_from_file(self, shp):
        """
        read shapka from file
        :rtype: list of str
        """
        try:
            f_shp = open(shp, 'r', encoding='cp1251')
            t_s = f_shp.readlines()
            t_t_s = []
            for i in t_s:
                t_i = i.replace('\n','')
                t_t_s.append(t_i)
            #print(t_t_s)
            return t_t_s
        except:
            print('���������� ��������� ���� �����:', shp)
            raise

    def _shp_parse(self, str_shp):
        top_flag = True
        for i in str_shp:
            if i[:2] == 'G/':
                self.gr_list.append(i)
                top_flag = False
                continue
            if i[:2] == '�/':
                self.p_string = i[2:]
                continue
            if i[:2] == 'R/':
                self.rzd_string = i[2:]
                continue
            if i[:2] == 'Z/':
                self.bottom.append(i[:2])
                continue
            if top_flag:
                self.top.append(i)
        return

    def _replace_mmyyyy(self, top, year, month):
        temp_top = []
        for i in top:
            t_i = i
            if '#M' in i:
                t_i.replace('#M', month)
            if '#G' in i:
                t_i.replace('#G  ', year)
            temp_top.append(t_i)
        return temp_top

    def _make_simple_gr_list(self, gr_list):
        simple_gr_list = []
        for i in gr_list:
            t_s = i.split('/')
            try:
                simple_gr_list.append([int(t_s[1]), int(t_s[4])])
            except:
                print('������ ��������� �����:', i)
                raise
        return simple_gr_list

    def get_top(self):
        return self.top

    def get_bottom(self):
        return  self.bottom

    def get_rzd_string(self):
        return self.rzd_string

    def get_p_string(self):
        return self.p_string

    def get_gr_list(self):
        return self.simple_gr_list

    def __init__(self, shp, year, month):
        self.str_shp = self._read_from_file(shp)
        self.top = []
        self.bottom = []
        self.gr_list = []
        self.simple_gr_list = []
        self.rzd_string = ''
        self.p_string = ''
        self._shp_parse(self.str_shp)
        self.top = self._replace_mmyyyy(self.top, year, month)
        self.simple_gr_list = self._make_simple_gr_list(self.gr_list)


def check_global_dir():
    if  not os.path.isdir("META"):
        print("������ ����������! ����������� ������� �������� �������: META")
        return False
    '''if  not os.path.isdir("LOG"):
        os.mkdir("LOG")
        print("������ �������: LOG")
    if  not os.path.isdir("TXT"):
        os.mkdir("TXT")
        print("������ �������: TXT")'''
    return True

def check_argv(argv):
    # �������� ���������� ����������
    if len(argv) != 4:
        print('\n� ��������� ������ ���� �������� ��� ��������� - ��� ������, ���, �����')
        print('������: matrix2txt.py 495 2015 06')
        print('-------------------------------------------------------------------------------------------------')
        print('��� ������, ���, ����� ������������ ��� ������������ ����� ����� �������� ������� � �������� META')
        print('../META/495/495_2015_06.json')
        return False
    return True

def replace_path(js):
    """
    make %path% substitutions
    :param js:
    :return:
    """
    global_key = js.keys()
    str_dict = str(js)
    cnt = 0
    while "%" in str_dict:
        cnt += 1
        for i in global_key:
            if type(js[i]) is str:
                src_value = '%' + i + '%'
                dest_value = js[i]
                str_dict = str_dict.replace(src_value, dest_value)
        if cnt == 100:
            print('������ ��� ����������� ����������, ������ ��������.')
            print('������������ �������� ���������� �����������')
            print('����������������� ������:')
            print(str_dict[str_dict.find('%'):])
    try:
        js = eval(str_dict)
    except:
        print('������ �������������� ����� �������� ����� ����������� ���� (��������� �������������� � �������)')
        raise
    return js


def read_meta(argv):
    f_name = argv[1] + '_' + argv[2] + '_' + argv[3] + '.json'
    f_path = 'META/' + argv[1] + '/' + f_name
    try:
        f = open(f_path, 'r', encoding = 'cp1251')
    except:
        print('������ ������� ����� ������� ������:', f_path)
        raise
        return False
    try:
        js = json.load(f)
    except:
        print("������ ������� ����� �������� ������.")
        print("������ ��������� ����� json\n")
        raise
        return False
    js = replace_path(js)
    return js

def get_datetime():
    ''' �������� ������� ����-����� � �������  YYYYY-MM-DD hh:mm.cc'''
    import time
    #c_dtime = time.localtime()[:6]
    #c_dtime = str(c_dtime).replace(',','').replace(' ','').replace('(','').replace(')','')
    tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec = time.localtime()[:6]
    c_dtime = str(tm_year) +'-' + str(tm_mon).rjust(2,'0') + '-' +str(tm_mday).rjust(2,'0') + ' ' +str(tm_hour).rjust(2,'0') + ':'
    c_dtime = c_dtime + str(tm_min).rjust(2,'0') + '.' + str(tm_sec).rjust(2,'0')
    return c_dtime


class Log_to_file(object):
    # ������� ������ ������������ ������
    # text -> stdout   ������������� �  text -> file,stdout
    def __init__(self,log_file):
        self._file = log_file
    def write(self, line):
        self._file.write(line)
        sys.__stdout__.write(line)
    def flush(self):
        self._file.flush()
        sys.__stdout__.flush()

def PrintException():
    # �������� ��������� ���������� � ����
    import linecache
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('    EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj),file=log_file)


if __name__ == '__main__':
    # ��������� ���-���� � ������� ���������� ��� ����������� ������ �������� ���������� � ���������
    import sys
    import time
    import os
    import json

    # �������� ������� ���������� ����������
    if not check_global_dir():
        sys.exit()

    # �������� ����������
    if not check_argv(sys.argv):
        sys.exit()

    # ������ ���� ���������� � ����������
    meta = read_meta(sys.argv)
    if not meta:
        sys.exit()

    # print(meta)
    m_shp = Shapka(meta["TEXT_01"]["SHP"], meta["YEAR"], meta["MONTH"])

    '''top = m_shp.get_top()
    for i in top:
        print(i)
    print()
    gr = m_shp.get_gr_list()
    for i in gr:
        print(i)
    print()
    print(m_shp.get_p_string())
    print(m_shp.get_rzd_string())'''

    '''m_matrix = Matrix(meta)
    m_cell = m_matrix.get_cell(1, 1, 221)
    print(m_cell)
    m_cell = m_matrix.get_cell(1, 1, 221)
    print(m_cell)
    m_cell = m_matrix.get_cell(1, 1, 221)
    print(m_cell)'''
