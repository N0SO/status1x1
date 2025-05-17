#!/usr/bin/env python3
from __init__ import VERSION
from moqputils.moqpdbutils import *
from status1x1.ses import SES
#from moqputils.configs.moqpdbconfig import * # To use the production DB
from moqpdbconfig import * #To use the SANDBOXDB
from datetime import datetime
import csv, os.path
HEADER = 'CALL\tOWNERCALL\tCW\tPH\tRY\tTOTAL\tID'

class mySES(SES):
    """
    Adds a parameter for the table index (id) and logid. The logid will 
    remain 'None' if there is no log in the database from the special
    event station.
    """
    def __init__(self,
                 callsign=None,
                 Start_date=None,
                 End_date=None,
                 logid=None,
                 sesid=None):
        super().__init__(   callsign,
                            Start_date,
                            End_date )
        self.logid = logid
        self.id = sesid
        
class sesSum(mySES):
    def __init__(self,
                 callsign=None,
                 Start_date=None,
                 End_date=None,
                 logid=None,
                 sesid=None,
                 cw=None,
                 ph=None,
                 ry=None,
                 total=None):    
        super().__init__(   callsign,
                            Start_date,
                            End_date,
                            logid,
                            sesid )
        self.cw=cw
        self.ph=ph
        self.ry=ry
        self.total=total
        
    def totalQSOs(self):
        if (self.cw and self.ph and self.ry):
            self.total = self.cw + self.ph + self.ry
            return self.total
        else:
            return None

class seStats():
    
    def __init__(self, args=None):
        self.sesDict = dict()
        if args.inputpath:
            if args.inputpath.upper() == 'INIT':
                self._initTable() #S""" Initialize SESCALLS Table only"""
            else:
                """ 
                Read SESCALLS data from CSV input file and initialize
                SESCALLS table with that data
                """
                self.initSESTable(args.inputpath)
        pass
        
    def _initTable(self, senames = None):
        db = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
        db.setCursorDict()
        print (f'Using database {DBNAME}')
        dquery ='DROP TABLE IF EXISTS SESCALLS'
        dbcquery = """CREATE TABLE `SESCALLS` (
          `ID` int(11) NOT NULL AUTO_INCREMENT,
          `SESCALL` varchar(10) DEFAULT NULL,
          `OWNERCALL` varchar(10) DEFAULT NULL COMMENT 'From 1x1callsigns.org',
          `OWNERNAME` varchar(60) DEFAULT NULL COMMENT 'From 1x1callsigns.org',
          `OWNERADDRESS` varchar(128) DEFAULT NULL COMMENT 'From 1x1callsigns.org',
          `OWNEREMAIL` varchar(40) DEFAULT NULL COMMENT 'From 1x1callsigns.org',
          `OWNERPHONE` varchar(20) DEFAULT NULL COMMENT 'From 1x1callsigns.org',
          `LOGID` int(11) DEFAULT NULL COMMENT 'ID of submitted log',
          `SESOPS` varchar(256) DEFAULT NULL COMMENT 'May be able to get from submitted log.\r\n',
          `EVENTNOTE` varchar(256) DEFAULT NULL COMMENT 'From 1x1callsigns.org',
          `SESNOTES` varchar(256) DEFAULT NULL,
          `YEAR` year(4) NOT NULL DEFAULT current_timestamp(),
           PRIMARY KEY (`ID`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        """
        db.write_query(dquery) # Delete old SESCALLS table if it exists
        db.write_query(dbcquery) # create new empty table 
  
    def _readCSVFile(self, csvFile):
        with open(csvFile,'r') as csvfile:
            fileData=[]
            csvreader = csv.DictReader(csvfile, delimiter='\t', quotechar='|')
            for row in csvreader:
                #print("Row:", row)
                fileData.append(row)
                ses=mySES(callsign=row['CALL '])
                ses.opcall=row['OP CALL']
                ses.opname=row['NAME']
                ses.opemail=row['EMAIL']
                ses.opaddress=row['ADDRESS']
                ses.opphone=row['PHONE']
                ses.sename=row['EVENT']
                self.sesDict[row['CALL ']] = ses
            return fileData
            
    def write_to_db(self, fdata=None, init=True):
        current_year = datetime.now().year
        db = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
        db.setCursorDict()

        if init:
            self._initTable()
        if fdata:
            for row in fdata:
                sesid = db.write_pquery(\
                   """INSERT INTO SESCALLS 
                      (SESCALL, OWNERCALL, OWNERNAME, OWNERADDRESS, 
                       OWNEREMAIL, OWNERPHONE, EVENTNOTE, YEAR)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                   [ row['CALL '],
                     row['OP CALL'],
                     row['NAME'],
                     row['ADDRESS'],
                     row['EMAIL'],
                     row['PHONE'],
                     row['EVENT'],
                     current_year ] )
                self.sesDict[row['CALL ']].id = sesid
                #print(f'ID: {sesid} {row}')
        else:
            for key in self.sesDict.keys():
                sesid = db.write_pquery(\
                   """INSERT INTO SESCALLS 
                      (SESCALL, OWNERCALL, OWNERNAME, OWNERADDRESS, 
                       OWNEREMAIL, OWNERPHONE, EVENTNOTE, YEAR)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                   [ self.sesDict[key].callsign,
                     self.sesDict[key].opcall,
                     self.sesDict[key].opname,
                     self.sesDict[key].opaddress,
                     self.sesDict[key].opemail,
                     self.sesDict[key].opphone,
                     self.sesDict[key].sename,
                     current_year ] )
                self.sesDict[key].id = sesid
        
                
        return True
            
    def initSESTable(self, csvfile):
        if (os.path.exists(csvfile)):            
            if (os.path.isfile(csvfile)):
                filedata = self._readCSVFile(csvfile)
            else:
                print(f'{csvfile} is not a file.')
                return False
        else:
            print(f'{csvfile} does not exist.')
            return False
        
        if (filedata):
            result=self.write_to_db()
            if result:
                self.addLogIDs()
            return result
        else:
            print(f'No CSV data in file {csvfile}.')
            return False
            
    def _addLogID(self, db, secall):
        logh = db.fetchLogHeader(secall)
        if (logh):
            result = db.write_query(f"""  UPDATE SESCALLS
                                            SET LOGID={logh[0]['ID']}
                                          WHERE ID={self.sesDict[secall].id};""")
            self.sesDict[secall].logid=logh[0]['ID']
        else:
            print(f'No log for {secall}.')

        

    def addLogIDs(self):
        db = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
        db.setCursorDict()
        
        #sescalls = db.read_query("""SELECT ID, SESCALL FROM SESCALLS;""")
        #for secall in sescalls:
        #    self._addLogID(db, secall['SESCALL'], secall['ID'])
        #    self._addLogID(db, secall['SESCALL'], secall['ID'])
        for call in self.sesDict.keys():
            secall = db.read_query(f"""SELECT ID, SESCALL FROM SESCALLS
                                        WHERE SESCALL = '{call}';""")
            if (secall):
                #self.sesDict[call].id = secall[0]['ID']
                self._addLogID(db, call) 

    def sesReport(self, args):
        if args.callsign:
            callsign = args.callsign.upper()
            reportype = args.reportType.lower()
            db = MOQPDBUtils(HOSTNAME, USER, PW, DBNAME)
            db.setCursorDict()
            if callsign == 'ALLCALLS':
                csvd=self.allCalls(db, callsign, reportype)
            else:
                csvd=self.oneCall(db, callsign, reportype, header=True)
            self.showCSV(csvd)
                
    def oneCall(self, db, call, rtype, header=False):
        #print(f'{rtype} Report for {call}...')
        #sesum = db.read_query(f"""SELECT SESCALLS.ID, 
        #                                SESCALLS.SESCALL,
        #                                SESCALLS.OWNERCALL,
        #                                SUMMARY.CWQSO AS 'CW',
        #                                SUMMARY.PHQSO AS 'PH',
        #                                SUMMARY.RYQSO AS 'RY'  
        #                             FROM (SESCALLS JOIN SUMMARY 
        #                             ON (SESCALLS.LOGID = SUMMARY.LOGID))
        #                             WHERE SESCALLS.SESCALL = '{call}';""")
        secall = db.read_query(f"""SELECT ID, SESCALL, OWNERCALL, LOGID
                                FROM SESCALLS WHERE SESCALL='{call}'""")
        if secall: scall = secall
        if scall['LOGID']:
            sesum = db.read_query(f"""SELECT CWQSO, PHQSO, RYQSO 
                                   FROM SUMMARY 
                                   WHERE LOGID = '{scall['LOGID']}""")
        if sesum:
            ssum = sesum[0]
            ssum['TOTAL'] = ssum['CW'] + ssum['PH'] + ssum['RY']
        else:
            ssum = {'TOTAL':None, 'CW':None, 'PH':None, 'RY':None}

        if rtype == 'csv':
            csvdata = self.makeCSV(ssum, header=header)
        
        return csvdata
            
    def allCalls(self, db, call, rtype):
        #print(f'{rtype} Report for {call}...')
        sescalls = db.read_query("""SELECT ID, SESCALL FROM SESCALLS;""")
        csvd = []
        header = True
        for call in sescalls:
            t=self.oneCall(db, call['SESCALL'], rtype, header=header)
            for l in t:
                csvd.append(l)
            if header:
                header = False
        return csvd

    def makeCSV(self, cvd, header=False):
        if header:
            csvreturn = [HEADER]
        else:
            csvreturn = []
        
        csvreturn.append(f"""{ self.sesDictcvd['SESCALL'] }\t{ cvd['OWNERCALL'] }\t{ cvd['CW'] }\t{ cvd['PH'] }\t{ cvd['RY'] }\t{ cvd['TOTAL'] }\t{ cvd['ID'] }""")
        
        return csvreturn

    def showCSV(self, csv):
        for l in csv:
            print(l)
