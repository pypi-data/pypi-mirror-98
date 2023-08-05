![](https://travis-ci.com/AntelopeLCA/core.svg?branch=master&status=passed) ![](https://coveralls.io/repos/github/AntelopeLCA/core/badge.svg?branch=master)

# core
Antelope Catalog - reference implementation.

This repository provides code that enables access to different forms of life cycle 
inventory and impact assessment data, ideally from both local and remote sources.  It
allows you to view and index data sources, inspect their contents, and perform 
exchange relation queries, quantity relation queries, and LCIA computations.

At present, the Antelope Catalog relies on local LCA data on your machine, just like other
LCA software.  However, the plan is to remove this requirement by off-loading 
computing requirements to the cloud.   

## Additional Packages

The software for constructing and inverting background matrices, which requires 
[SciPy](https://www.scipy.org), is in a separate repository called 
[antelope_background](https://github.com/AntelopeLCA/background).  The idea is that 
these computations can be performed remotely, allowing lightweight clients to run
without scientific computing software (other than python).  However, at the moment 
this is not yet available.

The [antelope_foreground](https://github.com/AntelopeLCA/foreground) package allows
users to construct and compute product models that use a mixture of data sources.

Please visit and install these packages to access and test these functions. 

## Quick Start

### 1. Configure a local catalog

`antelope_core` is on PyPI-- note the optional dependency if you want to access datasets 
in XML formats (ILCD, EcoSpoldV1, EcoSpoldV2): 

    user@host$ pip install antelope_core[XML]
    
Antelope stores its content in a `catalog` --- for automated unit testing, this should be
specified in an environment variable:

    user@host$ export ANTELOPE_CATALOG_ROOT=/path/to/where/you/want/catalog
    
Once that's done, the catalog can be "seeded" with a core set of free tools by running the
local configuration unit test.  This is a bit tricky because unit tests are not usually
designed to be run on distributed code, so it requires a bit of a hack to specify the 
location of the installed package (note that if you are using a virtual environment, your
site-packages directory is inside that virtual environment):

    user@host$ python -m unittest discover -s /path/to/your/site-packages -p test_aa_local.py 

That will install: two different USLCI implementations (both somewhat stale), and the TRACI 2.1
LCIA methodology.

### 2. Start Running

You are now ready to perform LCIA calculations:

    user@host$ python3
    >>> from antelope_core import LcCatalog
    >>> from antelope import enum  # a simple "enumerate-and-show items" for interactive use
    
If you have defined your catalog root in your environment, you can import it:

    >>> from antelope_core.catalog.catalog_root import CATALOG_ROOT
    >>> cat = LcCatalog(CATALOG_ROOT) 
    Loading JSON data from /path/to/your/catalog/reference-quantities.json:
    local.qdb: /path/to/your/catalog/reference-quantities.json
    local.qdb: /data/GitHub/lca-tools/lcatools/qdb/data/elcd_reference_quantities.json
    25 new quantity entities added (25 total)
    6 new flow entities added (6 total)

Else, you can make it anything you want

    >>> cat = LcCatalog('/path/to/anywhere') 
    Loading JSON data from /path/to/anywhere/reference-quantities.json:
    local.qdb: /path/to/anywhere/reference-quantities.json
    local.qdb: /data/GitHub/lca-tools/lcatools/qdb/data/elcd_reference_quantities.json
    25 new quantity entities added (25 total)
    6 new flow entities added (6 total)
    
You then interact with the catalog by making queries to specific data sources:

    >>> cat.show_interfaces()  # output shown after running `test_aa_local`
    lcia.ipcc.2007.traci21 [basic, index, quantity]
    local.lcia.traci.2.1 [basic, index, quantity]
    local.qdb [basic, index, quantity]
    local.uslci.ecospold [basic, exchange, quantity]
    local.uslci.olca [basic, exchange, quantity]
     
    >>> lcias = enum(cat.query('local.lcia.traci.2.1').lcia_methods())
    local.lcia.traci.2.1: /data/LCI/TRACI/traci_2_1_2014_dec_10_0.xlsx
    Loading workbook /data/LCI/TRACI/traci_2_1_2014_dec_10_0.xlsx
    Applying stored configuration
    Applying context hint local.lcia.traci.2.1:air => to air
    Applying context hint local.lcia.traci.2.1:water => to water
    Applying configuration to Traci21Factors with 11 entities at /data/LCI/TRACI/traci_2_1_2014_dec_10_0.xlsx
    Missing canonical quantity-- adding to LciaDb
    registering local.lcia.traci.2.1/Acidification Air
     [00] [local.lcia.traci.2.1] Acidification Air [kg SO2 eq] [LCIA]
    Missing canonical quantity-- adding to LciaDb
    registering local.lcia.traci.2.1/Ecotoxicity, freshwater
     [01] [local.lcia.traci.2.1] Ecotoxicity, freshwater [CTUeco] [LCIA]
    Missing canonical quantity-- adding to LciaDb
    registering local.lcia.traci.2.1/Eutrophication Air
     [02] [local.lcia.traci.2.1] Eutrophication Air [kg N eq] [LCIA]
    Missing canonical quantity-- adding to LciaDb
    registering local.lcia.traci.2.1/Eutrophication Water
     [03] [local.lcia.traci.2.1] Eutrophication Water [kg N eq] [LCIA]
    Missing canonical quantity-- adding to LciaDb
    registering local.lcia.traci.2.1/Global Warming Air
     [04] [local.lcia.traci.2.1] Global Warming Air [kg CO2 eq] [LCIA]
    Missing canonical quantity-- adding to LciaDb
    registering local.lcia.traci.2.1/Human Health Particulates Air
     [05] [local.lcia.traci.2.1] Human Health Particulates Air [PM2.5 eq] [LCIA]
    Missing canonical quantity-- adding to LciaDb
    registering local.lcia.traci.2.1/Human health toxicity, cancer
     [06] [local.lcia.traci.2.1] Human health toxicity, cancer [CTUcancer] [LCIA]
    Missing canonical quantity-- adding to LciaDb
    registering local.lcia.traci.2.1/Human health toxicity, non-cancer
     [07] [local.lcia.traci.2.1] Human health toxicity, non-cancer [CTUnoncancer] [LCIA]
    Missing canonical quantity-- adding to LciaDb
    registering local.lcia.traci.2.1/Ozone Depletion Air
     [08] [local.lcia.traci.2.1] Ozone Depletion Air [kg CFC-11 eq] [LCIA]
    Missing canonical quantity-- adding to LciaDb
    registering local.lcia.traci.2.1/Smog Air
     [09] [local.lcia.traci.2.1] Smog Air [kg O3 eq] [LCIA]
     
    >>> lcias[3].show()
    QuantityRef catalog reference (Eutrophication Water)
    origin: local.lcia.traci.2.1
    UUID: f07dbefc-a5a0-3380-92fb-4c5c8a82fabb
       Name: Eutrophication Water
    Comment: 
    ==Local Fields==
               Indicator: kg N eq
              local_Name: Eutrophication Water
           local_Comment: 
    local_UnitConversion: {'kg N eq': 1.0}
            local_Method: TRACI 2.1
          local_Category: Eutrophication Water
         local_Indicator: kg N eq
         
    >>> _=enum(lcias[3].factors())
    Imported 14 factors for [local.lcia.traci.2.1] Eutrophication Water [kg N eq] [LCIA]
     [00]   7.29 [GLO] [kg N eq / kg] local.lcia.traci.2.1/phosphorus: water (Eutrophication Water [kg N eq] [LCIA])
     [01]   3.19 [GLO] [kg N eq / kg] local.lcia.traci.2.1/phosphorus pentoxide: water (Eutrophication Water [kg N eq] [LCIA])
     [02]   2.38 [GLO] [kg N eq / kg] local.lcia.traci.2.1/phosphate: water (Eutrophication Water [kg N eq] [LCIA])
     [03]   2.31 [GLO] [kg N eq / kg] local.lcia.traci.2.1/phosphoric acid: water (Eutrophication Water [kg N eq] [LCIA])
     [04]  0.986 [GLO] [kg N eq / kg] local.lcia.traci.2.1/nitrogen: water (Eutrophication Water [kg N eq] [LCIA])
     [05]  0.779 [GLO] [kg N eq / kg] local.lcia.traci.2.1/ammonium: water (Eutrophication Water [kg N eq] [LCIA])
     [06]  0.779 [GLO] [kg N eq / kg] local.lcia.traci.2.1/ammonia: water (Eutrophication Water [kg N eq] [LCIA])
     [07]  0.451 [GLO] [kg N eq / kg] local.lcia.traci.2.1/nitric oxide: water (Eutrophication Water [kg N eq] [LCIA])
     [08]  0.291 [GLO] [kg N eq / kg] local.lcia.traci.2.1/nitrogen dioxide: water (Eutrophication Water [kg N eq] [LCIA])
     [09]  0.291 [GLO] [kg N eq / kg] local.lcia.traci.2.1/nitrogen oxides: water (Eutrophication Water [kg N eq] [LCIA])
     [10]  0.237 [GLO] [kg N eq / kg] local.lcia.traci.2.1/nitrate: water (Eutrophication Water [kg N eq] [LCIA])
     [11]  0.227 [GLO] [kg N eq / kg] local.lcia.traci.2.1/nitric acid: water (Eutrophication Water [kg N eq] [LCIA])
     [12]   0.05 [GLO] [kg N eq / kg] local.lcia.traci.2.1/biological oxygen demand: water (Eutrophication Water [kg N eq] [LCIA])
     [13]   0.05 [GLO] [kg N eq / kg] local.lcia.traci.2.1/chemical oxygen demand: water (Eutrophication Water [kg N eq] [LCIA])
     
    >>>

Specific objects, whose IDs are known, can be retrieved by ID: 
     
    >>> p = cat.query('local.uslci.olca').get('ba5df01a-626b-35b8-859f-f1df42dd54a0')
    ...
     
    >>> p.show()
    ProcessRef catalog reference (ba5df01a-626b-35b8-859f-f1df42dd54a0)
    origin: local.uslci.olca
    UUID: ba5df01a-626b-35b8-859f-f1df42dd54a0
       Name: Polyethylene, low density, resin, at plant, CTR
    Comment: 
    ==Local Fields==
       SpatialScope: RNA
      TemporalScope: {'begin': '2002-01-01-05:00', 'end': '2003-01-01-05:00'}
    Classifications: ['Chemical Manufacturing', 'All Other Basic Organic Chemical Manufacturing']

    >>> rxs = enum(p.references())
     [00] [ Polyethylene, low density, resin, at plant, CTR [RNA] ]*==>  1 (kg) Polyethylene, low density, resin, at plant, CTR 
     [01] [ Polyethylene, low density, resin, at plant, CTR [RNA] ]*==>  0.429 (MJ) Recovered energy, for Polyethylene, low density, resin, at plant, CTR
     
    >>> 

LCIA can be computed for process inventories (note, however, that without `antelope_background` it is not
possible to compute LCI results.  In this case the cradle-to-resin dataset is already an LCI). Again, 
to do that, please visit / install [antelope_background](https://github.com/AntelopeLCA/background).

    >>> res = lcias[3].do_lcia(p.inventory(rxs[0]))
    ...
    
    >>> res.show_details()
    [local.lcia.traci.2.1] Eutrophication Water [kg N eq] [LCIA] kg N eq
    ------------------------------------------------------------

    [local.uslci.olca] Polyethylene, low density, resin, at plant, CTR [RNA]:
       1.14e-05 =       0.05  x   0.000228 [GLO] local.lcia.traci.2.1/chemical oxygen demand, water, unspecified
       5.89e-06 =      0.779  x   7.55e-06 [GLO] local.lcia.traci.2.1/ammonia, water, unspecified
       2.85e-06 =       0.05  x    5.7e-05 [GLO] local.lcia.traci.2.1/biological oxygen demand, water, unspecified
       7.29e-07 =       7.29  x      1e-07 [GLO] local.lcia.traci.2.1/phosphorus, water, unspecified
       7.62e-08 =      0.986  x   7.73e-08 [GLO] local.lcia.traci.2.1/nitrogen, water, unspecified
       2.42e-08 =      0.779  x    3.1e-08 [GLO] local.lcia.traci.2.1/ammonium, water, unspecified
       2.1e-05 [local.lcia.traci.2.1] Eutrophication Water [kg N eq] [LCIA]
       
    >>>

Search requires an index to be created:
    
    >>> q = cat.query('local.uslci.olca')
    >>> _=enum(q.processes(Name='polyethylene')
    ---------------------------------------------------------------------------
    IndexRequired                             Traceback (most recent call last)
    ...
    IndexRequired: itype index required for attribute processes | ()

    >>> cat.index_ref(q.origin)
    ...
    'local.uslci.olca.index.20210205'
    
    >>> _=enum(q.processes(Name='polyethylene')
     [00] [local.uslci.olca] Polyethylene, low density, resin, at plant [RNA]
     [01] [local.uslci.olca] Polyethylene, linear low density, resin, at plant [RNA]
     [02] [local.uslci.olca] Polyethylene terephthalate, resin, at plant [RNA]
     [03] [local.uslci.olca] Polyethylene, linear low density, resin, at plant, CTR [RNA]
     [04] [local.uslci.olca] Polyethylene, low density, resin, at plant, CTR [RNA]
     [05] [local.uslci.olca] Polyethylene, high density, resin, at plant, CTR [RNA]
     [06] [local.uslci.olca] Polyethylene, high density, resin, at plant  [RNA]
     [07] [local.uslci.olca] Polyethylene terephthalate, resin, at plant, CTR [RNA]
     
    >>>
    
### Installing Ecoinvent
If you have an ecoinvent license, you can install it in your catalog by first downloading 
the 7z files that contain the EcoSpold datasets and storing them on your system.

You will need to create a folder for ecoinvent, and then create a subfolder for each version 
(say, '3.7.1'), and put the 7z files in that.

    user@host$ mkdir -p /path/to/Ecoinvent/3.7.1

The 7z files unfortunately need to be extracted before they can be loaded.  After you are done
you should have something that looks like this:

    user@host$ ls /path/to/Ecoinvent/3.7.1
    'ecoinvent 3.7.1_cutoff_ecoSpold02'  'ecoinvent 3.7.1_cutoff_ecoSpold02.7z'
    user@host$ 
    
After that, you can setup ecoinvent in your catalog from within python:

    >>> from antelope_core.data_sources.ecoinvent import EcoinventConfig
    >>> ec = EcoinventConfig('/path/to/Ecoinvent')
    >>> _=enum(ec.references)
     [00] local.ecoinvent.3.7.1.cutoff
     
    >>> ec.register_all_resources(cat)
    >>> 
    
Again, you will need to index the resources before being able to search through them- this takes 
several minutes. This is why we are working on a remote solution for this problem.

Warning: if you want to do Ecoinvent LCI as well, you will need 
[antelope_background](https://github.com/AntelopeLCA/background) -- please
visit that page.

# Contributing

Fork, open an issue, whatever.
