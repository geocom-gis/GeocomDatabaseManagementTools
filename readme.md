# Geocom Database Management Tools

Geocom Database Management Tools help to create enterprise geodatabase, set database permissions, version data and manage other database tasks. These are standard tools used by Geocom Informatik AG. For more information please contact: support@geocom.ch. 

#### DISCLAMER: Please be aware that this product is not supported. Further information can be found in the license file.

------
## Requirements

- Installation of ArcGIS Desktop (minimum version 10.2). 
- Installation of a database client software, if you plan working with RDBMS.

------
## Installation 

1. Download the *Geocom Database Management Tools* 
3. Open ArcCatalog.
4. Navigate to *Catalog Tree*.
5. Create a new connection to the folder with the scripts.
6. Depending on your ArcGIS Desktop version choose appropriate toolbox (only when you use ArcGIS 10.2.x you need to use dedicated toolbox).
7. Before running the scripts read the chapter "Usage"


------
## Usage 

In the example below you will find a sample workflow how to set up a complete enterprise geodatabase. 

First you need create a new enterprise geodatabase and copy the data into it. Next step is to set permissions for roles and users. After that, feature classes and tables need to be registered as versioned. Lastly Geocom recommends to set up new spatial index values in order to keep high data performance. 


1. Create enterprise geodatabase (MSSQL).
2. Copy geodatabase to geodatabase.
3. Set permissions.
4. Register data as versioned.
5. Set spatial index geometry (MSSQL) or Set Spatial index sdebinary.

**IMPORTANT**: Always run the tools in exactly the same order.

> Some workflows are already predefined in the toolbox (see Toolgroup in folder *workflows*).
>
> You can create your own workflows and add them as a tool or use them as a standalone python script or batch-workflow.

------
## Help

Detailed description of each tool can be found in the "Tool Help" or in the "Description Page" in ArcMap or ArcCatalog.

#### Tool Help

1. To open "Tool help" navigate in ArcCatalog or in ArcMap to "Catalog Tree" and open the desired tool.
2. After the tools window opens click the button "Show Help >>". 
3. A new side panel will open with a description for the whole tool and for each field.

#### Description Page

1. To open "Description Page" navigate in ArcCatalog to "Catalog Tree" and select the desired tool.
2. In the right ArcCatalog window click on the bookmark "Description".
3. In the "Description Page" you will find the complete tool description presented in the standard ESRI template. 

**IMPORTANT**: Both options provide exactly the same information about the tools. 

------
## Known issues

- Geocom Database Management Tools do not support Oracle database.
- Geocom Database Management Tools do not support Esri Workgroup license.
- The tool "Set spatial index sdebinary" supports only standard Geocom databases. All the customer extensions (e.g. new feature classes or tables) will be ignored.
- The tool "Set spatial index sdebinary" supports only german database model.
