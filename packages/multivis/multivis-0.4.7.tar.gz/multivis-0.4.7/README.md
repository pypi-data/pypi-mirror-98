# MultiVis
The MultiVis package contains the necessary tools for visualisation of multivariate data.

## Installation

### Dependencies
multivis requires:
- Python (>=3.5)
- NumPy (==1.19.2)
- Pandas (==0.25.1)
- Matplotlib (==3.1.1)
- Seaborn (==0.9.0)
- Networkx (==2.3.0)
- SciPy (==1.3.1)
- Scikit-learn (==0.21.3)
- tqdm (==4.36.1)
- xlrd (==1.2.0)

### User installation
The recommend way to install multivis and dependencies is to using ``conda``:
```console
conda install -c brett.chapman multivis
```
or ``pip``:
```console
pip install multivis
```
Alternatively, to install directly from github:
```console
pip install https://github.com/brettChapman/multivis/archive/master.zip
```

### API
For further detail on the usage refer to the docstring.

#### multivis
- [Edge](https://github.com/brettChapman/multivis/blob/master/multivis/Edge.py): Generates dataframe of nodes and edges.
	- [init_parameters](https://github.com/brettChapman/multivis/blob/master/multivis/Edge.py#L34-L43)
		- [peaktable] : Pandas dataframe containing peak data. Must contain 'Name' and 'Label'.
		- [datatable] : Pandas dataframe matrix containing scores.
		- [pvalues] : Pandas dataframe matrix containing score/similarity pvalues (if available, otherwise set to None)
	- [methods](https://github.com/brettChapman/multivis/blob/master/multivis/Edge.py#L45-L122)
		- [set_params] : Set parameters
			- [filter_type] : The value type to filter similarities on (default: 'pvalue')
			- [hard_threshold] : Value to filter similarities on (default: 0.005)
			- [withinBlocks] : Include scores within blocks if building multi-block network (default: False)
			- [sign] : The sign of the score/similarity to filter on ('pos', 'neg' or 'both') (default: 'both')
					
		- [build] : Builds the nodes and edges.
		- [getNodes] : Returns a Pandas dataframe of all nodes.
		- [getEdges] : Returns a Pandas dataframe of all edges.        	

- [Network](https://github.com/brettChapman/multivis/blob/master/multivis/Network.py): Inherits from Edge and generates dataframe of nodes, edges, and a NetworkX graph.
	- [init_parameters](https://github.com/brettChapman/multivis/blob/master/multivis/Network.py#L33-L37)
		- [peaktable] : Pandas dataframe containing peak data. Must contain 'Name' and 'Label'.
		- [datatable] : Pandas dataframe matrix containing scores.
		- [pvalues] : Pandas dataframe matrix containing score/similarity pvalues.
	- [methods](https://github.com/brettChapman/multivis/blob/master/multivis/Network.py#L39-L59)
		- [set_params] : Set parameters
			- [filter_type] : The value type to filter the data on (default: 'pvalue')
			- [hard_threshold] : Value to filter the data on (default: 0.005)
			- [link_type] : The value type to represent links in the network (default: 'score')
			- [withinBlocks] : Include scores within blocks if building multi-block network (default: False)
			- [sign] : The sign of the score/similarity to filter on ('pos', 'neg' or 'both') (default: 'both')
					
		- [build] : Builds nodes, edges and NetworkX graph.
		- [getNetworkx] : Returns a NetworkX graph.
		- [getLinkType] : Returns the link type parameter used in building the network.

- [edgeBundle](https://github.com/brettChapman/multivis/blob/master/multivis/edgeBundle.py): Generates and displays a Hierarchical edge bundle plot.
	- [init_parameters](https://github.com/brettChapman/multivis/blob/master/multivis/edgeBundle.py#L33-37)
		- [edges] : Pandas dataframe containing edges generated from Edge.
	- [methods](https://github.com/brettChapman/multivis/blob/master/multivis/edgeBundle.py#L39-L104)
		- [set_params] : Set parameters
			- [html_file] : Name to save the HTML file as (default: 'hEdgeBundle.html')
			- [innerRadiusOffset] : Sets the inner radius based on the offset value from the canvas width/diameter (default: 120)
			- [blockSeparation] : Value to set the distance between different segmented blocks (default: 1)
			- [linkFadeOpacity] : The link fade opacity when hovering over/clicking nodes (default: 0.05)
			- [mouseOver] : Setting to 'True' swaps from clicking to hovering over nodes to select them (default: True)
			- [fontSize] : The font size in pixels set for each node (default: 10)
			- [backgroundColor] : Set the background colour of the plot (default: 'white')
			- [foregroundColor] : Set the foreground colour of the plot (default: 'black')
			- [node_data] : Peak Table column names to include in the mouse over information (default: 'Name' and 'Label')			
			- [nodeColorScale] : The scale to use for colouring the nodes ("linear", "reverse_linear", "log", "reverse_log", "square", "reverse_square", "area", "reverse_area", "volume", "reverse_volume", "ordinal") (default: 'linear')
			- [node_color_column] : The Peak Table column to use for node colours (default: None sets to black)
			- [node_cmap] : Set the CMAP colour palette to use for colouring the nodes (default: 'brg')
			- [edgeColorScale] : The scale to use for colouring the edges, if edge_color_value is 'pvalue' ("linear", "reverse_linear", "log", "reverse_log", "square", "reverse_square", "area", "reverse_area", "volume", "reverse_volume", "ordinal") (default: 'linear')
			- [edge_color_value] : Set the values to colour the edges by. Either 'sign', 'score' or 'pvalue' (default: 'score')
			- [edge_cmap] : Set the CMAP colour palette to use for colouring the edges (default: 'brg')
			- [addArcs] : Setting to 'True' adds arcs around the edge bundle for each block (default: False)
			- [arcRadiusOffset] : Sets the arc radius offset from the inner radius (default: 20)
			- [extendArcAngle] : Sets the angle value to add to each end of the arcs (default: 2)
			- [arc_cmap] : Set the CMAP colour palette to use for colouring the arcs (default: 'Set1')

		- [build] : Generates the JavaScript embedded HTML code, writes to a HTML file and opens it in a browser.
		- [buildDashboard] : Generates the JavaScript embedded HTML code in a dashboard format, writes to a HTML file and opens it in a browser.
		
- [plotNetwork](https://github.com/brettChapman/multivis/blob/master/multivis/plotNetwork.py): Generates and displays a static NetworkX graph given a user defined layout.
	- [init_parameters](https://github.com/brettChapman/multivis/blob/master/multivis/plotNetwork.py#L41-L45)
		- [g] : NetworkX graph.
	- [methods](https://github.com/brettChapman/multivis/blob/master/multivis/plotNetwork.py#L47-L211)
		- [set_params] : Set parameters
			- [imageFileName] : The image file name to save to (default: 'networkPlot.jpg')
			- [edgeLabels] : Setting to 'True' labels all edges with the similarity score (default: True)
			- [saveImage] : Setting to 'True' will save the image to file (default: True)
			- [layout] : Set the NetworkX layout type ('circular', 'kamada_kawai', 'random', 'spring', 'spectral') (default: 'spring')
			- [dpi] : The number of Dots Per Inch (DPI) for the image (default: 200)
			- [figSize] : The figure size as a tuple (width,height) (default: (30,20))
			- [node_cmap] : The CMAP colour palette to use for nodes (default: 'brg')
			- [colorScale] : The node colour scale to apply ("linear", "reverse_linear", "log", "reverse_log", "square", "reverse_square", "area", "reverse_area", "volume", "reverse_volume", "ordinal") (default: 'linear')
			- [node_color_column] : The Peak Table column to use for node colours (default: None sets to black)
			- [sizeScale] : The node size scale to apply ("linear", "reverse_linear", "log", "reverse_log", "square", "reverse_square", "area", "reverse_area", "volume", "reverse_volume", "ordinal") (default: 'reverse_linear')
			- [size_range] : The node size scale range to apply. Tuple of length 2. Minimum size to maximum size (default: (150,2000))
			- [sizing_column] : The node sizing column to use (default: sizes all nodes to 1)	
			- [alpha] :  Node opacity value (default: 0.5)
			- [nodeLabels] : Setting to 'True' will label the nodes (default: True)
			- [fontSize] : The font size set for each node (default: 15)
			- [keepSingletons] : Setting to 'True' will keep any single nodes not connected by edges in the NetworkX graph) (default: True)
			- [column] : Column from Peak Table to filter on (default: no filtering)
			- [threshold] : Value to filter on (default: no filtering)
			- [operator] : The comparison operator to use when filtering (default: '>')
			- [sign] : The sign of the score to filter on ('pos', 'neg' or 'both') (default: 'pos')
		
		- [build] : Generates and displays the NetworkX graph.

- [springNetwork](https://github.com/brettChapman/multivis/blob/master/multivis/springNetwork.py): Interactive spring-embedded network which inherits data from the NetworkX graph.
	- [init_parameters](https://github.com/brettChapman/multivis/blob/master/multivis/springNetwork.py#L38-L42)
		- [g] : NetworkX graph.
	- [methods](https://github.com/brettChapman/multivis/blob/master/multivis/springNetwork.py#L44-L113)
		- [set_params] : Set parameters
			- [node_size_scale] : dictionary(Peak Table column name as index: dictionary('scale': ("linear", "reverse_linear", "log", "reverse_log", "square", "reverse_square", "area", "reverse_area", "volume", "reverse_volume", "ordinal")
                	                                                                            'range': a number array of length 2 - minimum size to maximum size)) (default: sizes all nodes to 10 with no dropdown menu)
			- [node_color_scale] : dictionary(Peak Table column name as index: dictionary('scale': ("linear", "reverse_linear", "log", "reverse_log", "square", "reverse_square", "area", "reverse_area", "volume", "reverse_volume", "ordinal")
			- [html_file] : Name to save the HTML file as (default: 'springNetwork.html')
			- [backgroundColor] : Set the background colour of the plot (default: 'white')
			- [foregroundColor] : Set the foreground colour of the plot (default: 'black')
			- [chargeStrength] : The charge strength of the spring-embedded network (force between nodes) (default: -120)
			- [groupByBlock] : Setting to 'True' will group nodes by 'Block' if present in the data (default: False)
			- [groupFociStrength] : Set the strength of foci for each group (default: 0.2)
			- [intraGroupStrength] : Set the strength between each group (default: 0.01)
			- [groupLayoutTemplate] : Set the layout template to use for grouping (default: 'treemap')
			- [node_text_size] : The text size for each node (default: 15)
			- [fix_nodes] : Setting to 'True' will fix nodes in place when manually moved (default: False)
			- [displayLabel] : Setting to 'True' will set the node labels to the 'Label' column, otherwise it will set the labels to the 'Name' column from the Peak Table (default: False)
			- [node_data] : Peak Table column names to include in the mouse over information (default: 'Name' and 'Label')
			- [link_type] : The link type used in building the network (default: 'score')
			- [link_width] : The width of the links (default: 0.5)
			- [pos_score_color] : Colour value for positive scores. Can be HTML/CSS name, hex code, and (R,G,B) tuples (default: 'red')
			- [neg_score_color] : Colour value for negative scores. Can be HTML/CSS name, hex code, and (R,G,B) tuples (default: 'black')
		
		- [build] : Generates the JavaScript embedded HTML code and writes to a HTML file and opens it in a browser.
		- [buildDashboard] : Generates the JavaScript embedded HTML code in a dashboard format, writes to a HTML file and opens it in a browser.

- [clustermap](https://github.com/brettChapman//multivis/blob/master/multivis/clustermap.py): Hierarchical Clustered Heatmap.
	- [init_parameters](https://github.com/brettChapman//multivis/blob/master/multivis/clustermap.py#L42-L50)
		- [scores] : Pandas dataframe scores.
        	- [row_linkage] : Precomputed linkage matrix for the rows from a linkage clustered distance/similarities matrix
        	- [col_linkage] : Precomputed linkage matrix for the columns from a linkage clustered distance/similarities matrix
	- [methods](https://github.com/brettChapman//multivis/blob/master/multivis/clustermap.py#L52-L350)
		- [set_params] : Set parameters
			- [xLabels] : A Pandas Series for labelling the X axis of the HCH
			- [yLabels] : A Pandas Series for labelling the Y axis of the HCH
			- [imageFileName] : The image file name to save to (default: 'clusterMap.png')
			- [saveImage] : Setting to 'True' will save the image to file (default: True)
			- [dpi] : The number of Dots Per Inch (DPI) for the image (default: 200)
			- [figSize] : The figure size as a tuple (width,height) (default: (80,70))
			- [dendrogram_ratio_shift] : The ratio to shift the position of the dendrogram in relation to the heatmap (default: 0.0)
			- [dendrogram_line_width] : The line width of the dendrograms (default: 1.5)
			- [fontSize] : The font size set for each node (default: 30)
			- [heatmap_cmap] : The CMAP colour palette to use for the heatmap (default: 'RdYlGn')
			- [cluster_cmap] : The CMAP colour palette to use for the branch seperation of clusters in the dendrogram (default: 'Set1')
			- [rowColorCluster] : Setting to 'True' will display a colour bar for the clustered rows (default: False)
			- [colColorCluster] : Setting to 'True' will display a colour bar for the clustered columns (default: False)
			- [row_color_threshold] : The colouring threshold for the row dendrogram (default: 10)
			- [col_color_threshold] : The colouring threshold for the column dendrogram (default: 10)
		
		- [build] : : Generates and displays the Hierarchical Clustered Heatmap (HCH).

- [polarDendrogram](https://github.com/brettChapman/multivis/blob/master/multivis/polarDendrogram.py): Polar dendrogram
	- [init_parameters](https://github.com/brettChapman/multivis/blob/master/multivis/polarDendrogram.py#L36-L40)
		- [dn] : Dendrogram dictionary labelled by Peak Table index
	- [methods](https://github.com/brettChapman/multivis/blob/master/multivis/polarDendrogram.py#42-L159)
		- set_params : Set parameters
			- [imageFileName] : The image file name to save to (default: 'polarDendrogram.png')
			- [saveImage] : Setting to 'True' will save the image to file (default: True)
			- [branch_scale] : The branch distance scale to apply ('linear', 'log', 'square') (default: 'linear')
			- [gap] : The gap size within the polar dendrogram (default: 0.1)
			- [grid] : Setting to 'True' will overlay a grid over the polar dendrogram (default: False)
			- [style_sheet] : Setting the Seaborn style-sheet (see https://python-graph-gallery.com/104-seaborn-themes/) (default: 'seaborn-white')
			- [dpi] : The number of Dots Per Inch (DPI) for the image (default: 200)
			- [figSize] : The figure size as a tuple (width,height) (default: (10,10))
			- [fontSize] : The font size for all text (default: 15)
			- [PeakTable] : The Peak Table Pandas dataframe (default: empty dataframe)
			- [textColorScale] : The scale to use for colouring the text ("linear", "reverse_linear", "log", "reverse_log", "square", "reverse_square", "area", "reverse_area", "volume", "reverse_volume", "ordinal") (default: 'linear')
			- [text_color_column] : The colour column to use from Peak Table (Can be colour or numerical values such as 'pvalue') (default: 'black')
			- [label_column] : The label column to use from Peak Table (default: use original Peak Table index from cartesian dendrogram)
			- [text_cmap] : The CMAP colour palette to use (default: 'brg')

		- [getClusterPlots] : Generates plots of mean peak area over the 'Class' variable for each cluster from the polar dendrogram
			- [column_numbers] : The number of columns to display in the plots (default: 2)
			- [log] : Setting to 'True' will log the data (default: True)
			- [autoscale] :  Setting to 'True' will scale the data to unit variance (Default: True)
			- [figSize] : The figure size as a tuple (width,height) (default: (10,20))
			- [saveImage] : Setting to 'True' will save the image to file (default: True)
			- [imageFileName] : The image file name to save to (default: 'clusterPlots.png')
			- [dpi] : The number of Dots Per Inch (DPI) for the image (default: 200)
		
		- [build] : Generates and displays the Polar dendrogram.

- [pca](https://github.com/brettChapman/multivis/blob/master/multivis/pca.py): Principle Component Analysis (PCA) plot
	- [parameters](https://github.com/brettChapman/multivis/blob/master/multivis/pca.py#L7)
		- [data] : array-like matrix, shape (n_samples, n_features)
		- [imageFileName] : The image file name to save to (default: 'PCA.png')
		- [saveImage] : Setting to 'True' will save the image to file (default: True)
		- [dpi] : The number of Dots Per Inch (DPI) for the image (default: 200)
		- [pcx] : The first component (default: 1)
		- [pcy] : The second component (default: 2)
		- [group_label] : Labels to assign to each group/class in the PCA plot (default: None)
		- [sample_label] : Labels to assign to each sample in the PCA plot (default: None)
		- [peak_label] : Labels to assign to each peak in the loadings biplot (default: None)
		- [markerSize] : The size of each marker (default: 100)
		- [fontSize] : The font size set for each node (default: 12)
		- [figSize] : The figure size as a tuple (width,height) (default: (20,10))
		- [cmap] : The CMAP colour palette to use (default: 'Set1')

- [pcoa](https://github.com/brettChapman/multivis/blob/master/multivis/pcoa.py): Principle Coordinates Analysis (PCoA) plot
	- [parameters](https://github.com/brettChapman/multivis/blob/master/multivis/pcoa.py#L8)
		- [scores] : array-like matrix, shape (n_samples, n_features)
		- [imageFileName] : The image file name to save to (default: 'PCOA.png')
		- [saveImage] : Setting to 'True' will save the image to file (default: True)
		- [dpi] : The number of Dots Per Inch (DPI) for the image (default: 200)
		- [n_components] : Number of components (default: 2)
		- [max_iter] : Maximum number of iterations of the SMACOF algorithm (default: 300)
		- [eps] : Relative tolerance with respect to stress at which to declare convergence (default: 1e-3)
		- [seed] : Seed number used by the random number generator for the RandomState instance (default: 3)
		- [group_label] : Labels to assign to each group/class (default: None)
		- [peak_label] : Labels to assign to each peak (default: None)
		- [markerSize] : The size of each marker (default: 100)
		- [fontSize] : The font size set for each node (default: 12)
		- [figSize] : The figure size as a tuple (width,height) (default: (20,10))
		- [cmap] : The CMAP colour palette to use (default: 'Set1')

#### multivis.utils

- [loadData](https://github.com/brettChapman/multivis/blob/master/multivis/utils/loadData.py): Loads and validates the Data and Peak sheet from an excel file.
	- [parameters](https://github.com/brettChapman/multivis/blob/master/multivis/utils/loadData.py#L6)
		- [filename] : The name of the excel file (.xlsx file) e.g. 'Data.xlsx'.
		- [DataSheet] : The name of the data sheet in the file e.g. 'Data'. The data sheet must contain an 'Idx', 'SampleID', and 'Class' column.
		- [PeakSheet] : The name of the peak sheet in the file e.g. 'Peak'. The peak sheet must contain an 'Idx', 'Name', and 'Label' column.
	- [Returns](https://github.com/brettChapman/multivis/blob/master/multivis/utils/loadData.py#L52)
		- DataTable: Pandas dataFrame
		- PeakTable: Pandas dataFrame

- [mergeBlocks](https://github.com/brettChapman/multivis/blob/master/multivis/utils/mergeBlocks.py): Merges multiply different Data Tables and Peak Tables into a single Peak Table and Data Table (used for multi-block/multi-omics data preparation). The 'Name' column needs to be unique across all blocks. Automatically annotates the merged Peak Table with a 'Block' column using the dictionary keys.
	- [parameters](https://github.com/brettChapman/multivis/blob/master/multivis/utils/mergeBlocks.py#L5)
		- [peak_blocks] : A dictionary of Pandas Peak Table dataframes from different datasets indexed by dataset type.
		- [data_blocks] : A dictionary of Pandas Data Table dataframes from different datasets indexed by dataset type.
	- [Returns](https://github.com/brettChapman/multivis/blob/master/multivis/utils/mergeBlocks.p#77)
		- [DataTable] : Merged Pandas dataFrame
		- [PeakTable] : Merged Pandas dataFrame

- [scaleData](https://github.com/brettChapman/multivis/blob/master/multivis/utils/scaleData.py): Scales data in forward or reverse order based on different scaling options.
	- [parameters](https://github.com/brettChapman/multivis/blob/master/multivis/utils/scaleData.py#L4)
		- [data] : A 1D numpy array of values
		- [scale] : The scaling option chosen to apply to the data
		- [min] : The minimum value for scaling
		- [max] : The maximum value for scaling
	- [Returns](https://github.com/brettChapman/multivis/blob/master/multivis/utils/scaler.py#L25)
		- [scaled_data] : A scaled numpy array

- [scaler](https://github.com/brettChapman/multivis/blob/master/multivis/utils/scaler.py): Scales a series of values in a numpy array based on different scaling functions.
	- [parameters](https://github.com/brettChapman/multivis/blob/master/multivis/utils/scaler.py#L4)
		- [data] : A 1D numpy array of values
		- [type] : The scaler type to apply based on sklearn preprocessing functions
		- [newMin] : The minimum value for scaling
		- [newMax] : The maximum value for scaling
	- [Returns](https://github.com/brettChapman/multivis/blob/master/multivis/utils/scaler.py#L25)
		- [scaled_data] : A scaled numpy array

- [corrAnalysis](https://github.com/brettChapman/multivis/blob/master/multivis/utils/corrAnalysis.py): Correlation analysis with Pearson, Spearman or Kendall's Tau.
	- [parameters](https://github.com/brettChapman/multivis/blob/master/multivis/utils/corrAnalysis.py#L7)
		- [df_data] : A Pandas dataframe matrix of values
		- [correlationType] : The correlation type to apply. Either 'Pearson', 'Spearman' or 'KendallTau'
	- [Returns](https://github.com/brettChapman/multivis/blob/master/multivis/utils/corrAnalysis.py#L60)
		- [df_corr] : Pandas dataframe matrix of all correlation coefficients
		- [df_pval] : Pandas dataframe matrix of all correlation pvalues

- [cluster](https://github.com/brettChapman/multivis/blob/master/multivis/utils/cluster.py): Clusters data using a linkage cluster method. If the data is correlated the correlations are first preprocessed, then clustered, otherwise a distance metric is applied to non-correlated data before clustering.
	- [parameters](https://github.com/brettChapman/multivis/blob/master/multivis/utils/cluster.py#L7)
		- [matrix] : A Pandas dataframe matrix of scores
		- [transpose_non_correlated] : Setting to 'True' will transpose the matrix if it is not correlated data
		- [is_correlated] : Setting to 'True' will treat the matrix as if it contains correlation coefficients
		- [distance_metric] : Set the distance metric. Used if the matrix does not contain correlation coefficients.
		- [linkage_method] : Set the linkage method for the clustering.
	- [Returns](https://github.com/brettChapman/multivis/blob/master/multivis/utils/cluster.py#L47)
		- [matrix] : The original matrix, transposed if transpose_non_correlated is 'True' and is_correlated is 'False'.
		- [row_linkage] : linkage matrix for the rows from a linkage clustered distance/similarities matrix
		- [col_linkage] : linkage matrix for the columns from a linkage clustered distance/similarities matrix

### License
Multivis is licensed under the MIT license.

### Authors
- Brett Chapman
- https://scholar.google.com.au/citations?user=A_wYNAQAAAAJ&hl=en

### Correspondence
Dr. Brett Chapman, Post-doctoral Research Fellow at the Western Crop Genetics Alliance, Murdoch University.
E-mail: brett.chapman@murdoch.edu.au, brett.chapman78@gmail.com

### Citation
If you would cite multivis in a scientific publication, you can use the following: [currently pending publication submission
