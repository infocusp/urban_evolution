var images = {
    '5 year': {
      '2015': [ee.Image("projects/nikkitiwari/assets/Predictions/Predictions_five_year/export_2015"),
               ee.Image("projects/nikkitiwari/assets/urban_evo/labels/five_year/label_2015-01-01_urban_label")],
      '2016': [ee.Image("projects/nikkitiwari/assets/Predictions/Predictions_five_year/export_2016"),
               ee.Image("projects/nikkitiwari/assets/urban_evo/labels/five_year/label_2016-01-01_urban_label")],
      '2017': [ee.Image("projects/nikkitiwari/assets/Predictions/Predictions_five_year/export_2017"),
               ee.Image("projects/nikkitiwari/assets/urban_evo/labels/five_year/label_2017-01-01_urban_label")],
      '2018': [ee.Image("projects/nikkitiwari/assets/Predictions/Predictions_five_year/export_2018"),
               ee.Image("projects/nikkitiwari/assets/urban_evo/labels/five_year/label_2018-01-01_urban_label")],
      '2019': [ee.Image("projects/nikkitiwari/assets/Predictions/Predictions_five_year/export_2019"),
               ee.Image("projects/nikkitiwari/assets/urban_evo/labels/five_year/label_2019-01-01_urban_label")],
      '2020': [ee.Image("projects/nikkitiwari/assets/Predictions/Predictions_five_year/export_2020"),
               ee.Image("projects/nikkitiwari/assets/urban_evo/labels/five_year/label_2020-01-01_urban_label")]
    },
    '1 year': {
      '2011': [ee.Image("projects/nikkitiwari/assets/urban_evo/predictions/next_year/export_2011"),
               ee.Image("projects/nikkitiwari/assets/urban_evo/labels/next_year/label_2011-01-01_urban_label")],
      '2012': [ee.Image("projects/nikkitiwari/assets/urban_evo/predictions/next_year/export_2012"),
               ee.Image("projects/nikkitiwari/assets/urban_evo/labels/next_year/label_2012-01-01_urban_label")],
      '2013': [ee.Image("projects/nikkitiwari/assets/urban_evo/predictions/next_year/export_2013"),
               ee.Image("projects/nikkitiwari/assets/urban_evo/labels/next_year/label_2013-01-01_urban_label")],
      '2014': [ee.Image("projects/nikkitiwari/assets/urban_evo/predictions/next_year/export_2014"),
               ee.Image("projects/nikkitiwari/assets/urban_evo/labels/next_year/label_2014-01-01_urban_label")],
      '2015': [ee.Image("projects/nikkitiwari/assets/urban_evo/predictions/next_year/export_2015"),
               ee.Image("projects/nikkitiwari/assets/urban_evo/labels/next_year/label_2015-01-01_urban_label")],
      '2016': [ee.Image("projects/nikkitiwari/assets/urban_evo/predictions/next_year/export_2016"),
               ee.Image("projects/nikkitiwari/assets/urban_evo/labels/next_year/label_2016-01-01_urban_label")],
      '2017': [ee.Image("projects/nikkitiwari/assets/urban_evo/predictions/next_year/export_2017"),
               ee.Image("projects/nikkitiwari/assets/urban_evo/labels/next_year/label_2017-01-01_urban_label")],
      '2018': [ee.Image("projects/nikkitiwari/assets/urban_evo/predictions/next_year/export_2018"),
               ee.Image("projects/nikkitiwari/assets/urban_evo/labels/next_year/label_2018-01-01_urban_label")],
      '2019': [ee.Image("projects/nikkitiwari/assets/urban_evo/predictions/next_year/export_2019"),
               ee.Image("projects/nikkitiwari/assets/urban_evo/labels/next_year/label_2019-01-01_urban_label")],
      '2020': [ee.Image("projects/nikkitiwari/assets/urban_evo/predictions/next_year/export_2020"),
               ee.Image("projects/nikkitiwari/assets/urban_evo/labels/next_year/label_2020-01-01_urban_label")],
      '2021': [ee.Image("projects/nikkitiwari/assets/urban_evo/predictions/next_year/export_2021"),
               ee.Image("projects/nikkitiwari/assets/urban_evo/labels/next_year/label_2021-01-01_urban_label")],
      '2022': [ee.Image("projects/nikkitiwari/assets/urban_evo/predictions/next_year/export_2022"),
               ee.Image("projects/nikkitiwari/assets/urban_evo/labels/next_year/label_2022-01-01_urban_label")],
      '2023': [ee.Image("projects/nikkitiwari/assets/urban_evo/predictions/next_year/export_2023"),
               ee.Image("projects/nikkitiwari/assets/urban_evo/labels/next_year/label_2023-01-01_urban_label")]
    }
  };
  var visParams = {min: -1, max:3, palette:['red','green','orange','blue','FFFDD7']}
  // Visualization parameters
  var visParams_compare = {
    min: 0,
    max: 4,
    palette: [
      'white',  // Background/NaN (Black)
      '00FF00',  // Matches (Green)
      'FF7F7F',  // Difference Type 1 (Light Red)
      'e2062c',  // Difference Type 2 (Medium Red)
      'maroon'   // Difference Type 3 (Dark Red)
    ]
  };
  
  // Add labels above the dropdowns
  var modelLabel = ui.Label({
    value: 'Select Model',
    style: {
      fontWeight: 'bold',
      fontSize: '15px',
      // margin: '0 0 4px 0',
      // padding: '0'
    }
  });
  var yearLabel = ui.Label({
    value: 'Select Year',
    style: {
      fontWeight: 'bold',
      fontSize: '15px',
      // margin: '0 0 4px 0',
      // padding: '0'
    }
  });
  
  // Function to clear only the image layers
  function clearImageLayers() {
    var layers = Map.layers();
    layers.forEach(function(layer) {
      print(layers)
        layers.remove(layer);
    });
  }
  
  // Create a reset button
  var resetButton = ui.Button({
    label: 'Reset Layers',
    onClick: function() {
      Map.layers().reset();  // Remove all layers
    },
    style: { 
      position: 'top-right'  // Adjust as needed
    }
  });
  
  // Add the button to the UI
  Map.add(resetButton);
  
  // Create the model selector drop-down
  var modelSelect = ui.Select({
    items: Object.keys(images),
    // value: '5 year',
    placeholder: 'Select Model',
    onChange: function(selectedModel) {
          // Clear the map when a new model is selected
    // clearImageLayers(); 
    Map.layers().reset();
      // Get the years for the selected model
      var years = Object.keys(images[selectedModel]);
      // Update year drop-down items
      yearSelect.setPlaceholder('Select Year');
      yearSelect.items().reset(years);
      
    }
  });
  
  
  // Create the year selector drop-down
  var yearSelect = ui.Select({
    placeholder: 'Select Year',
    onChange: function(selectedYear) {
      var selectedModel = modelSelect.getValue();
      var selectedImages = images[selectedModel][selectedYear];
      // clearImageLayers();
      Map.layers().reset();
      // Map.addLayer(selectedImage, visParams, selectedModel + ' - ' + selectedYear);
      var mask = selectedImages[1].neq(-1)
      var mask_pred = selectedImages[0].neq(-1)
      selectedImages[1] = selectedImages[1].updateMask(mask)
      selectedImages[0] = selectedImages[0].updateMask(mask_pred)
      Map.addLayer(selectedImages[0], visParams, 'Predictions - ' + selectedYear, true, 0.8);
      Map.addLayer(selectedImages[1], visParams, 'Ground Truth - ' + selectedYear, false, 0.8);
      // 1. Identify Class 3 Matches (both are 3)
      var class3Match = selectedImages[0].eq(3).and(selectedImages[1].eq(3));  // Both are 3 -> Black (0)
      var sameClass = selectedImages[0].eq(selectedImages[1]).and(selectedImages[0].neq(3)); // Same class but not 3 -> Green (1)
      var differentClass = selectedImages[0].neq(selectedImages[1]).and(class3Match.not()); // Different classes -> Red shades
  
      var absDiff = selectedImages[0].subtract(selectedImages[1]).abs();
      var combinedImage = ee.Image(0)  // Initialize with Black (0)
                          .where(class3Match, 0)         // Case: Both Class 3 -> Black (0)
                          .where(sameClass, 1)           // Case: Same class (0,1,2) -> Green (1)
                          .where(differentClass, absDiff.add(1)); // Case: Different classes -> Red shades (2-10)
  
      Map.addLayer(combinedImage.clip(selectedImages[0].geometry()), visParams_compare, 'Prediction Accuracy - ' + selectedYear, false, 0.8);
    }
  });
  
  // Create a panel to hold the drop-down and set its style
  var controlPanel = ui.Panel({
    widgets: [modelSelect, yearSelect],
    style: {
      position: 'top-right',
      padding: '12px',
      backgroundColor: 'rgba(255, 255, 255, 0.6)'  // Semi-transparent background
    }
  });
  // Update the panel to include labels
  controlPanel.widgets().reset([
    modelLabel, modelSelect, 
    yearLabel, yearSelect
  ]);
  
  
  // Add the drop-down to the UI
  Map.add(controlPanel);
  // Center the map to a region of interest
  Map.setCenter(77.578,  23.1289, 5);
  
  
  // Create a title label
  var titleLabel = ui.Label({
    value: 'Urban Evo Prediction',
    style: {
      fontSize: '24px',
      fontWeight: 'bold',
      margin: '0 0 6px 0',
      textAlign: 'center'
    }
  });
  
  // Create an info label with basic usage instructions
  var infoLabel = ui.Label({
    value: 'Urban Evo is a tool which predicts the possibility of urbanization across locations over the next one or five year time period \n\n'+
    'How to Use? \n\n'+
    '1) Select the time range you want to predict for ie next 1 or 5 years \n'+
    '2) Select the year you want to predict urbanization fom the dropdown \n'+
    '3) This will display an image denoting the possible urbanization classes\n'+
    '4) Click on the map to compare predicted and actual values.\n'+
    '5) The Predicted and actual values for that region will be displayed in the panel on right.\n'+
    '6) Use the legend to understand layers and class colors.\n'+
    '7) Reset selections anytime using the reset button.\n\n'+
    'For Eg: If we select 5 year and year 2016, we get an image displaying the possible urbanization for years 2016-2021\n\n'+
    'Additional Features:\n\n'+
    'Pan & Zoom Controls → Use the mouse to navigate the map.\n'+
    'Custom Layers → Turn layers on/off to focus on specific data.',
    
    style: {
      fontSize: '14px',
      whiteSpace: 'pre-wrap',
      margin: '0 0 6px 0'
    }
  });
  
  var information_title = ui.Label({
    value: 'Interpretation of Results:',
    
    style: {
      fontSize: '20px',
      fontWeight: 'bold',
      whiteSpace: 'pre-wrap',
      margin: '0 0 6px 0'
    }});
    
  
  var urb_legend_title = ui.Label({
    value: 'Urbanization classes Legend:',
    
    style: {
      fontSize: '14px',
      fontWeight: 'bold',
      whiteSpace: 'pre-wrap',
      margin: '0 0 6px 0'
    }});
  
  var mismatch_legend_title = ui.Label({
    value: 'Prediction Accuracy Map Legend:',
    
    style: {
      fontSize: '14px',
      fontWeight: 'bold',
      whiteSpace: 'pre-wrap',
      margin: '0 0 6px 0'
    }});
    
  var urb_legend_info = ui.Label({
    value:  '- High Density urban grid cell: Represents urban cell with dense population.\n'+
    '- Low Density urban grid cell: Represents urban cell with lesser population.\n'+
    '- Peri urban grid cell: Represents the transitional cell from rural to urban\n'+
    '- Rural grid cell: Represents the Rural region\n\n',
    
    style: {
      fontSize: '14px',
      whiteSpace: 'pre-wrap',
      margin: '0 0 6px 0'
    }});
    
  var missmatch_legend_info = ui.Label({
    value:  '- Exact Urban Match: Urban Prediction matches actual values.\n'+
    '- Class I Mismatch: The region has a mismatch of 1 class.\n'+
    '- Class II Mismatch: The region has a mismatch of 2 classes.\n'+
    '- Class III  Mismatch: The region has a mismatch of 3 classes\n\n',
    
    style: {
      fontSize: '14px',
      whiteSpace: 'pre-wrap',
      margin: '0 0 6px 0'
    }});
    
  // Create the information panel
  var infoPanel = ui.Panel({
    widgets: [titleLabel, infoLabel, information_title, urb_legend_title, urb_legend_info, mismatch_legend_title, missmatch_legend_info],
    style: {
      position: 'top-left',
      padding: '12px',
      backgroundColor: 'rgba(255, 255, 255, 0.6)',  // Semi-transparent background
      width: '500px'
    }
  });
  
  // Add the information panel to the map
  Map.add(infoPanel);
  
  // Comparision Legend
  
  var legend = ui.Panel({
    style: {
      position: 'bottom-right',
      padding: '8px 15px'
    }
  });
  
  // Title for the legend
  var legendTitle = ui.Label({
    value: 'Prediction Accuracy Map',
    style: {
      fontWeight: 'bold',
      fontSize: '18px',
      margin: '0 0 4px 0',
      padding: '0'
    }
  });
  
  function addLegendItem(color, name) {
    var colorBox = ui.Label({
      style: {
        backgroundColor: color,
        padding: '8px',
        margin: '0 0 4px 0'
      }
    });
  
    var description = ui.Label({
      value: name,
      style: {
        margin: '0 0 4px 6px'
      }
    });
  
    // Add color box and description to a single row
    legend.add(ui.Panel({
      widgets: [colorBox, description],
      layout: ui.Panel.Layout.Flow('horizontal')
    }));
  }
  legend.add(legendTitle);
  
  // Add legend to map
  Map.add(legend);
  addLegendItem('00FF00', 'Exact Urban Match');
  addLegendItem('FF7F7F', 'I Class Mismatch');
  addLegendItem('e2062c', 'II Class Mismatch');
  addLegendItem('maroon', 'III Class Mismatch');
  
  
  // Code for LEGEND
  var legend = ui.Panel({
    style: {
      position: 'bottom-right',
      padding: '8px 15px'
    }
  });
  
  // Title for the legend
  var legendTitle = ui.Label({
    value: 'Urbanization Classes',
    style: {
      fontWeight: 'bold',
      fontSize: '18px',
      margin: '0 0 4px 0',
      padding: '0'
    }
  });
  
  function addLegendItem(color, name) {
    var colorBox = ui.Label({
      style: {
        backgroundColor: color,
        padding: '8px',
        margin: '0 0 4px 0'
      }
    });
  
    var description = ui.Label({
      value: name,
      style: {
        margin: '0 0 4px 6px'
      }
    });
  
    // Add color box and description to a single row
    legend.add(ui.Panel({
      widgets: [colorBox, description],
      layout: ui.Panel.Layout.Flow('horizontal')
    }));
  }
  legend.add(legendTitle);
  
  // Add legend to map
  Map.add(legend);
  addLegendItem('green', 'High Density urban grid cell');
  addLegendItem('orange', 'Low Density urban grid cell');
  addLegendItem('blue', 'Peri urban grid cell');
  addLegendItem('FFFDD7', 'Rural grid cell');
  
  
  // On Click parameters on UI
  var resultsPanel = ui.Panel({
    style: { position: 'middle-right', padding: '8px', backgroundColor: 'white' }
  });
  var infoLabel = ui.Label('Prediction & Truth: Click to Compare');
  resultsPanel.add(infoLabel);
  Map.add(resultsPanel);
  
  var classMapping = {
    0: 'High Density urban grid cell',
    1: 'Low Density urban grid cell',
    2: 'Peri urban grid cell',
    3: 'Rural grid cell'
  };
  
  
  // Function to get values on click
  Map.onClick(function(coords) {
    var point = ee.Geometry.Point([coords.lon, coords.lat]);
  
    // Get pixel values for the first two layers
    var layers = Map.layers();
    var firstLayer = layers.get(0).getEeObject();
    var secondLayer = layers.get(1).getEeObject();
  
    // Sample the images at the clicked point
    var values = ee.Image.cat([firstLayer, secondLayer]).sample(point, 30).first();
   
    values.evaluate(function(result) {
      resultsPanel.clear();
      if (result) {
  
        var value1 = result['properties'].b1 
        var value2 = result['properties'].b1_1;
  
        var selectedYear = yearSelect.getValue();
        var selectedModel = modelSelect.getValue();
        var year_label = ui.Label('For ' + selectedModel + ' Model ' + 'and Year ' +  selectedYear);
        var label1 = ui.Label('Ground Truth: ' +  classMapping[value2] || 'Unknown');
        var label2 = ui.Label('Predictions: ' + classMapping[value1] || 'Unknown');
  
        // Update UI label
        resultsPanel.add(year_label);
        resultsPanel.add(label1);
        resultsPanel.add(label2);
      } else {
        infoLabel.setValue('No data at clicked location.');
      }
    });
  });
  