

#########################################################
## 内置系统指标
##
##
#########################################################

class SystemIndex:
    MAP_INDEX= {
        "MA":{ 
            "Name":"MA",
            "Script":'''
            T1:MA(C,M1);
            T2:MA(C,M2);
            T3:MA(C,M3);
            ''',
            "Args": [ { "Name":"M1", "Value":15 }, { "Name":"M2", "Value":20 }, { "Name":"M3", "Value":30} ]
            },

        "KDJ":{
            "Name":"KDJ",
            "Script":'''
            RSV:=(CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100;
            K:SMA(RSV,M1,1);
            D:SMA(K,M2,1);
            J:3*K-2*D;
            ''',
            "Args": [ { "Name":"N", "Value":9 }, { "Name":"M1", "Value":3 }, { "Name":"M2", "Value":3} ]
            },

        "MACD":{
            "Name":"MACD",
            "Script":'''
            DIF:EMA(CLOSE,SHORT)-EMA(CLOSE,LONG);
            DEA:EMA(DIF,MID);
            MACD:(DIF-DEA)*2,COLORSTICK;
            ''',
            # 脚本参数
            "Args": [ { "Name":"SHORT", "Value":12 }, { "Name":"LONG", "Value":26 }, { "Name":"MID", "Value":9 } ]
            }   
    }

    @staticmethod
    def Get(name) :
        if (name in SystemIndex.MAP_INDEX.keys()):
            return SystemIndex.MAP_INDEX[name]
        else:
            return None