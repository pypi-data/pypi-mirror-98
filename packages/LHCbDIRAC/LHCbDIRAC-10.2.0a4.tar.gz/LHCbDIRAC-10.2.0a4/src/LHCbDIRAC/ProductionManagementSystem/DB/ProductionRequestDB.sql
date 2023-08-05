/* ---------------------------------------------------------------------------#
# (c) Copyright 2019 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                      */

-- ------------------------------------------------------------------------------

-- When installing via dirac tools, the following is not needed (still here for reference)
--
-- DROP DATABASE IF EXISTS ProductionRequestDB;
-- CREATE DATABASE ProductionRequestDB;
-- ------------------------------------------------------------------------------
-- Database owner definition
-- USE mysql;
-- Must set passwords for database user by replacing "must_be_set".
-- GRANT SELECT,INSERT,LOCK TABLES,UPDATE,DELETE,CREATE,DROP,ALTER ON ProductionRequestDB.* TO Dirac@localhost IDENTIFIED BY 'FillIt';
-- FLUSH PRIVILEGES;

--
--  Schema definition for the Production Requests table
--  history ( logging ) information
-- -
-- ------------------------------------------------------------------------------
USE ProductionRequestDB;
-- -----------------------------------------------------------------------------

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS ProductionRequests;
CREATE TABLE ProductionRequests (
  RequestID int(11) NOT NULL AUTO_INCREMENT,
  ParentID int(11) DEFAULT NULL,
  MasterID int(11) DEFAULT NULL,
  RequestName varchar(128) DEFAULT '',
  RequestType varchar(32) DEFAULT '',
  RequestState varchar(32) DEFAULT '',
  RequestPriority varchar(32) DEFAULT '',
  RequestAuthor varchar(128) DEFAULT '',
  RequestPDG varchar(128) DEFAULT '',
  RequestWG  varchar(128) DEFAULT '',
  SimCondition varchar(128) DEFAULT '',
  SimCondID int(11) DEFAULT NULL,
  SimCondDetail blob,
  ProPath varchar(128) DEFAULT '',
  ProID int(11) DEFAULT NULL,
  ProDetail blob,
  EventType varchar(128) DEFAULT '',
  NumberOfEvents int(11) DEFAULT '0',
  Description blob,
  Comments blob,
  Inform blob,
  RealNumberOfEvents bigint(20) DEFAULT '0',
  Extra blob,
  IsModel tinyint(1) DEFAULT '0',
  StartingDate DATETIME DEFAULT NULL,
  FinalizationDate DATETIME DEFAULT NULL,
  RetentionRate varchar(32) DEFAULT '1',
  FastSimulationType varchar(32) DEFAULT 'None',
  PRIMARY KEY (RequestID),
  KEY ParentID (ParentID),
  KEY MasterID (MasterID),
  KEY RequestName (RequestName),
  KEY RequestType (RequestType),
  KEY RequestState (RequestState),
  KEY RequestPriority (RequestPriority),
  KEY RequestAuthor (RequestAuthor),
  KEY RequestWG (RequestWG),
  KEY SimCondition (SimCondition),
  KEY ProPath (ProPath),
  KEY EventType (EventType),
  KEY NumberOfEvents (NumberOfEvents),
  KEY IsModel (IsModel),
  FOREIGN KEY (MasterID) REFERENCES ProductionRequests (RequestID),
  FOREIGN KEY (ParentID) REFERENCES ProductionRequests (RequestID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS ProductionProgress;
CREATE TABLE ProductionProgress (
  ProductionID int(11) NOT NULL,
  RequestID int(11) DEFAULT NULL,
  Used tinyint(1) DEFAULT '1',
  BkEvents bigint unsigned DEFAULT NULL,
  PRIMARY KEY (ProductionID),
  KEY RequestID (RequestID),
  KEY Used (Used),
  FOREIGN KEY (RequestID) REFERENCES ProductionRequests (RequestID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS RequestHistory;
CREATE TABLE RequestHistory (
  recid int(11) NOT NULL AUTO_INCREMENT,
  RequestID int(11) NOT NULL,
  RequestState varchar(32) DEFAULT '',
  RequestUser varchar(128) DEFAULT '',
  TimeStamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (recid),
  KEY RequestID (RequestID),
  KEY TimeStamp (TimeStamp),
  FOREIGN KEY (RequestID) REFERENCES ProductionRequests (RequestID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
