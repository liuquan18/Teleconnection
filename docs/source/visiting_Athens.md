# Visiting Athens
The paper focuses on the following scientific question: How does global warming influence the internal variability of teleconnection modes like the North Atlantic Oscillation (NAO) and East Atlantic (EA) pattern, in terms of extreme states? Since we only focus on the internal variability, the externally forced signal is removed beforehand. The global warming’s influence on internal variability of NAO and EA is then represented as the difference between the last 10 years and the first 10 years in the 1% CO_2 run. 

To ensure the robustness, the spatial pattern are decomposed with EOF analysis over all the temporal_ensemble fields (that's 150*100 samples), and all vetical altitudes (Horizontal_vetival EOF), hereafter referred as "all_pattern". Then the indexes are generated by projecting the geopotential height data onto the "all_pattern". Here shows the statistics of standardized indexes (with temporal_ens_mean and _std).

## 1. More negative extreme NAO and EA in a warmer climate
PDF and violin plots show obvious increased negative extremes. 
### PDF in 850hpa
![PDF850](plots/first10_last10/all_whole_std/whole_PDF_850.png)
Fig 1. **More negative extreme North Atlantic Oscillation and East Atlantic pattern in a warmer climate.** Probability Density Function of North Atlantic Oscillation (upper left) and East Atlantic pattern (upper right) indexes in first10 years (shadings) and last10 years (lines) at 850hpa geopotential height.

### PDF in 1000hpa
![PDF1000](plots/first10_last10/all_whole_std/whole_PDF_1000.png)
Fig 2. The same as Fig 1. but for 1000hpa geopotential height. 

### violin plot
![violin](plots/first10_last10/all_whole_std/violin_vertical.png)
Fig 3. **More negative extreme North Atlanci Osciilation and East Atlantic pattern.** Violin plots of North Atlantic Oscillation (left) and East Atlantic pattern (right) in the first10 years (blue) and last10 years (orange) at all altitudes.

## 2. Increased count of negative extreme cases
We define the cases above (below) the 2std as the extreme events. The count of the extreme cases over different altitudes are shown as following: NAO shows clear increased negative extremes, the count of positive extreme stays the same. EA shows similiar result as NAO, but not so clear over lower altitudes.

### NAO vertical Profile
![NAO_profile](plots/first10_last10/all_whole_std/NAO_profile.png)
Fig 4. **Raised negative extremes of North Atlantic Oscillation in a warmer climate.** Vertical profile of extreme counts of North Atlantic Oscillation at all altitudes in the first10 (solid) and last10 (dashed) years. the last column shows the difference.

### EA vertical profile
![EA_profile](plots/first10_last10/all_whole_std/EA_profile.png)
Fig 5. The same as Fig 4, but for East Atlantic pattern. 

## 4. return period of extremes

**Extreme Value Theory** provides another way to check the extremeness of the index.
Since the index among ensemble domain are Indentical Independent Distributed, the idea of "Block Maximum" of Extreme Value Theory can be extended to ensemble domain. i.e, the maximum along ensemble should also fit to the extreme distribution.
### 4.1 The return period of NAO and EA at 500hpa.
![NAO_return period](plots/first10_last10/all_whole_std/NAO_return_period.png)
Fig 6 The return period of NAO index in the first10 (blue) and last10 (red) years
![EA_return period](plots/first10_last10/all_whole_std/EA_return_period.png)
Fig 7 The return period of EA index in the first10 (blue) and last10 (red) years.


### 4.2 the median return period vertical profile

![NAO vertical profile](plots/first10_last10/all_whole_std/NAO_return_period_vetical.png)
Fig 8 the vertical profile of median return period of NAO index in the first10 (blue) and last10 (red) years.

![EA vertical profile](plots/first10_last10/all_whole_std/EA_return_period_vetical.png)
Fig 9 the vertical profile of median return period of EA index in the first10 (blue) and last10 (red) years.


## 5. The extreme spatial patterns
composite analysis of geopotential height data in terms of different extreme types and different periods shows the change in spatial patterns of extreme cases.

For **NAO**, positive extreme shows tripole pattern in the last10 years, compared to dipole pattern in the first10 years. negative extremes shows typical NAO spatial patterns, but strengthened in amplitude. The clear pattern change of NAO positive extremes may correspond to the non-obvious change of extreme positive extreme counts. Thus, dynamical patterns to generate the index are also excuted. 
For **EA**, both positive and negative extremes show eastward shifts, such shifts are more obvious if dynamical spatial patterns are adopted.
### spatial pattern change (Z500)
![spatail_pattern_Z500](plots/first10_last10/all_whole_std/whole_extreme_spatial_pattern_Z500.png)
Fig 10. **Spatial patterns of extremes in a warmer climate.** the composite analysis of 500hpa geopotential height data in terms of different extreme types and periods.
### spatial pattern change (section)
![spatail_pattern_section](plots/first10_last10/all_whole_std/extreme_spatial_pattern_section.png)
Fig 11. **sptial patterns of extremes in a warmer climate.** Zonally averaged sptail pattern of extremes (rows) of North Atlantic Oscillation (left) and meridionally averaged spatial patterns of East Atlantic pattern (right).

## 6. Effects of increased extreme events of teleconnections

Does such kind of change matter? Here we do the composite analysis of temperature and precipitation in terms of different extreme types.

**Surface temperature - NAO extreme types**

Composite analysis of surface temperature in terms of different NAO extreme types. The last column shows the difference. 

![NAO_temp](plots/wrap_up_aftervoc/NAO_temp.png)
Fig 12. **Less warming over Northern Eurasia in winter.** composite analsysis of surface temperature in terms of different extreme types (rows) and different periods (first 2 cols). The last columns shows the difference.

for NAO extremes, the influence of positive extremes (warm anomalies over northern Eurasia) gets weaker in the last 10 years. The influence of negative extreme events (cold anomalies over northern Eurasia) gets stronger in the last 10 years. Overall, both positive and negative extremes of NAO lead to less warming over northern Eurasia and the adjacent polar regions. 

![EA_temp](plots/wrap_up_aftervoc/EA_TEMP.png)
For EA extremes, both the influences of positive extremes (warm anomalies over Eurasia) and negative extremes (cold anomalies over Eurasia) extend eastward to East Asia. 
Fig 13. **Cooling extends to east Eurasia.** Same as Fig 8. but for East Atlantic pattern. 

## 5. different definition of extremes in the first10 and last10 years

### NAO extreme counts vertical profile
![NAO_self_dynamic](plots/first10_last10/dynamic_self_std/NAO_self.png)

### EA extreme counts vertical profile
![EA_self_dynamic](plots/first10_last10/dynamic_self_std/EA_self.png)


### extreme sptial patterns
![Z500](plots/first10_last10/dynamic_self_std/dynamic_self_extreme_pattern_Z500.png)
![section](plots/first10_last10/dynamic_self_std/dynamic_self_extreme_pattern_section.png)

## 6. problems
- papers to read