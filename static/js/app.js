function buildMetadata(sample) {
  d3.json(`/metadata/${sample}`).then((data) => {

    let PANEL = d3.select("#sample-metadata");

    PANEL.html("");
    // let node = document.createElement("div"); 
    Object.entries(data).forEach(([key, value]) => {
      PANEL.append("div").text(`${key}: ${value}`);
    });

   
  });
}

function buildCharts(sample) {
  d3.json(`/samples/${sample}`).then((data) => {
    const otu_ids = data.otu_ids;
    const otu_labels = data.otu_labels;
    const sample_values = data.sample_values;

    let bubbleLayout = {
      margin: { t: 0 },
      hovermode: "closest",
      plot_bgcolor:"grey",
      paper_bgcolor:"grey", 
      xaxis: { title: "OTU ID" }
    };
    let bubbleData = [
      {
        x: otu_ids,
        y: sample_values,
        text: otu_labels,
        mode: "markers",
        marker: {
          size: sample_values,
          color: otu_ids,
          colorscale: "Electric"
        }
      }
    ];

    Plotly.plot("bubble", bubbleData, bubbleLayout);

    let pieData = [
      {
        values: sample_values.slice(0, 10),
        labels: otu_ids.slice(0, 10),
        hovertext: otu_labels.slice(0, 10),
        hoverinfo: "hovertext",
        // colorscale: "Jet",
        type: "pie"
      }
    ];

    let pieLayout = {
      plot_bgcolor:"grey",
      paper_bgcolor:"grey",
      colorway: [
        "#000000",
        "#0c000c",
        "#190019",
        "#260026",
        "#330033",
        "#400040",
        "#4c004c",
        "#590059",
        "#660066",
        "#730073"
      ],
      margin: { t: 0, l: 0 }
    };

    Plotly.plot("pie", pieData, pieLayout);
  });
}

function init() {
  
  let dropdown = d3.select("#selDataset");

  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      dropdown
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {

  buildCharts(newSample);
  buildMetadata(newSample);
}


init();
