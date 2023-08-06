This is an abstract bundle of lite tools, follow next to install detail tools, and use `nxp_lite_tools` command to find the link of this page.

**1. Power performance data submitter**

Install:

    $ pip install -UI nxp_lite_tools[pp]

Usage:

    $ nxp_pp_submit -h
    usage: nxp_pp_submit [-h] -c CONFIG -r RESULT [-d]

    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            release config
      -r RESULT, --result RESULT
                            result file
      -d, --debug           mode

Desc:

    -c CONFIG: put the path of config.ini
    -r RESULT: if result file specified, submit this single result
               if result folder specified, iterate all .json and .csv in the folder, then submit all results
    -d       : set this flag if submit results to staging server
    
**2. Lf history data submitter**

Install:

    $ pip install -UI nxp_lite_tools[lf]

Import example:

    from nxp_lf import DbModel
    db_model = DbModel("Linux_Factory_On_Demand")

**3. NPI dashboard data submitter**

Install:

    $ pip install -UI nxp_lite_tools[pb]

Usage:

    $ nxp_pb_submit ...

**4. Customized lava docker slave install script**

Install:

    $ pip install -UI nxp_lite_tools[ls]

Usage:

    $ lava_docker_slave