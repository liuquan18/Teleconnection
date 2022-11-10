# Depedent Index from dynamical spatial patterns
The indexes here are used to show the main plots in the paper.
- *Horizontal-vertical EOF* (dependent) takes the whole troposphere as a whole, the magnitude of the spatial patterns strengthen, the shift of the centers of actions are mild (compared to horizontal EOF).
- *dynamical spatial patterns* makes sure that the index also reveals the change of the spatial patterns. 

## Two methods of standardization are applied here 
1. all_first and all_last are generated, then standard by its own temporal *mean* and *std*. index in first10 years and last10 years are selected.

    - generate `all_first` and `all_last`
    
        > the pattern 
    ```python
    # standard      ---- make  all levels standard.
    # dependent     ---- the chosen vetical strategy.
    # fixed pattern ---- fix the pattern to be `first` or `last`.
    eof_sira,pc_sira,fra_sira = sp.season_eof(
        geopotential_height,
        nmode=2,
        method ="rolling_eof",
    window=10,fixed_pattern='all',return_full_eof= False,independent = True,standard=True)
    ```



2. all_first, all_last, and all_all are generated. then first10_first and last10_last are selected. both of them are standard with the temporal mean and std of all_all.
