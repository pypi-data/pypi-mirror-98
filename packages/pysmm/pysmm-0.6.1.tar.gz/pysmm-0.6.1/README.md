# pysmm
PYthon Sentinel-1 soil-Moisture Mapping (PYSMM)

<p>This package acts as an interface to Google Earth Engine for the estimation of surface soil moisture based
on Copernicus Sentinel-1 intensity data. It is meant as a supplement to the following publication: <i> Greifeneder, F.,
C. Notarnicola, W. Wagner. A machine learning based approach for global surface soil moisture estimations with Google 
Earth Engine. </i>
The estimation of soil moisture is based on a Gradient Boosting Trees Regression machine learning approach. The model training
was performed based on in-situ data from the International Soil Moisture Network (ISMN). PYSMM all processing steps
for spatial and temporal mapping of surface soil moisture are fully executed online on GEE - none of the input data-sets
needs to be downloaded.</p>

<p>
Acknowledgements: This work was partially funded by the Horizon 2020 project "Ecopotential – 
Improving Future Ecosystem Benefits through Earth Observation, which has received funding from the European Research
Council (ERC) under the European Union's Horizon 2020 research and innovation programme
(grant agreement n° 641762) and the European Fund for Regional Development project "DPS4ESLAB".
</p>

<p>
To view the package documentation and instructions for the installation go to: http://pysmm.readthedocs.io/en/latest/
</p>

