# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        gc_sql_utils
# Purpose:
#
# Author:      Geocom Informatik AG
#
# Created:     01.04.2018
# Copyright:   (c) Geocom Informatik AG 2018
#-------------------------------------------------------------------------------

getServerProperty = """
            SELECT SERVERPROPERTY('{property}')
            """

createDB = """
            CREATE DATABASE [{dbName}] ON  PRIMARY
            ( NAME = N'{dbName}_dat', FILENAME = N'{dbDataPath}{dbName}.mdf' , SIZE = {dbSize}MB , FILEGROWTH = {dbGrowth}MB )
            LOG ON
            ( NAME = N'{dbName}_log', FILENAME = N'{dbLogPath}{dbName}_log.ldf' , SIZE = {logSize}MB , FILEGROWTH = {logGrowth}MB )

            ALTER DATABASE [{dbName}] SET ANSI_NULL_DEFAULT OFF
            ALTER DATABASE [{dbName}] SET ANSI_NULLS OFF
            ALTER DATABASE [{dbName}] SET ANSI_PADDING OFF
            ALTER DATABASE [{dbName}] SET ANSI_WARNINGS OFF
            ALTER DATABASE [{dbName}] SET ARITHABORT OFF
            ALTER DATABASE [{dbName}] SET AUTO_CLOSE OFF
            ALTER DATABASE [{dbName}] SET AUTO_CREATE_STATISTICS ON
            ALTER DATABASE [{dbName}] SET AUTO_SHRINK OFF
            ALTER DATABASE [{dbName}] SET AUTO_UPDATE_STATISTICS ON
            ALTER DATABASE [{dbName}] SET CURSOR_CLOSE_ON_COMMIT OFF
            ALTER DATABASE [{dbName}] SET CURSOR_DEFAULT  GLOBAL
            ALTER DATABASE [{dbName}] SET CONCAT_NULL_YIELDS_NULL OFF
            ALTER DATABASE [{dbName}] SET NUMERIC_ROUNDABORT OFF
            ALTER DATABASE [{dbName}] SET QUOTED_IDENTIFIER OFF
            ALTER DATABASE [{dbName}] SET RECURSIVE_TRIGGERS OFF
            ALTER DATABASE [{dbName}] SET DISABLE_BROKER
            ALTER DATABASE [{dbName}] SET AUTO_UPDATE_STATISTICS_ASYNC OFF
            ALTER DATABASE [{dbName}] SET DATE_CORRELATION_OPTIMIZATION OFF
            ALTER DATABASE [{dbName}] SET PARAMETERIZATION SIMPLE
            ALTER DATABASE [{dbName}] SET READ_WRITE
            ALTER DATABASE [{dbName}] SET RECOVERY {recoveryModel}
            ALTER DATABASE [{dbName}] SET MULTI_USER
            ALTER DATABASE [{dbName}] SET PAGE_VERIFY CHECKSUM
            ALTER DATABASE [{dbName}] SET ALLOW_SNAPSHOT_ISOLATION ON
            ALTER DATABASE [{dbName}] SET READ_COMMITTED_SNAPSHOT ON
            """

selDbExists = """
            SELECT name FROM master.sys.databases WHERE name = '{dbName}';
            """

selDefaultDataPath = """
            SELECT SERVERPROPERTY('instancedefaultdatapath')
            """

selDefaultLogPath = """
            SELECT SERVERPROPERTY('instancedefaultlogpath');
            """

selSDEuserExists = """
            SELECT name FROM master.sys.syslogins WHERE name='sde';
            """

createSDELogin = """
            CREATE LOGIN [sde] WITH PASSWORD='{sdePwd}', DEFAULT_DATABASE=[master], DEFAULT_LANGUAGE=[Deutsch], CHECK_EXPIRATION=OFF, CHECK_POLICY=OFF;
            """

changePermissions = """
            USE {database};
            DROP SCHEMA {dbEditor};
            DROP SCHEMA {dbViewer};
            REVOKE ALL TO {dbEditor};
            REVOKE ALL TO {dbViewer};
            """

grantRolePermissions = """
            USE {database};
            GRANT EXECUTE TO [R_SDE_EDITOR];
            """

changeSpatialType = """
            USE {database}
            UPDATE sde.SDE_dbtune SET config_string = 'SDEBINARY' WHERE (keyword = 'DEFAULTS') AND (parameter_name = 'GEOMETRY_STORAGE')
            """

changeDefaultSchema = """
            USE {database};
            ALTER USER {dbEditor} WITH DEFAULT_SCHEMA = {dbOwner};
            ALTER USER {dbViewer} WITH DEFAULT_SCHEMA = {dbOwner};
            """

getSpIndexName = """
            SELECT IndexName = ind.name
            FROM sys.indexes ind
            INNER JOIN sys.index_columns ic ON ind.object_id = ic.object_id and ind.index_id = ic.index_id
            INNER JOIN sys.columns col ON ic.object_id = col.object_id and ic.column_id = col.column_id
            INNER JOIN sys.tables t ON ind.object_id = t.object_id
            WHERE ind.is_primary_key = 0
            AND ind.is_unique = 0
            AND ind.is_unique_constraint = 0
            AND t.is_ms_shipped = 0
            AND ind.type = 4
            AND t.name = '{tablename}';
            """

changeSpIndex = """
            SET ARITHABORT ON
            SET CONCAT_NULL_YIELDS_NULL ON
            SET QUOTED_IDENTIFIER ON
            SET ANSI_NULLS ON
            SET ANSI_PADDING ON
            SET ANSI_WARNINGS ON
            SET NUMERIC_ROUNDABORT OFF
            CREATE SPATIAL INDEX [{idxname}] ON [{dbschema}].[{tablename}]
            ([SHAPE]) USING GEOMETRY_GRID
            WITH (BOUNDING_BOX =({xmin}, {ymin}, {xmax}, {ymax}), GRIDS =(LEVEL_1 = {l1},LEVEL_2 = {l2},LEVEL_3 = {l3},LEVEL_4 = {l4}),
            CELLS_PER_OBJECT = {cells}, PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = ON, DROP_EXISTING = ON, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, DATA_COMPRESSION = {compression}) ON [PRIMARY];
            """

changeSpIndexAuto = """
            SET ARITHABORT ON
            SET CONCAT_NULL_YIELDS_NULL ON
            SET QUOTED_IDENTIFIER ON
            SET ANSI_NULLS ON
            SET ANSI_PADDING ON
            SET ANSI_WARNINGS ON
            SET NUMERIC_ROUNDABORT OFF
            CREATE SPATIAL INDEX [{idxname}] ON [{dbschema}].[{tablename}]
            ([SHAPE]) USING GEOMETRY_AUTO_GRID
            WITH (BOUNDING_BOX =({xmin}, {ymin}, {xmax}, {ymax}),
            CELLS_PER_OBJECT = {cells}, PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = ON, DROP_EXISTING = ON, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, DATA_COMPRESSION = {compression}) ON [PRIMARY];
            """

getTableId = """
            SELECT registration_id,imv_view_name
            FROM sde.SDE_table_registry
            WHERE table_name = '{tablename}'
            """

# script from: http://blogs.lessthandot.com/index.php/DataMgmt/DBAdmin/fixing-orphaned-database-users/
fixOrphanedUsers = """
            SET NOCOUNT ON
            USE {database}
            GO
            DECLARE @loop INT
            DECLARE @USER sysname

            IF OBJECT_ID('tempdb..#Orphaned') IS NOT NULL
             BEGIN
              DROP TABLE #orphaned
             END

            CREATE TABLE #Orphaned (UserName sysname, UserSID VARBINARY(85),IDENT INT IDENTITY(1,1))

            INSERT INTO #Orphaned
            EXEC SP_CHANGE_USERS_LOGIN 'report';

            IF(SELECT COUNT(*) FROM #Orphaned) > 0
            BEGIN
             SET @loop = 1
             WHILE @loop <= (SELECT MAX(IDENT) FROM #Orphaned)
              BEGIN
                SET @USER = (SELECT UserName FROM #Orphaned WHERE IDENT = @loop)
                IF(SELECT COUNT(*) FROM sys.server_principals WHERE [Name] = @USER) <= 0
                 BEGIN
                    EXEC SP_ADDLOGIN @USER,'{password}'
                 END

                EXEC SP_CHANGE_USERS_LOGIN 'update_one',@USER,@USER
                PRINT @USER + ' link to DB user reset';
                SET @loop = @loop + 1
              END
            END
            SET NOCOUNT OFF
            """


restoreDB = """
            USE [master]
            RESTORE DATABASE [was_lachen] FROM  DISK = N'D:\MSSQL\Backup\was_lachen.bak' WITH  FILE = 1,  MOVE N'was_lachen_dat' TO N'D:\MSSQL\DATA\was_lachen.mdf',  MOVE N'was_lachen_log' TO N'D:\MSSQL\DATA\was_lachen_log.ldf',  NOUNLOAD,  STATS = 5
            GO
            """

createRole = """
            USE {database};
            CREATE ROLE {role};
            GRANT EXECUTE TO {role};
            """