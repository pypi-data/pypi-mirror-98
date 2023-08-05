

## Description

The <a href="https://www.youwol.com/">YouWol</a> local full-stack environment.
This is the first version of the module, documentation will be completed in the near future.

The environment provides:
- A local version of the YouWol platform
- A developer environment to extend the platform with personal contributions (packages, backends, frontends)

The key objective is to allow developers to contribute to the platform using their favorites tools.

## Requirements

* Python 3.6.*

The YouWol environment can be completed by installing *pipelines* (see section below),
whose may require additional installation (e.g. *node*, *gcc*, etc).
The pipelines should drive you to install their dependencies.

## Installation

```bash
pip install youwol
```
The environment comes with a few pipelines:
-  **youwol.pipelines.library_webpack_ts**: pipeline for npm library based on *typescript* and building with *webpack*
-  **youwol.pipelines.flux_pack**: pipeline for flux's modules box (flux is the low-code solution proposed by YouWol). 
It is also based on *typescript* and *webpack* but includes skeletons of flux modules
-  **youwol.pipelines.scribble_html**: simple HTML/javascript/css page for rapid solution prototyping
-  **youwol.pipelines.fastapi**: python server powered by <a href='https://fastapi.tiangolo.com/'>fastapi</a> library


The environment can be completed by installing new pipelines and using them in the configuration file
(search for *yw_pipeline* in <a href='https://pypi.org/'>pypi</a>).

For developers: to facilitate searching standalone pipelines, we recommend using the prefix 'yw_pipeline_*' in your
package name.


