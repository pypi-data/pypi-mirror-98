#-*- coding: utf-8 -*-

import snap7
import random
import sys
from datetime import datetime
from enum import Enum

from EasyS7.Utility import *
from EasyS7.DataTypes.DTdint import  DTdint
from EasyS7.DataTypes.DTbool import  DTbool
from EasyS7.DataTypes.DTtime import  DTtime
from EasyS7.DataTypes.DTint import  DTint
from EasyS7.DataTypes.DTstring import  DTstring
from decimal import Decimal as D

class Areas(Enum):
    Input = 1
    Output = 2
    Merker = 3
    DB = 4
    Counter = 5
    Timer = 6

class DataTypes(Enum):
    Real = 1
    Bool = 2
    DInt = 3
    UDInt = 4
    Int = 5
    DTime = 6
    String = 7
    Multiple = 8


class DataBlockObj(object):
		pass





def dbRead(plc,db_num,length,dbitems):

    data=plc.db_read(db_num,0,length)
    obj = DataBlockObj()

    for item in dbitems:
        value = (None,item['name'])
        offset = int(item['bytebit'].split('.')[0])

        if item['datatype']=='Real':
            value = (snap7.util.get_real(data,offset),item['name'].replace(" ","_").replace("/","_"))
            obj.__setattr__(item['name'].replace(" ","_").replace("/","_"), value[0])

        if item['datatype']=='Bool':
            bit =int(item['bytebit'].split('.')[1])
            BoolObj=DTbool(data,bit)
            value = (snap7.util.get_bool(data,offset,bit),item['name'].replace(" ","_").replace("/","_"))
            obj.__setattr__(item['name'].replace(" ","_").replace("/","_"), value[0])

        if item['datatype']=='DInt' :

            DintObj=DTdint(data)
            value=(DintObj.readValue(offset),item['name'].replace(" ","_").replace("/","_"))
            obj.__setattr__(item['name'].replace(" ","_").replace("/","_"), value[0])

        if item['datatype']=='UDInt':

            DintObj=DTdint(data)
            value=(DintObj.readValueU(offset),item['name'].replace(" ","_").replace("/","_"))
            obj.__setattr__(item['name'].replace(" ","_").replace("/","_"), value[0])

        if item['datatype']=='Int':

            IntObj=DTint(data)
            value=(IntObj.readValue(offset),item['name'].replace(" ","_").replace("/","_"))
            obj.__setattr__(item['name'].replace(" ","_").replace("/","_"), value[0])


        """if item['datatype']=='Time':

            TimeObj=DTtime() # burası düzeltilecek
            value=(TimeObj.readValue(offset),item['name'].replace(" ","_").replace("/","_"))
            obj.__setattr__(item['name'].replace(" ","_").replace("/","_"), value[0])"""



        if item['datatype'].startswith('String'):
            value = snap7.util.get_string(data, offset,int(item['datatype'].split('[')[1][:-1])+1)
            obj.__setattr__(item['name'].replace(" ","_").replace("/","_"), value)

        #obj.__setattr__(item['name'].replace(" ","_").replace("/","_"), value[0])


    return obj


def dbWrite(plc,itemArray): # {data_type, offset, data,}
    print(itemArray)
    offsets = { "Bool":1,"Int": 2,"Real":4,"Time":4,"DInt":4,"UDInt":4}#yeni offset degerleri eklenicek
    seq,length = [x["offset"] for x in itemArray],[x["data_type"] for x in itemArray]

    maximum=max(seq, key=float)
    minimum = min(seq, key=float)

    idx = seq.index(maximum)
    if length[idx].startswith('String'):

        lastByte = int(maximum)+(int(length[idx].split('[')[1][:-1]))

    else:

        lastByte = int(maximum)+(offsets[length[idx]])
           

    byte_array=bytearray(lastByte-int(minimum))
    
    print(byte_array)
    
    for item in itemArray:

        if item['data_type']=='Real':
            
            snap7.util.set_real(byte_array,int(item["offset"]-int(minimum)),item["data"])

        elif item['data_type']=='Bool':
                
                
                bool_index = int((D(str(item["offset"])) - D(str(int(item["offset"])))) * 10)
                
                
                snap7.util.set_bool(byte_array,int(item["offset"]-int(minimum)),bool_index,item["data"])

        elif item['data_type']=='DInt' :
            
            DIntObj = DTdint(byte_array)
            byte_array = DIntObj.set_dint(byte_array,int(item["offset"]-int(minimum)),item["data"])

        elif item['data_type']=='UDInt':
            
            DIntObj = DTdint(byte_array)
            byte_array = DIntObj.set_udint(byte_array,int(item["offset"]-int(minimum)),item["data"])

        elif item['data_type']=='Int':
            
            snap7.util.set_int(byte_array,int(item["offset"]-int(minimum)),item["data"])

    return byte_array


def dbReadArea(plc,area_type, address ,item_data_type,  db_num = 999, bool_index = -1, string_max_size = -1):
    address_integer = int(address)
    address_fraction = (address-address_integer)*10
    value = None

    if area_type == Areas.Input:
        area = snap7.snap7types.S7AreaPE
        offset = address_integer*8 + address_fraction
    elif area_type == Areas.Output:
        area = snap7.snap7types.S7AreaPA
        offset = address_integer*8 + address_fraction
    elif area_type == Areas.Merker:
        area = snap7.snap7types.S7AreaMK
        offset = address_integer*8 + address_fraction
    elif area_type == Areas.DB:
        if db_num == 999:
            print("[Error] : Data Block Number Not Defined. Use Optional Argument db_num.")
            sys.exit()
        area = snap7.snap7types.S7AreaDB
        offset = address
    elif area_type == Areas.Counter:
        area = snap7.snap7types.S7AreaCT
        offset = address_integer*16 + address_fraction
    elif area_type == Areas.Timer:
        area = snap7.snap7types.S7AreaTM
        offset = address_integer*16 + address_fraction



    if item_data_type == DataTypes.Real:
        byte_array = plc.read_area(area,db_num,offset,4)
        value = snap7.util.get_real(byte_array,0)
        

    elif item_data_type == DataTypes.Bool:
        if bool_index <0 : 
            print("[Error] : Bool Index Not Defined. Use Optional Argument bool_index")
            sys.exit()
        else:
            byte_array = plc.read_area(area,db_num,offset,1)
            value = snap7.util.get_bool(byte_array,0,bool_index)

    elif item_data_type == DataTypes.DInt:

        byte_array = plc.read_area(area,db_num,offset,4)
        DTdintObj = DTdint(byte_array)
        value = DTdintObj.db_readDint(byte_array,0 )
        

    elif item_data_type == DataTypes.UDInt:
        byte_array = plc.read_area(area,db_num,offset,4)
        value=struct.unpack('>L' ,struct.pack('4B',*byte_array))[0]

    elif item_data_type == DataTypes.Int:
        byte_array = plc.read_area(area,db_num,offset,2)
        value = snap7.util.get_int(byte_array,0)

    elif item_data_type == DataTypes.DTime:

        print("[ERROR] : Time Not Implemented")
        sys.exit()

        
        

    elif item_data_type == DataTypes.String:
        if string_max_size <= 0 :
            print("[Error] : Max String Size Not Defined. Use Optional Argument string_max_size")
            sys.exit()
        else:
            
            
            byte_array = plc.read_area(area,db_num,offset,string_max_size)
            
            value = snap7.util.get_string(byte_array,0,string_max_size)

    return value




def dbWriteArea(plc,area_type, address ,item_data_type, item, db_num = 999, bool_index = -1, string_max_size = -1):

    address_integer = int(address)
    address_fraction = (address-address_integer)*10
    byte_array = None

    if area_type == Areas.Input:
        area = snap7.snap7types.S7AreaPE
        #offset = address_integer*8 + address_fraction
    elif area_type == Areas.Output:
        area = snap7.snap7types.S7AreaPA
        #offset = address_integer*8 + address_fraction
    elif area_type == Areas.Merker:
        area = snap7.snap7types.S7AreaMK
        #offset = address_integer*8 + address_fraction
    elif area_type == Areas.DB:
        if db_num == 1:
            print("[Error] : Data Block Number Not Defined. Use Optional Argument db_num.")
            sys.exit()
        area = snap7.snap7types.S7AreaDB
        #offset = address
    elif area_type == Areas.Counter:
        area = snap7.snap7types.S7AreaCT
        #offset = address_integer*16 + address_fraction
    elif area_type == Areas.Timer:
        area = snap7.snap7types.S7AreaTM
        #offset = address_integer*16 + address_fraction

    
    offset = int(address)
    
    if item_data_type == DataTypes.Real:
        byte_array = bytearray(4)
        snap7.util.set_real(byte_array,0,item)

    elif item_data_type == DataTypes.Bool:
        if bool_index == 999 : 
            print("[Error] : Bool Index Not Defined. Use Optional Argument bool_index")
            sys.exit()
        else:
           
            byte_array = plc.read_area(area,db_num,offset,1)
            snap7.util.set_bool(byte_array,0,bool_index,item)

    elif item_data_type == DataTypes.DInt:
        byte_array = bytearray(4)
        DIntObj = DTdint(byte_array)
        byte_array = DIntObj.set_dint(byte_array,0,item)

    elif item_data_type == DataTypes.UDInt:
        byte_array = bytearray(4)
        DIntObj = DTdint(byte_array)
        byte_array = DIntObj.set_udint(byte_array,0,item)

    elif item_data_type == DataTypes.Int:
        byte_array = bytearray(4)
        snap7.util.set_int(byte_array,0,item)

    elif item_data_type == DataTypes.DTime:

        print("[ERROR] : Time Not Implemented")
        sys.exit()
        """dtl = plc.db_read(db_num,16, 8)
        
        pdb.set_trace()
        
        DTimeObject = DTtime()
        byte_array1 = (DTimeObject.set_dtime(item))
        byte_array = dtl
        pdb.set_trace()"""
        
        

    elif item_data_type == DataTypes.String:
        if string_max_size <= 0 :
            print("[Error] : Max String Size Not Defined. Use Optional Argument string_max_size")
            sys.exit()
        else:
            
            StringObj = DTstring()
            byte_array = plc.read_area(area,db_num,offset,string_max_size)

            StringObj.set_string(byte_array,0,item,string_max_size)

    elif item_data_type == DataTypes.Multiple:
        byte_array = dbWrite(plc,item)

        
        


          
    
   

    plc.write_area(area,db_num,offset,byte_array)


